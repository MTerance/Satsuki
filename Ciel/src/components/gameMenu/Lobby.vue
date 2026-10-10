<template>
<PlayerSection  @player-added="onPlayerAdded" @player-removed="onPlayerRemoved"></PlayerSection>
<QuizzSelector></QuizzSelector>

<button active="Is">Start Game</button>

</template>

<script setup lang="ts">
import QuizzSelector from './quizzSection/quizzSelector.vue';
import PlayerSection from './playersSection/PlayerSection.vue';
import type { Player } from '@/models/player';

const onPlayerAdded = (player: Player): void => {

};

const onPlayerRemoved = (id: number): void => {

};


const IsGameCompleted = (): boolean => {


    // Implement the logic to check if the game is completed
    return false; // Placeholder return value   
}

</script>