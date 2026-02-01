<script setup lang="ts">
import SatsukiLauncher from './views/SatsukiLauncher.vue'
import MainStatusNavBar from './components/MainStatusNavBar.vue'
</script>

<template>
  <!-- Barre de statut Socket.IO en haut -->
  <MainStatusNavBar />
  <SatsukiLauncher />
</template>

<style scoped>
/* App simplifié - SatsukiLauncher gère son propre style */
</style>
