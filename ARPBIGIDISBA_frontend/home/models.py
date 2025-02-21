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

class BreakpointTable(models.Model):
    breakpoint_table_id = models.AutoField(primary_key=True)
    table_version_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Tabla Puntos de corte")
    table_version_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Versíón de tabla")
    valid_date = models.DateTimeField(verbose_name="Fecha inicio de validez")
    organism = models.CharField(max_length=100, blank=True, null=True, verbose_name="Organismo")
    organization = models.CharField(max_length=50, blank=True, null=True, verbose_name="Organización")
    filepath = models.FilePathField(max_length=255, blank=True, null=True)
    mic_breakpoints = models.JSONField(blank=True, null=True)
    zd_breakpoints = models.JSONField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'breakpoint'

    def __str__(self):
        return self.table_version_name

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
    fastq_path = models.CharField(max_length=255, blank=True, null=True, db_comment="Ruta de ubicación de los archivos fastq del aislado")
    denovo_assembly_path = models.CharField(max_length=255, blank=True, null=True, db_comment="Ruta de ubicación de los archivos de ensamblaje denovo del aislado")
    assembler = models.ForeignKey(Assembler, models.DO_NOTHING, db_column='assembler_id', blank=True, null=True, db_comment="Ensamblador utilizado")

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
    isolate_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nombre aislado", db_comment="Nombre del aislado")
    isolate_project_code = models.CharField(unique=True, max_length=50, blank=True, null=True, verbose_name="Código proyecto", db_comment="código del proyecto")
    species = models.CharField(max_length=255, blank=True, null=True, verbose_name="Especie", db_comment="Especie del aislado")
    project_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nombre proyecto", db_comment="Nombre del proyecto")
    isolation_day = models.IntegerField(blank=True, null=True, db_comment="Día de obtención del aislado")
    isolation_month = models.IntegerField(blank=True, null=True, db_comment="Mes de obtención del aislado")
    isolation_year = models.IntegerField(blank=True, null=True, db_comment="Año de obtención del aislado")
    isolation_date = models.DateField(blank=True, null=True, verbose_name="Fecha aislado", db_comment="Fecha completa de obtención del aislado")
    isolate_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="Origen aislado", db_comment="Origen clínico del aislado")
    isolate_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="Comentarios aislado", db_comment="Comentarios sobre el aislado")

    class Meta:
        managed = True
        db_table = 'metadata_general'

    def __str__(self):
        return self.isolate_name
        # return str(self.isolate_id)


class MetadataClinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    patient_code = models.CharField(max_length=255, blank=True, null=True)
    sample_type = models.ForeignKey(SampleType, models.DO_NOTHING, db_column='sample_type_id', blank=True, null=True, verbose_name="Tipo de muestra", db_comment="Tipo de muestra del que se obtuvo el aislado")
    hospital_id = models.ForeignKey(Hospital, models.DO_NOTHING, related_name='hospitals', db_column='hospital_id', blank=True, null=True, db_comment="Hospital donde se obtuvo el aislado")
    collection_ward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Departamento donde se obtuvo", db_comment="Departamento del hospital donde se obtuvo el aislado")

    class Meta:
        managed = True
        db_table = 'metadata_clinic'


