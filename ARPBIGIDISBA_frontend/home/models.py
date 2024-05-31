from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Archivo(models.Model):
    archivo_id = models.AutoField(primary_key=True)
    aislado = models.OneToOneField('MetadataGeneral', models.DO_NOTHING, blank=True, null=True)
    fastq = models.CharField(max_length=255, blank=True, null=True)
    ensamblado = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'archivo'


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


class Fenotipo(models.Model):
    fenotipo_id = models.AutoField(primary_key=True)
    aislado = models.OneToOneField('MetadataGeneral', models.DO_NOTHING, blank=True, null=True)
    metodo_suscept = models.CharField(max_length=100, blank=True, null=True)
    cmi_id = models.CharField(max_length=10, blank=True, null=True)
    cat_clinica = models.CharField(max_length=3, blank=True, null=True)
    perfil_ecdc = models.CharField(max_length=3, blank=True, null=True)
    perfil_idsa = models.CharField(max_length=3, blank=True, null=True)
    test_cloxa = models.CharField(max_length=3, blank=True, null=True)
    test_mbl = models.CharField(max_length=3, blank=True, null=True)
    test_blee = models.CharField(max_length=3, blank=True, null=True)
    test_carba_a = models.CharField(db_column='test_carba_A', max_length=3, blank=True, null=True)  # Field name made lowercase.
    serotipo_invitro = models.CharField(max_length=3, blank=True, null=True)
    cevs = models.IntegerField(blank=True, null=True)
    virulencia_galleria = models.IntegerField(blank=True, null=True)
    fenot_hipermutador = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fenotipo'


class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True)
    hospital_nombre = models.CharField(max_length=255, blank=True, null=True)
    pais = models.CharField(max_length=255, blank=True, null=True)
    region = models.CharField(max_length=255, blank=True, null=True)
    localidad = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Hospitales'
        managed = False
        db_table = 'hospital'


class Libreria(models.Model):
    libreria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    metodo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'libreria'


class LocusHipermutacion(models.Model):
    hipermut_id = models.AutoField(primary_key=True)
    locus = models.CharField(max_length=20, blank=True, null=True)
    nombre_oficial = models.CharField(max_length=6, blank=True, null=True)
    nombre_sinonimo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Locus hipermutación'
        verbose_name_plural = 'Loci hipermutación'
        managed = False
        db_table = 'locus_hipermutacion'


class LocusMlst(models.Model):
    mlst_id = models.AutoField(primary_key=True)
    locus = models.CharField(max_length=20, blank=True, null=True)
    nombre_oficial = models.CharField(max_length=6, blank=True, null=True)
    nombre_sinonimo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Locus MLST'
        verbose_name_plural = 'Loci MLST'
        managed = False
        db_table = 'locus_mlst'


class LocusVirulencia(models.Model):
    virulencia_id = models.AutoField(primary_key=True)
    locus = models.CharField(max_length=20, blank=True, null=True)
    nombre_oficial = models.CharField(max_length=6, blank=True, null=True)
    nombre_sinonimo = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Locus virulencia'
        verbose_name_plural = 'Loci virulencia'
        managed = False
        db_table = 'locus_virulencia'


class MetadataClinico(models.Model):
    clinico_id = models.AutoField(primary_key=True)
    paciente_id = models.CharField(max_length=255, blank=True, null=True)
    tipo_muestra = models.CharField(max_length=255, blank=True, null=True)
    hospital = models.OneToOneField(Hospital, models.DO_NOTHING, db_column='hospital', blank=True, null=True)
    servicio_obtencion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Dato clínico'
        verbose_name_plural = 'Datos clínicos'
        managed = False
        db_table = 'metadata_clinico'


class MetadataGeneral(models.Model):
    aislado_id = models.AutoField(primary_key=True)
    aislado_nombre = models.CharField(max_length=50, blank=True, null=True)
    aislado_exportar_id = models.CharField(unique=True, max_length=50, blank=True, null=True)
    especie = models.CharField(max_length=255, blank=True, null=True)
    nombre_proyecto = models.CharField(max_length=255, blank=True, null=True)
    aislamiento_dia = models.IntegerField(blank=True, null=True)
    aislamiento_mes = models.IntegerField(blank=True, null=True)
    aislamiento_year = models.IntegerField(blank=True, null=True)
    aislamiento_fecha = models.DateField(blank=True, null=True)
    origen = models.CharField(max_length=255, blank=True, null=True)
    observaciones = models.CharField(max_length=255, blank=True, null=True)
    parental_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.aislado_nombre

    class Meta:
        verbose_name = 'Metadato general'
        verbose_name_plural = 'Metadatos generales'
        managed = False
        db_table = 'metadata_general'


