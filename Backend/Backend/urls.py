from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static

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
    ModeloViewSet,
    login_view
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
    path('login/', login_view, name='login'),
    path('', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


