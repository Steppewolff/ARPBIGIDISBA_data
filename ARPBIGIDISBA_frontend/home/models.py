# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from random import choices

import multiselectfield
from django.db import models
from multiselectfield import MultiSelectField

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
    fastq_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="FASTQ path", db_comment="Path to the folder where FASTQ files of the isolate are stored")
    fastq_files_names = models.JSONField(blank=True, null=True, verbose_name="FASTQ file/s name/s", db_comment="Name of the FASTQ files of the isolate, separated by comma if more than one")
    denovo_assembly_path = models.CharField(max_length=255, blank=True, null=True, verbose_name="De novo files path", db_comment="Path to the folder where de novo files of the isolate are stored")
    denovo_assembly_ena_url = models.CharField(max_length=255, blank=True, null=True, verbose_name="ENA de novo file url", db_comment="Path to the endpoint in ENA database where assembly file of the isolate is stored")
    denovo_fastq_ena_url = models.JSONField(blank=True, null=True, verbose_name="ENA FASTQ url", db_comment="JSON with paths to endpoints in ENA database where FASTQ files of the isolate are stored")
    ena_accession = models.CharField(max_length=100, blank=True, null=True, verbose_name="ENA accession number", db_comment="Accession number of the isolate in ENA database")
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
    isolate_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Isolate name", db_comment="Isolate name in its project")
    isolate_project_code = models.CharField(unique=True, max_length=50, blank=True, null=True, verbose_name="Project code", db_comment="Official project code")
    species = models.CharField(max_length=255, blank=True, null=True, verbose_name="Species", db_comment="Isolate species")
    project_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Project name", db_comment="Internal name of the project")
    isolation_day = models.IntegerField(blank=True, null=True, verbose_name="Isolate obtention day", db_comment="Isolate obtention day")
    isolation_month = models.IntegerField(blank=True, null=True, verbose_name="Isolate obtention month", db_comment="Isolate obtention month")
    isolation_year = models.IntegerField(blank=True, null=True, verbose_name="Isolate obtention year", db_comment="Isolate obtention year")
    isolation_date = models.DateField(blank=True, null=True, verbose_name="Isolate obtention date", db_comment="Whole date of obtention of the isolate")
    isolate_source = models.CharField(max_length=255, blank=True, null=True, verbose_name="Isolate origin", db_comment="Clinic origin of the isolate")
    isolate_comments = models.CharField(max_length=255, blank=True, null=True, verbose_name="Isolate comments", db_comment="Comments about the isolate")

    class Meta:
        managed = True
        db_table = 'metadata_general'

    def __str__(self):
        return self.isolate_name
        # return str(self.isolate_id)


class MetadataClinic(models.Model):
    clinic_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    patient_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Patient code", db_comment="Code of the patient in the project")
    sample_type = models.ForeignKey(SampleType, models.DO_NOTHING, db_column='sample_type_id', blank=True, null=True, verbose_name="Sample type", db_comment="Type of the sample from which the isolate was obtained")
    # hospital_id = models.ForeignKey(Hospital, models.DO_NOTHING, related_name='hospitals', db_column='hospital_id', blank=True, null=True, verbose_name="Hospital", db_comment="Name of the hospital where the isolate was obtained")
    hospital = models.ForeignKey(Hospital, models.DO_NOTHING, related_name='hospitals', db_column='hospital_id', blank=True, null=True, verbose_name="Hospital", db_comment="Name of the hospital where the isolate was obtained")
    collection_ward = models.CharField(max_length=255, blank=True, null=True, verbose_name="Ward", db_comment="Name of the departament where the isolate was obtained")

    class Meta:
        managed = True
        db_table = 'metadata_clinic'


