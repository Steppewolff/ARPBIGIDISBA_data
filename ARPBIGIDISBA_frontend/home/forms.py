from django.forms import Form, ChoiceField, CharField, ModelChoiceField, ModelForm, Select, TextInput

from .models import Hospital, Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral

class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id

class MetadataGeneralForm(ModelForm):
    aislado_nombre = ModelChoiceField(queryset=MetadataGeneral.objects.values_list('isolate_name', flat=True).distinct(), label='Nombre del aislado', empty_label='Selecciona un aislado', required=False)

    class Meta:
        model = MetadataGeneral
        exclude = ('isolate_project_id',)

class HospitalForm(ModelForm):
    country = ModelChoiceField(queryset=Hospital.objects.values_list('country', flat=True).distinct(), to_field_name="country", label='País', empty_label='Selecciona un país', required=False)
    region = ModelChoiceField(queryset=Hospital.objects.values_list('region', flat=True).distinct(), to_field_name="region", label='Región', empty_label='Selecciona una región', required=False)
    city = ModelChoiceField(queryset=Hospital.objects.values_list('town', flat=True).distinct(), to_field_name="town", label='Localidad', empty_label='Selecciona una localidad', required=False)
    hospital = ModelChoiceField(queryset=Hospital.objects.values_list('hospital_name', flat=True).distinct(), to_field_name="hospital_name",label='Hospital', empty_label='Selecciona un hospital', required=False)
    class Meta:
        model = Hospital
        fields = ['hospital', 'country', 'region', 'town']

class MicForm(ModelForm):
    class Meta:
        model = Mic
        exclude = ('mic_id', 'isolate',)

class FenotipoForm(ModelForm):
    class Meta:
        model = PhenotypicData
        exclude = ('isolate', 'mic_id')
