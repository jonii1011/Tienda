from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class Cliente(models.Model):
    dni = models.CharField(max_length=20, primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_de_nacimiento = models.DateField()
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo hashear si es un nuevo cliente
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class FormaDePago(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    forma_pago = models.ForeignKey(FormaDePago, on_delete=models.CASCADE)

    def __str__(self):
        return f"Venta {self.id_venta} - {self.cliente}"

class DetalleVenta(models.Model):
    cantidad = models.IntegerField()
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cantidad} de {self.producto} en {self.venta}"

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    descripcion = models.TextField()
    tipo_producto = models.ForeignKey('TipoProducto', on_delete=models.CASCADE)
    modelo = models.ForeignKey('Modelo', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)  # Campo para la imagen

    def __str__(self):
        return self.nombre

class Modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    nombre_modelo = models.CharField(max_length=100)
    version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nombre_modelo} - {self.version}"

class TipoProducto(models.Model):
    id_tipo_producto = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre_tipo

class Carrito(models.Model):
    id_carrito = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Carrito de {self.cliente}"

class DetalleCarrito(models.Model):
    cantidad = models.IntegerField()
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cantidad} de {self.producto} en {self.carrito}"

class Administrador(models.Model):
    id_administrador = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=128)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.pk:  # Solo hashear si es un nuevo administrador
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol}"

