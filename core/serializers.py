from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Dependencia, Vehiculo, BajaVehiculo, Auditoria

class DependenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependencia
        fields = '__all__'

class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'
        read_only_fields = ['estatus', 'fecha_alta', 'fecha_actualizacion']

class BajaVehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BajaVehiculo
        fields = ['motivo', 'numero_autorizacion']

class AuditoriaSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()
    class Meta:
        model = Auditoria
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    group = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'is_active', 'group']
        read_only_fields = ['id']

    def create(self, validated_data):
        group_name = validated_data.pop('group', None)
        user = User.objects.create_user(**validated_data)
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user

    def update(self, instance, validated_data):
        group_name = validated_data.pop('group', None)
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        if group_name:
            instance.groups.clear()
            group, _ = Group.objects.get_or_create(name=group_name)
            instance.groups.add(group)
        return instance
