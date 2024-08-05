from django_filters import rest_framework as filters
from .models import Hospital, Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral, MetadataClinic, InvitroSerotype, \
    SampleType


class MultiFilter(filters.FilterSet):
    isolate_name = filters.CharFilter(lookup_expr='icontains', distinct=True)
    species = filters.CharFilter(lookup_expr='icontains', distinct=True)
    project_name = filters.CharFilter(lookup_expr='icontains', distinct=True)

    isolation_date = filters.NumberFilter(field_name='isolation_date', lookup_expr='year',
                                               label='Contents', distinct=True)
    isolation_date__gt = filters.NumberFilter(field_name='isolation_date', lookup_expr='year__gt')
    isolation_date__lt = filters.NumberFilter(field_name='isolation_date', lookup_expr='year__lt')

    isolate_source = filters.ModelChoiceFilter(field_name='isolate_source', queryset=MetadataGeneral.objects.all(), distinct=True)

    class Meta:
        model = MetadataGeneral
        fields = ['isolate_name', 'species', 'project_name', 'isolation_date', 'isolate_source']
        #, 'ecdc_resistance_profile.phenotypicdata_set': ['exact']
