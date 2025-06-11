import django_filters
from .models import Sample

class SampleFilter(django_filters.FilterSet):
    strain = django_filters.ChoiceFilter(choices=(), label='Strain')
    species = django_filters.ChoiceFilter(choices=(), label='Species')
    rack = django_filters.ChoiceFilter(choices=(), label='Rack')
    box = django_filters.ChoiceFilter(choices=(), label='Box')

    class Meta:
        model = Sample
        fields = ['strain', 'species', 'rack', 'box']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['strain'].extra['choices'] = [('', 'Todos')] + list(Sample.objects.values_list('strain', 'strain').distinct().order_by('strain'))
        self.filters['species'].extra['choices'] = [('', 'Todos')] + list(Sample.objects.values_list('species', 'species').distinct().order_by('species'))
        self.filters['rack'].extra['choices'] = [('', 'Todos')] + list(Sample.objects.values_list('rack', 'rack').distinct().order_by('rack'))
        self.filters['box'].extra['choices'] = [('', 'Todos')] + list(Sample.objects.values_list('box', 'box').distinct().order_by('box'))