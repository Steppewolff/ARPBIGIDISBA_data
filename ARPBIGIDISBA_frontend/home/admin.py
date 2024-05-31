from django.contrib import admin

from .models import Archivo, Fenotipo, Hospital, Libreria, LocusMlst, LocusHipermutacion, LocusVirulencia, MetadataClinico, MetadataGeneral, Mic, Plataforma, ResistomaAdquirido, ResistomaMutante, Secuencia, Secuenciacion, Tecnica, TipoMuestra

class ArchivoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Archivo._meta.fields]  # Mostrar todos los campos

class FenotipoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Fenotipo._meta.fields]  # Mostrar todos los campos

class HospitalAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Hospital._meta.fields]  # Mostrar todos los campos

class LibreriaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Libreria._meta.fields]  # Mostrar todos los campos

class LocusMlstAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LocusMlst._meta.fields]  # Mostrar todos los campos

class LocusHipermutacionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LocusHipermutacion._meta.fields]  # Mostrar todos los campos

class LocusVirulenciaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LocusVirulencia._meta.fields]  # Mostrar todos los campos

class MetadataClinicoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MetadataClinico._meta.fields]  # Mostrar todos los campos

class MetadataGeneralAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MetadataGeneral._meta.fields]  # Mostrar todos los campos

class MicAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mic._meta.fields]  # Mostrar todos los campos

class PlataformaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Plataforma._meta.fields]  # Mostrar todos los campos

class ResistomaAdquiridoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ResistomaAdquirido._meta.fields]  # Mostrar todos los campos

class ResistomaMutanteAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ResistomaMutante._meta.fields]  # Mostrar todos los campos

class SecuenciaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Secuencia._meta.fields]  # Mostrar todos los campos

class SecuenciacionAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Secuenciacion._meta.fields]  # Mostrar todos los campos

class TecnicaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Tecnica._meta.fields]  # Mostrar todos los campos

class TipoMuestraAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TipoMuestra._meta.fields]  # Mostrar todos los campos


# Register your models here.
admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(Fenotipo, FenotipoAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(Libreria, LibreriaAdmin)
admin.site.register(LocusMlst, LocusMlstAdmin)
admin.site.register(LocusHipermutacion, LocusHipermutacionAdmin)
admin.site.register(LocusVirulencia, LocusVirulenciaAdmin)
admin.site.register(MetadataClinico, MetadataClinicoAdmin)
admin.site.register(MetadataGeneral, MetadataGeneralAdmin)
admin.site.register(Mic, MicAdmin)
admin.site.register(Plataforma, PlataformaAdmin)
admin.site.register(ResistomaAdquirido, ResistomaAdquiridoAdmin)
admin.site.register(ResistomaMutante, ResistomaMutanteAdmin)
admin.site.register(Secuencia, SecuenciaAdmin)
admin.site.register(Secuenciacion, SecuenciacionAdmin)
admin.site.register(Tecnica, TecnicaAdmin)
admin.site.register(TipoMuestra, TipoMuestraAdmin)
