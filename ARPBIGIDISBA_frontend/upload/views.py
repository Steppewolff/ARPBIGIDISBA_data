from django.apps import apps
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView
from django.db import transaction, models
from django.contrib import messages
from django.contrib.messages import get_messages
from collections import Counter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.templatetags.static import static
from django.http import FileResponse, Http404
from django.conf import settings
from io import StringIO
import pandas as pd
import numpy as np
import os.path
import re
import os
import json
import uuid

from home.models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, Hospital, SampleType

FK_FIELDS_CONFIG = {
    'hospital_id': {
        'label': 'Hospital',
        'model': 'Hospital',
        'display_field': 'hospital_name',
        'pk_field': 'hospital_id',
    },
    'sample_type_id': {
        'label': 'Sample type',
        'model': 'SampleType',
        'display_field': 'sample',
        'pk_field': 'sample_type_id',
    },
    'oprd_reference_id': {
        'label': 'oprD reference',
        'model': 'OprdReference',
        'display_field': 'reference_strain',
        'pk_field': 'oprd_reference_id',
    },
    'pdc_variant_id': {
        'label': 'PDC variant',
        'model': 'PdcVariant',
        'display_field': 'variant_name',
        'pk_field': 'pdc_variant_id',
    },
    'ward_id': {
        'label': 'Ward collection',
        'model': 'Ward',
        'display_field': 'ward_name_en',
        'pk_field': 'ward_id',
    },
}

# Create variables manual
def manual_file(db_columns_helpers):
    folder = 'static/pdf'
    pdf_file = 'explicacion_variables_bdd.pdf'
    pdf_path = os.path.join(settings.BASE_DIR, folder, pdf_file)

# Comprobar si el archivo existe
    if not os.path.exists(pdf_path):
        # Crear el directorio si no existe
        # os.makedirs(folder, exist_ok=True)

        # Crear un objeto canvas para el PDF
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter

        # Configurar posición inicial y espaciado
        x = 50
        y = height - 50
        row_height = 20

        # Escribir las cabeceras
        c.drawString(x, y, "Campo BDD")
        c.drawString(x + 200, y, "Explicación del campo")
        y -= row_height

        # Escribir los datos del diccionario
        for key, value in db_columns_helpers.items():
            # Si se llega al final de la página, crea una nueva
            if y < 50:
                c.showPage()
                y = height - 50

            c.drawString(x, y, str(key))
            c.drawString(x + 200, y, str(value))
            y -= row_height

        # Guardar el PDF
        c.save()
        print(f"Archivo PDF creado: {pdf_path}")
    else:
        print("El archivo PDF ya existe.")

def descargar_manual_bdd(request):
    # Ruta completa del archivo PDF (asegúrate que la carpeta 'xls' esté en la raíz del proyecto o ajusta la ruta)
    pdf_path = os.path.join(settings.BASE_DIR, 'static/pdf', 'explicacion_variables_bdd.pdf')

    if os.path.exists(pdf_path):
        return FileResponse(open(pdf_path, 'rb'), content_type='application/pdf')
    else:
        raise Http404("El archivo PDF no existe.")

