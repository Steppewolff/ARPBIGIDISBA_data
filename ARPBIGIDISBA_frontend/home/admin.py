from django.contrib import admin
from .custom_admin import custom_admin_site  # Importamos el Admin personalizado
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django import forms
try:
    from multiselectfield import MultiSelectField as _MSF
except Exception:
    _MSF = None

from .models import AcquiredResistome, Assembler, FilePath, FlowcellKit, Hospital, HypermutationGene, InterestGenes, InvitroSerotype, \
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


class AcquiredResistomeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AcquiredResistome._meta.fields]  # Mostrar todos los campos


class AssemblerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Assembler._meta.fields]  # Mostrar todos los campos


class FilePathAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FilePath._meta.fields]  # Mostrar todos los campos

# This dictionary maps subset codes to their descriptions in InterestGenesAdmin, it is necessary for displaying the subset field in a human-readable format due to it is a multiselect field, different from the others.
SUBSET_MAP = {
    'BASIC': 'Basic resistome',
    'CR': 'Cefiderocol resistance',
    'MLST': 'Locus for MLST identification',
    '-': 'N/A',
    'OT': 'Other',
}

@admin.register(InterestGenes)
class InterestGenesAdmin(admin.ModelAdmin):
    # Construimos dinámicamente list_display colocando display_subset en la posición deseada.
    def _build_list_display(self):
        # Todos los campos del modelo (nombre)
        fields = [f.name for f in InterestGenes._meta.fields]
        # Si el campo 'subset' existe en fields, lo quitamos (no queremos mostrar raw subset)
        if 'subset' in fields:
            fields.remove('subset')

        # Determinar índices objetivo
        func_idx = None
        poly_idx = None
        if 'function' in fields:
            func_idx = fields.index('function') + 1  # queremos después de 'function'
        if 'polymorphisms' in fields:
            poly_idx = fields.index('polymorphisms')  # queremos antes de 'polymorphisms'

        # Calcular lugar de inserción
        if func_idx is not None and poly_idx is not None:
            insert_at = min(func_idx, poly_idx)
        elif func_idx is not None:
            insert_at = func_idx
        elif poly_idx is not None:
            insert_at = poly_idx
        else:
            insert_at = len(fields)  # al final si ninguno existe

        # Insertar la columna de display en la posición calculada
        fields.insert(insert_at, 'display_subset')
        return fields

    list_display = property(_build_list_display)  # se evalúa al cargar la clase/admin

    def display_subset(self, obj):
        """Muestra las etiquetas legibles del multiselect en el listado."""
        val = getattr(obj, 'subset', None)
        if not val:
            return '-'
        if isinstance(val, (list, tuple)):
            labels = [SUBSET_MAP.get(k, k) for k in val]
            return ', '.join(labels) if labels else '-'
        if isinstance(val, str):
            keys = [k.strip() for k in val.split(',') if k.strip()]
            labels = [SUBSET_MAP.get(k, k) for k in keys]
            return ', '.join(labels) if labels else '-'
        return str(val)

    display_subset.short_description = 'Subset'
    display_subset.admin_order_field = 'subset'


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
    exclude = ('mic_id', 'dlx', 'dlx_clinical_category', 'lvx', 'lvx_clinical_category', 'mxl', 'mxl_clinical_category', 'net', 'net_clinical_category', 'caz_cloxa', 'imi_cloxa')
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
# admin.site.register(InterestGenes, InterestGenesAdmin)
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