class Mic(models.Model):
    mic_id = models.AutoField(primary_key=True, verbose_name="MIC_id")
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    pip = models.CharField(max_length=10, blank=True, null=True, verbose_name="Piperacillin", help_text="PIP-ARO:0000078", db_comment='Valor numérico de la concentración mínima inhibitoria de piperacilina')
    pip_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Piperacillin clinical category", help_text="PIP-ARO:0000078 clinical category", db_comment='Categoría clínica de resistencia del aislado a piperacilina')
    pip_tz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Piperacillin/Tazobactam", help_text="PIP/TZ-ARO:3004021", db_comment='Valor numérico de la concentración mínima inhibitoria de piperacilina/tazobactam')
    pip_tz_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Piperacillin/Tazobactam clinical category", help_text="PIP/TZ-ARO:3004021 clinical category", db_comment='Categoría clínica de resistencia del aislado a piperacilina/tazobactam')
    fep = models.CharField(max_length=10, blank=True, null=True, verbose_name="Cefepime", help_text="FEP-ARO:0000059", db_comment='Valor numérico de la concentración mínima inhibitoria de cefepima')
    fep_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Cefepime clinical category", help_text="FEP-ARO:0000059 clinical category", db_comment='Categoría clínica de resistencia del aislado a cefepima')
    cfdc = models.CharField(max_length=10, blank=True, null=True, verbose_name="Cefiderocol", help_text="FDC-ARO:3004474", db_comment='Valor numérico de la concentración mínima inhibitoria de cefiderocol')
    cfdc_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Cefiderocol clinical category", help_text="FDC-ARO:3004474 clinical category", db_comment='Categoría clínica de resistencia del aislado a cefiderocol')
    caz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ceftazidime", help_text="CAZ-ARO:0000060", db_comment='Valor numérico de la concentración mínima inhibitoria de ceftazidima')
    caz_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Ceftazidime clinical category", help_text="CAZ-ARO:0000060 clinical category", db_comment='Categoría clínica de resistencia del aislado a ceftazidima')
    caz_avi = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ceftazidime/Avibactam", help_text="CAZ/AVI-ARO:3007072", db_comment='Valor numérico de la concentración mínima inhibitoria de ceftazidima/avibactam')
    caz_avi_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Ceftazidime/Avibactam clinical category", help_text="CAZ/AVI-ARO:3007072 clinical category", db_comment='Categoría clínica de resistencia del aislado a ceftazidima/avibactam')
    tol = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ceftolozane", help_text="TOL-ARO:3003927", db_comment='Valor numérico de la concentración mínima inhibitoria de ceftolozano')
    tol_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Ceftolozane clinical category", help_text="TOL-ARO:3003927 clinical category", db_comment='Categoría clínica de resistencia del aislado a tebipenem pivoxil')
    ctz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ceftolozane/Tazobactam", help_text="TOL/TZ-ARO:3004724", db_comment='Valor numérico de la concentración mínima inhibitoria de ceftolozano/tazobactam')
    ctz_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Ceftolozane/Tazobactam clinical category", help_text="TOL/TZ-ARO:3004724 clinical category", db_comment='Categoría clínica de resistencia del aislado a ceftolozano')
    imi = models.CharField(max_length=10, blank=True, null=True, verbose_name="Imipenem", help_text="IMI-ARO:3000170", db_comment='Valor numérico de la concentración mínima inhibitoria de imipenem')
    imi_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Imipenem clinical category", help_text="IMI-ARO:3000170 clinical category", db_comment='Categoría clínica de resistencia del aislado a imipenem')
    #*********************************************************************************************************************************************************
    # Pendiente de revisar help_text
    #*********************************************************************************************************************************************************
    imi_rel = models.CharField(max_length=10, blank=True, null=True, verbose_name="Imipenem/Relebactam", help_text="IMI/REL-ARO:????????", db_comment='Valor numérico de la concentración mínima inhibitoria de imipenem/relebactam')
    imi_rel_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Imipenem/Relebactam clinical category", help_text="IMI/REL-ARO:???????? clinical category", db_comment='Categoría clínica de resistencia del aislado a imipenem/relebactam')
    mer = models.CharField(max_length=10, blank=True, null=True, verbose_name="Meropenem", help_text="MER-ARO:0000073", db_comment='Valor numérico de la concentración mínima inhibitoria de meropenem')
    mer_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Meropenem clinical category", help_text="MER-ARO:0000073 clinical category", db_comment='Categoría clínica de resistencia del aislado a meropenem')
    mer_vab = models.CharField(max_length=10, blank=True, null=True, verbose_name="Meropenem/Vaborbactam", help_text="MER/VAB-ARO:3007146", db_comment='Valor numérico de la concentración mínima inhibitoria de meropenem/vaborbactam')
    mer_vab_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Meropenem/Vaborbactam clinical category", help_text="MER/VAB-ARO:3007146 clinical category", db_comment='Categoría clínica de resistencia del aislado a meropenem/vaborbactam')
    atm = models.CharField(max_length=10, blank=True, null=True, verbose_name="Aztreonam", help_text="AZT-ARO:3000550", db_comment='Valor numérico de la concentración mínima inhibitoria de aztreonam')
    atm_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Aztreonam clinical category", help_text="AZT-ARO:3000550 clinical category", db_comment='Categoría clínica de resistencia del aislado a aztreonam')
    azt_avi = models.CharField(max_length=10, blank=True, null=True, verbose_name="Aztreonam/Avibactam", help_text="AZT/AVI-ARO:3007366", db_comment='Valor numérico de la concentración mínima inhibitoria de aztreonam/avibactam')
    azt_avi_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Aztreonam/Avibactam clinical category", help_text="AZT/AVI-ARO:3007366 clinical category", db_comment='Categoría clínica de resistencia del aislado a aztreonam/avibactam')
    cip = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ciprofloxacin", help_text="CIP-ARO:0000036", db_comment='Valor numérico de la concentración mínima inhibitoria de ciprofloxacino')
    cip_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Ciprofloxacin clinical category", help_text="CIP-ARO:0000036 clinical category", db_comment='Categoría clínica de resistencia del aislado a ciprofloxacino')
    dlx = models.CharField(max_length=10, blank=True, null=True, verbose_name="Delafloxacin", help_text="DLX-ARO:3004462", db_comment='Valor numérico de la concentración mínima inhibitoria de delafloxacino')
    dlx_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Delafloxacin clinical category", help_text="DLX-ARO:3004462 clinical category", db_comment='Categoría clínica de resistencia del aislado a delafloxacino')
    lvx = models.CharField(max_length=10, blank=True, null=True, verbose_name="Levofloxacin", help_text="LVX-ARO:0000071", db_comment='Valor numérico de la concentración mínima inhibitoria de levofloxacino')
    lvx_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Levofloxacin clinical category", help_text="LVX-ARO:0000071 clinical category", db_comment='Categoría clínica de resistencia del aislado a levofloxacino')
    mxl = models.CharField(max_length=10, blank=True, null=True, verbose_name="Moxifloxacin", help_text="MXL-ARO:0000074", db_comment='Valor numérico de la concentración mínima inhibitoria de moxifloxacino')
    mxl_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Moxifloxacin clinical category", help_text="MXL-ARO:0000074 clinical category", db_comment='Categoría clínica de resistencia del aislado a moxifloxacino')
    ami = models.CharField(max_length=10, blank=True, null=True, verbose_name="Amikacin", help_text="AMI-ARO:0000013", db_comment='Valor numérico de la concentración mínima inhibitoria de amikacina')
    ami_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Amikacin clinical category", help_text="AMI-ARO:0000013 clinical category", db_comment='Categoría clínica de resistencia del aislado a amikacina')
    gen = models.CharField(max_length=10, blank=True, null=True, verbose_name="Gentamycin", help_text="GEN-ARO:3007382", db_comment='Valor numérico de la concentración mínima inhibitoria de gentamicina')
    gen_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Gentamycin clinical category", help_text="GEN-ARO:3007382 clinical category", db_comment='Categoría clínica de resistencia del aislado a gentamicina')
    net = models.CharField(max_length=10, blank=True, null=True, verbose_name="Netilmycin", help_text="NET-ARO:0000038", db_comment='Valor numérico de la concentración mínima inhibitoria de netilmicina')
    net_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Netilmycin clinical category", help_text="NET-ARO:0000038 clinical category", db_comment='Categoría clínica de resistencia del aislado a netilmicina')
    tob = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tobramycin", help_text="TOB-ARO:0000052", db_comment='Valor numérico de la concentración mínima inhibitoria de tobramicina')
    tob_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Tobramycin clinical category", help_text="TOB-ARO:0000052 clinical category", db_comment='Categoría clínica de resistencia del aislado a tobramicina')
    col = models.CharField(max_length=10, blank=True, null=True, verbose_name="Colistin", help_text="COL-ARO:0000067", db_comment='Valor numérico de la concentración mínima inhibitoria de colistina')
    col_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Colistin clinical category", help_text="COL-ARO:0000067 clinical category", db_comment='Categoría clínica de resistencia del aislado a colistina')
    fo = models.CharField(max_length=10, blank=True, null=True, verbose_name="Fosfomycin", help_text="FOS-ARO:0000025", db_comment='Valor numérico de la concentración mínima inhibitoria de fosfomicina')
    fo_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Fosfomycin clinical category", help_text="FOS-ARO:0000025 clinical category", db_comment='Categoría clínica de resistencia del aislado a fosfomicina')
    tic = models.CharField(max_length=10, blank=True, null=True, verbose_name="Ticarcillin", help_text="TIC-ARO:3003832", db_comment='Valor numérico de la concentración mínima inhibitoria de ticarcilina')
    tic_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Ticarcillin clinical category", help_text="TIC-ARO:3003832 clinical category", db_comment='Categoría clínica de resistencia del aislado a ticarcilina')
    ptz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Piperacillin/Tazobactam", help_text="PIP/TZ-ARO:3004021", db_comment='Valor numérico de la concentración mínima inhibitoria de piperacilina/tazobactam')
    ptz_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Piperacillin/Tazobactam clinical category", help_text="PIP/TZ-ARO:3004021 clinical category", db_comment='Categoría clínica de resistencia del aislado a piperacilina/tazobactam')
    taz = models.CharField(max_length=10, blank=True, null=True, verbose_name="Tazobactam", help_text="TZ-ARO:0000077", db_comment='Valor numérico de la concentración mínima inhibitoria de tazobactam')
    taz_clinical_category = models.CharField(max_length=2, blank=True, null=True, verbose_name="Tazobactam clinical category", help_text="TZ-ARO:0000077 clinical category", db_comment='Categoría clínica de resistencia del aislado a tazobactam')
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

