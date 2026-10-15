<template>
<PlayerSection  @player-added="onPlayerAdded" @player-removed="onPlayerRemoved" @player-updated="onPlayerUpdated"></PlayerSection>
<QuizzSelector></QuizzSelector>

<button active="Is">Start Game</button>

</template>

<script setup lang="ts">
import QuizzSelector from './quizzSection/quizzSelector.vue';
import PlayerSection from './playersSection/PlayerSection.vue';
import type { Player } from '@/models/player';
import clientservice, { OrderTarget } from '@/services/clientService';

const onPlayerAdded = async (player: Player): Promise<void> => {
   await clientservice.sendOrder('AddPlayer', player,OrderTarget.SCENE);
};

const onPlayerUpdated = async (player: Player): Promise<void> => {
    await clientservice.sendOrder('UpdatePlayer', player, OrderTarget.SCENE);
};

const onQuizzSelected = (quizzId: string): void => {


};
    
const onPlayerRemoved = async (id: string): Promise<void> => {
    await clientservice.sendOrder('RetirePlayer', id, OrderTarget.SCENE);
};

const IsGameCompleted = (): boolean => {


    // Implement the logic to check if the game is completed
    return false; // Placeholder return value   
}

</script>