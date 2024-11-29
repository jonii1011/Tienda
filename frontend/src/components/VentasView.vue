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
          <v-list-item @click="verPerfil">
            <v-list-item-title>Mi Perfil</v-list-item-title>
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
      <v-card class="mx-auto" style="max-width: 800px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); background-color: #f5f5f5; margin-top: 60px;">
        <v-card-title class="headline text-center" style="font-weight: bold; color: black;">Historial de pedidos</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item-group v-if="ventas.length">
              <v-list-item v-for="venta in ventas" :key="venta.id_venta">
                <v-list-item-content>
                  <v-list-item-title><strong>ID Venta:</strong> {{ venta.id_venta }}</v-list-item-title>
                  <v-list-item-title><strong>Cliente:</strong> {{ venta.cliente.nombre }}</v-list-item-title>
                  <v-list-item-title><strong>Forma de pago:</strong> {{ venta.forma_pago.nombre }}</v-list-item-title>
                  <v-list-item-title><strong>Fecha:</strong> {{ new Date(venta.fecha_venta).toLocaleString() }}</v-list-item-title>
                  <v-list-item-title><strong>Detalles:</strong></v-list-item-title>
                  <v-list-item>
                    <v-list-item-content>
                      <v-list dense>
                        <v-list-item v-for="detalle in venta.detalles" :key="detalle.producto.id_producto">
                          <v-list-item-content>
                            <v-list-item-title><strong>Producto:</strong> {{ detalle.producto.nombre }} {{ detalle.producto.modelo_detalle.nombre_modelo }} {{ detalle.producto.modelo_detalle.version }}</v-list-item-title>
                            <v-list-item-title><strong>Cantidad:</strong> {{ detalle.cantidad }}</v-list-item-title>
                            <v-list-item-title><strong>Precio Unitario:</strong> ${{ detalle.producto.precio }}</v-list-item-title>
                          </v-list-item-content>
                        </v-list-item>
                        <v-list-item-title>
                          <strong>Total:</strong> ${{ calcularTotal(venta) }}
                        </v-list-item-title>
                      </v-list>
                    </v-list-item-content>
                  </v-list-item>
                  <v-btn color="red" @click="eliminarVenta(venta.id_venta)">Eliminar</v-btn>
                </v-list-item-content>
              </v-list-item>
            </v-list-item-group>
            <v-list-item v-else>
              <v-list-item-content>
                <v-list-item-title>No hay pedidos registradas.</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
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
      ventas: [] // Almacena las ventas recuperadas
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'nombreUsuario', 'userRole', 'cantidadCarrito']),
    isAdmin() {
      return this.userRole === 'administrador';
    },
  },
  mounted() {
    this.cargarVentas(); // Cargar las ventas al montar el componente
  },
  methods: {
    async cargarVentas() {
      try {
        const token = localStorage.getItem('access_token');
        const response = await axios.get('http://127.0.0.1:8000/ventas/', {
          headers: {
            'Authorization': `Bearer ${token}` // Incluye el token de autorización
          }
        });
        console.log("respuesta", response.data);
        this.ventas = response.data; // Asigna los datos a la variable
      } catch (error) {
        console.error('Error al cargar las ventas:', error);
      }
    },
    async eliminarVenta(id) {
      try {
        const token = localStorage.getItem('access_token');
        await axios.delete(`http://127.0.0.1:8000/ventas/${id}/`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });
        // Actualizar la lista de ventas después de eliminar
        this.ventas = this.ventas.filter(venta => venta.id_venta !== id);
      } catch (error) {
        console.error('Error al eliminar la venta:', error);
      }
    },
    calcularTotal(venta) {
    return venta.detalles.reduce((total, detalle) => {
      return total + (detalle.cantidad * detalle.producto.precio);
    }, 0);
    },
    inicio() {
      this.$router.push('/');
    },
    cerrarSesion() {
      this.$store.dispatch('logout'); // Llama a la acción de logout de Vuex
      this.$router.push('/login'); // Redirige a la página de inicio de sesión
    },
    contacto() {
      // Lógica para contacto
    },
    verCarrito() {
      this.$router.push('/carrito'); 
    },
    verPerfil() {
      this.$router.push({ name: 'PerfilView', params: { userId: this.userId } });
    },
  }
};
</script>

<style scoped>
.logo {
  width: 40px; /* Ajusta el tamaño según sea necesario */
  height: auto;
  }
</style>
  