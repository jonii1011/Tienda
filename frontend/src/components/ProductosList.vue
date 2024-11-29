<template>
  <v-app>
    <v-app-bar app color="grey" dark>
      <div style="display: flex; align-items: center; margin: 0;">
        <h3>IMPORT TDF</h3>
        <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
      </div>
      <v-spacer></v-spacer>
      <v-btn text @click="inicio" class="menu">Inicio</v-btn>
      <v-btn text v-if="isAdmin" @click="agregarProducto" class="menu">Agregar productos</v-btn>
      <v-btn text v-if="isAdmin" @click="agregarModelo" class="menu">Agregar modelos</v-btn>
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
          <v-list-item v-if="!isAdmin" @click="verPedido">
            <v-list-item-title>Mis pedidos</v-list-item-title>
          </v-list-item>
          <v-list-item @click="cerrarSesion">
            <v-list-item-title>Cerrar Sesión</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn v-if="!isAdmin && isAuthenticated" icon @click="verCarrito">
        <v-badge
          color="red"
          :content="cantidadCarrito"
          overlap
        >
          <v-icon>mdi-cart</v-icon>
        </v-badge>
      </v-btn>
    </v-app-bar>

    <v-container class="mt-15 mb-50" style="padding-bottom: 100px;">
      <v-row>
        <v-col cols="12" md="4">
          <v-select
            v-model="filtroModelo"
            :items="modelosOpciones"
            label="Filtrar por modelo"
            clearable
          ></v-select>
        </v-col>
        <v-col cols="12" md="4">
          <v-select
            v-model="filtroTipo"
            :items="tiposOpciones"
            label="Filtrar por tipo"
            clearable
          ></v-select>
        </v-col>
        <v-col cols="12" md="2">
          <v-text-field
            v-model.number="precioMin"
            label="Precio Mínimo"
            type="number"
            clearable
            placeholder="Precio mínimo"
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="2">
          <v-text-field
            v-model.number="precioMax"
            label="Precio Máximo"
            type="number"
            clearable
            placeholder="Precio máximo"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <v-col cols="12" class="text-center">
          <v-btn text @click="ordenarProductos('asc')" class="mr-2">Ordenar de Menor a Mayor</v-btn>
          <v-btn text @click="ordenarProductos('desc')">Ordenar de Mayor a Menor</v-btn>
        </v-col>
      </v-row>

      <v-row>
        <v-col v-for="producto in productosFiltrados" :key="producto.id_producto" cols="12" sm="6" md="4">
          <v-card>
            <v-img :src="producto.imagen" height="200px" contain></v-img>
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
              <v-btn v-if="isAuthenticated && !isAdmin" color="grey" @click="agregarAlCarrito(producto)">
                Agregar al Carrito
              </v-btn>
              <v-btn v-if="!isAuthenticated && !isAdmin" color="grey" @click="iniciarSesion">
                Iniciar Sesión para Agregar
              </v-btn>
              <v-btn v-if="isAdmin" color="grey" @click="editarProducto(producto)">Editar</v-btn>
              <v-btn v-if="isAdmin" color="red" @click="eliminarProducto(producto)">Eliminar</v-btn>
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
      filtroModelo: null,
      filtroTipo: null,
      precioMin: null,
      precioMax: null,
      orden: null, // 'asc' o 'desc'
      modelosOpciones: [],
      tiposOpciones: [
        { text: 'Smartphone', value: 1 },
        { text: 'Accesorio', value: 2 },
      ],
      errorMessage: null,
    };
  },
  created() {
    this.fetchProductos(); // Llama a la función para cargar productos
  },
  computed: {
    ...mapGetters(['cantidadCarrito']),
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
    isAdmin() {
      return this.$store.getters.userRole === 'administrador';
    },
    nombreUsuario() {
      return this.$store.getters.nombreUsuario;
    },
    userId() {
      return this.$store.getters.userId;
    },
    productosFiltrados() {
      return this.productos.filter((producto) => {
        const cumpleModelo = this.filtroModelo ? 
          (producto.modelo_detalle && producto.modelo_detalle.nombre_modelo === this.filtroModelo) : 
          true;

        const cumpleTipo = this.filtroTipo ? 
          producto.tipo_producto === this.filtroTipo : 
          true;

        const cumplePrecio = (
          (this.precioMin === null || producto.precio >= Number(this.precioMin)) &&
          (this.precioMax === null || producto.precio <= Number(this.precioMax))
        );

        return cumpleModelo && cumpleTipo && cumplePrecio;
      }).sort((a, b) => {
        if (this.orden === 'asc') {
          return a.precio - b.precio;
        } else if (this.orden === 'desc') {
          return b.precio - a.precio;
        }
        return 0;
      });
    },
  },
  methods: {
    ordenarProductos(orden) {
      this.orden = orden;
    },
    fetchProductos() {
      axios.get('http://127.0.0.1:8000/productos/')
        .then(response => {
          this.productos = response.data;
          this.errorMessage = null;

          this.modelosOpciones = [...new Set(this.productos
            .map(producto => producto.modelo_detalle ? producto.modelo_detalle.nombre_modelo : null)
            .filter(modelo => modelo !== null)
          )].map(modelo => ({ text: modelo, value: modelo }));
        })
        .catch(error => {
          this.errorMessage = 'Error al cargar los productos';
          console.error(error);
        });
    },
    agregarAlCarrito(producto) {
      if (this.isAuthenticated) {
        console.log(`Agregado al carrito: ${producto.nombre}`);
        this.$store.dispatch('agregarAlCarrito', producto); // Agrega el producto al carrito en Vuex
      } else {
        alert('Debes iniciar sesión para agregar productos al carrito.');
      }
    },
    inicio() {
      this.$router.push('/');
    },
    iniciarSesion() {
      this.$router.push('/login');
    },
    cerrarSesion() {
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
    verPerfil() {
      this.$router.push({ name: 'PerfilView', params: { userId: this.userId } });
    },
    verCarrito() {
      this.$router.push('/carrito'); 
    },
    contacto() {
      this.$router.push('/contacto'); // Redirige a la página de contacto
    },
    verPedido() {
      this.$router.push('/ventas'); 
    },
    agregarProducto() {
      this.$router.push('/GestionProductos'); // Redirige a la página para agregar productos
    },
    agregarModelo() {
      this.$router.push('/modelo'); // Redirige a la página de gestión de productos
    },
    editarProducto(producto) {
      this.$router.push({ 
        name: 'GestionProductos', 
        params: { 
          modo: 'editar', 
          id_producto: producto.id_producto,
          id_tipo_producto: producto.tipo_producto ? producto.tipo_producto.id_tipo_producto : null,
          id_modelo: producto.modelo ? producto.modelo.id_modelo : null
        } 
      });
    },
    eliminarProducto(producto) {
      // Confirmar eliminación del producto
      if (confirm("¿Estás seguro de que deseas eliminar este producto?")) {
        axios.delete(`http://localhost:8000/productos/${producto.id_producto}/`)
          .then(() => {
            // Actualiza la lista de productos después de eliminar
            this.fetchProductos();
            alert("Producto eliminado exitosamente."); // Mensaje de éxito
          })
          .catch(error => {
            this.errorMessage = "Hubo un error al eliminar el producto.";
            console.error(error);
          });
      }
    },
  },
};
</script>








<style scoped>
.logo {
  position: absolute;
  height: 55px;
  margin: 0;
  padding: 0;
}
.menu{
  text-decoration: none;
  color: white;
}

.product-title {
  font-size: 1.5em; /* Ajusta el tamaño de la fuente según sea necesario */
  font-weight: bold; /* Hace que el texto esté en negrita */
  text-align: center; /* Centra el texto */
  width: 100%; /* Asegura que ocupe todo el ancho */
}
  
.price {
  font-weight: bold;
  color: rgb(63, 63, 63);
  text-align: center; /* Centra el precio */
}
</style>