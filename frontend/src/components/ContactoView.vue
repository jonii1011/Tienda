<template>
  <v-app>
    <v-app-bar app color="grey" dark>
      <div style="display: flex; align-items: center; margin: 0;">
        <h3>IMPORT TDF</h3>
        <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
      </div>
      <v-spacer></v-spacer>
      <v-btn text @click="inicio" class="menu">Inicio</v-btn>
      <v-btn text @click="producto" class="menu">Productos</v-btn>
      <v-btn v-if="!isAuthenticated" color="black" @click="iniciarSesion">Iniciar Sesión</v-btn>
      <v-menu v-else>
        <template v-slot:activator="{ on, attrs }">
          <v-btn v-bind="attrs" v-on="on">{{ nombreUsuario }}</v-btn>
        </template>
        <v-list>
          <v-list-item @click="verPerfil">
            <v-list-item-title>Mi Perfil</v-list-item-title>
          </v-list-item>
          <v-list-item v-if="userRole != 'administrador'" @click="verPedido">
            <v-list-item-title>Mis pedidos</v-list-item-title>
          </v-list-item>
          <v-list-item @click="cerrarSesion">
            <v-list-item-title>Cerrar Sesión</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn v-if="userRole != 'administrador' && isAuthenticated" icon @click="verCarrito">
        <v-badge color="red" :content="cantidadCarrito" overlap>
          <v-icon>mdi-cart</v-icon>
        </v-badge>
      </v-btn>
    </v-app-bar>

    <v-container class="mx-auto pa-4" style="max-width: 500px; margin-top: 120px;">
      <v-card>
        <v-card-title class="headline">Formulario de Contacto</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="nombre"
              label="Nombre"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="correo"
              label="Correo Electrónico"
              :rules="[rules.required, rules.email]"
              required
            ></v-text-field>
            <v-textarea
              v-model="mensaje"
              label="Mensaje"
              :rules="[rules.required]"
              required
            ></v-textarea>
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          </v-form>
        </v-card-text>
        <v-card-actions style="justify-content: flex-start;">
          <v-btn color="primary" @click="enviarFormulario" :loading="loading" :disabled="!valid">Enviar</v-btn>
          <v-btn color="grey" @click="resetForm">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>

    <v-snackbar v-model="snackbar" timeout="3000">
      {{ snackbarMessage }}
    </v-snackbar>

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
      nombre: '',
      correo: '',
      mensaje: '',
      valid: false,
      loading: false,
      errorMessage: '',
      snackbar: false,
      snackbarMessage: '',
      rules: {
        required: value => !!value || 'Requerido.',
        email: value => /.+@.+\..+/.test(value) || 'Email no válido.',
      },
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'nombreUsuario', 'userRole', 'userId', 'cantidadCarrito', 'correoUsuario']),
  },
  mounted() {
    // Cargar datos del usuario si está autenticado
    if (this.isAuthenticated) {
      this.nombre = this.nombreUsuario; // Asigna el nombre del usuario
      this.correo = this.correoUsuario;
    }
  },
  methods: {
    async enviarFormulario() {
      if (this.$refs.form.validate()) {
        this.loading = true; // Activar el estado de carga
        try {
          await axios.post('http://127.0.0.1:8000/api/contacto/', {
            nombre: this.nombre,
            correo: this.correo,
            mensaje: this.mensaje,
          });

          this.snackbarMessage = 'Gracias por tu mensaje. Nos comunicaremos contigo pronto.';
          this.snackbar = true;

          // Limpiar el formulario
          this.resetForm();
        } catch (error) {
          console.error('Error al enviar el formulario:', error);
          this.errorMessage = 'Hubo un problema al enviar tu mensaje. Intenta nuevamente más tarde.';
        } finally {
          this.loading = false; // Desactivar el estado de carga
        }
      }
    },
    resetForm() {
      this.nombre = '';
      this.correo = '';
      this.mensaje = '';
      this.errorMessage = '';
      this.$refs.form.reset();
    },
    inicio() {
      this.$router.push('/');
    },
    producto() {
      this.$router.push('/productos');
    },
    iniciarSesion() {
      this.$router.push('/login'); // Redirige a la página de inicio de sesión
    },
    verPerfil() {
      this.$router.push({ name: 'PerfilView', params: { userId: this.userId } });
    },
    verPedido() {
      this.$router.push('/ventas'); 
    },
    cerrarSesion() {
      this.$store.dispatch('logout'); // Llama a la acción de logout de Vuex
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
  .menu {
    text-decoration: none;
    color: white;
  }
  .error-message {
    color: red;
    text-align: center;
  }
  </style>
  