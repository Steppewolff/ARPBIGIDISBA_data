from django.apps import apps
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView

from home.models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, Hospital, SampleType

# Create your views here.
def home(request):
    return render(request, 'home.html')


class DashboardListView(ListView):
    model = MetadataGeneral
    template_name = 'dashboard.html'
