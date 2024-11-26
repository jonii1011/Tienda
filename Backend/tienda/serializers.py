from rest_framework import serializers
from .models import Usuario, Producto, Modelo, Venta, TipoProducto, DetalleVenta, FormaDePago, Carrito, DetalleCarrito

class UsuarioSerializer(serializers.ModelSerializer):
    contraseña = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Usuario
        fields = ['id', 'dni', 'nombre', 'apellido', 'fecha_de_nacimiento', 
                  'direccion', 'telefono', 'email', 'rol', 'is_active', 'is_staff', 'contraseña']
        read_only_fields = ['id', 'fecha_creacion']

    def create(self, validated_data):
        # Extraer la contraseña del diccionario validado
        contraseña = validated_data.pop('contraseña', None)
        user = Usuario(**validated_data)
        if contraseña is not None:
            user.set_password(contraseña)
        user.save()
        return user

    def update(self, instance, validated_data):
        # Permitir la actualización de los campos, excepto la contraseña
        contraseña = validated_data.pop('contraseña', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if contraseña is not None:
            instance.set_password(contraseña)
        instance.save()
        return instance

class TipoProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = '__all__' 

class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__' 


class ProductoSerializer(serializers.ModelSerializer):
    modelo_detalle = serializers.SerializerMethodField()

    class Meta:
        model = Producto
        fields = '__all__'  # Asegúrate de incluir los campos que necesitas
        extra_kwargs = {
            'modelo': {'required': False},  # Asegúrate de que sea opcional
        }

    def get_modelo_detalle(self, obj):
        # Obtiene el modelo relacionado
        if obj.modelo:  # Verifica si el modelo existe
            return {
                "nombre_modelo": obj.modelo.nombre_modelo,
                "version": obj.modelo.version
            }
        return None  # Retorna None si no hay modelo relacionado
        

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

class VentaSerializer(serializers.ModelSerializer):
    detalles = DetalleVentaSerializer(many=True, read_only=True, source='detalleventa_set')

    class Meta:
        model = Venta
        fields = ['id_venta', 'cliente', 'forma_pago', 'fecha_venta', 'detalles']

class FormaDePagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaDePago
        fields = '__all__'

class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = '__all__'

class DetalleCarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleCarrito
        fields = '__all__'