class Mic(models.Model):
    mic_id = models.AutoField(primary_key=True, verbose_name="MIC_id")
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    pip = models.CharField(max_length=10, blank=True, null=True, verbose_name="Piperacilina", db_comment='Valor numérico de la concentración mínima inhibitoria de piperacilina')
    pip_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a piperacilina')
    pip_tz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Piperacilina/Tazobactam", db_comment='Valor numérico de la concentración mínima inhibitoria de piperacilina/tazobactam')
    pip_tz_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a piperacilina/tazobactam')
    fep = models.CharField(max_length=10, blank=True, null=True, verbose_name="Cefepima", db_comment='Valor numérico de la concentración mínima inhibitoria de cefepima')
    fep_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a cefepima')
    cfdc = models.CharField(max_length=10, blank=True, null=True, verbose_name="Cefiderocol", db_comment='Valor numérico de la concentración mínima inhibitoria de cefiderocol')
    cfdc_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a cefiderocol')
    caz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ceftazidima", db_comment='Valor numérico de la concentración mínima inhibitoria de ceftazidima')
    caz_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a ceftazidima')
    caz_avi = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ceftazidima/Avibactam", db_comment='Valor numérico de la concentración mínima inhibitoria de ceftazidima/avibactam')
    caz_avi_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a ceftazidima/avibactam')
    ctz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ceftolozano", db_comment='Valor numérico de la concentración mínima inhibitoria de ceftolozano')
    ctz_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a ceftolozano')
    imi = models.CharField(max_length=10, blank=True, null=True, verbose_name="Imipenem", db_comment='Valor numérico de la concentración mínima inhibitoria de imipenem')
    imi_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a imipenem')
    imi_rel = models.CharField(max_length=10, blank=True, null=True, verbose_name="Imipenem/Relebactam", db_comment='Valor numérico de la concentración mínima inhibitoria de imipenem/relebactam')
    imi_rel_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a imipenem/relebactam')
    mer = models.CharField(max_length=10, blank=True, null=True, verbose_name="Meropenem", db_comment='Valor numérico de la concentración mínima inhibitoria de meropenem')
    mer_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a meropenem')
    mer_vab = models.CharField(max_length=10, blank=True, null=True, verbose_name="Meropenem/Vaborbactam", db_comment='Valor numérico de la concentración mínima inhibitoria de meropenem/vaborbactam')
    mer_vab_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a meropenem/vaborbactam')
    azt = models.CharField(max_length=10, blank=True, null=True, verbose_name="Aztreonam", db_comment='Valor numérico de la concentración mínima inhibitoria de aztreonam')
    azt_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a aztreonam')
    azt_avi = models.CharField(max_length=10, blank=True, null=True, verbose_name="Aztreonam/Avibactam", db_comment='Valor numérico de la concentración mínima inhibitoria de aztreonam/avibactam')
    azt_avi_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a aztreonam/avibactam')
    cip = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ciprofloxacino", db_comment='Valor numérico de la concentración mínima inhibitoria de ciprofloxacino')
    cip_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a ciprofloxacino')
    dlx = models.CharField(max_length=10, blank=True, null=True, verbose_name="Delafloxacino", db_comment='Valor numérico de la concentración mínima inhibitoria de delafloxacino')
    dlx_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a delafloxacino')
    lvx = models.CharField(max_length=10, blank=True, null=True, verbose_name="Levofloxacino", db_comment='Valor numérico de la concentración mínima inhibitoria de levofloxacino')
    lvx_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a levofloxacino')
    mxl = models.CharField(max_length=10, blank=True, null=True, verbose_name="Moxifloxacino", db_comment='Valor numérico de la concentración mínima inhibitoria de moxifloxacino')
    mxl_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a moxifloxacino')
    ami = models.CharField(max_length=10, blank=True, null=True, verbose_name="Amikacina", db_comment='Valor numérico de la concentración mínima inhibitoria de amikacina')
    ami_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a amikacina')
    gen = models.CharField(max_length=10, blank=True, null=True, verbose_name="Gentamicina", db_comment='Valor numérico de la concentración mínima inhibitoria de gentamicina')
    gen_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a gentamicina')
    net = models.CharField(max_length=10, blank=True, null=True, verbose_name="Netilmicina", db_comment='Valor numérico de la concentración mínima inhibitoria de netilmicina')
    net_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a netilmicina')
    tob = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tobramicina", db_comment='Valor numérico de la concentración mínima inhibitoria de tobramicina')
    tob_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a tobramicina')
    col = models.CharField(max_length=10, blank=True, null=True, verbose_name="Colistina", db_comment='Valor numérico de la concentración mínima inhibitoria de colistina')
    col_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a colistina')
    fo = models.CharField(max_length=10, blank=True, null=True, verbose_name="Fosfomicina", db_comment='Valor numérico de la concentración mínima inhibitoria de fosfomicina')
    fo_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a fosfomicina')
    tic = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ticarcilina", db_comment='Valor numérico de la concentración mínima inhibitoria de ticarcilina')
    tic_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a ticarcilina')
    ptz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Piperacilina/Tazobactam", db_comment='Valor numérico de la concentración mínima inhibitoria de piperacilina/tazobactam')
    ptz_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a piperacilina/tazobactam')
    taz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tazobactam", db_comment='Valor numérico de la concentración mínima inhibitoria de tazobactam')
    taz_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a tazobactam')
    cza = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ceftazidima/Avibactam", db_comment='Valor numérico de la concentración mínima inhibitoria de ceftazidima/avibactam')
    cza_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a ceftazidima/avibactam')
    tol = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tebipenem pivoxil", db_comment='Valor numérico de la concentración mínima inhibitoria de tebipenem pivoxil')
    tol_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a tebipenem pivoxil')
    atm = models.CharField(max_length=10, blank=True, null=True, verbose_name="Aztreonam", db_comment='Valor numérico de la concentración mínima inhibitoria de aztreonam')
    atm_clinical_category = models.CharField(max_length=2, blank=True, null=True, db_comment='Categoría clínica de resistencia del aislado a aztreonam')
    caz_cloxa = models.CharField(max_length=3, blank=True, null=True, db_comment='Valor numérico de la concentración mínima inhibitoria de ceftazidima/cloxacilina')
    imi_cloxa = models.CharField(max_length=3, blank=True, null=True, db_comment='Valor numérico de la concentración mínima inhibitoria de imipenem/cloxacilina')
    mic_comments = models.CharField(max_length=255, blank=True, null=True, db_comment='Comentarios de la concentración mínima inhibitoria')

    class Meta:
        managed = True
        db_table = 'mic'
        verbose_name = 'MIC'

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
    ab_susceptibility_method = models.CharField(max_length=100, blank=True, null=True, verbose_name="Test susceptibilidad antibiótica", db_comment="Método utilizado para determinar la susceptibilidad antibiótica")
    mic = models.ForeignKey(Mic, models.DO_NOTHING, db_column='mic_id', blank=True, null=True)
    ecdc_resistance_profile = models.CharField(max_length=3, blank=True, null=True, verbose_name="Perfil ECDC", db_comment='Perfil de resistencia según ECDC')
    idsa_resistance_profile = models.CharField(max_length=3, blank=True, null=True, verbose_name="Perfil IDSA", db_comment='Perfil de resistencia según IDSA')
    cloxa_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="Test cloxa", db_comment='Valor del test cloxa de ceftazidima, valores: +/-')
    mbl_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="Test mbl", db_comment='Valor del test mbl, valores: +/-')
    esbl_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="Test esbl", db_comment='Valor del test esbl, valores: +/-')
    class_a_carbapenemase_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="Test Carbapenemasas clase A", db_comment='Valor del test de carbapenemasas clase A')
    invitro_serotype = models.ForeignKey(InvitroSerotype, models.DO_NOTHING, db_column='invitro_serotype_id', blank=True, null=True, verbose_name="Serotipo in vitro")
    hypermutator_phenotype = models.CharField(max_length=15, blank=True, null=True, verbose_name="Fenotipo hipermutador", db_comment='Fenotipo hipermutador')
    phenotypic_comments = models.TextField(blank=True, null=True, verbose_name="Comentarios fenotipo", db_comment='Comentarios sobre el fenotipo del aislado')

    class Meta:
        managed = True
        db_table = 'phenotypic_data'
        verbose_name_plural = 'Phenotypic Data'


