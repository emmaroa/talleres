from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from rest_framework import viewsets, status, decorators, response, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Dependencia, Vehiculo, BajaVehiculo, Auditoria
from .serializers import (
    DependenciaSerializer,
    VehiculoSerializer,
    BajaVehiculoSerializer,
    AuditoriaSerializer,
    UserSerializer,
)
from .permissions import IsAdmin, IsCapturista
from .filters import VehiculoFilter

class HomeView(TemplateView):
    template_name = 'core/vehiculo_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehiculos'] = Vehiculo.objects.all()[:50]
        return context

class LoginView(DjangoLoginView):
    template_name = 'login.html'
    next_page = reverse_lazy('home')


def logout_view(request):
    logout(request)
    return response.Response({'detail': 'logged out'})

class DependenciaViewSet(viewsets.ModelViewSet):
    queryset = Dependencia.objects.all()
    serializer_class = DependenciaSerializer
    permission_classes = [IsAdmin]

class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    filterset_class = VehiculoFilter
    search_fields = ['numero_economico', 'placas', 'serie', 'descripcion']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'baja']:
            permission_classes = [IsCapturista]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [perm() for perm in permission_classes]

    def perform_create(self, serializer):
        instance = serializer.save()
        Auditoria.objects.create(usuario=self.request.user, accion='ALTA', entidad='Vehiculo', entidad_id=instance.id)

    def perform_update(self, serializer):
        instance = serializer.save()
        Auditoria.objects.create(usuario=self.request.user, accion='EDICION', entidad='Vehiculo', entidad_id=instance.id)

    @decorators.action(detail=True, methods=['post'])
    def baja(self, request, pk=None):
        vehiculo = self.get_object()
        serializer = BajaVehiculoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        BajaVehiculo.objects.create(
            vehiculo=vehiculo,
            motivo=serializer.validated_data['motivo'],
            numero_autorizacion=serializer.validated_data['numero_autorizacion'],
            usuario=request.user
        )
        vehiculo.estatus = Vehiculo.ESTATUS_BAJA
        vehiculo.save()
        Auditoria.objects.create(usuario=request.user, accion='BAJA', entidad='Vehiculo', entidad_id=vehiculo.id)
        return response.Response({'status': 'baja registrada'})

    @decorators.action(detail=True, methods=['get'])
    def historial(self, request, pk=None):
        vehiculo = self.get_object()
        auditorias = Auditoria.objects.filter(entidad='Vehiculo', entidad_id=vehiculo.id)
        baja = BajaVehiculo.objects.filter(vehiculo=vehiculo)
        return response.Response({
            'auditorias': AuditoriaSerializer(auditorias, many=True).data,
            'bajas': BajaVehiculoSerializer(baja, many=True).data,
        })

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

class TokenObtainPairViewCustom(TokenObtainPairView):
    pass

class TokenRefreshViewCustom(TokenRefreshView):
    pass
