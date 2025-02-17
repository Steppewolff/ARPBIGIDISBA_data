from django.apps import apps
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django_tables2 import SingleTableView, SingleTableMixin, RequestConfig
from django_tables2.export.export import TableExport
from django_filters.views import FilterView
from django.db import transaction
from django.contrib import messages
from django.contrib.messages import get_messages
from collections import Counter
from io import StringIO
import pandas as pd
import numpy as np
import os.path
import re

from home.models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, Hospital, SampleType

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

# Create your views here.
def applications(request):
    if request.method == 'POST':
        return render(request, 'aplicaciones.html')
    else:
        return render(request, 'aplicaciones.html')