class Mic(models.Model):
    mic_id = models.AutoField(primary_key=True)
    aislado = models.OneToOneField(MetadataGeneral, on_delete=models.DO_NOTHING, blank=True, null=True)
    mic_fecha = models.DateField(blank=True, null=True)
    pip = models.CharField(max_length=10, blank=True, null=True)
    pip_tz = models.CharField(max_length=10, blank=True, null=True)
    fep = models.CharField(max_length=10, blank=True, null=True)
    cfdc = models.CharField(max_length=10, blank=True, null=True)
    caz = models.CharField(max_length=10, blank=True, null=True)
    caz_avi = models.CharField(max_length=10, blank=True, null=True)
    ct = models.CharField(max_length=10, blank=True, null=True)
    imi = models.CharField(max_length=10, blank=True, null=True)
    imi_rel = models.CharField(max_length=10, blank=True, null=True)
    mer = models.CharField(max_length=10, blank=True, null=True)
    mer_vab = models.CharField(max_length=10, blank=True, null=True)
    azt = models.CharField(max_length=10, blank=True, null=True)
    azt_avi = models.CharField(max_length=10, blank=True, null=True)
    cip = models.CharField(max_length=10, blank=True, null=True)
    dlx = models.CharField(max_length=10, blank=True, null=True)
    lvx = models.CharField(max_length=10, blank=True, null=True)
    mxl = models.CharField(max_length=10, blank=True, null=True)
    ami = models.CharField(max_length=10, blank=True, null=True)
    gen = models.CharField(max_length=10, blank=True, null=True)
    net = models.CharField(max_length=10, blank=True, null=True)
    tob = models.CharField(max_length=10, blank=True, null=True)
    col = models.CharField(max_length=10, blank=True, null=True)
    fo = models.CharField(max_length=10, blank=True, null=True)
    tic = models.CharField(max_length=10, blank=True, null=True)
    ptz = models.CharField(max_length=10, blank=True, null=True)
    taz = models.CharField(max_length=10, blank=True, null=True)
    cza = models.CharField(max_length=10, blank=True, null=True)
    tol = models.CharField(max_length=10, blank=True, null=True)
    atm = models.CharField(max_length=10, blank=True, null=True)
    caz_cloxa = models.CharField(max_length=3, blank=True, null=True)
    imi_cloxa = models.CharField(max_length=3, blank=True, null=True)
    mic_observaciones = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mic'


class Plataforma(models.Model):
    plataforma_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    proveedor = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plataforma'


class ResistomaAdquirido(models.Model):
    resistoma_adq_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20, blank=True, null=True)
    tipo_funcion = models.CharField(max_length=6, blank=True, null=True)

    class Meta:
        verbose_name = 'Mutación resistoma adquirido'
        verbose_name_plural = 'Mutaciones resistoma adquirido'
        managed = False
        db_table = 'resistoma_adquirido'


class ResistomaMutante(models.Model):
    resistoma_mut_id = models.AutoField(primary_key=True)
    locus = models.CharField(max_length=20, blank=True, null=True)
    nombre_oficial = models.CharField(max_length=6, blank=True, null=True)
    nombre_sinonimo = models.CharField(max_length=6, blank=True, null=True)
    nombre_pbp = models.CharField(max_length=6, blank=True, null=True)
    especie = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Mutación resistoma mutacional'
        verbose_name_plural = 'Mutaciones resistoma mutacional'
        managed = False
        db_table = 'resistoma_mutante'


class Secuencia(models.Model):
    secuencia_id = models.AutoField(primary_key=True)
    aislado = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True)
    perfil_mlst = models.JSONField(blank=True, null=True)
    clon = models.CharField(max_length=10, blank=True, null=True)
    complejo_clonal = models.CharField(max_length=10, blank=True, null=True)
    resistoma_mutante = models.JSONField(blank=True, null=True)
    resistoma_adquirido = models.JSONField(blank=True, null=True)
    genes_virulencia = models.JSONField(blank=True, null=True)
    genes_hipermutacion = models.JSONField(blank=True, null=True)
    serotipo_insilico = models.CharField(max_length=3, blank=True, null=True)
    betalactamasas_adquiridas = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'secuencia'


class Secuenciacion(models.Model):
    secuenciacion_id = models.AutoField(primary_key=True)
    aislado = models.OneToOneField(MetadataGeneral, models.DO_NOTHING, blank=True, null=True)
    tecnica_sec = models.ForeignKey('Tecnica', models.DO_NOTHING, db_column='tecnica_sec', blank=True, null=True)
    plataforma_sec = models.ForeignKey(Plataforma, models.DO_NOTHING, db_column='plataforma_sec', blank=True, null=True)
    motivo_sec = models.CharField(max_length=100, blank=True, null=True)
    origen_sec = models.CharField(max_length=100, blank=True, null=True)
    preparacion_librerias = models.ForeignKey(Libreria, models.DO_NOTHING, db_column='preparacion_librerias', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Secuenciaciones'
        managed = False
        db_table = 'secuenciacion'


class Tecnica(models.Model):
    tecnica_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, blank=True, null=True)
    lecturas = models.CharField(max_length=255, blank=True, null=True)
    metodo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tecnica'


class TipoMuestra(models.Model):
    tipo_muestra_id = models.AutoField(primary_key=True)
    tipo = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Tipo de muestra'
        verbose_name_plural = 'Tipos de muestra'
        managed = False
        db_table = 'tipo_muestra'
