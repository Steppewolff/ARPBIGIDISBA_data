from django.shortcuts import render, redirect
from django.views.generic.edit import FormMixin, ModelFormMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django_tables2 import SingleTableView

from .models import Mic, MetadataGeneral
from .tables import MicTable
from .forms import HospitalForm, MicForm, MetadataGeneralForm, FenotipoForm


# Create your views here.
def home(request):
    return render(request, 'home.html')


def busqueda(request):
    if request.method == 'POST':
        metadatageneral_form = MetadataGeneralForm(request.POST)
        hospital_form = HospitalForm(request.POST)
        mic_form = MicForm(request.POST)
        fenotipo_form = FenotipoForm(request.POST)

        if metadatageneral_form.is_valid() and hospital_form.is_valid() and mic_form.is_valid() and fenotipo_form.is_valid():
            # metadatageneral = metadatageneral_form.save()
            # hospital = hospital_form.save()
            # mic = mic_form.save()
            # fenotipo = fenotipo_form.save()
            # Hacer algo con los modelos guardados, por ejemplo, redirigir a otra página
            # return redirect('/resultados/')
            # pass
            return redirect('/resultados')
            # return render(request, 'resultados.html')


    else:
        metadatageneral_form = MetadataGeneralForm()
        hospital_form = HospitalForm()
        mic_form = MicForm()
        fenotipo_form = FenotipoForm()


    return render(request, 'busqueda.html', {'metadatageneral_form': metadatageneral_form, 'hospital_form': hospital_form, 'mic_form': mic_form, 'fenotipo_form': fenotipo_form})


# class BusquedaTemplateView(TemplateView):
#     template_name = 'busqueda.html'


    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # aislado = get_object_or_404(MetadataGeneral, aislado_nombre=self.kwargs['aislado_nombre'])
    #     context['hospital_form'] = HospitalForm
    #     context['mic_form'] = MicForm
    #     return context

class ResultadosTableView(SingleTableView):
    model = Mic
    template_name = 'resultados.html'
    table_class = MicTable

    # if request.method == 'POST':
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super(ResultadosTableView, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("mic_id")
        return qs

def pipelines(request):
    return render(request, 'pipelines.html')


def dashboard(request):
    return render(request, 'dashboard.html')


def documentacion(request):
    return render(request, 'documentacion.html')


def cargadatos(request):
    return render(request, 'cargadatos.html')


def contacto(request):
    return render(request, 'contacto.html')
