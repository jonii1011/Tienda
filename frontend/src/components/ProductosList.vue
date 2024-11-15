<template>
  <v-app>
    <v-app-bar app color="grey" dark>
      <div style="display: flex; align-items: center; margin: 0;">
        <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
      </div>
      <v-spacer></v-spacer>
      <v-btn text><router-link to="/" class="menu">Inicio</router-link></v-btn>
      <v-btn text><router-link to="/productos/lista" class="menu">Productos</router-link></v-btn>
      <v-btn text><router-link to="/contacto" class="menu">Contacto</router-link></v-btn>
      <v-btn color="black" @click="iniciarSesion">Iniciar Sesión</v-btn>
    </v-app-bar>

    <v-container class="mt-15 mb-50">
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
        <v-col cols="12" md="4">
          <v-select
            v-model="filtroPrecio"
            :items="precioOpciones"
            label="Filtrar por precio"
            clearable
          ></v-select>
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
              <v-btn color="grey" @click="agregarAlCarrito(producto)">Agregar al Carrito</v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

<script>
import axios from 'axios'; 
export default {
  data() {
    return {
      productos: [],
      filtroNombre: '',
      filtroModelo: null,
      filtroTipo: null,
      filtroPrecio: null,
      precioOpciones: [
        { text: 'Todos', value: null },
        { text: 'Menos de 800', value: 800 },
        { text: '900 - 1200', value: [900, 1200] },
      ],
      modelosOpciones: [],
      tiposOpciones: [
        { text: 'Smartphone', value: 1 },
        { text: 'Accesorio', value: 2 },
      ],
      errorMessage: null,
    };
  },
  created() {
    this.fetchProductos();
  },
  computed: {
    productosFiltrados() {
  // Filtra la lista de productos según varios criterios
  return this.productos.filter((producto) => {
    // Verifica si el nombre del producto incluye el texto del filtro (insensible a mayúsculas)
    const cumpleNombre = producto.nombre.toLowerCase().includes(this.filtroNombre.toLowerCase());

    // Verifica si hay un filtro de modelo y si el modelo del producto coincide
    const cumpleModelo = this.filtroModelo ? 
      (producto.modelo_detalle && producto.modelo_detalle.nombre_modelo === this.filtroModelo) : 
      true; // Si no hay filtro, se considera que cumple

    // Verifica si hay un filtro de tipo y si el tipo del producto coincide
    const cumpleTipo = this.filtroTipo ? 
      producto.tipo_producto === this.filtroTipo : 
      true; // Si no hay filtro, se considera que cumple

    // Verifica si hay un filtro de precio
    const cumplePrecio = this.filtroPrecio ? (
      // Si el filtro de precio es un rango (array)
      Array.isArray(this.filtroPrecio) ?
        (producto.precio >= this.filtroPrecio[0] && producto.precio <= this.filtroPrecio[1]) : // Comprueba si el precio está dentro del rango
        (producto.precio < this.filtroPrecio) // Comprueba si el precio es menor que el valor del filtro
    ) : true; // Si no hay filtro, se considera que cumple

    // Retorna verdadero solo si el producto cumple con todos los filtros
    return cumpleNombre && cumpleModelo && cumpleTipo && cumplePrecio;
  });
}
  },
  methods: {
    fetchProductos() {
      axios.get('http://127.0.0.1:8000/productos/')
        .then(response => {
          this.productos = response.data;
          this.errorMessage = null;

          // Extraer modelos únicos para el filtro y evitar null
          this.modelosOpciones = [...new Set(this.productos
            .map(producto => producto.modelo_detalle ? producto.modelo_detalle.nombre_modelo : null)
            .filter(modelo => modelo !== null) // Filtrar valores null
          )].map(modelo => ({ text: modelo, value: modelo }));
        })
        .catch(error => {
          this.errorMessage = 'Error al cargar los productos';
          console.error(error);
        });
    },
    agregarAlCarrito(producto) {
      console.log('Agregado al carrito:', producto);
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