REFERENCE_STRAIN_OPTIONS=(
    ('GCF_000006765.1', 'PAO1_GCF_000006765.1'),
    ('GCF_000014625.1', 'PA14_GCF_000014625.1'),
    ('-', 'N/A'),
    ('OT', 'Other'),
)

FUNCTION_OPTIONS=(
    ('AR', 'Antibiotic resistance'),
    ('HYP', 'Hypermutation'),
    ('-', 'N/A'),
    ('OT', 'Other'),
)

SUBSET_OPTIONS=(
    ('BASIC', 'Basic resistome'),
    ('CR', 'Cefiderocol resistance'),
    ('MLST', 'Locus for MLST identification'),
    ('-', 'N/A'),
    ('OT', 'Other'),
)

class InterestGenes(models.Model):
    interest_genes_id = models.AutoField(primary_key=True)
    locus = models.CharField(max_length=20, blank=True, null=True)
    reference_strain = models.CharField(max_length=100, choices=REFERENCE_STRAIN_OPTIONS, blank=True, null=True)
    start_position = models.IntegerField(blank=True, null=True)
    end_position = models.IntegerField(blank=True, null=True)
    official_name = models.CharField(max_length=20, blank=True, null=True)
    synonym_name = models.CharField(max_length=20, blank=True, null=True)
    pbp_name = models.CharField(max_length=20, blank=True, null=True)
    function = models.CharField(max_length=255, choices=FUNCTION_OPTIONS, blank=True, null=True)
    subset = multiselectfield.MultiSelectField(max_length=100, choices=SUBSET_OPTIONS, blank=True, null=True)
    polymorphisms = models.JSONField(blank=True, null=True, db_comment="Known polymorphisms, in JSON format")
    allele = models.CharField(max_length=100, blank=True, null=True, db_comment="Allele and (strain reference)")
    species = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'genes_of_interest'
        verbose_name = 'Gene of interest'
        verbose_name_plural = 'Genes of interest'