# Create your views here.
def upload(request):
    if request.method == 'POST' and 'fileselect' in request.FILES:
        for key in ['df', 'all_fields', 'amr_loci', 'loci_ext', 'mandatory_fields',
                    'amr_columns', 'amr_mutations', 'active_fk', 'fk_mappings']:
            request.session.pop(key, None)
        upload_id = str(uuid.uuid4())
        request.session['upload_id'] = upload_id
        request.session.modified = True

        file = request.FILES['fileselect']
        loci_ext = request.POST.get('loci')

        extensions = ['xls', 'xlsx']
        if file.name.endswith (tuple(extensions)):
            df = pd.read_excel(file)
        elif file.name.endswith ('.csv'):
            df = pd.read_csv(file)
        else:
            return JsonResponse({'error': 'Formato de archivo no soportado'}, status=400)

        request.session['file'] = file.name
        request.session['df'] = df.to_json(orient='split')
        request.session['loci_ext'] = loci_ext

        df_columns = df.columns.tolist()
        amr_loci = []
        locus_pattern = r"PA ?\d{4}"

        if loci_ext in ('muts', 'pols'):
            for column in df_columns:
                if re.search(locus_pattern, column):
                    amr_loci.append(column)

        # Load the available database columns from the session
        db_columns =  request.session['db_columns']
        db_columns_helpers = request.session['db_columns_helpers']
        request.session['amr_loci'] = amr_loci

        df_columns = [column for column in df_columns if not re.search(locus_pattern, column)]

        df_noamr = df.filter(df_columns, axis=1)
        df_rows = df_noamr.to_dict('split')['data']

        manual_file(db_columns_helpers)

        return render(request, 'cargadatos.html', {'df_columns': df_columns, 'db_columns': db_columns, 'df_rows': df_rows, 'file': file, 'amr_loci': amr_loci, 'db_columns_helpers': db_columns_helpers, 'loci_ext': loci_ext, 'upload_id': upload_id})

    else:
        db_columns = []
        db_columns_helpers = {}
        db_columns_dbname = {}
        tables = ['FilePath', 'MetadataClinic', 'MetadataGeneral', 'Mic', 'PhenotypicData', 'SequenceAnalysis', 'SequencingInfo']

        for table in tables:
            table_fields = apps.get_model('home', table)._meta.get_fields()
            for field in table_fields:
                if ('_id' not in field.name
                        and not isinstance(field, models.ForeignKey)
                        and not isinstance(field, models.OneToOneField)
                        and not isinstance(field, models.JSONField)
                        and not isinstance(field, models.OneToOneRel)
                        and not isinstance(field, models.ManyToOneRel)):
                    if table == 'Mic' and field.help_text != "":
                        db_columns.append(field.help_text)
                        db_columns_helpers[field.help_text] = field.db_comment
                        db_columns_dbname[field.help_text] = field.name
                    elif table != 'Mic':
                        db_columns.append(field.verbose_name)
                        db_columns_helpers[field.verbose_name] = field.db_comment
                        db_columns_dbname[field.verbose_name] = field.name

        # Añadir FK fields al listado de columnas disponibles
        for fk_key, config in FK_FIELDS_CONFIG.items():
            db_columns.append(config['label'])
            db_columns_helpers[config['label']] = f"Campo FK: {fk_key}"
            db_columns_dbname[config['label']] = fk_key

        db_columns = sorted(db_columns)
        db_columns.insert(0, 'Do NOT write this in DB')

        db_columns = sorted(db_columns)
        db_columns.insert(0, 'Do NOT write this in DB')

        # Write the available database columns in the session
        request.session['db_columns'] = db_columns
        request.session['db_columns_helpers'] = db_columns_helpers
        request.session['db_columns_dbname'] = db_columns_dbname

        manual_file(db_columns_helpers)

        return render(request, 'cargadatos.html')

