from django.contrib import admin
from .custom_admin import custom_admin_site  # Importamos el Admin personalizado
from advanced_filters.admin import AdminAdvancedFiltersMixin

from .models import AcquiredResistome, Assembler, FilePath, FlowcellKit, Hospital, HypermutationGene, InvitroSerotype, \
    LocusMlst, MetadataClinic, MetadataGeneral, Mic, MutationalResistome, PhenotypicData, SampleType, SequenceAnalysis, \
    SequencingInfo, SequencingLibrary, SequencingPlatform, SequencingTechnology, VirulenceGene

class ModeloRelacionadoMetadataClinic(admin.TabularInline):  # o StackedInline
    model = MetadataClinic  # Modelo relacionado
    extra = 0  # Opcional: número de formularios vacíos

class ModeloRelacionadPhenotypicData(admin.TabularInline):  # o StackedInline
    model = PhenotypicData  # Modelo relacionado
    extra = 0  # Opcional: número de formularios vacíos

class ModeloRelacionadSequenceAnalysis(admin.TabularInline):  # o StackedInline
    model = SequenceAnalysis  # Modelo relacionado
    extra = 0  # Opcional: número de formularios vacíos

class ModeloRelacionadMic(admin.TabularInline):  # o StackedInline
    model = Mic  # Modelo relacionado
    extra = 0  # Opcional: número de formularios vacíos

class ModeloRelacionadFilePath(admin.TabularInline):  # o StackedInline
    model = FilePath  # Modelo relacionado
    extra = 0  # Opcional: número de formularios vacíos

@admin.register(MetadataGeneral)
class ModeloPrincipalAdmin(admin.ModelAdmin):
    inlines = [ModeloRelacionadoMetadataClinic, ModeloRelacionadPhenotypicData, ModeloRelacionadSequenceAnalysis, ModeloRelacionadMic, ModeloRelacionadFilePath]
    # list_display = ('campo1', 'campo2', 'get_otro_campo')

    # def get_otro_campo(self, obj):
    #     # Si la relación es OneToOne o existe un único objeto relacionado,
    #     # podemos acceder directamente
    #     return obj.modelorelacionado.campo
    # get_otro_campo.short_description = 'Campo Relacionado'

class AcquiredResistomeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AcquiredResistome._meta.fields]  # Mostrar todos los campos


class AssemblerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Assembler._meta.fields]  # Mostrar todos los campos


class FilePathAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FilePath._meta.fields]  # Mostrar todos los campos


class FlowcellKitAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FlowcellKit._meta.fields]  # Mostrar todos los campos


class HospitalAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Hospital._meta.fields]  # Mostrar todos los campos
    list_filter = ["country", "region", "town"]


class HypermutationGeneAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HypermutationGene._meta.fields]  # Mostrar todos los campos


class InvitroSerotypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in InvitroSerotype._meta.fields]  # Mostrar todos los campos


class LocusMlstAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LocusMlst._meta.fields]  # Mostrar todos los campos


class MetadataClinicAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MetadataClinic._meta.fields]  # Mostrar todos los campos

    class Media:
        js = (
            'js/admin_js.js',  # project static folder
        )


class MetadataGeneralAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MetadataGeneral._meta.fields]  # Mostrar todos los campos

    class Media:
        js = (
            'js/admin_js.js',  # project static folder
        )


class MicAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mic._meta.fields]  # Mostrar todos los campos

    class Media:
        js = (
            'js/admin_js.js',  # project static folder
        )


class MutationalResistomeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MutationalResistome._meta.fields]  # Mostrar todos los campos


class PhenotypicDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PhenotypicData._meta.fields]  # Mostrar todos los campos

    class Media:
        js = (
            'js/admin_js.js',  # project static folder
        )


class SampleTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SampleType._meta.fields]  # Mostrar todos los campos


class SequenceAnalysisAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequenceAnalysis._meta.fields]  # Mostrar todos los campos

    class Media:
        js = (
            # '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',  # jquery
            'js/admin_js.js',  # project static folder
        )


class SequencingInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequencingInfo._meta.fields]  # Mostrar todos los campos


class SequencingLibraryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequencingLibrary._meta.fields]  # Mostrar todos los campos


class SequencingPlatformAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequencingPlatform._meta.fields]  # Mostrar todos los campos


class SequencingTechnologyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequencingTechnology._meta.fields]  # Mostrar todos los campos


class VirulenceGeneAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VirulenceGene._meta.fields]  # Mostrar todos los campos


class MicAdminFilter(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = [field.name for field in Mic._meta.fields]  # Mostrar todos los campos
    list_filter = [field.name for field in Mic._meta.fields if
                   field.name not in ['mic_id', 'mic_comments', 'isolate']]  # simple list filters

    advanced_filter_fields = [field.name for field in Mic._meta.fields if
                              field.name not in ['mic_id', 'mic_comments', 'isolate']]

    class Media:
        js = (
            'js/admin_js.js',  # project static folder
        )

# Register your models here using admin.py
admin.site.register(AcquiredResistome, AcquiredResistomeAdmin)
admin.site.register(Assembler, AssemblerAdmin)
admin.site.register(FilePath, FilePathAdmin)
admin.site.register(FlowcellKit, FlowcellKitAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(HypermutationGene, HypermutationGeneAdmin)
admin.site.register(InvitroSerotype, InvitroSerotypeAdmin)
admin.site.register(LocusMlst, LocusMlstAdmin)
admin.site.register(MetadataClinic, MetadataClinicAdmin)
# admin.site.register(MetadataGeneral, MetadataGeneralAdmin)
admin.site.register(MutationalResistome, MutationalResistomeAdmin)
admin.site.register(PhenotypicData, PhenotypicDataAdmin)
admin.site.register(SampleType, SampleTypeAdmin)
admin.site.register(SequenceAnalysis, SequenceAnalysisAdmin)
admin.site.register(SequencingInfo, SequencingInfoAdmin)
admin.site.register(SequencingLibrary, SequencingLibraryAdmin)
admin.site.register(SequencingPlatform, SequencingPlatformAdmin)
admin.site.register(SequencingTechnology, SequencingTechnologyAdmin)
admin.site.register(VirulenceGene, VirulenceGeneAdmin)
# admin.site.register(Mic, MicAdmin)
admin.site.register(Mic, MicAdminFilter)

# Register your models here using custom_admin.py
# custom_admin_site.register(AcquiredResistome, AcquiredResistomeAdmin)
# custom_admin_site.register(Assembler, AssemblerAdmin)
# custom_admin_site.register(FilePath, FilePathAdmin)
# custom_admin_site.register(FlowcellKit, FlowcellKitAdmin)
# custom_admin_site.register(Hospital, HospitalAdmin)
# custom_admin_site.register(HypermutationGene, HypermutationGeneAdmin)
# custom_admin_site.register(InvitroSerotype, InvitroSerotypeAdmin)
# custom_admin_site.register(LocusMlst, LocusMlstAdmin)
# custom_admin_site.register(MetadataClinic, MetadataClinicAdmin)
# # custom_admin_site.register(MetadataGeneral, MetadataGeneralAdmin)
# custom_admin_site.register(MutationalResistome, MutationalResistomeAdmin)
# custom_admin_site.register(PhenotypicData, PhenotypicDataAdmin)
# custom_admin_site.register(SampleType, SampleTypeAdmin)
# custom_admin_site.register(SequenceAnalysis, SequenceAnalysisAdmin)
# custom_admin_site.register(SequencingInfo, SequencingInfoAdmin)
# custom_admin_site.register(SequencingLibrary, SequencingLibraryAdmin)
# custom_admin_site.register(SequencingPlatform, SequencingPlatformAdmin)
# custom_admin_site.register(SequencingTechnology, SequencingTechnologyAdmin)
# custom_admin_site.register(VirulenceGene, VirulenceGeneAdmin)
# # custom_admin_site.register(Mic, MicAdmin)
# custom_admin_site.register(Mic, MicAdminFilter)