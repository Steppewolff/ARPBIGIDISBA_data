from django.apps import apps
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView
import pandas as pd
import numpy as np
import os.path
from tkinter import filedialog
import json
import re

#from home.models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, Hospital, SampleType

# **********************************************************************************************************************
# Variables para almacenar nombres de campos y opciones de select
field_names = []
select_fields = []
select_options = []
excel_df = []
matched_db_fields = {}
values_list = []

db_value = ""


# Functions to read and operate data from files
def read_input_file():
    # Limpiar listas de campos y opciones de select
    tables = []
    df_dictionary = []
    field_names.clear()
    select_options.clear()

#    file_path = filedialog.askopenfilename(filetypes=filetypes, initialdir="FuentesInformacion")

#     if file_path:
#         try:
#             df = pd.read_excel(file_path) if file_path.endswith(('.xls', '.xlsx')) else pd.read_csv(file_path)
#             df_dictionary = df.to_dict('records')
#             excel_fields = df.columns.tolist()
#             # excel_df = df.values.tolist()
#
#             # Conectar a la base de datos MySQL para obtener nombres de campos de la tabla
#             db_obj = db.db.PsDb()
#             db_obj.connect()
#             result = db_obj.get_variable_names_db()
#             tables = db_obj.get_table_names_db('psdb_json')
#             table_index = 0
#             table_aux = {}
#             for table in tables:
#                 # print(table['Tables_in_psdb_json'])
#                 if table['Tables_in_psdb_json'] == 'metadata_general':
#                     table_index = tables.index(table)
#                     table_aux = table
#             tables.pop(table_index)
#             tables.insert(0, table_aux)
#
#             # print('df_dictionary:')
#             # print(df_dictionary)
#             db_obj.disconnect()
#         except pd.errors.EmptyDataError:
#             print("Error: El archivo está vacío.")
#         except Exception as e:
#             print(f"Error al leer el archivo: {e}")
#
#     print_match_file(tables, df_dictionary, excel_fields)
#
#
# def print_match_file(tables, df_dictionary, excel_fields):
#     if os.path.exists('match_file.txt'):
#         match_file = open('match_file.txt', 'w+')
#     else:
#         match_file = open('match_file.txt', 'x+')
#     match_file.write("Campos de la base de datos:")
#     match_file.write("\n")
#
#     for table in tables:
#         db_obj = db.db.PsDb()
#         db_obj.connect()
#         response = db_obj.get_variable_names_table(table['Tables_in_psdb_json'])
#         variables = [diccionario['COLUMN_NAME'] for diccionario in response]
#         db_obj.disconnect()
#         # sql_columns = "INSERT INTO " + table['Tables_in_psdb'] + "("
#         match_file.write(table['Tables_in_psdb_json'] + "\n")
#
#         for variable in variables:
#             match_file.write("\t" + variable + " : \n")
#
#     match_file.close()
#     read_matches(df_dictionary, excel_fields)
#
#
# def read_matches(df_dictionary, excel_fields):
#     print(
#         "Pulsa cualquier tecla para continuar cuando se haya completado el archivo de equivalencias 'match_file_input.txt'")
#     input()
#     table_name = ""
#     tables_values = {}
#     db_obj = db.db.PsDb()
#     db_obj.connect()
#     locus_resistoma = db_obj.loci_list('mutational_resistome')
#     resistoma_dict = {}
#     locus_mlst = db_obj.loci_list('locus_mlst')
#     mlst_dict = {}
#     locus_virulencia = db_obj.loci_list('virulence_gene')
#     virulencia_dict = {}
#     locus_hipermutacion = db_obj.loci_list('hypermutation_gene')
#     hipermutacion_dict = {}
#     db_obj.disconnect()
#
#     if os.path.exists('match_file_input.txt'):
#         match_file = open('match_file_input.txt', 'r')
#         for line in match_file.readlines():
#             if line == "Campos de la base de datos:\n":
#                 print(line)
#             # if line[0] != "\t" and line != "Campos de la base de datos:\n":
#             elif line[0] != "\t":
#                 print(line)
#                 line = line.rstrip("\n")
#                 table_name = line
#                 tables_values[table_name] = {}
#             else:
#                 # print(line)
#                 line = line.rstrip("\n")
#                 line = line.lstrip("\t")
#                 line_values = line.split(":")
#                 # for value in line_values:
#                 #     value = value.lstrip(" ")
#                 #     value = value.rstrip(" ")
#                 #     line_values[line_values.index(value)] = value
#
#                 if table_name in tables_values and line_values[1] != '':
#                     tables_values[table_name].update({line_values[0]: line_values[1]})
#
#         for field in excel_fields:
#             field = field.split(" ")[0]
#             if field in locus_resistoma:
#                 resistoma_dict[field] = {}
#             elif field in locus_mlst:
#                 mlst_dict[field] = {}
#             elif field in locus_virulencia:
#                 virulencia_dict[field] = {}
#             elif field in locus_hipermutacion:
#                 hipermutacion_dict[field] = {}
#             else:
#                 pass
#
#     else:
#         print("No se ha encontrado el archivo 'match_file_input.txt'")
#
#     write_sql_script(df_dictionary, tables_values, resistoma_dict, mlst_dict, virulencia_dict, hipermutacion_dict)
#
#
# def write_sql_script(df_dictionary, tables_values, resistoma_dict, mlst_dict, virulencia_dict, hipermutacion_dict):
#     sql_script = ""
#     sql_script_comments = ""
#
#     db_obj = db.db.PsDb()
#     db_obj.connect()
#
#     print("Introduce el NOMBRE EXACTO de la columna del archivo excel que contiene el identificador aislado:")
#     id_aislado = ""
#     id_aislado = input()
#
#     for isolate in df_dictionary:
#         for key, value in isolate.items():
#             locus = key.split(" ")[0]
#             if locus in resistoma_dict:
#                 if str(isolate[key]) == 'nan':
#                     mutant = 'WT'
#                 else:
#                     mutant = isolate[key]
#                 resistoma_dict[locus] = mutant
#             elif locus in mlst_dict:
#                 if isolate[key] == 'nan':
#                     mutant = 'WT'
#                 else:
#                     mutant = isolate[key]
#                 mlst_dict[locus] = mutant
#             elif locus in virulencia_dict:
#                 if isolate[key] == 'nan':
#                     mutant = 'WT'
#                 else:
#                     mutant = isolate[key]
#                 virulencia_dict[locus] = mutant
#             elif locus in hipermutacion_dict:
#                 if isolate[key] == 'nan':
#                     mutant = 'WT'
#                 else:
#                     mutant = isolate[key]
#                 hipermutacion_dict[locus] = mutant
#
#         sql_count = db_obj.count('metadata_general', 'isolate_name', isolate[id_aislado])
#         if sql_count == 0:
#             success = db_obj.insert_row('metadata_general', 'isolate_name', isolate[id_aislado])
#
#         isolate_id = db_obj.get_row_id('metadata_general', 'isolate_name', isolate[id_aislado])
#
#         if len(resistoma_dict) > 0:
#             resistoma_json = json.dumps(resistoma_dict)
#
#         if len(mlst_dict) > 0:
#             mlst_json = json.dumps(mlst_dict)
#
#         if len(virulencia_dict) > 0:
#             virulencia_json = json.dumps(virulencia_dict)
#
#         if len(hipermutacion_dict) > 0:
#             hipermutacion_json = json.dumps(hipermutacion_dict)
#
#         for table, fields in tables_values.items():
#             if len(fields) > 0:
#
#                 duplicate_update = {}
#
#                 if table != 'metadata_general':
#                     sql_count = db_obj.count(table, 'isolate_id', isolate_id)
#                     if sql_count == 0:
#                         success = db_obj.insert_row(table, 'isolate_id', isolate_id)
#                     table_id = db_obj.get_table_id(table)
#                     row_id = db_obj.get_row_id(table, 'isolate_id', isolate_id)
#
#                 sql_script = sql_script + "INSERT INTO " + table + "("
#                 if table != 'metadata_general': sql_script = sql_script + table_id + ", "
#                 table_variables = db_obj.get_variable_names_table(table)
#                 for variable in table_variables:
#                     if variable['COLUMN_NAME'] == 'isolate_id': sql_script = sql_script + "isolate_id, "
#
#                 for field, column_name in fields.items():
#                     if column_name in isolate:
#                         sql_script = sql_script + field + ", "
#
#                 if table == 'sequence_analysis':
#                     if len(resistoma_dict) > 0:
#                         sql_script = sql_script + 'mutational_resistome' + ", "
#                     if len(mlst_dict) > 0:
#                         sql_script = sql_script + 'mlst_allelic_profile' + ", "
#                     if len(virulencia_dict) > 0:
#                         sql_script = sql_script + 'virulence_gene' + ", "
#                     if len(hipermutacion_dict) > 0:
#                         sql_script = sql_script + 'hypermutation_gene' + ", "
#
#                 sql_script = sql_script[:-2] + ") VALUES ("
#
#                 if table != 'metadata_general': sql_script = sql_script + "'" + str(row_id) + "', "
#                 sql_script = sql_script + "'" + str(isolate_id) + "', "
#                 for field, column_name in fields.items():
#                     value_field = ""
#                     if column_name in isolate:
#                         if table == 'metadata_clinic':
#                             if field == 'hospital':
#                                 value_field = db_obj.get_row_id('hospital', 'hospital_name', isolate[column_name])
#                             elif field == 'sample_type':
#                                 value_field = db_obj.get_row_id('sample_type', 'sample', isolate[column_name])
#                             else:
#                                 value_field = isolate[column_name]
#
#                         elif table == 'sequencing_info':
#                             if field == 'sequencing_technology':
#                                 value_field = db_obj.get_row_id('sequencing_technology', 'sequencing_technology_name',
#                                                                 isolate[column_name])
#                             elif field == 'sequencing_platform':
#                                 value_field = db_obj.get_row_id('sequencing_platform', 'sequencing_platform_name',
#                                                                 isolate[column_name])
#                             elif field == 'sequencing_library':
#                                 value_field = db_obj.get_row_id('sequencing_library', 'sequencing_library_method',
#                                                                 isolate[column_name])
#                             else:
#                                 value_field = isolate[column_name]
#
#                         elif table == 'phenotypic_data':
#                             if field == 'invitro_serotype_id':
#                                 value_field = db_obj.get_row_id('invitro_serotype', 'invitro_value',
#                                                                 isolate[column_name])
#                             else:
#                                 value_field = isolate[column_name]
#
#                         else:
#                             value_field = isolate[column_name]
#
#                         if value_field == None:
#                             # reg_value = db_obj.get_value_byid(table, field)
#                             sql_script_comments = "INSERT INTO " + table + "(" + field + ") VALUES (" + str(isolate[column_name]) + ") ON DUPLICATE KEY UPDATE " + table + " SET " + field + " = CONCAT(" + field + "," + str(isolate[column_name]) + ");"
#                         else:
#                             if str(value_field) == 'nan':
#                                 value_field = '-'
#                             elif isinstance(value_field, str):
#                                 value_field = escape_quotes(value_field)
#
#                             sql_script = sql_script + "'" + str(value_field) + "'" + ", "
#                             duplicate_update[field] = value_field
#
#                 if table == 'sequence_analysis':
#                     if len(resistoma_dict) > 0:
#                         sql_script = sql_script + "'" + resistoma_json + "', "
#                     if len(mlst_dict) > 0:
#                         sql_script = sql_script + "'" + mlst_json + "', "
#                     if len(virulencia_dict) > 0:
#                         sql_script = sql_script + "'" + virulencia_json + "', "
#                     if len(hipermutacion_dict) > 0:
#                         sql_script = sql_script + "'" + hipermutacion_json + "', "
#
#                 sql_script = sql_script[:-2] + ") "
#
#                 if len(duplicate_update) > 0:
#                     sql_script = sql_script + "ON DUPLICATE KEY UPDATE "
#
#                     for field, field_value in duplicate_update.items():
#                         # if column_name in isolate:
#                         sql_script = sql_script + field + " = '" + str(field_value) + "'" + ", "
#
#                     if table == 'sequence_analysis':
#                         if len(resistoma_dict) > 0:
#                             sql_script = sql_script + "mutational_resistome = '" + resistoma_json + "', "
#                         if len(mlst_dict) > 0:
#                             sql_script = sql_script + "mlst_allelic_profile = '" + mlst_json + "', "
#                         if len(virulencia_dict) > 0:
#                             sql_script = sql_script + "virulence_gene = '" + virulencia_json + "', "
#                         if len(hipermutacion_dict) > 0:
#                             sql_script = sql_script + "hypermutation_gene = '" + hipermutacion_json + "', "
#
#                     # if len(duplicate_update) > 0:
#                         sql_script = sql_script[:-2] + "; \n"
#                 else:
#                     sql_script = sql_script + "; \n"
#
#     db_obj.disconnect()
#     file = open('sql_script.sql', 'w')
#     file.write(sql_script)
#     file.write(sql_script_comments)
#
# read_input_file()

