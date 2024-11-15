<template>
  <v-app>
    <v-app-bar app color="grey" dark>
      <div style="display: flex; align-items: center; margin: 0;">
        <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
      </div>
      <v-spacer></v-spacer>
      <v-btn text><router-link to="/productos/lista" class="menu">Productos</router-link></v-btn>
      <v-btn text><router-link to="/productos/lista" class="menu">Contacto</router-link></v-btn>
      <v-btn color="black" @click="iniciarSesion">Iniciar Sesión</v-btn>
    </v-app-bar>

    <div class="image-container">
      <v-img
        src="@/assets/IPHONES.jpeg"
        height="400"
        class="d-flex align-center"
      >
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
      <v-row>
        <v-col v-for="producto in productos.slice(0, 3)" :key="producto.id_producto" cols="12" sm="6" md="4">
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
              <v-btn color="grey" @click="agregarAlCarrito(producto)">Agregar al Carrito</v-btn>
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
import axios from 'axios'; 
export default {
  name: 'HomeView',
  data() {
    return {
      productos: [],
    };
  },
  created() {
    this.fetchProductos();
  },
  methods: {
    fetchProductos() {
      axios.get('http://127.0.0.1:8000/productos/')
        .then(response => {
          this.productos = response.data;
          this.errorMessage = null;
        })
        .catch(error => {
          this.errorMessage = 'Error al cargar los productos';
          console.error(error);
        });
    },
    verProductos() {
      this.$router.push('/productos/lista');
    },
    agregarAlCarrito(product) {
      console.log(`Agregado al carrito: ${product.name}`);
    },
    iniciarSesion() {
      this.$router.push('/login');
    },
  },
};
</script>


<style scoped>
.logo {
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

.menu{
  text-decoration: none;
  color: white;
}
</style>




