<template>
  <v-app>
    <v-app-bar app color="grey" dark>
      <div style="display: flex; align-items: center;">
        <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
        <h3 class="title">IMPORT TDF</h3>
      </div>
      <v-spacer></v-spacer>
      <v-btn text @click="inicio" class="menu">Inicio</v-btn>
      <v-btn text @click="producto" class="menu">Productos</v-btn>
      <v-btn text @click="contacto" class="menu">Contacto</v-btn>
    </v-app-bar>

    <v-card class="mx-auto" style="max-width: 600px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); background-color: #f5f5f5;">
      <v-card-title class="headline text-center" style="font-weight: bold; color: black;">Registrar Cliente</v-card-title>
      <v-card-text>
        <v-form ref="registerForm" v-model="valid">
          <v-text-field
            v-model="dni"
            label="DNI"
            :rules="[rules.required]"
            required
            outlined
            dense
            class="my-2"
            color="grey"
          ></v-text-field>
          <v-text-field
            v-model="nombre"
            label="Nombre"
            :rules="[rules.required]"
            required
            outlined
            dense
            class="my-2"
            color="grey"
          ></v-text-field>
          <v-text-field
            v-model="apellido"
            label="Apellido"
            :rules="[rules.required]"
            required
            outlined
            dense
            class="my-2"
            color="grey"
          ></v-text-field>
          <v-text-field
            v-model="fecha_de_nacimiento"
            label="Fecha de nacimiento"
            :rules="[rules.required]"
            type="date"
            required
            outlined
            dense
            class="my-2"
            color="grey"
          ></v-text-field>
          <v-text-field
            v-model="direccion"
            label="Dirección"
            :rules="[rules.required]"
            required
            outlined
            dense
            class="my-2"
            color="grey"
          ></v-text-field>
          <v-text-field
            v-model="telefono"
            label="Teléfono"
            :rules="[rules.required]"
            required
            outlined
            dense
            class="my-2"
            color="grey"
          ></v-text-field>
          <v-text-field
            v-model="email"
            label="Email"
            :rules="[rules.required, rules.email]"
            required
            outlined
            dense
            class="my-2"
            color="grey"
          ></v-text-field>
          <v-text-field
            v-model="contraseña"
            label="Contraseña"
            :rules="[rules.required]"
            type="password"
            required
            outlined
            dense
            class="my-2"
            color="grey"
          ></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="grey darken-2" @click="registrarCliente" class="white--text">Registrar</v-btn>
        <v-spacer></v-spacer>
        <v-btn color="grey" @click="resetRegisterForm">Cancelar</v-btn>
      </v-card-actions>
    </v-card>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      dni: '',
      nombre: '',
      apellido: '',
      fecha_de_nacimiento: '',
      direccion: '',
      telefono: '',
      email: '',
      contraseña: '',
      valid: false,
      errorMessage: '',
      rules: {
        required: value => !!value || 'Este campo es requerido',
        email: value => /.+@.+\..+/.test(value) || 'Este debe ser un email válido'
      },
    };
  },
  methods: {
    registrarCliente() {
      if (!this.dni || !this.nombre || !this.apellido || !this.fecha_de_nacimiento || 
          !this.direccion || !this.telefono || !this.email || !this.contraseña) {
        alert("Por favor, completa todos los campos requeridos.")
      }

      const clienteData = {
        dni: this.dni,
        nombre: this.nombre,
        apellido: this.apellido,
        fecha_de_nacimiento: this.fecha_de_nacimiento,
        direccion: this.direccion,
        telefono: this.telefono,
        email: this.email,
        contraseña: this.contraseña,
      };

      axios.post('http://127.0.0.1:8000/usuario/', clienteData)
        .then(() => {
          alert("CLIENTE REGISTRADO EXITOSAMENTE");
          this.resetRegisterForm();
          this.$router.go(-1);
        })
        .catch(error => {
          console.error("Error al añadir el cliente:", error.response.data);
        });
    },
    resetRegisterForm() {
      this.dni = '';
      this.nombre = '';
      this.apellido = '';
      this.fecha_de_nacimiento = '';
      this.direccion = '';
      this.telefono = '';
      this.email = '';
      this.contraseña = '';
      this.errorMessage = '';
      this.$refs.registerForm.reset();
    },
    inicio() {
      this.$router.push("/");
    },
    producto() {
      this.$router.push("/productos/lista");
    },
    contacto() {
      this.$router.push("/contacto");
    },
  },
};
</script>

<style scoped>
.logo {
  height: 55px;
}
.title {
  margin-left: 10px;
  color: white;
}
.menu {
  text-decoration: none;
  color: white;
}
.v-card {
  margin: 50px auto;
  border-radius: 12px;
}
</style>


  