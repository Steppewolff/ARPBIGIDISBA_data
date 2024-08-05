from django.forms import Form, ChoiceField, CharField, ModelChoiceField, ModelForm, Select, TextInput

from .models import Hospital, Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral, MetadataClinic, InvitroSerotype, SampleType


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id


class MetadataGeneralForm(ModelForm):
    isolate_name = ModelChoiceField(
        queryset=MetadataGeneral.objects.values_list('isolate_name', flat=True).distinct(), to_field_name="isolate_name", label='Nombre del aislado',
        empty_label='Selecciona un aislado', required=False) # , widget=TextInput(attrs={'name': 'Nombre aislado en forms'})
    project_name = ModelChoiceField(
        queryset=MetadataGeneral.objects.values_list('project_name', flat=True).distinct(), label='Proyecto',
        empty_label='Selecciona un proyecto', required=False) # , widget=TextInput(attrs={'name': 'Nombre proyecto en forms'})

    class Meta:
        model = MetadataGeneral
        exclude = ('isolate_project_id',)
        # widgets = {'project_name': TextInput(attrs={'name': 'Nombre proyecto en forms'})}

    def __init__(self, *args, **kwargs):
        super(MetadataGeneralForm, self).__init__(*args, **kwargs)
        self.fields["project_name"].widget.attrs.update({"name": "custom_name"})


class MetadataClinicForm(ModelForm):
    # sample_type = ModelChoiceField(queryset=MetadataClinic.objects.values_list('sample_type__sample', flat=True).distinct(),
    #                            to_field_name='sample_type', label='Tipo de muestra', empty_label='Selecciona un tipo de muestra', required=False)
    sample_type = ModelChoiceField(queryset=SampleType.objects.all(), widget=Select(),
                               to_field_name='sample', label="Tipo de muestra", empty_label='Selecciona un tipo de muestra', required=False)
    # attrs={'id': .id}
    collection_ward = ModelChoiceField(queryset=MetadataClinic.objects.values_list('collection_ward', flat=True).distinct(),
                              to_field_name="collection_ward", label='Departamento', empty_label='Selecciona un departamento',
                              required=False)
    #
    # def label_from_instance(self, obj):
    #     return f'{obj.first_name}'

    class Meta:
        model = MetadataClinic
        fields = ['sample_type', 'collection_ward'] # 'patient_id', 'hospital',

    def __init__(self, *args, **kwargs):
        super(MetadataClinicForm, self).__init__(*args, **kwargs)
        self.fields['sample_type'].label_from_instance = lambda obj: obj.sample


class HospitalForm(ModelForm):
    country = ModelChoiceField(queryset=Hospital.objects.values_list('country', flat=True).distinct(),
                               to_field_name="country", label='País', empty_label='Selecciona un país', required=False)
    region = ModelChoiceField(queryset=Hospital.objects.values_list('region', flat=True).distinct(),
                              to_field_name="region", label='Región', empty_label='Selecciona una región',
                              required=False)
    town = ModelChoiceField(queryset=Hospital.objects.values_list('town', flat=True).distinct(), to_field_name="town",
                            label='Localidad', empty_label='Selecciona una localidad', required=False)
    hospital = ModelChoiceField(queryset=Hospital.objects.values_list('hospital_name', flat=True).distinct(),
                                to_field_name="hospital_name", label='Hospital', empty_label='Selecciona un hospital',
                                required=False)

    class Meta:
        model = Hospital
        fields = ['hospital', 'country', 'region', 'town']

    def __init__(self, *args, **kwargs):
        super(HospitalForm, self).__init__(*args, **kwargs)
        # self.fields["hospital"].label_from_instance = lambda obj: obj.hospital_id


class MicForm(ModelForm):
    class Meta:
        model = Mic
        fields = ['pip', 'pip_tz', 'fep', 'cfdc', 'caz', 'caz_avi', 'ct', 'imi', 'imi_rel', 'mer',
                  'mer_vab', 'azt', 'azt_avi', 'cip', 'dlx', 'lvx', 'mxl', 'ami', 'gen', 'net', 'tob',
                  'col', 'fo', 'tic', 'ptz', 'taz', 'cza', 'tol', 'atm']


class FenotipoForm(ModelForm):
    ecdc_resistance_profile = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('ecdc_resistance_profile', flat=True).distinct(),
        label='Perfil ECDC', empty_label='Selecciona un perfil ECDC', required=False)
    idsa_resistance_profile = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('idsa_resistance_profile', flat=True).distinct(),
        label='Perfil IDSA', empty_label='Selecciona un perfil IDSA', required=False)
    cloxa_test = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('cloxa_test', flat=True).distinct(),
        label='Test cloxa', empty_label='Selecciona un resultado', required=False)
    mbl_test = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('mbl_test', flat=True).distinct(),
        label='Test mbl', empty_label='Selecciona un resultado', required=False)
    esbl_test = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('esbl_test', flat=True).distinct(),
        label='Test esbl', empty_label='Selecciona un resultado', required=False)
    invitro_serotype = ModelChoiceField(
        queryset=InvitroSerotype.objects.values_list('invitro_value', flat=True).distinct(),
        label='Serotipo in vitro', empty_label='Selecciona un resultado', required=False)

    class Meta:
        model = PhenotypicData
        fields = ['ecdc_resistance_profile', 'idsa_resistance_profile', 'cloxa_test', 'mbl_test', 'esbl_test', 'invitro_serotype']


class SequenceAnalysisForm(ModelForm):
    clonal_complex = ModelChoiceField(
        queryset=SequenceAnalysis.objects.values_list('clonal_complex', flat=True).distinct(),
        label='Complejo clonal', empty_label='Selecciona un Complejo clonal', required=False)
    insilico_serotype = ModelChoiceField(
        queryset=InvitroSerotype.objects.values_list('invitro_value', flat=True).distinct(),
        label='Serotipo in silico', empty_label='Selecciona un resultado', required=False)

    class Meta:
        model = SequenceAnalysis
        fields = ['clonal_complex', 'insilico_serotype']
