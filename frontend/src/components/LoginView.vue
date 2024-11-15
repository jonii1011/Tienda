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
    </v-app-bar>
    
    <v-container style="margin-top: 64px;"> <!-- Ajusta el valor según la altura de tu app-bar -->
      <v-card>
        <v-card-title class="headline">Iniciar Sesión</v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="email"
              label="Email"
              :rules="[rules.required, rules.email]"
              required
            ></v-text-field>
            <v-text-field
              v-model="contraseña"
              label="Contraseña"
              :rules="[rules.required]"
              type="password"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" @click="login">Iniciar Sesión</v-btn>
          <v-btn color="grey" @click="resetForm">Cancelar</v-btn>
        </v-card-actions>
      </v-card>
    </v-container>
  </v-app>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      loginDialog: false,
      email: '',
      contraseña: '', // Asegúrate de usar 'contraseña' aquí
      valid: false,
      loading: false,
      rules: {
        required: value => !!value || 'Este campo es requerido',
        email: value => /.+@.+\..+/.test(value) || 'Este debe ser un email válido',
      },
      productos: [] // Asegúrate de cargar tus productos aquí
    };
  },
  methods: {
    async login() {
    if (this.$refs.form.validate()) {
      this.loading = true; // Inicia el indicador de carga
      try {
        const response = await axios.post('http://127.0.0.1:8000/login/', {
          email: this.email,
          contraseña: this.contraseña,
        });
        alert(response.data.message);
      } catch (error) {
        if (error.response) {
          alert(error.response.data.error);
        } else {
          alert('Error en la conexión');
        }
      } finally {
        this.loading = false; // Detiene el indicador de carga
      }
    }
  },
    resetForm() {
      this.email = '';
      this.contraseña = '';
      this.$refs.form.reset();
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
  height: 55px;
  margin: 0;
  padding: 0;
}
.menu {
  text-decoration: none;
  color: white;
}
</style>

