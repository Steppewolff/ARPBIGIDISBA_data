# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcquiredResistome(models.Model):
    acquired_resistome_id = models.AutoField(primary_key=True)
    acquired_gene_name = models.CharField(max_length=20, blank=True, null=True)
    gene_type = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'acquired_resistome'


class Assembler(models.Model):
    assembler_id = models.AutoField(primary_key=True)
    assembler_name = models.IntegerField(unique=True, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'assembler'

    def __str__(self):
        return self.assembler_name


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FilePath(models.Model):
    file_path_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField('MetadataGeneral', models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    fastq_path = models.CharField(max_length=255, blank=True, null=True)
    denovo_assembly_path = models.CharField(max_length=255, blank=True, null=True)
    assembler = models.ForeignKey(Assembler, models.DO_NOTHING, db_column='assembler', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'file_path'


class FlowcellKit(models.Model):
    flowcell_kit_id = models.AutoField(primary_key=True)
    flowcell_kit_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'flowcell_kit'

    def __str__(self):
        return self.flowcell_kit_name


class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True, db_column='hospital_id')
    hospital_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre hospital")
    hospital_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Código hospital")
    hospital_ccn = models.CharField(max_length=10, blank=True, null=True, verbose_name="Código CCN hospital")
    hospital_codcnh = models.CharField(max_length=6, blank=True, null=True, verbose_name="Código CODCNH hospital")
    hospital_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comentarios hospital")
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name="País")
    region = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comunidad autónoma")
    sub_region = models.CharField(max_length=255, blank=True, null=True, verbose_name="Provincia")
    town = models.CharField(max_length=255, blank=True, null=True, verbose_name="Localidad")
    geo_longitude = models.FloatField(blank=True, null=True, verbose_name="Longitud")
    geo_latitude = models.FloatField(blank=True, null=True, verbose_name="Latitud")

    class Meta:
        managed = True
        db_table = 'hospital'

    def __str__(self):
        return self.hospital_name


class SampleType(models.Model):
    sample_type_id = models.AutoField(primary_key=True, verbose_name="Tipo de muestra")
    sample = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tipo de muestra")

    class Meta:
        managed = True
        db_table = 'sample_type'

    def __str__(self):
        return self.sample


class HypermutationGene(models.Model):
    hypermutation_gene_id = models.AutoField(primary_key=True)
    locus = models.CharField(max_length=20, blank=True, null=True)
    official_name = models.CharField(max_length=6, blank=True, null=True)
    synonym_name = models.CharField(max_length=6, blank=True, null=True)
    species = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hypermutation_gene'


class InvitroSerotype(models.Model):
    invitro_serotype_id = models.AutoField(primary_key=True)
    invitro_value = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'invitro_serotype'

    def __str__(self):
        return self.invitro_value


class LocusMlst(models.Model):
    mlst_id = models.AutoField(primary_key=True)
    locus = models.CharField(max_length=20, blank=True, null=True)
    official_name = models.CharField(max_length=6, blank=True, null=True)
    synonym_name = models.CharField(max_length=6, blank=True, null=True)
    species = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'locus_mlst'


class MetadataGeneral(models.Model):
    isolate_id = models.AutoField(primary_key=True)
    isolate_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nombre aislado")
    isolate_project_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    species = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especie")
    project_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre proyecto")
    isolation_day = models.IntegerField(blank=True, null=True)
    isolation_month = models.IntegerField(blank=True, null=True)
    isolation_year = models.IntegerField(blank=True, null=True)
    isolation_date = models.DateField(blank=True, null=True, verbose_name="Fecha aislado")
    isolate_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="Origen aislado")
    isolate_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comentarios aislado")

    class Meta:
        managed = True
        db_table = 'metadata_general'

    def __str__(self):
        return self.isolate_name
        # return str(self.isolate_id)


class MetadataClinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    patient_id = models.CharField(max_length=255, blank=True, null=True)
    sample_type = models.ForeignKey(SampleType, models.DO_NOTHING, db_column='sample_type', blank=True, null=True, verbose_name="Tipo de muestra")
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, related_name='hospitals', db_column='hospital', blank=True, null=True)
    collection_ward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Departamento donde se obtuvo")

    class Meta:
        managed = True
        db_table = 'metadata_clinic'


class Mic(models.Model):
    mic_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    pip = models.CharField(max_length=10, blank=True, null=True)
    pip_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    pip_tz = models.CharField(max_length=10, blank=True, null=True)
    pip_tz_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    fep = models.CharField(max_length=10, blank=True, null=True)
    fep_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    cfdc = models.CharField(max_length=10, blank=True, null=True)
    cfdc_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    caz = models.CharField(max_length=10, blank=True, null=True)
    caz_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    caz_avi = models.CharField(max_length=10, blank=True, null=True)
    caz_avi_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    ctz = models.CharField(max_length=10, blank=True, null=True)
    ctz_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    imi = models.CharField(max_length=10, blank=True, null=True)
    imi_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    imi_rel = models.CharField(max_length=10, blank=True, null=True)
    imi_rel_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    mer = models.CharField(max_length=10, blank=True, null=True)
    mer_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    mer_vab = models.CharField(max_length=10, blank=True, null=True)
    mer_vab_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    azt = models.CharField(max_length=10, blank=True, null=True)
    azt_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    azt_avi = models.CharField(max_length=10, blank=True, null=True)
    azt_avi_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    cip = models.CharField(max_length=10, blank=True, null=True)
    cip_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    dlx = models.CharField(max_length=10, blank=True, null=True)
    dlx_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    lvx = models.CharField(max_length=10, blank=True, null=True)
    lvx_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    mxl = models.CharField(max_length=10, blank=True, null=True)
    mxl_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    ami = models.CharField(max_length=10, blank=True, null=True)
    ami_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    gen = models.CharField(max_length=10, blank=True, null=True)
    gen_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    net = models.CharField(max_length=10, blank=True, null=True)
    net_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    tob = models.CharField(max_length=10, blank=True, null=True)
    tob_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    col = models.CharField(max_length=10, blank=True, null=True)
    col_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    fo = models.CharField(max_length=10, blank=True, null=True)
    fo_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    tic = models.CharField(max_length=10, blank=True, null=True)
    tic_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    ptz = models.CharField(max_length=10, blank=True, null=True)
    ptz_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    taz = models.CharField(max_length=10, blank=True, null=True)
    taz_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    cza = models.CharField(max_length=10, blank=True, null=True)
    cza_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    tol = models.CharField(max_length=10, blank=True, null=True)
    tol_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    atm = models.CharField(max_length=10, blank=True, null=True)
    atm_clinical_category = models.CharField(max_length=2, blank=True, null=True)
    caz_cloxa = models.CharField(max_length=3, blank=True, null=True)
    imi_cloxa = models.CharField(max_length=3, blank=True, null=True)
    mic_comments = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mic'

    def __str__(self):
        return str(self.mic_id)


class MutationalResistome(models.Model):
    mutational_resistome_id = models.AutoField(primary_key=True)
    locus = models.CharField(max_length=20, blank=True, null=True)
    official_name = models.CharField(max_length=6, blank=True, null=True)
    synonym_name = models.CharField(max_length=6, blank=True, null=True)
    pbp_name = models.CharField(max_length=6, blank=True, null=True)
    species = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'mutational_resistome'


