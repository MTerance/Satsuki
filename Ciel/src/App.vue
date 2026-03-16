<script setup lang="ts">
import SatsukiLauncher from './views/SatsukiLauncher.vue'
import MainStatusNavBar from './components/MainStatusNavBar.vue'
import MainGameMenu from './components/gameMenu/MainGameMenu.vue'
</script>

<template>
  <!-- Barre de statut Socket.IO en haut -->
  <MainStatusNavBar />
  <SatsukiLauncher />
</template>

<style scoped>
/* App simplifié - SatsukiLauncher gère son propre style */
</style>
