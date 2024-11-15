from rest_framework import serializers
from .models import Cliente, Producto, Modelo, Venta, TipoProducto, DetalleVenta, FormaDePago, Carrito, DetalleCarrito, Administrador

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

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
        
class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'

class DetalleVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = '__all__'

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

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = '__all__'
