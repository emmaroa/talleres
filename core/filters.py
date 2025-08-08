import django_filters
from .models import Vehiculo

class VehiculoFilter(django_filters.FilterSet):
    numero_economico = django_filters.CharFilter(lookup_expr='icontains')
    placas = django_filters.CharFilter(lookup_expr='icontains')
    dependencia = django_filters.CharFilter(field_name='dependencia__nombre', lookup_expr='icontains')
    texto = django_filters.CharFilter(method='filter_texto')

    class Meta:
        model = Vehiculo
        fields = ['numero_economico', 'placas', 'dependencia', 'estatus']

    def filter_texto(self, queryset, name, value):
        return queryset.filter(descripcion__icontains=value)
