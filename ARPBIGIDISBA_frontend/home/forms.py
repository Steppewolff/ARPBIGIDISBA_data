from django.forms import Form, ChoiceField, CharField, ModelChoiceField, ModelForm, Select, TextInput

from .models import Hospital, Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral, MetadataClinic, InvitroSerotype, SampleType


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id


class MetadataGeneralForm(ModelForm):
    isolate_name = ModelChoiceField(
        queryset=MetadataGeneral.objects.values_list('isolate_name', flat=True).distinct(), to_field_name="isolate_name", label='Isolate name',
        empty_label='Select an isolate', required=False) # , widget=TextInput(attrs={'name': 'Nombre aislado en forms'})
    project_name = ModelChoiceField(
        queryset=MetadataGeneral.objects.values_list('project_name', flat=True).distinct(), label='Project',
        empty_label='Select a project', required=False) # , widget=TextInput(attrs={'name': 'Nombre proyecto en forms'})

    class Meta:
        model = MetadataGeneral
        exclude = ('isolate_project_id',)

    def __init__(self, *args, **kwargs):
        super(MetadataGeneralForm, self).__init__(*args, **kwargs)
        self.fields["project_name"].widget.attrs.update({"name": "custom_name"})


class MetadataClinicForm(ModelForm):
    sample_type = ModelChoiceField(queryset=SampleType.objects.all(), widget=Select(),
                               to_field_name='sample_type_id', label="Sample type", empty_label='Select a sample type', required=False)

    collection_ward = ModelChoiceField(queryset=MetadataClinic.objects.values_list('collection_ward', flat=True).distinct(),
                              to_field_name="collection_ward", label='Obtaining ward', empty_label='Select a ward',
                              required=False)

    class Meta:
        model = MetadataClinic
        fields = ['sample_type', 'collection_ward'] # 'patient_id', 'hospital',

    def __init__(self, *args, **kwargs):
        super(MetadataClinicForm, self).__init__(*args, **kwargs)
        self.fields['sample_type'].label_from_instance = lambda obj: obj.sample_en


class HospitalForm(ModelForm):
    country = ModelChoiceField(queryset=Hospital.objects.values_list('country', flat=True).distinct(), widget=Select(),
                               to_field_name='country', label="Country", empty_label='Select a country', required=False)


    region = ModelChoiceField(queryset=Hospital.objects.values_list('region', flat=True).distinct(),
                              to_field_name="clinic_id", label='Region', empty_label='Select a region',
                              required=False)
    town = ModelChoiceField(queryset=Hospital.objects.values_list('town', flat=True).distinct(), to_field_name="town",
                            label='Town', empty_label='Select a town', required=False)
    hospital = ModelChoiceField(queryset=Hospital.objects.all().distinct(),
                                to_field_name="hospital_id", label='Hospital', empty_label='Select a hospital', required=False)


    class Meta:
        model = Hospital
        fields = ['hospital', 'country', 'region', 'town']

    def __init__(self, *args, **kwargs):
        super(HospitalForm, self).__init__(*args, **kwargs)
        # self.fields["hospital"].label_from_instance = lambda obj: obj.hospital_id


class MicForm(ModelForm):
    class Meta:
        model = Mic
        fields = ['tic',
                  'pip',
                  'pip_tz',
                  'caz',
                  'caz_avi',
                  'tol',
                  'ctz',
                  'fep',
                  'cfdc',
                  'fep_tan',
                  'fep_zid',
                  'fdc_xer',
                  'atm',
                  'azt_avi',
                  'imi',
                  'imi_rel',
                  'mer',
                  'mer_vab',
                  'mer_nac',
                  'mer_xer',
                  'ami',
                  'tob',
                  'gen',
                  'net',
                  'cip',
                  'lvx',
                  'dlx',
                  'mxl',
                  'col',
                  'fo',
                  'taz',
                  'avi',
                  'rel',
                  'nac',
                  'dur',
                  'xer',
                  ]


class FenotipoForm(ModelForm):
    ecdc_resistance_profile = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('ecdc_resistance_profile', flat=True).distinct(),
        label='ECDC profile', empty_label='Select a ECDC profile', required=False)
    idsa_resistance_profile = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('idsa_resistance_profile', flat=True).distinct(),
        label='IDSA profile', empty_label='Select a IDSA profile', required=False)
    cloxa_test = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('cloxa_test', flat=True).distinct(),
        label='Cloxa test', empty_label='Select a result', required=False)
    mbl_test = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('mbl_test', flat=True).distinct(),
        label='MBL test', empty_label='Select a result', required=False)
    esbl_test = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('esbl_test', flat=True).distinct(),
        label='ESBL test', empty_label='Select a result', required=False)
    invitro_serotype = ModelChoiceField(
        queryset=InvitroSerotype.objects.values_list('invitro_value', flat=True).distinct(),
        label='In vitro serotype', empty_label='Select a result', required=False)

    class Meta:
        model = PhenotypicData
        fields = ['ecdc_resistance_profile', 'idsa_resistance_profile', 'cloxa_test', 'mbl_test', 'esbl_test', 'invitro_serotype']


class SequenceAnalysisForm(ModelForm):
    clonal_complex = ModelChoiceField(
        queryset=SequenceAnalysis.objects.values_list('clonal_complex', flat=True).distinct(),
        label='Clonal complex', empty_label='Select a clonal complex', required=False)
    insilico_serotype = ModelChoiceField(
        queryset=InvitroSerotype.objects.values_list('invitro_value', flat=True).distinct(),
        label='In silico serotype', empty_label='Select a result', required=False)

    class Meta:
        model = SequenceAnalysis
        fields = ['clonal_complex', 'insilico_serotype']
