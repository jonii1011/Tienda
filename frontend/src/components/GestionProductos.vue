<template>
  <v-app>
    <v-app-bar app color="grey" dark>
      <div style="display: flex; align-items: center; margin: 0;">
        <h3>IMPORT TDF</h3>
        <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
      </div>
      <v-spacer></v-spacer>
      <v-btn text @click="inicio" class="menu">Inicio</v-btn>
      <v-btn text v-if="isAdmin" @click="agregarModelo" class="menu">Agregar modelos</v-btn>
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
    </v-app-bar>

    <v-container style="margin-top: 80px;">
      <v-container v-if="isAdmin" class="mt-5">
        <v-card>
          <v-card-title>
            <span class="headline">{{ modo === 'editar' ? 'Editar Producto' : 'Agregar Producto' }}</span>
          </v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Nombre"
                    v-model="producto.nombre"
                    :rules="[v => !!v || 'Nombre es requerido']"
                    outlined
                    required
                    color="primary"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Precio"
                    v-model="producto.precio"
                    :rules="[v => !!v || 'Precio es requerido']"
                    outlined
                    required
                    type="number"
                    color="primary"
                  ></v-text-field>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="6">
                  <v-text-field
                    label="Stock"
                    v-model="producto.stock"
                    :rules="[v => !!v || 'Stock es requerido']"
                    outlined
                    required
                    type="number"
                    color="primary"
                  ></v-text-field>
                </v-col>
                <v-col cols="12" sm="6">
                  <v-textarea
                    label="Descripción"
                    v-model="producto.descripcion"
                    :rules="[v => !!v || 'Descripción es requerida']"
                    outlined
                    required
                    color="primary"
                  ></v-textarea>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="6">
                  <v-file-input
                    label="Imagen"
                    v-model="producto.imagen"
                    :rules="[v => !!v || 'Imagen es requerida']"
                    outlined
                    color="primary"
                  ></v-file-input>
                  <img v-if="imagenUrl" :src="imagenUrl" alt="Imagen del producto" style="max-width: 100px; margin-top: 10px;" />
                </v-col>
                <v-col cols="12" sm="6">
                  <v-select
                    label="Tipo de Producto"
                    v-model="tipo_producto_id"
                    :items="tiposProducto"
                    item-text="nombre_tipo"
                    item-value="id_tipo_producto"
                    :rules="[v => !!v || 'Tipo de producto es requerido']"
                    outlined
                    required
                    color="primary"
                  ></v-select>
                </v-col>
              </v-row>

              <v-row>
                <v-col cols="12" sm="6">
                  <v-select
                    label="Modelo"
                    v-model="id_modelo"
                    :items="modelosFormatted"
                    item-text="displayName"
                    item-value="id_modelo"
                    outlined
                    required
                    color="primary"
                  ></v-select>
                </v-col>
                <v-col cols="12" sm="6" class="d-flex align-center justify-end">
                  <v-btn color="white" @click="guardarProducto" elevation="2">
                    {{ modo === 'editar' ? 'Actualizar Producto' : 'Agregar Producto' }}
                  </v-btn>
                </v-col>
              </v-row>
            </v-form>
          </v-card-text>
        </v-card>
      </v-container>
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
  data() {
    return {
      modo: this.$route.params.modo,
      producto: {
        nombre: '',
        precio: '',
        stock: '',
        descripcion: '',
        imagen: null, // Para el file input
      },
      tipo_producto_id: null,
      id_modelo: null,
      valid: false,
      tiposProducto: [],
      modelos: [],
      imagenUrl: '', // Propiedad para la URL de la imagen
    };
  },
  created() {
    this.verificarRol();
    this.cargarTiposProducto();
    this.cargarModelos();

    if (this.modo === 'editar') {
      const id_producto = this.$route.params.id_producto;
      this.tipo_producto_id = this.$route.params.id_tipo_producto; // Accede al ID del tipo de producto
      this.id_modelo = this.$route.params.id_modelo; // Accede al ID del modelo

      this.cargarProducto(id_producto); // Cargar el producto por ID
    }
  },
  computed: {
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
    isAdmin() {
      return this.$store.getters.userRole === 'administrador';
    },
    nombreUsuario() {
      return this.$store.getters.nombreUsuario;
    },
    modelosFormatted() {
      return this.modelos.map(modelo => ({
        ...modelo,
        displayName: `${modelo.nombre_modelo} - ${modelo.version}`
      }));
    }
  },
  methods: {
    cargarProducto(id) {
      axios.get(`http://127.0.0.1:8000/productos/${id}/`)
        .then(response => {
          console.log('Producto cargado:', response.data);
          this.producto = {
            nombre: response.data.nombre,
            precio: response.data.precio,
            stock: response.data.stock,
            descripcion: response.data.descripcion,
            imagen: null, // Para el file input
          };
          this.tipo_producto_id = response.data.tipo_producto; // Asignar directamente el ID
          this.id_modelo = response.data.modelo; // Asignar directamente el ID
          this.imagenUrl = response.data.imagen; // Guardar la URL de la imagen existente
        })
        .catch(error => {
          console.error('Error al cargar el producto:', error);
          alert('Error al cargar el producto. Por favor, intenta nuevamente.');
        });
    },
    verificarRol() {
      console.log('User Role:', this.$store.getters.userRole);
    },
    cargarTiposProducto() {
      axios.get('http://127.0.0.1:8000/tipoproductos/')
        .then(response => {
          this.tiposProducto = response.data;
          console.log('Tipos de producto cargados:', this.tiposProducto);
        })
        .catch(error => {
          console.error('Error al cargar tipos de producto:', error);
          this.tiposProducto = [];
        });
    },
    cargarModelos() {
      axios.get('http://127.0.0.1:8000/modelo/')
        .then(response => {
          this.modelos = response.data;
          console.log('Modelos cargados:', this.modelos);
        })
        .catch(error => {
          console.error('Error al cargar modelos:', error);
          this.modelos = [];
        });
    },
    guardarProducto() {
      const formData = new FormData();
      formData.append('nombre', this.producto.nombre);
      formData.append('precio', this.producto.precio);
      formData.append('stock', this.producto.stock);
      formData.append('descripcion', this.producto.descripcion);
      
      // Solo agregar la imagen si se ha seleccionado una nueva
      if (this.producto.imagen) {
        formData.append('imagen', this.producto.imagen);
      }

      formData.append('tipo_producto', this.tipo_producto_id);
      // Solo agregar el modelo si está definido
      if (this.id_modelo) {
        formData.append('modelo', this.id_modelo);
      }

      const url = this.modo === 'editar' 
        ? `http://127.0.0.1:8000/productos/${this.$route.params.id_producto}/` 
        : 'http://127.0.0.1:8000/productos/';

      const method = this.modo === 'editar' ? 'put' : 'post';

      axios({
        method: method,
        url: url,
        data: formData,
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        console.log('Producto guardado exitosamente:', response.data);
        this.$router.push('/productos/lista');
      })
      .catch(error => {
        if (error.response) {
          console.error('Error al guardar el producto:', error.response.data);
          alert(`Error al guardar el producto: ${JSON.stringify(error.response.data)}`);
        } else if (error.request) {
          console.error('No se recibió respuesta del servidor:', error.request);
        } else {
          console.error('Error al configurar la solicitud:', error.message);
        }
      });
    },
    inicio() {
      this.$router.push('/');
    },
    iniciarSesion() {
      this.$store.dispatch('login', { userName: 'Nombre de Usuario', role: 'administrador' });
      this.$router.push('/gestionproductos');
    },
    cerrarSesion() {
      this.$store.dispatch('logout');
      this.$router.push('/');
    },
    verPerfil() {
      this.$router.push({ name: 'PerfilView', params: { userId: this.userId } });
    },
    agregarModelo() {
      this.$router.push('/modelo'); // Redirige a la página de gestión de productos
    }
  },
};
</script>

<style scoped>
.logo {
  width: 50px; /* Ajusta según sea necesario */
}
.menu {
  margin-left: 15px; /* Espaciado entre botones */
}
</style>
  