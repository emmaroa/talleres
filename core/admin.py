from django.contrib import admin
from .models import Dependencia, Vehiculo, BajaVehiculo, Auditoria
from django.utils.html import format_html

@admin.register(Dependencia)
class DependenciaAdmin(admin.ModelAdmin):
    search_fields = ['nombre']

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ['numero_economico', 'dependencia', 'estatus', 'foto_thumb']
    list_filter = ['estatus', 'dependencia']
    search_fields = ['numero_economico', 'placas', 'serie']

    def foto_thumb(self, obj):
        if obj.foto:
            return format_html('<img src="{}" width="50"/>', obj.foto.url)
        return '-'

@admin.register(BajaVehiculo)
class BajaVehiculoAdmin(admin.ModelAdmin):
    list_display = ['vehiculo', 'motivo', 'numero_autorizacion', 'fecha_baja', 'usuario']
    search_fields = ['vehiculo__numero_economico', 'numero_autorizacion']

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'accion', 'entidad', 'entidad_id', 'timestamp']
    list_filter = ['accion', 'usuario']
    search_fields = ['entidad', 'entidad_id']
