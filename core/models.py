from django.conf import settings
from django.db import models
from django.core.validators import MinLengthValidator

class Dependencia(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    clave = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Vehiculo(models.Model):
    ESTATUS_ACTIVO = 'ACTIVO'
    ESTATUS_BAJA = 'BAJA'
    ESTATUS_CHOICES = [
        (ESTATUS_ACTIVO, 'Activo'),
        (ESTATUS_BAJA, 'Baja'),
    ]

    numero_economico = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    dependencia = models.ForeignKey(Dependencia, on_delete=models.CASCADE)
    placas = models.CharField(max_length=20, unique=True, null=True, blank=True)
    serie = models.CharField(max_length=50, unique=True)
    factura = models.CharField(max_length=100, blank=True)
    resguardante = models.CharField(max_length=100, blank=True)
    foto = models.ImageField(upload_to='vehiculos/', blank=True, null=True)
    estatus = models.CharField(max_length=10, choices=ESTATUS_CHOICES, default=ESTATUS_ACTIVO)
    fecha_alta = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['numero_economico']),
            models.Index(fields=['placas']),
            models.Index(fields=['serie']),
        ]

    def __str__(self):
        return f"{self.numero_economico} - {self.descripcion}"

class BajaVehiculo(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, related_name='bajas')
    motivo = models.TextField(validators=[MinLengthValidator(20)])
    numero_autorizacion = models.CharField(max_length=100)
    fecha_baja = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Baja {self.vehiculo}"

class Auditoria(models.Model):
    ACCION_CHOICES = [
        ('ALTA', 'Alta'),
        ('EDICION', 'Edicion'),
        ('BAJA', 'Baja'),
        ('LOGIN', 'Login'),
        ('CREAR_USUARIO', 'Crear Usuario'),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    accion = models.CharField(max_length=20, choices=ACCION_CHOICES)
    entidad = models.CharField(max_length=100)
    entidad_id = models.IntegerField(null=True, blank=True)
    detalle = models.JSONField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.usuario} {self.accion} {self.entidad} {self.entidad_id}"
