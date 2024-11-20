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
            'nombre': user.nombre  
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


