from dataclasses import fields

from django_filters import rest_framework as filters, DateFromToRangeFilter
from django_filters import widgets, DateFilter
from django.forms import DateInput
from django import forms
from django.db import connection
from .models import Hospital, Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral, MetadataClinic, InvitroSerotype, \
    SampleType
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit


def obtener_opciones_filtro():
    """Extrae todas las claves únicas y sus valores únicos en la base de datos."""
    with connection.cursor() as cursor:
        # Obtener todas las claves y valores únicos, separando valores múltiples
        cursor.execute(
            """
                SELECT 
                    j.clave AS clave, 
                    JSON_UNQUOTE(JSON_EXTRACT(s.mutational_resistome_muts, CONCAT('$."', j.clave, '"'))) AS valor
                FROM sequence_analysis s
                JOIN JSON_TABLE(
                    JSON_KEYS(s.mutational_resistome_muts), 
                    "$[*]" COLUMNS (clave VARCHAR(255) PATH "$")
                ) AS j
                WHERE s.mutational_resistome_muts IS NOT NULL;;
            """)

        opciones = {}
        for clave, valor in cursor.fetchall():
            if clave and valor:
                valores_separados = [v.strip() for v in valor.split(";") if v.strip()]  # Separar valores múltiples
                if clave in opciones:
                    opciones[clave].update(valores_separados)
                else:
                    opciones[clave] = set(valores_separados)

        grupos = []
        for clave, valores in sorted(opciones.items()):
            subchoices = [(v, v) for v in sorted(valores)]
            grupos.append((clave, subchoices))
        return grupos

class GroupedSelect(forms.Select):
    """Widget para mostrar valores anidados bajo cada clave."""
    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = choices

    def render(self, name, value, attrs=None, renderer=None):
        """Renderiza el select anidando valores dentro de claves."""
        output = ['<select name="{}" class="form-control">'.format(name)]
        current_group = None
        for val, label, group in self.choices:
            if group != current_group:
                if current_group is not None:
                    output.append('</optgroup>')  # Cerrar grupo anterior
                output.append('<optgroup label="{}">'.format(group))  # Abrir nuevo grupo
                current_group = group
            output.append('<option value="{}">{}</option>'.format(val, label))
        output.append('</optgroup></select>')
        return '\n'.join(output)

class MultiFilter(filters.FilterSet):
    # OPCIONES_FILTRO = obtener_opciones_filtro()

    # isolate_name = filters.ModelChoiceFilter(field_name='isolate_name', queryset=MetadataGeneral.objects.values_list('isolate_name', flat=True).distinct(), to_field_name='isolate_name', label='Isolate name')
    isolate_name = filters.MultipleChoiceFilter(
        field_name='isolate_name',
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'id': 'isolateNameSelect'}),
        label='Isolate name'
    )
    species = filters.ModelChoiceFilter(field_name='species', queryset=MetadataGeneral.objects.values_list('species', flat=True).distinct(), to_field_name='species', label='Species')
    # project_name = filters.ModelChoiceFilter(field_name='project_name', queryset=MetadataGeneral.objects.values_list('project_name', flat=True).distinct(), to_field_name='project_name', label='Project')
    project_name = filters.MultipleChoiceFilter(
        field_name='project_name',
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'id': 'projectNameSelect'}),
        label='Project'
    )

    isolate_source = filters.ModelChoiceFilter(field_name='isolate_source', queryset=MetadataGeneral.objects.values_list('isolate_source', flat=True).distinct(), to_field_name='isolate_source', label='Isolate origin')

    isolation_date__gt = filters.DateFilter(field_name='isolation_date', widget=DateInput(attrs={'type': 'date'}), lookup_expr='gte', label='From (date)')
    isolation_date__lt = filters.DateFilter(field_name='isolation_date', widget=DateInput(attrs={'type': 'date'}), lookup_expr='lte', label='To (date)')

    incluir = filters.MultipleChoiceFilter(
        choices=[],
        # widget=GroupedSelect(choices=OPCIONES_FILTRO),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'id': 'myMultiSelect1'}),
        method='filtrar_incluir',
        label="Present mutations"
    )
    excluir = filters.MultipleChoiceFilter(
        choices=[],
        # widget=GroupedSelect(choices=OPCIONES_FILTRO),
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2', 'id': 'myMultiSelect2'}),
        method='filtrar_excluir',
        label="Absent mutations"
    )

    # def filtrar_isolate_name(self, queryset, name, value):
    #     if value:
    #         return queryset.filter(isolate_name__in=value)
    #     return queryset

    def filtrar_incluir(self, queryset, name, value):
        """Filtra registros donde una clave específica tenga un valor concreto."""
        if value:
            filtros = []
            for valor in value:
                filtros.append(f"JSON_SEARCH(mutational_resistome_muts, 'one', '{valor}') IS NOT NULL")
            return queryset.extra(where=[' OR '.join(filtros)])
        return queryset

    def filtrar_excluir(self, queryset, name, value):
        """Excluye registros donde una clave específica tenga un valor concreto."""
        if value:
            filtros = []
            for valor in value:
                filtros.append(f"JSON_SEARCH(mutational_resistome_muts, 'one', '{valor}') IS NOT NULL")
            return queryset.extra(where=[' NOT (' + ' OR '.join(filtros) + ')'])
        return queryset

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        opciones = obtener_opciones_filtro()
        self.filters['incluir'].extra['choices'] = opciones
        self.filters['excluir'].extra['choices'] = opciones
        self.filters['isolate_name'].extra['choices'] = [
            (v, v) for v in
            MetadataGeneral.objects.values_list('isolate_name', flat=True).distinct().order_by('isolate_name') if v
        ]
        self.filters['project_name'].extra['choices'] = [
            (v, v) for v in
            MetadataGeneral.objects.values_list('project_name', flat=True).distinct().order_by('project_name') if v
        ]

        self.form.helper = FormHelper(self.form)
        self.form.helper.form_method = 'GET'
        self.form.helper.layout = Layout(
            Row(
                Column('species', css_class='form-group col-md-4 mb-0'),
                Column('isolate_name', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('project_name', css_class='form-group col-md-4 mb-0'),
                Column('isolate_source', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('isolation_date__gt', css_class='form-group col-md-4 mb-0'),
                Column('isolation_date__lt', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('incluir', css_class='form-group col-md-6 mb-0'),
                Column('excluir', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Filtrar', css_class='btn btn-primary mt-3')
        )

    class Meta:
        model = MetadataGeneral
        fields = ['species', 'isolate_name', 'project_name', 'isolate_source','incluir', 'excluir']