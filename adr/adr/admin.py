from django.contrib import admin
from adr.models import *


class EdgeAdmin(admin.ModelAdmin):
    raw_id_fields = ["feature_id", "drug_id"]
    list_display = ["edge_type", "weight_value", "weight_units", "weight_measure", "feature", "drug"]


admin.site.register(Edge, EdgeAdmin)
admin.site.register(Target)
admin.site.register(Drug)
admin.site.register(Indication)
admin.site.register(ADR)
admin.site.register(SubStructure)
admin.site.register(PocketMotif)