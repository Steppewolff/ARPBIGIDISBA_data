from django.forms import Form, ChoiceField, CharField, ModelChoiceField, ModelForm, Select, TextInput, MultipleChoiceField, SelectMultiple, CheckboxSelectMultiple, Textarea
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field
from .models import Hospital, Mic, PhenotypicData, SequenceAnalysis, MetadataGeneral, MetadataClinic, InvitroSerotype, SampleType, Ward, SIR_OPTIONS


class MyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return "My Object #%i" % obj.id


class MetadataGeneralForm(ModelForm):
    isolate_name = MultipleChoiceField(
        choices=[],
        widget=SelectMultiple(attrs={'class': 'form-control select2', 'id': 'isolateNameSelect'}),
        label='Isolate name',
        required=False
    )
    project_name = MultipleChoiceField(
        choices=[],
        widget=SelectMultiple(attrs={'class': 'form-control select2', 'id': 'projectNameSelect'}),
        label='Project',
        required=False
    )

    class Meta:
        model = MetadataGeneral
        exclude = ('isolate_project_id',)

    def __init__(self, *args, **kwargs):
        super(MetadataGeneralForm, self).__init__(*args, **kwargs)
        # self.fields["project_name"].widget.attrs.update({"name": "custom_name"})
        self.fields['isolate_name'].choices = [
            (v, v) for v in MetadataGeneral.objects.values_list('isolate_name', flat=True).distinct().order_by('isolate_name') if v
        ]
        self.fields['project_name'].choices = [
            (v, v) for v in MetadataGeneral.objects.values_list('project_name', flat=True).distinct().order_by('project_name') if v
        ]

class MetadataClinicForm(ModelForm):
    sample_type = ModelChoiceField(queryset=SampleType.objects.all(), widget=Select(),
                               to_field_name='sample_type_id', label="Sample type", empty_label='Select a sample type', required=False)

    collection_ward = ModelChoiceField(
        queryset=Ward.objects.all().order_by('ward_name_en'),
        empty_label='Select a ward',
        required=False,
        label='Obtaining ward'
    )

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

class MicForm(ModelForm):
    class Meta:
        model = Mic
        fields = ['tic',
                  'tic_clinical_category',
                  'pip',
                  'pip_clinical_category',
                  'pip_tz',
                  'pip_tz_clinical_category',
                  'caz',
                  'caz_clinical_category',
                  'caz_avi',
                  'caz_avi_clinical_category',
                  'tol',
                  'tol_clinical_category',
                  'ctz',
                  'ctz_clinical_category',
                  'fep',
                  'fep_clinical_category',
                  'cfdc',
                  'cfdc_clinical_category',
                  'fep_tan',
                  'fep_tan_clinical_category',
                  'fep_zid',
                  'fep_zid_clinical_category',
                  'fdc_xer',
                  'fdc_xer_clinical_category',
                  'atm',
                  'atm_clinical_category',
                  'azt_avi',
                  'azt_avi_clinical_category',
                  'imi',
                  'imi_clinical_category',
                  'imi_rel',
                  'imi_rel_clinical_category',
                  'mer',
                  'mer_clinical_category',
                  'mer_vab',
                  'mer_vab_clinical_category',
                  'mer_nac',
                  'mer_nac_clinical_category',
                  'mer_xer',
                  'mer_xer_clinical_category',
                  'ami',
                  'ami_clinical_category',
                  'tob',
                  'tob_clinical_category',
                  'gen',
                  'gen_clinical_category',
                  'net',
                  'net_clinical_category',
                  'cip',
                  'cip_clinical_category',
                  'lvx',
                  'lvx_clinical_category',
                  'dlx',
                  'dlx_clinical_category',
                  'mxl',
                  'mxl_clinical_category',
                  'col',
                  'col_clinical_category',
                  'fo',
                  'fo_clinical_category',
                  'taz',
                  'taz_clinical_category',
                  'avi',
                  'avi_clinical_category',
                  'rel',
                  'rel_clinical_category',
                  'nac',
                  'nac_clinical_category',
                  'dur',
                  'dur_clinical_category',
                  'xer',
                  'xer_clinical_category',
                  ]


