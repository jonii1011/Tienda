<template>
  <v-app>
    <v-app-bar app color="grey" dark>
      <div style="display: flex; align-items: center; margin: 0;">
        <h3>IMPORT TDF</h3>
        <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
      </div>
      <v-spacer></v-spacer>
      <v-btn text @click="inicio" class="menu">Inicio</v-btn>
      <v-btn text v-if="!isAdmin" @click="contacto" class="menu">Contacto</v-btn>
      <v-btn v-if="!isAuthenticated" color="black" @click="iniciarSesion">Iniciar Sesión</v-btn>
      <v-menu v-else>
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="black" v-bind="attrs" v-on="on">{{ nombreUsuario }}</v-btn>
        </template>
        <v-list>
          <v-list-item @click="verPedido">
            <v-list-item-title>Mis pedidos</v-list-item-title>
          </v-list-item>
          <v-list-item @click="cerrarSesion">
            <v-list-item-title>Cerrar Sesión</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn icon @click="verCarrito">
        <v-badge color="red" :content="cantidadCarrito" overlap>
          <v-icon>mdi-cart</v-icon>
        </v-badge>
      </v-btn>
    </v-app-bar>

    <v-container class="mt-15 mb-50" style="padding-bottom: 100px;">
      <v-card class="mx-auto" style="max-width: 600px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); background-color: #f5f5f5; margin-top: 60px;">
        <v-card-title class="headline text-center" style="font-weight: bold; color: black;">Carrito de Compras</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item-group v-if="carrito.length">
              <v-list-item v-for="producto in carrito" :key="producto.id">
                <v-list-item-content>
                  <v-list-item-title><strong>Producto:</strong> {{ producto.nombre }} {{ producto.modelo_detalle.nombre_modelo }} {{ producto.modelo_detalle.version }}</v-list-item-title>
                  <v-list-item-title>
                      <strong>Cantidad:</strong>
                      <v-btn icon @click="disminuirCantidad(producto)">
                        <v-icon>mdi-minus</v-icon>
                      </v-btn>
                      {{ producto.cantidad }}
                      <v-btn icon @click="aumentarCantidad(producto)">
                        <v-icon>mdi-plus</v-icon>
                      </v-btn>
                    </v-list-item-title>
                  <v-list-item-title><strong>Precio:</strong> ${{ producto.precio }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
            <v-list-item v-else>
              <v-list-item-content>
                <v-list-item-title>No hay productos en el carrito.</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>

          <v-list-item>
            <v-list-item-content>
              <v-list-item-title class="headline"><strong>Total de la Compra:</strong> ${{ totalCompra }}</v-list-item-title>
            </v-list-item-content>
          </v-list-item>

          <!-- Selector de forma de pago -->
          <v-select
            v-model="formaPagoId"
            :items="formasDePago"
            item-text="nombre"
            item-value="id"
            label="Selecciona una forma de pago"
            class="mt-4"
            required
          ></v-select>
        </v-card-text>
        <v-card-actions>
          <v-btn color="green" @click="concretarVenta" v-if="carrito.length && formaPagoId">Concretar compra</v-btn>
          <v-btn color="grey" @click="vaciarCarrito" v-if="carrito.length">Vaciar Carrito</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>

    <v-footer app>
      <v-container>
        <v-row>
          <v-col class="text-center">
            <p>&copy; 2024 Import TDF. Todos los derechos reservados.</p>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  data() {
    return {
      formaPagoId: null, // Almacena el ID de la forma de pago seleccionada
      formasDePago: [] // Almacena las formas de pago disponibles
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'nombreUsuario', 'userRole', 'carrito', 'userId', 'cantidadCarrito']),
    isAdmin() {
      return this.userRole === 'administrador';
    },
    totalCantidad() {
      return this.carrito.reduce((total, producto) => total + producto.cantidad, 0);
    },
    totalCompra() {
    return this.carrito.reduce((total, producto) => total + (producto.precio * producto.cantidad), 0);
    },
  },
  mounted() {
    this.cargarFormasDePago(); // Cargar las formas de pago al montar el componente
  },
  methods: {
    async actualizarStock() {
      const productosParaActualizar = this.carrito.map(item => ({
        id_producto: item.id_producto,
        cantidad: item.cantidad
      }));

      try {
        console.log('Productos para actualizar:', productosParaActualizar);
        const token = localStorage.getItem('access_token');
        await axios.post('http://127.0.0.1:8000/actualizar-stock/', productosParaActualizar, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
      } catch (error) {
        console.error('Error al actualizar el stock:', error.response.data);
        alert('Ocurrió un error al actualizar el stock. Por favor, intenta nuevamente.');
      }
    },
    async verificarStock() {
      // Crear un objeto que contenga el id del producto y la cantidad del carrito
      const productosAVerificar = this.carrito.map(item => ({
        id_producto: item.id_producto,
        nombre: item.nombre,
        nombre_modelo: item.modelo_detalle.nombre_modelo,
        version: item.modelo_detalle.version,
        cantidad: item.cantidad,
        stock: item.stock // Asegúrate de que este atributo esté presente en cada producto
      }));

      // Verificar el stock de cada producto
      for (const producto of productosAVerificar) {
        if (producto.cantidad > producto.stock) {
          alert(`No hay suficiente stock para el producto: ${producto.nombre} ${producto.nombre_modelo} ${producto.version}. Solo hay ${producto.stock} disponibles.`);
          return false; // Detener si no hay suficiente stock
        }
      }
      return true; // Si todos los productos tienen suficiente stock
    },
    async cargarFormasDePago() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/formas-pago/');
        console.log('Formas de pago:', response.data); // Verifica la respuesta
        this.formasDePago = response.data; // Asigna los datos a la variable
      } catch (error) {
        console.error('Error al cargar las formas de pago:', error);
      }
    },
    inicio() {
      this.$router.push('/');
    },
    cerrarSesion() {
        this.$store.dispatch('logout');
        this.$router.push('/');
      },
    contacto() {
      // Lógica para contacto
    },
    verCarrito() {
      // Lógica para ver el carrito
    },
    aumentarCantidad(producto) {
      this.$store.dispatch('aumentarCantidad', producto.id_producto);
    },

    disminuirCantidad(producto) {
      this.$store.dispatch('disminuirCantidad', producto.id_producto);
    },
    verPedido() {
      this.$router.push('/ventas'); 
    },
    async concretarVenta() {
      if (!this.isAuthenticated) {
        alert('Debes iniciar sesión para realizar una compra.');
        return;
      }

      if (!this.formaPagoId) {
        alert('Por favor, selecciona una forma de pago.');
        return;
      }

      const stockDisponible = await this.verificarStock();
      if (!stockDisponible) {
        return; // Si no hay stock, se detiene aquí
      }

      const payload = {
        forma_pago_id: this.formaPagoId,
        cliente_id: this.userId,
        carrito: this.carrito.map(item => ({
          id_producto: item.id_producto,
          cantidad: item.cantidad
        }))
      };

      console.log('Payload:', payload);

      const token = localStorage.getItem('access_token');

      try {
        const response = await axios.post(`http://127.0.0.1:8000/ventas/`, payload, {
          headers: {
            'Authorization': `Bearer ${token}` // Asegúrate de incluir el token aquí
          }
        });
        alert("COMPRA FINALIZADA CON ÉXITO");
        console.log('Venta concretada:', response.data);
        
        // Actualiza el stock después de la venta
        await this.actualizarStock(); // Llama a la función para actualizar el stock
        this.vaciarCarrito(); // Llama a la acción para vaciar el carrito
      } catch (error) {
        console.error('Error al concretar la venta:', error.response ? error.response.data : error.message);
        alert('Ocurrió un error al concretar la venta. Por favor, intenta nuevamente.');
      }
    },
    vaciarCarrito() {
      this.$store.dispatch('vaciarCarrito');
    },
  },
};
</script>

<style scoped>
.logo {
  width: 50px; /* Ajusta el tamaño del logo */
}
</style>


  