# **********************************************************************************************************************

# Create your views here.
def upload(request):
    if request.method == 'POST' and 'fileselect' in request.FILES:
        file = request.FILES['fileselect']

        extensions = ['xls', 'xlsx']
        if file.name.endswith (tuple(extensions)):
            df = pd.read_excel(file)
        elif file.name.endswith ('.csv'):
            df = pd.read_csv(file)
        else:
            return JsonResponse({'error': 'Formato de archivo no soportado'}, status=400)

        df_json = df.to_json(orient='records')
        df_columns = df.columns.tolist()
        amr_loci = []
        locus_pattern = r"PA ?\d{4}"

        for column in df_columns:
            if re.search(locus_pattern, column):
                amr_loci.append(column)

        df_columns = [column for column in df_columns if not re.search(locus_pattern, column)]

        db_columns = []
        tables = ['FilePath', 'MetadataClinic', 'MetadataGeneral', 'Mic', 'PhenotypicData', 'SequenceAnalysis', 'SequencingInfo']

        df_noamr = df.filter(df_columns, axis=1)
        df_rows = df_noamr.to_dict('split')['data']

        for table in tables:
            table_fields = apps.get_model('home', table)._meta.get_fields()
            for field in table_fields:
                if '_id' not in field.name:
                    db_columns.append(field.name)

        db_columns = sorted(db_columns)
        db_columns.insert(0, 'No escribir en BDD')

        # Write the available database columns in the session
        request.session['db_columns'] = db_columns

        df_amr = df.filter(amr_loci, axis=1)
        df_amr.insert(0, 'isolate_name', df['Isolate'])
        df_amr = df_amr.replace(np.nan, '-')
        amr_mutations = df_amr.to_dict('split')['data']
        amr_columns = amr_loci.copy()
        amr_columns.insert(0, 'Isolate_name')

        return render(request, 'cargadatos.html', {'df_json': df_json, 'df_columns': df_columns, 'db_columns': db_columns, 'df_rows': df_rows, 'file': file, 'amr_loci': amr_loci, 'amr_columns': amr_columns, 'amr_mutations': amr_mutations})

    else:
        return render(request, 'cargadatos.html')