ATB_SUSCEPTIBILITY_METHOD_CHOICES = (
    ('DD', 'Disc diffusion (halo diameter in mm.)'),
    ('BM', 'Broth microdilution (mg/L)'),
    ('ET', 'E-test'),
    ('OT', 'Other'),
)

BROTH_TYPE_CHOICES = (
    ('IH', 'In-house)'),
    ('CM', 'Commercial'),
)

class PhenotypicData(models.Model):
    phenotypic_data_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    atb_susceptibility_method = models.CharField(max_length=100, blank=True, null=True, choices=ATB_SUSCEPTIBILITY_METHOD_CHOICES, verbose_name="ATB susceptibility method", db_comment="Method used to determine antibiotic susceptibility")
    atb_susceptibility_method_other = models.CharField(max_length=100, blank=True, null=True, verbose_name="ATB susceptibility other method", db_comment="Other method used to determine antibiotic susceptibility")
    broth_type = models.CharField(max_length=100, blank=True, null=True, choices=BROTH_TYPE_CHOICES, verbose_name="Broth type", db_comment="Type of broth used in the susceptibility test")
    commercial_panel_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Commercial panel name", db_comment="Name of the commercial panel used in the susceptibility test")
    mic = models.ForeignKey(Mic, models.DO_NOTHING, db_column='mic_id', blank=True, null=True)
    ecdc_resistance_profile = models.CharField(max_length=3, blank=True, null=True, verbose_name="ECDC profile", db_comment='Resistance profile following ECDC guidelines')
    idsa_resistance_profile = models.CharField(max_length=3, blank=True, null=True, verbose_name="IDSA profile", db_comment='Resistance profile following IDSA guidelines')
    cloxa_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="CLOXA test", db_comment='CLOXA test result, accepted values: +/-')
    mbl_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="MBL test", db_comment='MBL test result, accepted values: +/-')
    esbl_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="ESBL test", db_comment='ESBL test result, accepted values: +/-')
    class_a_carbapenemase_test = models.CharField(max_length=3, blank=True, null=True, verbose_name="Class A carbapenemases", db_comment='Class A carbapenemases test result')
    invitro_serotype = models.ForeignKey(InvitroSerotype, models.DO_NOTHING, db_column='invitro_serotype_id', blank=True, null=True, verbose_name="In vitro serotype")
    hypermutator_phenotype = models.CharField(max_length=15, blank=True, null=True, verbose_name="Hypermutator phenotype", db_comment='Hypermutator phenotype')
    phenotypic_comments = models.TextField(blank=True, null=True, verbose_name="Phenotypic comments", db_comment='Comments about isolate phenotype characteristics')

    class Meta:
        managed = True
        db_table = 'phenotypic_data'
        verbose_name_plural = 'Phenotypic Data'


