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
      <v-btn text @click="contacto" class="menu">Contacto</v-btn>
    </v-app-bar>
    
    <v-container style="margin-top: 120px;">
      <v-card v-if="!isAuthenticated">
        <v-card-title class="headline">Iniciar Sesión</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="email"
              label="Email"
              :rules="[rules.required, rules.email]"
              required
              aria-label="Email"
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="Contraseña"
              :rules="[rules.required]"
              type="password"
              required
              aria-label="Contraseña"
            ></v-text-field>
            <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          </v-form>
          <div class="text-center mt-3">
            <router-link to="/cliente-registrar" class="text-decoration-none">
              ¿No tienes cuenta? Regístrate aquí
            </router-link>
          </div>
        </v-card-text>
        <v-card-actions style="justify-content: flex-start;">
          <v-btn color="white" @click="handleLogin" :loading="loading" :disabled="!valid">Iniciar Sesión</v-btn>
          <v-btn color="grey" @click="resetForm">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
      <v-card v-else>
        <v-card-title class="headline">Bienvenido, {{ nombreUsuario }}</v-card-title>
        <v-card-text>
          Has iniciado sesión exitosamente.
        </v-card-text>
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
import { mapGetters, mapActions } from 'vuex';

export default {
  data() {
    return {
      email: '',
      password: '',
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
    ...mapGetters(['isAuthenticated', 'nombreUsuario']),
  },
  methods: {
    ...mapActions(['login', 'logout']),
    async handleLogin() {
      try {
        console.log('Email:', this.email); // Verifica el email
        console.log('Password:', this.password); // Verifica la contraseña

        await this.$store.dispatch('login', {
          email: this.email,
          password: this.password,
        });
      } catch (error) {
        console.error('Error al iniciar sesión:', error);
        this.errorMessage = 'Credenciales incorrectas'; // Mensaje de error
        this.snackbarMessage = 'Error al iniciar sesión';
        this.snackbar = true; // Muestra el snackbar
      }
    },
    handleLogout() {
      this.logout(); // Llama a la acción de logout
      this.$router.push('/'); // Redirige a inicio
    },
    resetForm() {
      this.email = '';
      this.password = '';
      this.errorMessage = '';
      this.$refs.form.reset();
    },
    inicio() {
      this.$router.push('/');
    },
    producto() {
      this.$router.push('/');
    },
    contacto() {
      this.$router.push('/');
    },
  },
};
</script>

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
.error-message {
  color: red;
  text-align: center;
}
</style>



