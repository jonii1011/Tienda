<template>
  <v-app>
    <v-app-bar app color="grey" dark>
      <div style="display: flex; align-items: center; margin: 0;">
        <h3>IMPORT TDF</h3>
        <v-img src="@/assets/file.png" alt="Logo" class="logo" contain></v-img>
      </div>
      <v-spacer></v-spacer>
      <v-btn text @click="inicio" class="menu">Inicio</v-btn>
      <v-btn text v-if="!isAdmin" @click="contacto" class="menu">Contacto</v-btn>
      <v-btn v-if="!isAuthenticated" color="black" @click="iniciarSesion">Iniciar Sesión</v-btn>
      <v-menu v-else>
        <template v-slot:activator="{ on, attrs }">
          <v-btn color="black" v-bind="attrs" v-on="on">{{ nombreUsuario }}</v-btn>
        </template>
        <v-list>
          <v-list-item @click="verPedido">
            <v-list-item-title>Mis pedidos</v-list-item-title>
          </v-list-item>
          <v-list-item @click="cerrarSesion">
            <v-list-item-title>Cerrar Sesión</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <v-container class="mt-15 mb-50">
      <v-card class="mx-auto" style="max-width: 600px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); background-color: #f5f5f5; margin-top: 60px;">
        <v-card-title class="headline text-center" style="font-weight: bold; color: black;">Perfil de Usuario</v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title v-if="!isAdmin"><strong>DNI:</strong> {{ usuario.dni }}</v-list-item-title>
                <v-list-item-title><strong>Nombre:</strong> {{ usuario.nombre }}</v-list-item-title>
                <v-list-item-title v-if="!isAdmin"><strong>Apellido:</strong> {{ usuario.apellido }}</v-list-item-title>
                <v-list-item-title v-if="!isAdmin"><strong>Fecha de nacimiento:</strong> {{ usuario.fecha_de_nacimiento }}</v-list-item-title>
                <v-list-item-title v-if="!isAdmin"><strong>Dirección:</strong> {{ usuario.direccion }}</v-list-item-title>
                <v-list-item-title v-if="!isAdmin"><strong>Teléfono:</strong> {{ usuario.telefono }}</v-list-item-title>
                <v-list-item-title><strong>Email:</strong> {{ usuario.email }}</v-list-item-title>
                <v-list-item-title><strong>Rol:</strong> {{ isAdmin ? 'Administrador' : 'Usuario' }}</v-list-item-title>
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-btn color="grey" @click="editarPerfil">Editar Perfil</v-btn>
          <v-spacer></v-spacer>
          <v-btn color="grey" @click="cerrarSesion">Cerrar Sesión</v-btn>
        </v-card-actions>
      </v-card>
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
      usuario: {},
    };
  },
  created() {
    this.fetchUsuario();
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
  methods: {
    fetchUsuario() {
      const userId = this.userId; // Obtiene el ID del usuario desde Vuex
      if (userId) {
        axios.get(`http://127.0.0.1:8000/usuario/${userId}/`) // Cambia la URL según tu API
          .then(response => {
            this.usuario = response.data;
          })
          .catch(error => {
            console.error('Error al cargar el perfil:', error);
          });
      } else {
        console.error('No se encontró el ID del usuario.');
      }
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
    verPedido() {
      this.$router.push('/ventas'); 
    },
    agregarProducto() {
      this.$router.push('/GestionProductos');
    },
    editarPerfil() {
      this.$router.push({ name: 'RegistrarCliente', 
      params: { id: this.userId } });
    },
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

  
  