class SequenceAnalysis(models.Model):
    sequence_analysis_id = models.AutoField(primary_key=True)
    isolate_id = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True, db_column='isolate_id')
    mlst_allelic_profile = models.JSONField(blank=True, null=True, verbose_name="MLST allelic profile", db_comment="Allelic values of loci used in multilocus strain typing, using JSON format")
    sequence_type = models.CharField(max_length=10, blank=True, null=True, verbose_name="Sequence type", db_comment="Sequence type of the isolate")
    clonal_complex = models.CharField(max_length=10, blank=True, null=True, verbose_name="Clonal complex", db_comment="Clonal complex of the isolate")
    mutational_resistome = models.JSONField(blank=True, null=True, db_comment="Mutational resistome, using JSON format")
    ame_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="AME loci", db_comment="Aminoglycoside modifying enzymes loci, name list comma-separated")
    beta_lactamase_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Beta-lactamases/Carbapenemases loci", db_comment="Beta-lactamases/Carbapenemases loci, name list comma-separated")
    fluoroquinolones_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Fluoroquinolones resistance determinants", db_comment="Fluoroquinolones resistance determinants loci, name list comma-separated")
    other_acq_loci = models.CharField(max_length=500, blank=True, null=True, verbose_name="Other acquired resistance determinants", db_comment="Other acquired resistance determinants, name list comma-separated")
    acquired_resistome = models.JSONField(blank=True, null=True, db_comment="Acquired resistome, in JSON format")
    virulence_genes = models.JSONField(blank=True, null=True, db_comment="Virulencia genes, in JSON format")
    hypermutation_genes = models.JSONField(blank=True, null=True, db_comment="Hypermutation genes, in JSON format")
    insilico_serotype = models.CharField(max_length=3, blank=True, null=True, verbose_name="In silico serotype", db_comment="Phenotypic in silico serotype of the isolate")
    betalactamase_pcr = models.JSONField(blank=True, null=True, db_comment="Beta-lactamases PCR results, in JSON format")

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
    sequencing_goal = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sequencing goal", db_comment="Objective for sequencing this isolate")
    sequencing_source = models.CharField(max_length=100, blank=True, null=True, verbose_name="Sequencing source", db_comment="Where was the sequencing obtained")
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
