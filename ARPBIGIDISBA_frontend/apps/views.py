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
from django.conf import settings
import pandas as pd
import numpy as np
import os.path
import re
import csv
import json
import apps.packages.automatizacion_rp as automatizacion_rp

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


def applications(request):
    if request.method == 'POST':
        return render(request, 'aplicaciones.html')
    else:
        return render(request, 'aplicaciones.html')

def load_scores(json_file):
    """Carga el diccionario de condiciones desde el archivo JSON."""
    with open(json_file, "r") as f:
        scores = json.load(f)
    return scores

def load_csv(uploaded_file):
    """Carga los registros del archivo CSV en una lista de filas."""
    records = []

    # Asegurar que la lectura comienza desde el inicio del archivo
    uploaded_file.seek(0)

    # Decodificar y leer líneas
    reader = csv.reader(uploaded_file.read().decode("utf-8").splitlines())
    for row in reader:
        records.append(row)
    return records

def amr_score_prediction(request):
    if request.method == 'POST' and 'variantCallingFile' in request.FILES:
        vc_file = request.FILES['variantCallingFile']

        # Cargar condiciones desde el JSON
        scores_json = load_scores(os.path.join(settings.BASE_DIR, 'static/json','SCORES_100WT.json'))

        # Cargar registros del CSV (se asume que el archivo tiene 14 columnas separadas por comas)
        records = load_csv(vc_file)

        score_results, score_eval_mutacional = automatizacion_rp.main(scores_json, records)

        antibiotics = list(score_results.keys())

        BETALACTAMIC_GENES = {"PA0958": "oprD", "PA4110": "PDC"}

        betalac_by_ab = {}
        mut_by_ab_filtered = {}
        for ab in antibiotics:
            betalac_by_ab[ab] = []
            mut_by_ab_filtered[ab] = []
            for entry in score_eval_mutacional.get(ab, []):
                gene = list(entry.keys())[0]
                if gene in BETALACTAMIC_GENES:
                    # Renombrar la clave al nombre de display (oprD / PDC)
                    betalac_by_ab[ab].append({BETALACTAMIC_GENES[gene]: list(entry.values())[0]})
                else:
                    mut_by_ab_filtered[ab].append(entry)

        for ab in antibiotics:
            genes_found = [list(e.keys())[0] for e in betalac_by_ab[ab]]
            for display_name in ["oprD", "PDC"]:
                if display_name not in genes_found:
                    betalac_by_ab[ab].append({display_name: 0})

        return render(
            request, 'amr_score_prediction.html', {
                'score_results': score_results,
                'score_eval_mutacional': mut_by_ab_filtered,
                'score_eval_adquirida': {ab: [] for ab in antibiotics},
                'score_eval_betalactamic': betalac_by_ab,
                'antibiotics': antibiotics,
            })

    else:
        return render(request, 'amr_score_prediction.html')