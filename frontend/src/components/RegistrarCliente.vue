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

    <v-card class="mx-auto" style="max-width: 600px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); background-color: #f5f5f5; margin-top: 100px;">
      <v-card-title class="headline text-center" style="font-weight: bold; color: black;">
        {{ isEditing ? 'Editar Cliente' : 'Registrar Cliente' }}
      </v-card-title>
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
            :type="showPassword ? 'text' : 'password'"
            required
            outlined
            dense
            class="my-2"
            color="grey"
          >
            <template v-slot:append>
              <v-btn icon @click="showPassword = !showPassword"> <!-- Botón para mostrar/ocultar -->
                <v-icon>{{ showPassword ? 'mdi-eye-off' : 'mdi-eye' }}</v-icon>
              </v-btn>
            </template>
          </v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="grey darken-2" @click="isEditing ? editarCliente() : registrarCliente()" class="white--text">
          {{ isEditing ? 'Actualizar' : 'Registrar' }}
      </v-btn>
        <v-spacer></v-spacer>
        <v-btn color="grey" @click="cancelar">Cancelar</v-btn>
      </v-card-actions>
    </v-card>
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
      dni: '',
      nombre: '',
      apellido: '',
      fecha_de_nacimiento: '',
      direccion: '',
      telefono: '',
      email: '',
      contraseña: '',
      showPassword: false, // Estado para controlar la visibilidad de la contraseña
      valid: false,
      isEditing: false,
      rules: {
        required: value => !!value || 'Este campo es requerido',
        email: value => /.+@.+\..+/.test(value) || 'Este debe ser un email válido'
      },
    };
  },
  methods: {
    registrarCliente() {
      const clienteData = this.getClienteData();
      console.log("Datos del cliente a registrar:", clienteData); // Verifica los datos
      axios.post('http://127.0.0.1:8000/usuario/', clienteData)
        .then(() => {
          alert("CLIENTE REGISTRADO EXITOSAMENTE");
          this.$router.go(-1);
        })
        .catch(error => {
          if (error.response) {
            console.error("Error al añadir el cliente:", error.response.data);
          } else {
            console.error("Error sin respuesta:", error.message);
          }
        });
    },
    editarCliente() {
      const id = this.$route.params.id;
      const clienteData = this.getClienteData();
      axios.put(`http://127.0.0.1:8000/usuario/${id}/`, clienteData)
        .then(() => {
          alert("CLIENTE ACTUALIZADO EXITOSAMENTE");
          this.$router.go(-1);
        })
        .catch(error => {
          console.error("Error al actualizar el cliente:", error.response.data);
        });
    },
    getClienteData() {
      return {
        dni: this.dni,
        nombre: this.nombre,
        apellido: this.apellido,
        fecha_de_nacimiento: this.fecha_de_nacimiento,
        direccion: this.direccion,
        telefono: this.telefono,
        email: this.email,
        contraseña: this.contraseña,
      };
    },
    cancelar() {
      this.$router.go(-1);
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
    loadClienteData(id) {
      axios.get(`http://127.0.0.1:8000/usuario/${id}/`)
        .then(response => {
          const cliente = response.data;
          this.dni = cliente.dni;
          this.nombre = cliente.nombre;
          this.apellido = cliente.apellido;
          this.fecha_de_nacimiento = cliente.fecha_de_nacimiento;
          this.direccion = cliente.direccion;
          this.telefono = cliente.telefono;
          this.email = cliente.email;
          // No se recomienda mostrar la contraseña
        })
        .catch(error => {
          console.error("Error al cargar los datos del cliente:", error);
        });
    },
  },
  created() {
    if (this.$route.params.id) {
      this.isEditing = true;
      this.loadClienteData(this.$route.params.id);
    }
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




  