def summary(request):
    if request.method == 'POST' and 'db_var_input' in request.POST:
        # Validar que el upload_id del formulario coincide con el de la sesión
        form_upload_id = request.POST.get('upload_id', '')
        session_upload_id = request.session.get('upload_id', '')
        if not form_upload_id or form_upload_id != session_upload_id:
            messages.error(request, 'La sesión de carga ha expirado o no es válida. Por favor, vuelve a subir el archivo.')
            return redirect('cargadatos')
        all_fields = {}
        # List with all the selected options in the db variables form

        db_columns_dbname = request.session['db_columns_dbname']
        all_fields = [list(field) for field in request.POST.items()]

        # mandatory_fields = {}

        # if 'option_isolate_name' not in dict(all_fields).values():
        #     mandatory_fields['isolate_name'] = 0
        #     messages.warning(request, 'No se ha seleccionado un campo para el nombre del aislado (isolate_name)')
        # else:
        #     mandatory_fields['isolate_name'] = 1
        #
        # if 'option_project_name' not in dict(all_fields).values():
        #     mandatory_fields['project_name'] = 0
        #     messages.warning(request, 'No se ha seleccionado un campo para el ID del proyecto (project_name)')
        # else:
        #     mandatory_fields['project_name'] = 1

        # Update list with variables, removing variable_ and option_ prefixes, and removing the 'Do NOT write this in DB' option
        all_fields = [field for field in all_fields if 'variable_' in field[0]]
        for index, field in enumerate(all_fields):
            for index_list, value in enumerate(field):
                if 'variable_' in value:
                    field[index_list] = field[index_list].replace('variable_', '')
                elif 'option_' in value:
                    field[index_list] = field[index_list].replace('option_', '')
                else:
                    pass

        mandatory_fields = eval_mandatory(request, all_fields)


        # if 'isolate_name' not in dict(all_fields).values():
        #     mandatory_fields['isolate_name'] = 0
        #     messages.warning(request, 'No se ha seleccionado un campo para el nombre del aislado (isolate_name)')
        # else:
        #     mandatory_fields['isolate_name'] = 1
        #
        # if 'project_name' not in dict(all_fields).values():
        #     mandatory_fields['project_name'] = 0
        #     messages.warning(request, 'No se ha seleccionado un campo para el ID del proyecto (project_name)')
        # else:
        #     mandatory_fields['project_name'] = 1

        # Write the selected options in the session
        request.session['all_fields'] = all_fields
        request.session['mandatory_fields'] = mandatory_fields

        # Get amr_loci list of tuples and dataframe with raw data
        amr_loci = request.session['amr_loci']
        df = pd.read_json(StringIO(request.session['df']), orient='split')

        all_fields = [field for field in all_fields if field[1] != 'Do NOT write this in DB']
        dict_fields = {field[1]: field[0] for field in all_fields}

        # --- Detección de FK fields activos ---
        fk_label_to_key = {v['label']: k for k, v in FK_FIELDS_CONFIG.items()}
        active_fk = {}
        for label, excel_col in dict_fields.items():
            if label in fk_label_to_key:
                fk_key = fk_label_to_key[label]
                config = FK_FIELDS_CONFIG[fk_key]
                model_obj = apps.get_model('home', config['model'])
                display_field = config['display_field']
                pk_field = config['pk_field']
                options = [
                    {'id': obj[pk_field], 'display': obj[display_field]}
                    for obj in model_obj.objects.values(pk_field, display_field)
                ]
                active_fk[fk_key] = {
                    'excel_col': excel_col,
                    'label': label,
                    'display_field': display_field,
                    'options': options,
                }

        fk_table = None
        if active_fk:
            isolate_col = dict_fields.get('Isolate name') or dict_fields.get('isolate_name')
            active_fk_list = list(active_fk.items())

            # Una entrada por valor único de cada campo FK
            fk_unique = []
            for fk_key, fk_info in active_fk_list:
                excel_col = fk_info['excel_col']
                unique_vals = df[excel_col].dropna().unique().tolist() if excel_col in df.columns else []
                fk_unique.append(
                    {
                        'field_name': fk_key,
                        'label': fk_info['label'],
                        'options': fk_info['options'],
                        'unique_values': [str(v) for v in unique_vals],
                    })

            fk_table = {
                'active_fk': active_fk_list,
                'fk_unique': fk_unique,
            }
            request.session['active_fk'] = {
                k: {'excel_col': v['excel_col'], 'label': v['label']}
                for k, v in active_fk.items()
            }
        else:
            request.session['active_fk'] = {}

        # fk_table = None
        # if active_fk:
        #     isolate_col = dict_fields.get('Isolate name') or dict_fields.get('isolate_name')
        #     active_fk_list = list(active_fk.items())
        #     fk_rows = []
        #     for idx, (_, row) in enumerate(df.iterrows()):
        #         cells = []
        #         for fk_key, fk_info in active_fk_list:
        #             cells.append({
        #                 'field_name': fk_key,
        #                 'raw_value': str(row[fk_info['excel_col']]) if fk_info['excel_col'] in row.index else '',
        #                 'options': fk_info['options'],
        #                 'display_field': fk_info['display_field'],
        #             })
        #         fk_rows.append({
        #             'idx': idx,
        #             'isolate_name': str(row[isolate_col]) if isolate_col else f'Fila {idx + 1}',
        #             'cells': cells,
        #         })
        #     fk_table = {
        #         'active_fk': list(active_fk.items()),
        #         'rows': fk_rows,
        #     }
        #     # Guardar en sesión sin options (no serializables directamente)
        #     request.session['active_fk'] = {
        #         k: {'excel_col': v['excel_col'], 'label': v['label']}
        #         for k, v in active_fk.items()
        #     }
        # else:
        #     request.session['active_fk'] = {}
        # --- Fin detección FK ---

        if 'Isolate name' in dict_fields:
            isolate_var = dict_fields['Isolate name']
        else:
            isolate_var = 'NA'
            r, c = df.shape
            na_column = [isolate_var for value in range(r)]

        amr_columns = []
        amr_mutations = {}
        request.session['amr_columns'] = amr_columns
        request.session['amr_mutations'] = amr_mutations

        if amr_loci:
            df_amr = df.filter(amr_loci, axis=1)
            if 'Isolate name' in dict_fields:
                df_amr.insert(0, 'isolate_name', df[str(isolate_var)])
            else:
                df_amr.insert(0, 'isolate_name', na_column)
            df_amr = df_amr.replace(np.nan, '-')
            amr_mutations = df_amr.to_dict('split')['data']
            amr_columns = amr_loci.copy()
            amr_columns.insert(0, 'Isolate_name')

        # return render(request, 'upload_summary.html', {'all_fields': all_fields, 'amr_columns': amr_columns, 'amr_mutations': amr_mutations, 'mandatory_fields': mandatory_fields})
        return render(request, 'upload_summary.html', {
            'all_fields': all_fields,
            'amr_columns': amr_columns,
            'amr_mutations': amr_mutations,
            'mandatory_fields': mandatory_fields,
            'fk_table': fk_table,
            'loci_ext': request.session.get('loci_ext', 'no'),
            'upload_id': request.session.get('upload_id', ''),
        })

    else:
        pass

