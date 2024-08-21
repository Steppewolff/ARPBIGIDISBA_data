from django_filters import rest_framework as filters, DateFromToRangeFilter
from django_filters import widgets, DateFilter
from django.forms import DateInput
from .models import Hospital, Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral, MetadataClinic, InvitroSerotype, \
    SampleType


class MultiFilter(filters.FilterSet):
    # isolate_name = filters.CharFilter(lookup_expr='icontains', distinct=True, label='Nombre del aislado')
    isolate_name = filters.ModelChoiceFilter(field_name='Nombre aislado', queryset=MetadataGeneral.objects.values_list('isolate_name', flat=True).distinct(), to_field_name='isolate_name', label='Nombre del aislado')
    species = filters.CharFilter(lookup_expr='icontains', distinct=True, label='Especie')
    project_name = filters.CharFilter(field_name='Nombre proyecto', lookup_expr='icontains', distinct=True, label='Proyecto')

    # isolation_date = filters.NumberFilter(field_name='isolation_date', lookup_expr='year',
    #                                            label='Año', distinct=True)
    isolation_date__gt = filters.DateFilter(field_name='isolation_date', widget=DateInput(attrs={'type': 'date'}), lookup_expr='gte', label='Desde (fecha)')
    isolation_date__lt = filters.DateFilter(field_name='isolation_date', widget=DateInput(attrs={'type': 'date'}), lookup_expr='lte', label='Hasta (fecha)')

    # isolate_source = filters.ModelChoiceFilter(field_name='isolate_source', queryset=MetadataGeneral.objects.all(), distinct=True, label='Origen del aislado')
    isolate_source = filters.ModelChoiceFilter(field_name='isolate_source', queryset=MetadataGeneral.objects.values_list('isolate_source', flat=True).distinct(), to_field_name='isolate_source', label='Origen del aislado')

    # ModelChoiceField(queryset=MetadataClinic.objects.values_list('sample_type__sample', flat=True).distinct(),
    #                            to_field_name='sample_type', label='Tipo de muestra', empty_label='Selecciona un tipo de muestra', required=False)

    # date_range = DateFromToRangeFilter(widget=DateRangeWidget(attrs={'placeholder': 'YYYY/MM/DD'}))

    class Meta:
        model = MetadataGeneral
        fields = ['isolate_name', 'species', 'project_name', 'isolation_date__gt', 'isolation_date__lt', 'isolate_source']
        #, 'ecdc_resistance_profile.phenotypicdata_set': ['exact']
