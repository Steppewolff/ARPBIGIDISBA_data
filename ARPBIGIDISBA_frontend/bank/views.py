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

    # Selectores para racks y boxes
    context = {
        'filter': filter,
        'table': table,
        'all_racks': Sample.objects.values_list('rack', flat=True).distinct().order_by('rack'),
        'all_boxes': Sample.objects.values_list('box', flat=True).distinct().order_by('box'),
    }

    return render(request, 'strain_bank.html', context)