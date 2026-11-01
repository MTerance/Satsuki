<template>
<PlayerSection @player-added="onPlayerAdded" @player-removed="onPlayerRemoved" @player-updated="onPlayerUpdated"></PlayerSection>
<QuizzSelector @quizz-selected="onQuizzSelected"> </QuizzSelector>

<button :disabled="!IsGameCompleted()">Start Game</button>

</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import QuizzSelector from './quizzSection/quizzSelector.vue';
import PlayerSection from './playersSection/PlayerSection.vue';
import type { Player } from '@/models/player';
import clientservice, { OrderTarget } from '@/services/clientService';
import type { SummaryQuizz } from '@/models/SummaryQuizz.ts';


 onMounted(() => {
     console.log('Lobby component mounted');
     console.log('Available quizzes:', QuizzSelector);
     console.log('Player section:', PlayerSection);
     clientservice.sendOrder('GetSceneState', null, OrderTarget.SYSTEM);
     
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
    /*
    if (QuizzSelector && PlayerSection) {
        return QuizzSelector.hasAChosenQuizz.value && PlayerSection.hasPlayers.value;
    }
        */
    return false;
}

</script>