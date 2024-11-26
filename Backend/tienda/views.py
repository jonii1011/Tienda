from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Producto, Venta, Modelo, DetalleVenta, FormaDePago, Carrito, DetalleCarrito, TipoProducto
from .serializers import (
    UsuarioSerializer,
    ProductoSerializer,
    TipoProductoSerializer,
    VentaSerializer,
    DetalleVentaSerializer,
    FormaDePagoSerializer,
    CarritoSerializer,
    DetalleCarritoSerializer,
    ModeloSerializer
)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id_producto=producto_id)
    carrito, created = Carrito.objects.get_or_create(cliente=request.user)
    detalle, created = DetalleCarrito.objects.get_or_create(carrito=carrito, producto=producto)
    detalle.cantidad += 1
    detalle.save()
    return redirect('ver_carrito')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ver_carrito(request):
    carrito = Carrito.objects.filter(cliente=request.user).first()
    detalles = DetalleCarrito.objects.filter(carrito=carrito)
    return render(request, 'carrito.html', {'detalles': detalles})

class AuthStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'isAuthenticated': True,
            'role': user.rol,  
            'nombre': user.nombre,
            'id': user.id  
        })

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

    def create(self, request, *args, **kwargs):
        print("Datos de solicitud:", request.data) 
        if 'contraseña' not in request.data:
            return Response({'error': 'La contraseña es requerida.'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        
        if 'contraseña' in data:
            data['contraseña'] = make_password(data['contraseña'])

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
    queryset = Venta.objects.select_related('cliente').prefetch_related('detalles')
    serializer_class = VentaSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        cliente = request.user
        forma_pago_id = request.data.get('forma_pago_id')
        carrito = request.data.get('carrito')

        if not carrito or len(carrito) == 0:
            return Response({"error": "El carrito está vacío"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Crear la venta
            venta = Venta.objects.create(cliente=cliente, forma_pago_id=forma_pago_id)

            for item in carrito:
                producto_id = item['id_producto']  # Este es correcto
                cantidad = item['cantidad']

                # Asegúrate de que el producto exista usando el campo correcto
                producto = get_object_or_404(Producto, id_producto=producto_id)

                # Crear el detalle de la venta
                DetalleVenta.objects.create(venta=venta, producto=producto, cantidad=cantidad)

            return Response({"mensaje": "Venta concretada con éxito"}, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer

class FormaDePagoViewSet(viewsets.ModelViewSet):
    queryset = FormaDePago.objects.all()
    serializer_class = FormaDePagoSerializer

class CarritoViewSet(viewsets.ModelViewSet):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    def get_queryset(self):
        # Devuelve solo el carrito del usuario autenticado
        return Carrito.objects.filter(cliente=self.request.user)

class DetalleCarritoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = DetalleCarrito.objects.all()
    serializer_class = DetalleCarritoSerializer

    def create(self, request, *args, **kwargs):
        producto_id = request.data.get('id_producto')
        cantidad = request.data.get('cantidad')
        cliente = request.user  # Asumiendo que el usuario está autenticado

        carrito, created = Carrito.objects.get_or_create(cliente=cliente)

        # Verificar si el producto ya está en el carrito
        detalle, created = DetalleCarrito.objects.get_or_create(carrito=carrito, producto_id=producto_id)

        if not created:
            # Si el producto ya existe en el carrito, solo actualizamos la cantidad
            detalle.cantidad += cantidad
            detalle.save()
        else:
            detalle.cantidad = cantidad
            detalle.save()

        serializer = self.get_serializer(detalle)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        # Devuelve solo los detalles del carrito del usuario autenticado
        carrito = Carrito.objects.get(cliente=self.request.user)
        return DetalleCarrito.objects.filter(carrito=carrito)