class SequenceAnalysis(models.Model):
    sequence_analysis_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    mlst_allelic_profile = models.JSONField(blank=True, null=True, verbose_name="Perfil alélico MLST", db_comment="Perfil alélico de MLST en formato JSON")
    sequence_type = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tipo de secuencia", db_comment="ST del aislado")
    clonal_complex = models.CharField(max_length=10, blank=True, null=True, verbose_name="Complejo clonal", db_comment="Complejo clonal del aislado")
    mutational_resistome = models.JSONField(blank=True, null=True, db_comment="Resistoma mutacional en formato JSON")
    ame_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Loci EMA", db_comment="Loci de enzimas de modificación de aminoglucósidos, listado de nombres separados por comas")
    beta_lactamase_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Loci beta lactamasas", db_comment="Loci de beta-lactamasas, listado de nombres separados por comas")
    carbapenemase_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Loci carbapeneasas", db_comment="Loci de carbapenemasas, listado de nombres separados por comas")
    other_acq_ab_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Loci otros AB adquiridos", db_comment="Loci de otros genes de resistencia adquiridos, listado de nombres separados por comas")
    acquired_resistome = models.JSONField(blank=True, null=True, db_comment="Resistoma adquirido en formato JSON")
    virulence_genes = models.JSONField(blank=True, null=True, db_comment="Genes de virulencia en formato JSON")
    hypermutation_genes = models.JSONField(blank=True, null=True, db_comment="Genes de hipermutación en formato JSON")
    insilico_serotype = models.CharField(max_length=3, blank=True, null=True, verbose_name="Serotipo in silico", db_comment="Serotipo in silico del aislado")
    betalactamase_pcr = models.JSONField(blank=True, null=True, db_comment="Resultados de PCR de beta-lactamasas en formato JSON")

    class Meta:
        managed = True
        db_table = 'sequence_analysis'
        verbose_name_plural = 'Sequence Analyses'


class SequencingInfo(models.Model):
    sequencing_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    sequencing_technology = models.ForeignKey('SequencingTechnology', models.DO_NOTHING,
                                              db_column='sequencing_technology_id', blank=True, null=True, db_comment="Tecnología de secuenciación para obtener el aislado")
    sequencing_platform = models.ForeignKey('SequencingPlatform', models.DO_NOTHING, db_column='sequencing_platform_id',
                                            blank=True, null=True, db_comment="Plataforma de secuenciación para obtener el aislado")
    flowcell_kit = models.ForeignKey(FlowcellKit, models.DO_NOTHING, db_column='flowcell_kit_id', blank=True, null=True, db_comment='Flowcell Kit utilizado en la secuenciación')
    sequencing_goal = models.CharField(max_length=100, blank=True, null=True, db_comment="Objetivo de la secuenciación, cual es el motivo para el que se realiza la secuenciación")
    sequencing_source = models.CharField(max_length=100, blank=True, null=True, db_comment="Fuente de la secuenciación, de donde se obtuvo la secuencia")
    library_method = models.ForeignKey('SequencingLibrary', models.DO_NOTHING, db_column='library_method_id', blank=True,
                                       null=True, db_comment="Método de preparación de la librería")

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