class PhenotypicData(models.Model):
    phenotypic_data_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    ab_susceptibility_method = models.CharField(max_length=100, blank=True, null=True, verbose_name="Test susceptibilidad antibiótica")
    mic = models.ForeignKey(Mic, models.DO_NOTHING, blank=True, null=True)
    ecdc_resistance_profile = models.CharField(max_length=3, blank=True, null=True, verbose_name="Perfil ECDC")
    idsa_resistance_profile = models.CharField(max_length=3, blank=True, null=True, verbose_name="Perfil IDSA")
    cloxa_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="Test cloxa")
    mbl_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="Test mbl")
    esbl_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="Test esbl")
    class_a_carbapenemase_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="Test Carbapenemasas clase A")
    invitro_serotype = models.ForeignKey(InvitroSerotype, models.DO_NOTHING, blank=True, null=True, verbose_name="Serotipo in vitro")
    hypermutator_phenotype = models.CharField(max_length=15, blank=True, null=True, verbose_name="Fenotipo hipermutador")
    phenotypic_comments = models.TextField(blank=True, null=True, verbose_name="Comentarios fenotipo")

    class Meta:
        managed = True
        db_table = 'phenotypic_data'
        verbose_name_plural = 'Phenotypic Data'


class SequenceAnalysis(models.Model):
    sequence_analysis_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    mlst_allelic_profile = models.JSONField(blank=True, null=True, verbose_name="Perfil alélico MLST")
    sequence_type = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tipo de secuencia")
    clonal_complex = models.CharField(max_length=10, blank=True, null=True, verbose_name="Complejo clonal")
    mutational_resistome = models.JSONField(blank=True, null=True)
    ame_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Loci EMA")
    beta_lactamase_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Loci beta lactamasas")
    carbapenemase_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Loci carbapeneasas")
    other_acq_ab_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Loci otros AB adquiridos")
    acquired_resistome = models.JSONField(blank=True, null=True)
    virulence_genes = models.JSONField(blank=True, null=True)
    hypermutation_genes = models.JSONField(blank=True, null=True)
    insilico_serotype = models.CharField(max_length=3, blank=True, null=True, verbose_name="Serotipo in silico")
    betalactamase_pcr = models.JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sequence_analysis'
        verbose_name_plural = 'Sequence Analyses'


class SequencingInfo(models.Model):
    sequencing_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    sequencing_technology = models.ForeignKey('SequencingTechnology', models.DO_NOTHING,
                                              db_column='sequencing_technology', blank=True, null=True)
    sequencing_platform = models.ForeignKey('SequencingPlatform', models.DO_NOTHING, db_column='sequencing_platform',
                                            blank=True, null=True)
    flowcell_kit = models.ForeignKey(FlowcellKit, models.DO_NOTHING, db_column='flowcell_kit', blank=True, null=True)
    sequencing_goal = models.CharField(max_length=100, blank=True, null=True)
    sequencing_source = models.CharField(max_length=100, blank=True, null=True)
    library_method = models.ForeignKey('SequencingLibrary', models.DO_NOTHING, db_column='library_method', blank=True,
                                       null=True)

    class Meta:
        managed = True
        db_table = 'sequencing_info'


class SequencingLibrary(models.Model):
    sequencing_library_id = models.AutoField(primary_key=True)
    sequencing_library_method = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sequencing_library'
        verbose_name_plural = 'Sequence libraries'

    def __str__(self):
        return self.sequencing_library_method


class SequencingPlatform(models.Model):
    sequencing_platform_id = models.AutoField(primary_key=True)
    sequencing_platform_name = models.CharField(max_length=255, blank=True, null=True)
    sequencing_platform_supplier = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sequencing_platform'

    def __str__(self):
        return self.sequencing_platform_name


class SequencingTechnology(models.Model):
    sequencing_technology_id = models.AutoField(primary_key=True)
    sequencing_technology_name = models.CharField(max_length=255, blank=True, null=True)
    reads_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'sequencing_technology'
        verbose_name_plural = 'Sequencing technologies'

    def __str__(self):
        return self.sequencing_technology_name


class VirulenceGene(models.Model):
    virulence_gene_id = models.AutoField(primary_key=True)
    locus = models.CharField(max_length=20, blank=True, null=True)
    official_name = models.CharField(max_length=6, blank=True, null=True)
    synonym_name = models.CharField(max_length=6, blank=True, null=True)
    species = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'virulence_gene'