# def eval_mandatory(request, all_fields):
#     mandatory_fields = request.session['mandatory_fields']
#
#     # if 'isolate_name' not in dict(all_fields).values():
#     if 'Isolate name' not in dict(all_fields).values():
#         mandatory_fields['isolate_name'] = 0
#         messages.warning(request, 'No se ha seleccionado un campo para el nombre del aislado (isolate_name)')
#     else:
#         mandatory_fields['isolate_name'] = 1
#
#     # if 'project_name' not in dict(all_fields).values():
#     if 'Project name' not in dict(all_fields).values():
#         mandatory_fields['project_name'] = 0
#         messages.warning(request, 'No se ha seleccionado un campo para el ID del proyecto (project_name)')
#     else:
#         mandatory_fields['project_name'] = 1
#
#     request.session['mandatory_fields'] = mandatory_fields
#
#     return mandatory_fields


def eval_mandatory(request, all_fields):
    mandatory_fields = {}

    # Campo obligatorio: isolate_name
    if 'Isolate name' not in dict(all_fields).values():
        mandatory_fields['isolate_name'] = 0
        messages.warning(
            request,
            'No se ha seleccionado un campo para el nombre del aislado (isolate_name)'
        )
    else:
        mandatory_fields['isolate_name'] = 1

    # Campo obligatorio: project_name
    if 'Project name' not in dict(all_fields).values():
        mandatory_fields['project_name'] = 0
        messages.warning(
            request,
            'No se ha seleccionado un campo para el ID del proyecto (project_name)'
        )
    else:
        mandatory_fields['project_name'] = 1

    # Guardar en sesión
    request.session['mandatory_fields'] = mandatory_fields

    return mandatory_fields

