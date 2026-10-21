<script setup lang="ts">
import MainStatusNavBar from './components/MainStatusNavBar.vue'
</script>

<template>
  <!-- Barre de statut en haut -->
  <MainStatusNavBar />
  <!-- Contenu routé : MainView (layout) + ses routes imbriquées -->
  <router-view />
</template>

<style scoped>
/* App simplifié - SatsukiLauncher gère son propre style */
</style>
