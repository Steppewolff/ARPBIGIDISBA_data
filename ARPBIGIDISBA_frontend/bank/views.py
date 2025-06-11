from django.shortcuts import render
from django_tables2 import RequestConfig

from .models import Sample
from .tables import SampleTable
from .filters import SampleFilter


def freezer_view(request):
    queryset = Sample.objects.all()
    filter = SampleFilter(request.GET, queryset=Sample.objects.all())
    table = SampleTable(filter.qs)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)

    # Datos serializables para el JS
    sample_data = list(
        filter.qs.values(
            'id', 'strain', 'species', 'clone', 'box', 'box_row', 'box_col',
            'rack', 'rack_row', 'rack_col', 'description', 'name'
        )
    )

    # Selectores para racks y boxes
    context = {
        'filter': filter,
        'table': table,
        'samples': sample_data,  # <- esto es lo importante para el json_script
        'all_racks': queryset.values_list('rack', flat=True).distinct().order_by('rack'),
        'all_boxes': queryset.values_list('box', flat=True).distinct().order_by('box'),
    }

    return render(request, 'strain_bank2.html', context)