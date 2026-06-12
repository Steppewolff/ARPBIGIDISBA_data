from django.contrib import admin
from .custom_admin import custom_admin_site  # Import custom admin site
from advanced_filters.admin import AdminAdvancedFiltersMixin
from django import forms
try:
    from multiselectfield import MultiSelectField as _MSF
except Exception:
    _MSF = None

from .models import AcquiredResistome, Assembler, FilePath, FlowcellKit, Hospital, HypermutationGene, InterestGenes, InvitroSerotype, \
    LocusMlst, MetadataClinic, MetadataGeneral, Mic, MutationalResistome, PhenotypicData, SampleType, SequenceAnalysis, \
    SequencingInfo, SequencingLibrary, SequencingPlatform, SequencingTechnology, VirulenceGene

class ModeloRelacionadoMetadataClinic(admin.TabularInline):  # or StackedInline
    model = MetadataClinic  # related model
    extra = 0  # number of empty forms

class ModeloRelacionadPhenotypicData(admin.TabularInline):  # or StackedInline
    model = PhenotypicData  # related model
    extra = 0  # optional: number of empty forms

class ModeloRelacionadSequenceAnalysis(admin.TabularInline):  # or StackedInline
    model = SequenceAnalysis  # related model
    extra = 0  # number of empty forms

class ModeloRelacionadMic(admin.TabularInline):  # or StackedInline
    model = Mic  # related model
    extra = 0  # number of empty forms

class ModeloRelacionadFilePath(admin.TabularInline):  # or StackedInline
    model = FilePath  # related model
    extra = 0  # number of empty forms

@admin.register(MetadataGeneral)
class ModeloPrincipalAdmin(admin.ModelAdmin):
    inlines = [ModeloRelacionadoMetadataClinic, ModeloRelacionadPhenotypicData, ModeloRelacionadSequenceAnalysis, ModeloRelacionadMic, ModeloRelacionadFilePath]


class AcquiredResistomeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AcquiredResistome._meta.fields]  # display all fields


class AssemblerAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Assembler._meta.fields]  # display all fields


class FilePathAdmin(admin.ModelAdmin):
    list_display = [field.name for field in FilePath._meta.fields]  # display all fields

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
    # Dynamically build list_display placing display_subset at the desired position.
    def _build_list_display(self):
        # All model field names
        fields = [f.name for f in InterestGenes._meta.fields]
        # If 'subset' is present, remove it (we don't want to show the raw subset value)
        if 'subset' in fields:
            fields.remove('subset')

        # Determine target insertion indices
        func_idx = None
        poly_idx = None
        if 'function' in fields:
            func_idx = fields.index('function') + 1  # we want after 'function'
        if 'polymorphisms' in fields:
            poly_idx = fields.index('polymorphisms')  # we want before 'polymorphisms'

        # Calculate insertion point
        if func_idx is not None and poly_idx is not None:
            insert_at = min(func_idx, poly_idx)
        elif func_idx is not None:
            insert_at = func_idx
        elif poly_idx is not None:
            insert_at = poly_idx
        else:
            insert_at = len(fields)  # append at the end if neither exists

        # Insert the display column at the calculated position
        fields.insert(insert_at, 'display_subset')
        return fields

    list_display = property(_build_list_display)  # evaluated when the class/admin loads

    def display_subset(self, obj):
        """Returns human-readable labels for the multiselect field in the list view."""
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
    list_display = [field.name for field in FlowcellKit._meta.fields]  # display all fields


class HospitalAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Hospital._meta.fields]  # display all fields
    list_filter = ["country", "region", "town"]


class HypermutationGeneAdmin(admin.ModelAdmin):
    list_display = [field.name for field in HypermutationGene._meta.fields]  # display all fields


class InvitroSerotypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in InvitroSerotype._meta.fields]  # display all fields


class LocusMlstAdmin(admin.ModelAdmin):
    list_display = [field.name for field in LocusMlst._meta.fields]  # display all fields


class MetadataClinicAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MetadataClinic._meta.fields]  # display all fields

    class Media:
        js = (
            'js/admin_js.js',
        )


class MetadataGeneralAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MetadataGeneral._meta.fields]  # display all fields

    class Media:
        js = (
            'js/admin_js.js',
        )


class MicAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Mic._meta.fields]  # display all fields
    exclude = ('mic_id', 'dlx', 'dlx_clinical_category', 'lvx', 'lvx_clinical_category', 'mxl', 'mxl_clinical_category', 'net', 'net_clinical_category', 'caz_cloxa', 'imi_cloxa')
    class Media:
        js = (
            'js/admin_js.js',
        )


class MutationalResistomeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in MutationalResistome._meta.fields]  # display all fields


class PhenotypicDataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PhenotypicData._meta.fields]  # display all fields

    class Media:
        js = (
            'js/admin_js.js',  # project static folder
        )


class SampleTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SampleType._meta.fields]  # display all fields


class SequenceAnalysisAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequenceAnalysis._meta.fields]  # display all fields

    class Media:
        js = (
            'js/admin_js.js',  # project static folder
        )


class SequencingInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequencingInfo._meta.fields]  # display all fields


class SequencingLibraryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequencingLibrary._meta.fields]  # display all fields


class SequencingPlatformAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequencingPlatform._meta.fields]  # display all fields


class SequencingTechnologyAdmin(admin.ModelAdmin):
    list_display = [field.name for field in SequencingTechnology._meta.fields]  # display all fields


class VirulenceGeneAdmin(admin.ModelAdmin):
    list_display = [field.name for field in VirulenceGene._meta.fields]  # display all fields


class MicAdminFilter(AdminAdvancedFiltersMixin, admin.ModelAdmin):
    list_display = [field.name for field in Mic._meta.fields]  # display all fields
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