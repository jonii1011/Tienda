<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';

export default {
  computed: {
    ...mapGetters(['isAuthenticated', 'nombreUsuario', 'userRole', 'userId']),
  },
  created() {
    this.$store.dispatch('initializeStore');
    this.checkAuthStatus();
  },
  methods: {
  async checkAuthStatus() {
    const token = localStorage.getItem('access_token');

    if (!token) {
      this.$store.dispatch('logout'); // Cerrar sesión si no hay token
      return;
    }

    try {
      const response = await axios.get('http://127.0.0.1:8000/auth/status/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      console.log('Respuesta de estado de autenticación:', response.data); 
      // Asegúrate de que la acción setAuth esté definida para manejar estos datos
      this.$store.commit('setAuth', {
        access: token,
        refresh: localStorage.getItem('refresh_token'),
        nombre: response.data.nombre || 'Usuario',
        role: response.data.role || '',
        id: response.data.id || '',
      });
    } catch (error) {
      console.error('Error al verificar el estado de autenticación:', error);
      this.$store.dispatch('logout'); // Cerrar sesión en caso de error
    }
  },
},
};
</script>

<style>
html, body {
  overflow: hidden;
}
</style>