def summary(request):
    if request.method == 'POST' and 'db_var_input' in request.POST:
        all_fields = {}
        # List with all the selected options in the db variables form
        all_fields = [list(field) for field in request.POST.items()]

        # Update list with variables, removing variable_ and option_ prefixes, and removing the 'No escribir en BDD' option
        all_fields = [field for field in all_fields if 'variable_' in field[0]]
        for index, field in enumerate(all_fields):
            for index_list, value in enumerate(field):
                if 'variable_' in value:
                    field[index_list] = field[index_list].replace('variable_', '')
                elif 'option_' in value:
                    field[index_list] = field[index_list].replace('option_', '')
                else:
                    pass

        # Write the selected options in the session
        request.session['all_fields'] = all_fields

        all_fields = [field for field in all_fields if field[1] != 'No escribir en BDD']


        return render(request, 'upload_summary.html', {'all_fields': all_fields}) # 'all_values': all_values})

    else:
        pass

def modal(request):
    # Comprobar si existen aislados con el mismo nombre en la base de datos, nombre sólo por un lado y nombre_proyecto por otro (aclararlo en el texto del modal)
    # Comprobar si el nombre del Hospital existe en la tabla o no, para modificarlo si hace falta
    # Comprobar si varias columnas del excel escriben a un mismo campo de la BDD
    # Comprobar si una columna del excel escribe a varios campos de la BDD
    # Pensar en más comprobaciones
    # El botón de escribir en BDD hace el .save
    # Ver cómo hacer los qs, usar Class Based Views, ver cual se ajusta mejor

    if 'all_fields' in request.session:
        all_fields = request.session['all_fields']
        db_columns = request.session['db_columns']
    else:
        all_fields = {}
        db_columns = []

    if request.method == 'POST' and 'db_var_modal' in request.POST:
        modified_fields = [list(field) for field in request.POST.items()]
        for index, field in enumerate(all_fields):
            for modified_field in modified_fields:
                if field[0] == modified_field[0]:
                    field[1] = modified_field[1]

        # Write the modified fields in the session
        request.session['all_fields'] = all_fields

        return render(request, 'upload_summary.html', {'all_fields': all_fields, 'db_columns': db_columns})

    else:
        return render(request, 'upload_modal.html', {'all_fields': all_fields, 'db_columns': db_columns})

def confirm(request):
    return render(request, 'upload_confirm.html')