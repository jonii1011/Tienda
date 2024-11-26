<template>
    <v-app>
      <v-app-bar app color="grey" dark>
        <div style="display: flex; align-items: center; margin: 0;">
          <h3>IMPORT TDF</h3>
          <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
        </div>
        <v-spacer></v-spacer>
        <v-btn text @click="inicio" class="menu">Inicio</v-btn>
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
  
      <v-container v-if="isAdmin" class="mt-15 mb-50">
        <v-card class="mx-auto" style="max-width: 600px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); background-color: #f5f5f5; margin-top: 60px;">
          <v-card-title class="headline text-center" style="font-weight: bold; color: black;">Agregar Modelo</v-card-title>
          <v-card-text>
            <v-form ref="form" v-model="valid">
              <v-text-field
                v-model="nombre"
                :rules="[rules.required]"
                label="Nombre del Modelo"
                required
              ></v-text-field>
              <v-text-field
                v-model="version"
                label="Versión"
                required
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="white" @click="guardarModelo">Guardar Modelo</v-btn>
            <v-spacer></v-spacer>
            <v-btn color="grey" @click="cancelar">Cancelar</v-btn>
          </v-card-actions>
        </v-card>
  
        <!-- Lista de Modelos -->
        <v-card class="mx-auto mt-5 mb-5" style="max-width: 600px; border-radius: 12px; background-color: #e0e0e0;">
          <v-card-title class="headline text-center" style="font-weight: bold; color: black;">Lista de Modelos</v-card-title>
          <v-list>
            <v-list-item v-for="modelo in modelos" :key="modelo.id_modelo"> <!-- Se eliminó 'index' -->
              <v-list-item-content>
                <v-list-item-title>{{ modelo.nombre_modelo }} - {{ modelo.version }}</v-list-item-title>
              </v-list-item-content>
              <v-list-item-action>
                <v-btn icon @click="eliminarModelo(modelo.id_modelo)">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </v-list-item-action>
            </v-list-item>
          </v-list>
        </v-card>
      </v-container>
  
      <v-footer>
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
        nombre: '',
        version: '',
        valid: false,
        modelos: [], // Propiedad para almacenar los modelos
        rules: {
          required: value => !!value || 'Este campo es obligatorio.',
        },
      };
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
      userId() {
        return this.$store.getters.userId;
      },
    },
    mounted() {
      this.obtenerModelos(); // Llamar a la función para obtener los modelos al montar el componente
    },
    methods: {
      obtenerModelos() {
        axios.get('http://127.0.0.1:8000/modelo/')
          .then(response => {
            this.modelos = response.data; // Asignar los modelos obtenidos a la propiedad modelos
          })
          .catch(error => {
            console.error('Error al obtener la lista de modelos:', error);
            alert('Error al cargar la lista de modelos. Por favor, intente nuevamente.');
          });
      },
      guardarModelo() {
        if (this.$refs.form.validate()) {
          const modeloData = {
            nombre_modelo: this.nombre,
            version: this.version || '',
          };
  
          axios.post('http://127.0.0.1:8000/modelo/', modeloData)
            .then(() => {
              alert('Modelo agregado exitosamente.');
              this.modelos.push(modeloData); // Agregar el nuevo modelo a la lista local
              this.limpiarFormulario();
            })
            .catch(error => {
              console.log('Datos enviados:', modeloData);
              console.error('Error al agregar el modelo:', error);
              alert('Error al agregar el modelo. Por favor, intente nuevamente.');
            });
        } else {
          alert('Por favor completa todos los campos requeridos.');
        }
      },
      eliminarModelo(id_modelo) {
        axios.delete(`http://127.0.0.1:8000/modelo/${id_modelo}/`)
          .then(() => {
            alert('Modelo eliminado exitosamente.');
            this.modelos = this.modelos.filter(modelo => modelo.id_modelo !== id_modelo); // Asegúrate de usar el ID correcto
          })
          .catch(error => {
            console.error('Error al eliminar el modelo:', error);
            alert('Error al eliminar el modelo. Por favor, intente nuevamente.');
          });
      },
      limpiarFormulario() {
        this.nombre = '';
        this.version = '';
        this.$refs.form.reset();
      },
      cancelar() {
        this.limpiarFormulario();
        this.$router.push('/'); // Redirige a la página de inicio o a donde desees
      },
      inicio() {
        this.$router.push('/');
      },
      cerrarSesion() {
        this.$store.dispatch('logout');
        this.$router.push('/');
      },
      contacto() {
        this.$router.push('/contacto');
      },
      agregarProducto() {
        this.$router.push('/GestionProductos');
      },
      verPerfil() {
      this.$router.push({ name: 'PerfilView', params: { userId: this.userId } });
    },
    },
  };
  </script>
  
<style>
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
</style>