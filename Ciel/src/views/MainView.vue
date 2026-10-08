<template>
  <div v-if="!isReady" class="main-view-loading">
    <p>Chargement...</p>
  </div>
  <router-view v-else />
</template>

<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import clientService from '../services/clientService.js';
import processService from '../services/processService.js';

const router = useRouter();
const route = useRoute();
const isReady = ref(false);

let stopConnectionWatch: (() => void) | null = null;
let stopSceneWatch: (() => void) | null = null;

// Correspondance scène serveur (nom de classe C#) → route enfant
const SCENE_ROUTES: Record<string, string> = {
  Title: 'game-title',
  Lobby: 'game-lobby',
  Credits: 'game-credits',
  MainMenu: 'game-main-menu',
  Arcade: 'game-arcade',
};

const goToLauncher = () => {
  if (route.name !== 'launcher') {
    console.log('[MainView] Pas de connexion/instance Satsuki → redirection vers le launcher');
    router.replace({ name: 'launcher' });
  }
};

// Navigue vers la route correspondant à la scène courante du serveur
const goToScene = (scene: string | null) => {
  if (!clientService.isConnected.value) {
    console.log('[MainView] goToScene ignoré : non connecté');
    return;
  }
  const target = (scene && SCENE_ROUTES[scene]) || 'menu';
  if (route.name === target) return; // déjà sur la bonne route
  console.log(`[MainView] Navigation → ${target} (scène: ${scene ?? 'aucune'})`);
  router.replace({ name: target });
};

/**
 * Vérifie l'état Satsuki et route en conséquence :
 * - Non connecté à une instance Satsuki OU aucune instance lancée
 *   → SatsukiLauncher (lancement / connexion)
 * - Connecté et instance en cours → route de la scène courante
 */
const evaluateAndRoute = async () => {
  try {
    if (!clientService.isConnected.value) {
      goToLauncher();
      return;
    }

    // Connecté : s'assurer qu'une instance Satsuki/Godot tourne toujours
    const result = await processService.checkSatsukiProcess();
    if (!result.running) {
      goToLauncher();
      return;
    }

    // Tout est en ordre : afficher la scène courante (ou le menu si inconnue)
    goToScene(clientService.currentScene.value);
  } catch (err) {
    console.error('[MainView] Erreur lors de la vérification Satsuki:', err);
    goToLauncher();
  }
};

onMounted(async () => {
  // Récupérer l'état de connexion réel du client TCP (main process),
  // au cas où une connexion existerait déjà avant le montage.
  // IMPORTANT : lier les listeners IPC avant toute lecture, sinon les
  // événements GAME_STATE émis avant le mount sont perdus.
  try {
    if (clientService.available) {
      // getStatus() lie les listeners IPC (évite de perdre les GAME_STATE précoces)
      const status = await clientService.getStatus();
      if (status?.connected) {
        clientService.isConnected.value = true;
      }
      // Récupère un gameState déjà reçu par le main (ex: 1er client)
      if (status?.gameState && !clientService.gameState.value) {
        clientService.gameState.value = status.gameState;
        console.log('[MainView] GameState récupéré depuis le main — scène:', status.currentScene);
      }
    }
  } catch (err) {
    console.warn('[MainView] Impossible de récupérer le statut Satsuki:', err);
  }

  // Réagir en temps réel aux changements de connexion
  stopConnectionWatch = watch(clientService.isConnected, async (connected) => {
    if (connected) {
      // Le serveur n'envoie GAME_STATE: qu'au premier client : le redemander.
      // Petit délai pour laisser le handshake (ClientTypeConfirmation) se terminer.
      setTimeout(() => { clientService.requestGameState(); }, 300);
      await evaluateAndRoute();
    } else {
      goToLauncher();
    }
  });

  // Réagir en temps réel aux changements de scène (GAME_STATE:)
  stopSceneWatch = watch(clientService.currentScene, (scene) => {
    console.log(`[MainView] Changement de scène détecté: ${scene ?? 'aucune'} (connecté: ${clientService.isConnected.value})`);
    goToScene(scene);
  });

  await evaluateAndRoute();
  isReady.value = true;
});

onUnmounted(() => {
  stopConnectionWatch?.();
  stopSceneWatch?.();
});
</script>

<style scoped>
.main-view-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
}
</style>