def modal(request):
    # Comprobar si el nombre del Hospital existe en la tabla o no, para modificarlo si hace falta
    # Valores de hospitales y tipo de muestra (pensar si hay alguno mas), ¿cómo se busca en los listados para encontrar sus ID? ¿o con el ORM se puede hacer de manera más directa?
    # Pensar en más comprobaciones

    if 'all_fields' in request.session:
        all_fields = request.session['all_fields']
        db_columns = request.session['db_columns']
    else:
        all_fields = {}
        db_columns = []

    # mandatory_fields = request.session['mandatory_fields']
    amr_columns = request.session['amr_columns']
    amr_mutations = request.session['amr_mutations']

    if request.method == 'POST' and 'db_var_modal' in request.POST:
        modified_fields = [list(field) for field in request.POST.items()]
        for index, field in enumerate(all_fields):
            for modified_field in modified_fields:
                if field[0] == modified_field[0]:
                    field[1] = modified_field[1]

        # Write the modified fields in the session
        request.session['all_fields'] = all_fields

        mandatory_fields = eval_mandatory(request, all_fields)

        return render(request, 'upload_summary.html', {'all_fields': all_fields, 'amr_columns': amr_columns, 'amr_mutations': amr_mutations, 'db_columns': db_columns, 'mandatory_fields': mandatory_fields, 'loci_ext': request.session.get('loci_ext', 'no'), 'upload_id': request.session.get('upload_id', '')})

    else:
        isolates_db_list = MetadataGeneral.objects.values_list('isolate_name', flat=True)
        isolates_project_list = MetadataGeneral.objects.values_list('isolate_project_code', flat=True)
        # isolates_excel_list = pd.read_json(StringIO(request.session['df']), orient='split')[dict(tuple(reversed(t)) for t in all_fields)['isolate_name']].tolist()
        difference_hospitals = []
        if 'hospital_name' in dict(tuple(reversed(t)) for t in all_fields):
            hospitals_db_list = Hospital.objects.values_list('hospital_name', flat=True)
            hospitals_excel_list = pd.read_json(StringIO(request.session['df']), orient='split')[dict(tuple(reversed(t)) for t in all_fields)['hospital_name']].tolist()
            difference_hospitals = set(hospitals_excel_list).difference(hospitals_db_list)

        mandatory_fields = eval_mandatory(request, all_fields)

        # common_isolates = set(isolates_db_list).intersection(isolates_excel_list)
        common_isolates = []
        count_dict = Counter(dict(all_fields).values())
        duplicates = [key for key, value in count_dict.items()
                      if count_dict[key] > 1 and key != 'Do NOT write this in DB']

        # return render(request, 'upload_modal.html', {'all_fields': all_fields, 'db_columns': db_columns, 'common_isolates': common_isolates, 'duplicates': duplicates, 'difference_hospitals': difference_hospitals, 'mandatory_fields': mandatory_fields})
        upload_id = request.GET.get('uid') or request.session.get('upload_id', '')
        return render(request, 'upload_modal.html', {'all_fields': all_fields, 'db_columns': db_columns, 'common_isolates': common_isolates, 'duplicates': duplicates, 'difference_hospitals': difference_hospitals, 'mandatory_fields': mandatory_fields, 'upload_id': upload_id})

