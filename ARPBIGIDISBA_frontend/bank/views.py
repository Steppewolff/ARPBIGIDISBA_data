from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django_tables2 import RequestConfig
from django.http import QueryDict

from .models import Sample
from .tables import SampleTable
from .filters import SampleFilter


def freezer_view(request):
    queryset = Sample.objects.all()
    filter = SampleFilter(request.GET, queryset=Sample.objects.all())
    table = SampleTable(filter.qs)
    RequestConfig(request, paginate={'per_page': 20}).configure(table)

    sample_data = list(
        filter.qs.values(
            'id', 'strain', 'species', 'clone', 'box', 'box_row', 'box_col',
            'rack', 'rack_row', 'rack_col', 'description', 'name'
        )
    )

    context = {
        'filter': filter,
        'table': table,
        'samples': sample_data,
        'all_racks': queryset.values_list('rack', flat=True).distinct().order_by('rack'),
        'all_boxes': queryset.values_list('box', flat=True).distinct().order_by('box'),
    }
    return render(request, 'strain_bank.html', context)


@require_POST
def sample_update_view(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    sample.name = request.POST.get('name', sample.name)
    sample.strain = request.POST.get('strain', sample.strain)
    sample.species = request.POST.get('species', sample.species)
    sample.clone = request.POST.get('clone', sample.clone)
    sample.box = request.POST.get('box', sample.box)
    sample.description = request.POST.get('description', sample.description)
    sample.save()

    # volver a la misma URL con los mismos filtros
    return redirect(request.META.get('HTTP_REFERER') or 'strain_bank')


@require_POST
def sample_delete_view(request, pk):
    sample = get_object_or_404(Sample, pk=pk)
    sample.delete()
    # volver a la misma URL con los mismos filtros
    return redirect(request.META.get('HTTP_REFERER') or 'strain_bank')