from rest_framework import viewsets
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from .models import Cliente, Producto, Venta, Modelo, DetalleVenta, FormaDePago, Carrito, DetalleCarrito, Administrador, TipoProducto
from .serializers import (
    ClienteSerializer,
    ProductoSerializer,
    TipoProductoSerializer,
    VentaSerializer,
    DetalleVentaSerializer,
    FormaDePagoSerializer,
    CarritoSerializer,
    DetalleCarritoSerializer,
    AdministradorSerializer,
    ModeloSerializer
)

@api_view(['POST'])
@csrf_exempt
def login_view(request):
    print(f"Datos recibidos: {request.data}")  # Para depuración

    email = request.data.get('email')
    contraseña = request.data.get('contraseña')

    if not email or not contraseña:
        return Response({'error': 'Email y contraseña son requeridos'}, status=400)

    # Intentar autenticar como Cliente
    try:
        cliente = Cliente.objects.get(email=email)
        print(f"Cliente encontrado: {cliente}")  # Para depuración
        print(f"Hash almacenado: {cliente.contraseña}")  # Imprimir el hash
        if check_password(contraseña, cliente.contraseña):
            return Response({'message': 'Inicio de sesión exitoso como cliente', 'dni': cliente.dni}, status=200)
        else:
            print("Contraseña incorrecta para cliente")  # Para depuración
    except Cliente.DoesNotExist:
        print("Cliente no encontrado")  # Para depuración

    # Intentar autenticar como Administrador
    try:
        administrador = Administrador.objects.get(email=email)
        print(f"Administrador encontrado: {administrador}")  # Para depuración
        if check_password(contraseña, administrador.contraseña):
            return Response({'message': 'Inicio de sesión exitoso como administrador', 'id_administrador': administrador.id_administrador}, status=200)
        else:
            print("Contraseña incorrecta para administrador")  # Para depuración
    except Administrador.DoesNotExist:
        print("Administrador no encontrado")  # Para depuración

    return Response({'error': 'Email o contraseña incorrectos'}, status=400)






class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

    def create(self, request, *args, **kwargs):
        # Obtén los datos del cliente
        data = request.data.copy()
        # Asegúrate de usar make_password para la contraseña
        if 'contraseña' in data:
            data['contraseña'] = make_password(data['contraseña'])
        # Llama al método de creación original
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        # Obtén el objeto cliente
        cliente = self.get_object()
        data = request.data.copy()
        
        # Si se proporciona una nueva contraseña, hashearla
        if 'contraseña' in data:
            data['contraseña'] = make_password(data['contraseña'])
        
        # Llama al método de actualización original
        return super().update(request, *args, **kwargs)

class TipoProductoViewSet(viewsets.ModelViewSet):
    queryset = TipoProducto.objects.all()
    serializer_class = TipoProductoSerializer

class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class FormaDePagoViewSet(viewsets.ModelViewSet):
    queryset = FormaDePago.objects.all()
    serializer_class = FormaDePagoSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

class DetalleCarritoViewSet(viewsets.ModelViewSet):
    queryset = DetalleCarrito.objects.all()
    serializer_class = DetalleCarritoSerializer

class AdministradorViewSet(viewsets.ModelViewSet):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
