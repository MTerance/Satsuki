<template>
  <div>
    <div class="card players-section">
      <div class="card-header">
        <h3 class="card-title">Joueurs</h3>
        <button class="btn-base btn-primary add-player-button" @click="openPlayerModal">
          + Add Player
        </button>
      </div>

      <!-- Slot menu joueur -->
      <slot name="player-menu" />

      <!-- Liste des joueurs -->
      <div class="items-list players-list">
        <div
          v-for="(player, index) in players"
          :key="player.id"
          class="item player-item"
          :style="{ color: player.color }"
        >
          <div class="item-info">
            <div class="item-main">
              <span class="color-dot player-color-dot" :style="{ backgroundColor: player.color }"></span>
              <span class="item-title player-name">{{ player.name }}</span>
            </div>
          </div>
          <button
            class="action-button remove remove-player-button"
            @click="removePlayer(index)"
            title="Supprimer le joueur"
          >
            ×
          </button>
        </div>
        <div v-if="players.length === 0" class="empty-state">Aucun joueur ajouté</div>
      </div>
    </div>

    <!-- Modal d'ajout de joueur -->
    <div v-if="isPlayerModalOpen" class="modal-overlay" @click="closePlayerModal">
      <div class="modal-container" @click.stop>
        <div class="modal-header">
          <h3 class="modal-title">Ajouter un joueur</h3>
          <button class="modal-close" @click="closePlayerModal">×</button>
        </div>

        <form @submit.prevent="submitPlayer" class="player-form">
          <div class="form-group">
            <label for="playerName" class="form-label">Nom du joueur</label>
            <input
              id="playerName"
              v-model="newPlayerForm.name"
              type="text"
              class="form-input"
              placeholder="Entrez le nom du joueur"
              required
              maxlength="20"
            />
          </div>

          <div class="form-group">
            <label class="form-label">Sexe</label>
            <div class="gender-options">
              <label class="gender-option">
                <input v-model="newPlayerForm.gender" type="radio" value="male" class="gender-radio" />
                <span class="gender-label">
                  <span class="gender-icon">👨</span>
                  Masculin
                </span>
              </label>
              <label class="gender-option">
                <input v-model="newPlayerForm.gender" type="radio" value="female" class="gender-radio" />
                <span class="gender-label">
                  <span class="gender-icon">👩</span>
                  Féminin
                </span>
              </label>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" @click="closePlayerModal" class="btn-cancel">Annuler</button>
            <button type="submit" class="btn-submit" :disabled="!newPlayerForm.name.trim() || !newPlayerForm.gender">Ajouter</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';

interface Player {
  id: number;
  name: string;
  color: string;
  gender: 'male' | 'female';
}

interface PlayerForm {
  name: string;
  gender: 'male' | 'female' | '';
}

const playerColors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#FFB347', '#98D8C8'];

const players = ref<Player[]>([]);
const isPlayerModalOpen = ref(false);
const newPlayerForm = ref<PlayerForm>({ name: '', gender: '' });
let playerIdCounter = 1;

// Emit events upward instead of handling socket logic here
const emit = defineEmits<{
  (e: 'player-added', payload: Player): void;
  (e: 'player-removed', id: number): void;
}>();

const openPlayerModal = () => {
  isPlayerModalOpen.value = true;
  newPlayerForm.value = { name: '', gender: '' };
};

const closePlayerModal = () => {
  isPlayerModalOpen.value = false;
  newPlayerForm.value = { name: '', gender: '' };
};

const submitPlayer = () => {
  if (!newPlayerForm.value.name.trim() || !newPlayerForm.value.gender) return;
  if (players.value.length >= playerColors.length) { alert(`Maximum ${playerColors.length} joueurs autorisés`); return; }

  const newPlayer: Player = { id: playerIdCounter++, name: newPlayerForm.value.name.trim(), color: playerColors[players.value.length], gender: newPlayerForm.value.gender as 'male' | 'female' };
  players.value.push(newPlayer);
  // Notify parent that a player was added
  emit('player-added', newPlayer);
  closePlayerModal();
};

const addPlayer = () => {
  if (players.value.length >= playerColors.length) { alert(`Maximum ${playerColors.length} joueurs autorisés`); return; }
  const newPlayer: Player = { id: playerIdCounter++, name: `Joueur ${players.value.length + 1}`, color: playerColors[players.value.length], gender: 'male' };
  players.value.push(newPlayer);
};

const removePlayer = (index: number) => {
  const playerToRemove = players.value[index];
  const playerId = playerToRemove.id;
  players.value.splice(index, 1);
  // Notify parent that a player was removed
  emit('player-removed', playerId);
  players.value.forEach((player, idx) => (player.color = playerColors[idx]));
};

// No socket listeners here — parent handles socket events

</script>

<style scoped>
/* rely on parent/global styles */
</style>
