from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from core import views as core_views

router = DefaultRouter()
router.register(r'vehiculos', core_views.VehiculoViewSet, basename='vehiculo')
router.register(r'dependencias', core_views.DependenciaViewSet)
router.register(r'usuarios', core_views.UserViewSet, basename='usuario')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
    path('api/token/', core_views.TokenObtainPairViewCustom.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', core_views.TokenRefreshViewCustom.as_view(), name='token_refresh'),
    path('', core_views.HomeView.as_view(), name='home'),
    path('accounts/login/', core_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', core_views.logout_view, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