def confirm(request):
    get_upload_id = request.GET.get('uid', '')
    session_upload_id = request.session.get('upload_id', '')
    if not get_upload_id or get_upload_id != session_upload_id:
        messages.error(request, 'La sesión de carga ha expirado o no es válida. Por favor, vuelve a subir el archivo.')
        return redirect('cargadatos')

    all_fields = request.session['all_fields']
    df = pd.read_json(StringIO(request.session['df']), orient='split')

    # input_fields = [field for field in all_fields]
    # input_fields = {field[1] : field[0] for field in all_fields}
    db_columns_dbname = request.session.get('db_columns_dbname', {})
    input_fields = {
        db_columns_dbname.get(field[1], field[1]): field[0]
        for field in all_fields
    }

    tables = ['MetadataGeneral', 'FilePath', 'MetadataClinic', 'Mic', 'PhenotypicData', 'SequenceAnalysis',
              'SequencingInfo']


    model_fields = {table: [] for table in tables}
    for model_name in model_fields:
        table_fields = apps.get_model('home', model_name)._meta.get_fields()
        for field in table_fields:
            if '_id' not in field.name and field.name in input_fields:
                model_fields[model_name].append(field.name)



    fk_mappings = request.session.get('fk_mappings', {})
    active_fk_session = request.session.get('active_fk', {})

    # Averiguar qué modelo tiene cada FK field
    fk_to_model = {}
    for fk_key in active_fk_session:
        for model_name in tables:
            try:
                apps.get_model('home', model_name)._meta.get_field(fk_key)
                fk_to_model[fk_key] = model_name
                break
            except Exception:
                pass
    loci_ext = request.session.get('loci_ext', 'no')
    amr_loci = request.session.get('amr_loci', [])

    with transaction.atomic():
        created_records = []  # lista de dicts
        edited_records = []  # lista de dicts

        for idx, (_, row) in enumerate(df.iterrows()):
            row_fk = fk_mappings.get(str(idx), {})

            metadata_general_data = {
                field: row[input_fields[field]]
                for field in model_fields['MetadataGeneral']
                if input_fields[field] in row
            }
            isolate_project_code = f"{metadata_general_data['project_name']}_{metadata_general_data['isolate_name']}"
            metadata_general_instance, mg_created = MetadataGeneral.objects.get_or_create(
                isolate_project_code=isolate_project_code,
                defaults=metadata_general_data
            )

            if mg_created:
                created_records.append(
                    {
                        'isolate_name': metadata_general_data.get('isolate_name', ''),
                        'project_name': metadata_general_data.get('project_name', ''),
                        'fields': {k: v for k, v in metadata_general_data.items()
                                   if k not in ('isolate_name', 'project_name')},
                    })
            else:
                mg_changed = {}
                for field, value in metadata_general_data.items():
                    if str(getattr(metadata_general_instance, field)) != str(value):
                        mg_changed[field] = value
                    setattr(metadata_general_instance, field, value)
                metadata_general_instance.save()
                if mg_changed:
                    edited_records.append(
                        {
                            'isolate_name': metadata_general_data.get('isolate_name', ''),
                            'project_name': metadata_general_data.get('project_name', ''),
                            'changed_fields': mg_changed,
                        })

            for model_name, fields in model_fields.items():
                if model_name == 'MetadataGeneral':
                    continue

                model_data = {
                    field: row[input_fields[field]]
                    for field in fields
                    if input_fields[field] in row
                }

                for fk_key, fk_model_name in fk_to_model.items():
                    if fk_model_name == model_name and fk_key in fk_mappings:
                        excel_col = active_fk_session.get(fk_key, {}).get('excel_col', '')
                        raw_val = str(row[excel_col]) if excel_col and excel_col in row.index else ''
                        selected_id = fk_mappings[fk_key].get(raw_val, '')
                        model_data[fk_key] = int(selected_id) if selected_id else None

                if model_name == 'SequenceAnalysis' and amr_loci:
                    resistome_data = {
                        locus: str(row[locus]) if locus in row.index and pd.notna(row[locus]) else ''
                        for locus in amr_loci
                    }
                    if loci_ext == 'muts':
                        model_data['mutational_resistome_muts'] = resistome_data
                    elif loci_ext == 'pols':
                        model_data['mutational_resistome_pols'] = resistome_data

                if model_data:
                    model_instance, rel_created = apps.get_model('home', model_name).objects.get_or_create(
                        isolate_id=metadata_general_instance, defaults=model_data)

                    if rel_created:
                        # Registro relacionado nuevo: todos los campos son añadidos
                        display_data = {
                            k: '(JSON)' if isinstance(v, dict) else v
                            for k, v in model_data.items()
                        }
                        existing = next(
                            (r for r in edited_records
                             if r['isolate_name'] == metadata_general_data.get('isolate_name', '')), None)
                        if existing:
                            existing['changed_fields'].update(display_data)
                        else:
                            edited_records.append(
                                {
                                    'isolate_name': metadata_general_data.get('isolate_name', ''),
                                    'project_name': metadata_general_data.get('project_name', ''),
                                    'changed_fields': display_data,
                                })

                    if not rel_created:
                        rel_changed = {}
                        for field, new_value in model_data.items():
                            if str(getattr(model_instance, field)) != str(new_value):
                                rel_changed[field] = '(JSON)' if isinstance(new_value, dict) else new_value
                                setattr(model_instance, field, new_value)
                        model_instance.save()
                        if rel_changed:
                            existing = next(
                                (r for r in edited_records
                                 if r['isolate_name'] == metadata_general_data.get('isolate_name', '')), None)
                            if existing:
                                existing['changed_fields'].update(rel_changed)
                            else:
                                edited_records.append(
                                    {
                                        'isolate_name': metadata_general_data.get('isolate_name', ''),
                                        'project_name': metadata_general_data.get('project_name', ''),
                                        'changed_fields': rel_changed,
                                    })

    # Cabeceras dinámicas para tabla de creados
    created_field_headers = []
    for record in created_records:
        for f in record.get('fields', {}).keys():
            if f not in created_field_headers:
                created_field_headers.append(f)

    return render(
        request, 'upload_confirm.html', {
            'created_records': created_records,
            'edited_records': edited_records,
            'created_field_headers': created_field_headers,
        })

def fk_save(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            request.session['fk_mappings'] = data
            request.session.modified = True
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)