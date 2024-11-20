from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


from tienda.views import (
    UsuarioViewSet,
    ProductoViewSet,
    VentaViewSet,
    DetalleVentaViewSet,
    FormaDePagoViewSet,
    CarritoViewSet,
    DetalleCarritoViewSet,
    TipoProductoViewSet,
    ModeloViewSet,
    AuthStatusView
)

router = DefaultRouter()
router.register(r'usuario', UsuarioViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'tipoproductos', TipoProductoViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalles-venta', DetalleVentaViewSet)
router.register(r'formas-pago', FormaDePagoViewSet)
router.register(r'carritos', CarritoViewSet)
router.register(r'detalles-carrito', DetalleCarritoViewSet)
router.register(r'modelo', ModeloViewSet)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/status/', AuthStatusView.as_view(), name='auth_status'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


