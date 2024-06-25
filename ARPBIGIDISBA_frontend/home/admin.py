from django.contrib import admin
from django.db import models
from advanced_filters.admin import AdminAdvancedFiltersMixin


from .models import AcquiredResistome, Assembler, FilePath, FlowcellKit, Hospital, HypermutationGene, InvitroSerotype, LocusMlst, MetadataClinic, MetadataGeneral, Mic, MutationalResistome, PhenotypicData, SampleType, SequenceAnalysis, SequencingInfo, SequencingLibrary, SequencingPlatform, SequencingTechnology, VirulenceGene

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

class MetadataGeneralAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MetadataGeneral._meta.fields]  # Mostrar todos los campos

class MicAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mic._meta.fields]  # Mostrar todos los campos

class MutationalResistomeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MutationalResistome._meta.fields]  # Mostrar todos los campos

class PhenotypicDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PhenotypicData._meta.fields]  # Mostrar todos los campos

class SampleTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SampleType._meta.fields]  # Mostrar todos los campos

class SequenceAnalysisAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequenceAnalysis._meta.fields]  # Mostrar todos los campos

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
    # list_display = ('pip', 'caz', 'fep')
    list_filter = [field.name for field in Mic._meta.fields if field.name not in ['mic_id', 'mic_comments', 'isolate']]  # simple list filters
    # list_filter = ('pip', 'caz', 'fep')  # simple list filters

    advanced_filter_fields = [field.name for field in Mic._meta.fields if field.name not in ['mic_id', 'mic_comments', 'isolate']]

class MicsAdmin(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    # list_filter = ('name', 'language', 'ts')   # simple list filters
    list_filter = [field.name for field in Mic._meta.fields]
    list_display = [field.name for field in Mic._meta.fields]  # Mostrar todos los campos

    # specify which fields can be selected in the advanced filter
    # creation form
    advanced_filter_fields = (
        'pip',
        'caz',
        'fep',

        # # even use related fields as lookup fields
        # 'country__name',
        # 'posts__title',
        # 'comments__content',
    )

# Register your models here.
admin.site.register(AcquiredResistome, AcquiredResistomeAdmin)
admin.site.register(Assembler, AssemblerAdmin)
admin.site.register(FilePath, FilePathAdmin)
admin.site.register(FlowcellKit, FlowcellKitAdmin)
admin.site.register(Hospital, HospitalAdmin)
admin.site.register(HypermutationGene, HypermutationGeneAdmin)
admin.site.register(InvitroSerotype, InvitroSerotypeAdmin)
admin.site.register(LocusMlst, LocusMlstAdmin)
admin.site.register(MetadataClinic, MetadataClinicAdmin)
admin.site.register(MetadataGeneral, MetadataGeneralAdmin)
# admin.site.register(Mic, MicAdmin)
admin.site.register(MutationalResistome, MutationalResistomeAdmin)
admin.site.register(PhenotypicData, PhenotypicDataAdmin)
admin.site.register(SampleType, SampleTypeAdmin)
admin.site.register(SequenceAnalysis, SequenceAnalysisAdmin)
admin.site.register(SequencingInfo, SequencingInfoAdmin)
admin.site.register(SequencingLibrary, SequencingLibraryAdmin)
admin.site.register(SequencingPlatform, SequencingPlatformAdmin)
admin.site.register(SequencingTechnology, SequencingTechnologyAdmin)
admin.site.register(VirulenceGene, VirulenceGeneAdmin)
admin.site.register(Mic, MicAdminFilter)