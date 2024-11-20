<template>
  <v-app>
    <v-app-bar app color="grey" dark>
      <div style="display: flex; align-items: center; margin: 0;">
        <h3>IMPORT TDF</h3>
        <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
      </div>
      <v-spacer></v-spacer>
      <v-btn text @click="verProductos" class="menu">Productos</v-btn>
      <v-btn text @click="contacto" class="menu">Contacto</v-btn>
      <v-btn v-if="!isAuthenticated" color="black" @click="iniciarSesion">Iniciar Sesión</v-btn>
      <v-menu v-else>
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" v-on="on">{{ nombreUsuario }}</v-btn>
        </template>
        <v-list>
          <v-list-item @click="verPerfil">
            <v-list-item-title>Mi Perfil</v-list-item-title>
          </v-list-item>
          <v-list-item v-if="userRole === 'administrador'" @click="agregarProducto">
            <v-list-item-title>Agregar Productos</v-list-item-title>
          </v-list-item>
          <v-list-item @click="cerrarSesion">
            <v-list-item-title>Cerrar Sesión</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <div class="image-container">
      <v-img src="@/assets/IPHONES.jpeg" height="400" class="d-flex align-center" alt="Imagen de iPhones">
        <v-container>
          <v-row>
            <v-col class="text-center">
              <h2 class="display-2 white--text">Los Mejores Celulares del Mercado</h2>
              <v-btn color="white" @click="verProductos" class="mt-4">Ver Productos</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-img>
      <div class="overlay"></div>
    </div>

    <v-container>
      <h2><center>PRODUCTOS DESTACADOS</center></h2>
      <br>
      <v-alert v-if="errorLoading" type="error">
        No se pudieron cargar los productos. Intenta nuevamente más tarde.
      </v-alert>
      <v-row>
        <v-col v-for="producto in productos.slice(0, 3)" :key="producto.id_producto" cols="12" sm="6" md="4">
          <v-card>
            <v-img :src="producto.imagen" height="200px" contain alt="Imagen del producto"></v-img>
            <div class="text-center">
              <v-card-subtitle class="product-title">
                {{ producto.nombre }}
                <span v-if="producto.modelo_detalle">
                  {{ producto.modelo_detalle.nombre_modelo }} {{ producto.modelo_detalle.version }}
                </span>
              </v-card-subtitle>
              <v-card-subtitle>{{ producto.descripcion }}</v-card-subtitle>
              <span class="price">${{ producto.precio }}</span>
            </div>
            <v-card-actions class="justify-center">
              <v-btn v-if="isAuthenticated" color="grey" @click="agregarAlCarrito(producto)">Agregar al Carrito</v-btn>
              <v-btn v-else color="grey" @click="iniciarSesion">Iniciar Sesión para Agregar</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
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
      productos: [],
      errorLoading: false,
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'nombreUsuario', 'userRole']),
  },
  watch: {
    nombreUsuario(newVal) {
      if (newVal) {
        console.log('Nombre de usuario actualizado:', newVal);
      }
    },
  },
  created() {
    if (!this.isAuthenticated) {
      this.$store.commit('loadAuthState');
    }
    this.fetchProductos(); // Llama a la función para cargar productos
  },
  methods: {
    async fetchProductos() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/productos/');
        this.productos = response.data;
      } catch (error) {
        console.error('Error al cargar los productos', error);
        this.errorLoading = true; // Muestra el mensaje de error
      }
    },
    iniciarSesion() {
      this.$router.push('/login'); // Redirige a la página de inicio de sesión
    },
    verPerfil() {
      this.$router.push('/perfil'); // Redirige a la página del perfil
    },
    agregarAlCarrito(producto) {
      if (this.isAuthenticated) {
        console.log(`Agregado al carrito: ${producto.nombre}`);
        // Lógica para agregar al carrito
      } else {
        alert('Debes iniciar sesión para agregar productos al carrito.');
      }
    },
    cerrarSesion() {
      this.$store.dispatch('logout'); // Llama a la acción de logout de Vuex
      this.$router.push('/login'); // Redirige a la página de inicio de sesión
    },
    verProductos() {
      this.$router.push('/productos/lista'); // Redirige a la página de productos
    },
    contacto() {
      this.$router.push('/contacto'); // Redirige a la página de contacto
    },
    agregarProducto() {
      this.$router.push('/GestionProductos'); // Redirige a la página de gestión de productos
    }
  }
};
</script>


<style scoped>
.image-container {
  position: relative;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
}
</style>


<style scoped>
.logo {
  height: 40px;
  margin-left: 10px;
}
.image-container {
  position: relative;
}
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.product-title {
  font-weight: bold;
}
.price {
  font-size: 1.2em;
  color: #ff5722;
}
</style>






<style scoped>
.v-card {
  max-width: 400px;
  margin: auto;
}
.logo {
  position: absolute;
  height: 55px;
  margin: 0;
  padding: 0;
}
.menu {
  text-decoration: none;
  color: white;
}
.image-container {
  position: relative;
}
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
}
</style>


<style scoped>
.logo {
  position: absolute;
  height: 55px;
  margin: 0;
  padding: 0;
}

.price {
  font-weight: bold;
  color: rgb(63, 63, 63);
}

.image-container {
  position: relative;
  width: 100%;
  margin: 0;
  padding: 0;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  pointer-events: none;
}

.v-card img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.v-card {
  align-items: center;
  text-align: center;
}

.v-card-actions {
  justify-content: center; /* Centra los botones en el card */
}

.product-title {
  font-size: 1.5em; /* Ajusta el tamaño de la fuente según sea necesario */
  font-weight: bold; /* Hace que el texto esté en negrita */
  text-align: center; /* Centra el texto */
  width: 100%; /* Asegura que ocupe todo el ancho */
}

.menu {
  text-decoration: none;
  color: white;
}
</style>