class MicSearchForm(Form):
    """
    Formulario de búsqueda MIC con multiselect para categorías clínicas
    """

    # Campos MIC numéricos (texto libre)
    tic = CharField(max_length=10, required=False)
    pip = CharField(max_length=10, required=False)
    pip_tz = CharField(max_length=10, required=False)
    caz = CharField(max_length=10, required=False)
    caz_avi = CharField(max_length=10, required=False)
    tol = CharField(max_length=10, required=False)
    ctz = CharField(max_length=10, required=False)
    fep = CharField(max_length=10, required=False)
    cfdc = CharField(max_length=10, required=False)
    fep_tan = CharField(max_length=10, required=False)
    fep_zid = CharField(max_length=10, required=False)
    fdc_xer = CharField(max_length=10, required=False)
    atm = CharField(max_length=10, required=False)
    azt_avi = CharField(max_length=10, required=False)
    imi = CharField(max_length=10, required=False)
    imi_rel = CharField(max_length=10, required=False)
    mer = CharField(max_length=10, required=False)
    mer_vab = CharField(max_length=10, required=False)
    mer_nac = CharField(max_length=10, required=False)
    mer_xer = CharField(max_length=10, required=False)
    ami = CharField(max_length=10, required=False)
    tob = CharField(max_length=10, required=False)
    gen = CharField(max_length=10, required=False)
    net = CharField(max_length=10, required=False)
    cip = CharField(max_length=10, required=False)
    lvx = CharField(max_length=10, required=False)
    dlx = CharField(max_length=10, required=False)
    mxl = CharField(max_length=10, required=False)
    col = CharField(max_length=10, required=False)
    fo = CharField(max_length=10, required=False)
    taz = CharField(max_length=10, required=False)
    avi = CharField(max_length=10, required=False)
    rel = CharField(max_length=10, required=False)
    nac = CharField(max_length=10, required=False)
    dur = CharField(max_length=10, required=False)
    xer = CharField(max_length=10, required=False)
    caz_cloxa = CharField(max_length=10, required=False)
    imi_cloxa = CharField(max_length=10, required=False)

    # Campos de categorías clínicas como MULTISELECT
    tic_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        # label="Categoría clínica TIC",
        label=Mic._meta.get_field('tic_clinical_category').verbose_name,
    )
    pip_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('pip_clinical_category').verbose_name,
    )
    pip_tz_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('pip_tz_clinical_category').verbose_name,
    )
    caz_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('caz_clinical_category').verbose_name,
    )
    caz_avi_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('caz_avi_clinical_category').verbose_name,
    )
    tol_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('tol_clinical_category').verbose_name,
    )
    ctz_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('ctz_clinical_category').verbose_name,
    )
    fep_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('fep_clinical_category').verbose_name,
    )
    cfdc_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('cfdc_clinical_category').verbose_name,
    )
    fep_tan_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('fep_tan_clinical_category').verbose_name,
    )
    fep_zid_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('fep_zid_clinical_category').verbose_name,
    )
    fdc_xer_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('fdc_xer_clinical_category').verbose_name,
    )
    atm_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('atm_clinical_category').verbose_name,
    )
    azt_avi_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('azt_avi_clinical_category').verbose_name,
    )
    imi_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('imi_clinical_category').verbose_name,
    )
    imi_rel_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('imi_rel_clinical_category').verbose_name,
    )
    mer_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('mer_clinical_category').verbose_name,
    )
    mer_vab_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('mer_vab_clinical_category').verbose_name,
    )
    mer_nac_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('mer_nac_clinical_category').verbose_name,
    )
    mer_xer_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('mer_xer_clinical_category').verbose_name,
    )
    ami_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('ami_clinical_category').verbose_name,
    )
    tob_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('tob_clinical_category').verbose_name,
    )
    gen_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('gen_clinical_category').verbose_name,
    )
    net_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('net_clinical_category').verbose_name,
    )
    cip_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('cip_clinical_category').verbose_name,
    )
    lvx_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('lvx_clinical_category').verbose_name,
    )
    dlx_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('dlx_clinical_category').verbose_name,
    )
    mxl_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('mxl_clinical_category').verbose_name,
    )
    col_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('col_clinical_category').verbose_name,
    )
    fo_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('fo_clinical_category').verbose_name,
    )
    taz_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('taz_clinical_category').verbose_name,
    )
    avi_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('avi_clinical_category').verbose_name,
    )
    rel_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('rel_clinical_category').verbose_name,
    )
    nac_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('nac_clinical_category').verbose_name,
    )
    dur_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('dur_clinical_category').verbose_name,
    )
    xer_clinical_category = MultipleChoiceField(
        choices=SIR_OPTIONS,
        required=False,
        widget=SelectMultiple,
        label=Mic._meta.get_field('xer_clinical_category').verbose_name,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['tic_clinical_category'].label = "Categoría clínica TIC init"
        self.helper = FormHelper()
        self.helper.form_method = 'get'

class FenotipoForm(ModelForm):
    ecdc_resistance_profile = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('ecdc_resistance_profile', flat=True).distinct(),
        label='ECDC profile', empty_label='Select a ECDC profile', required=False)
    dtr_profile = ModelChoiceField(
        queryset=PhenotypicData.objects.values_list('dtr_profile', flat=True).distinct(),
        label='DTR profile', empty_label='Select a DTR profile', required=False)
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
    sequence_type = ModelChoiceField(
        queryset=SequenceAnalysis.objects.values_list('sequence_type', flat=True).distinct().order_by('sequence_type'),
        label='Sequence type', empty_label='Select a Sequence type', required=False)
    insilico_serotype = ModelChoiceField(
        queryset=InvitroSerotype.objects.values_list('invitro_value', flat=True).distinct(),
        label='In silico serotype', empty_label='Select a result', required=False)

    class Meta:
        model = SequenceAnalysis
        fields = ['sequence_type', 'insilico_serotype']
