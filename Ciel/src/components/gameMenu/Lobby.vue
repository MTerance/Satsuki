<template>
<PlayerSection ref="playerSection" @player-added="onPlayerAdded" @player-removed="onPlayerRemoved" @player-updated="onPlayerUpdated"></PlayerSection>
<QuizzSelector ref="quizzSelector" @quizz-selected="onQuizzSelected"> </QuizzSelector>

<button :disabled="!IsGameCompleted()">Start Game</button>

</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue';
import QuizzSelector from './quizzSection/quizzSelector.vue';
import PlayerSection from './playersSection/PlayerSection.vue';
import type { Player } from '@/models/player';
import clientservice, { OrderTarget } from '@/services/clientService';
import type { SummaryQuizz } from '@/models/SummaryQuizz.ts';

// Instances des composants enfants (defineExpose côté enfants)
const playerSection = ref<InstanceType<typeof PlayerSection> | null>(null);
const quizzSelector = ref<InstanceType<typeof QuizzSelector> | null>(null);

 onMounted(() => {
     console.log('Lobby component mounted');

    // L'état de jeu (réponse GetSceneState / GAME_STATE:) est routé par
    // clientService sous l'ordre 'GameStateUpdate' (cf. satsuki-tcp-client.cjs).
    clientservice.onOrder('GameStateUpdate', (data) => {
        console.log('GameStateUpdate reçu dans Lobby:', data);
        const sceneState = data?.state?.CurrentStateScene;
        if (sceneState?.Content) {
            if (sceneState.Content.Players) playerSection.value?.setPlayers(sceneState.Content.Players);
            if (sceneState.Content.Quizz) quizzSelector.value?.setSelectedQuizz(sceneState.Content.Quizz);
        }
    });

    // Redemande l'état courant de la scène ({} plutôt que null → JsonData '{}').
    clientservice.sendOrder('GetSceneState', {}, OrderTarget.SYSTEM);
     
 }); 


const onPlayerAdded = async (player: Player): Promise<void> => {
   await clientservice.sendOrder('AddPlayer', player,OrderTarget.SCENE);
};

const onPlayerUpdated = async (player: Player): Promise<void> => {
    await clientservice.sendOrder('UpdatePlayer', player, OrderTarget.SCENE);
};

const onQuizzSelected = (quizz: SummaryQuizz): void => {
    console.log('Selected quizz:', quizz);

};
    
const onPlayerRemoved = async (id: string): Promise<void> => {
    await clientservice.sendOrder('RetirePlayer', id, OrderTarget.SCENE);
};

const IsGameCompleted = (): boolean => {
    return !!(quizzSelector.value?.hasAChosenQuizz && playerSection.value?.hasPlayers);
}

</script>