<template>
    <div class="card quizz-selector">
        <div class="quizz-selector-header">
            <h3> Quizz </h3>

            <div v-if="summaryQuizz == null">
                <p>No quizz selected</p>
                <button class="btn-base btn-primary">Select Quizz</button>
            </div>
            <div v-else>
                <p>Selected quizz: {{ summaryQuizz?.title }}</p>
                <p>Location: {{ summaryQuizz?.Location?.name }}</p>
                <p>Game Type: {{ summaryQuizz?.GameType?.name }}</p>
                <p>Estimated Time: {{ summaryQuizz?.EstimatedTime }} minutes</p>
                <button class="btn-base btn-secondary">Change Quizz</button>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">

import { ref, onMounted } from 'vue';

interface SummaryQuizz {
    title: string;
    Location: LocationQuizz;
    GameType: GameTypeQuizz;
    EstimatedTime: number;
}

interface GameTypeQuizz {
    id: number;
    name: string;
    imgPath: string;
}



interface LocationQuizz {
    id:number;
    name: string;
    imgPath: string;
}

const summaryQuizz = ref<SummaryQuizz | null>(null);

    onMounted(() => {
      console.log('Component is mounted');
    });





</script>


<style scoped>
</style>