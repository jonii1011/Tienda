from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from tienda.views import (
    ClienteViewSet,
    ProductoViewSet,
    VentaViewSet,
    DetalleVentaViewSet,
    FormaDePagoViewSet,
    CarritoViewSet,
    DetalleCarritoViewSet,
    AdministradorViewSet,
    TipoProductoViewSet,
    ModeloViewSet
)

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'tipoproductos', TipoProductoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalles-venta', DetalleVentaViewSet)
router.register(r'formas-pago', FormaDePagoViewSet)
router.register(r'carritos', CarritoViewSet)
router.register(r'detalles-carrito', DetalleCarritoViewSet)
router.register(r'administradores', AdministradorViewSet)
router.register(r'modelo', ModeloViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
]


