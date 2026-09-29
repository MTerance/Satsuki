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
    <div>
        <button @click="openQuizzSelectionModal" class="btn-base btn-secondary">
           <p v-if="summaryQuizz == null">Select Game</p>
           <p v-else>Change Game</p>
        </button>
    </div>

    <div v-if="isQuizzSelectionModalOpen" class="modal-overlay" @click="isQuizzSelectionModalOpen = false">
        <div class="modal-container" @click.stop>
            <div class="modal-header">
                <h3 class="modal-title">Select a Quizz</h3>
                <button class="modal-close" @click="isQuizzSelectionModalOpen = false">×</button>
            </div>

            <!-- Quizz selection content goes here -->
            <div class="quizz-selection-content">
                <!-- Example quizz options -->

                <p>Search for a quizz:</p>
                <textarea v-model="searchText"  @input="getAvailableGames" placeholder="Enter available quizzes name"></textarea>

                <div class="quizz-option" v-for="quizz in availableQuizzes" :key="quizz.id" @click="selectQuizz(quizz)">
                    <p>{{ quizz.title }}</p>
                </div>
            </div>
        </div>

    </div>

</template>

<script setup lang="ts">

import { ref, onMounted, computed } from 'vue';

interface SummaryQuizz {
    id: number;
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
const isQuizzSelectionModalOpen = ref(false);
const availableQuizzes = ref<SummaryQuizz[]>([]);
const searchText = ref('');

    onMounted(() => {
      console.log('Component is mounted');
    });

const openQuizzSelectionModal = () => {
    // Logic to open the quizz selection modal
    console.log('Open quizz selection modal');
    if (isQuizzSelectionModalOpen.value) {
        console.log('Quizz selection modal is already open');
        return;
    }
    isQuizzSelectionModalOpen.value = true;
};

const selectQuizz = (quizz: SummaryQuizz) => {
    // Logic to select a quizz
    console.log('Selected quizz:', quizz);
    summaryQuizz.value = quizz;
    closeQuizzSelectionModal();
};

const closeQuizzSelectionModal = () => {
    isQuizzSelectionModalOpen.value = false;
    searchText.value = '';

};

const getAvailableGames = async () => {
    try {
        if (searchText.value.length < 3) {
            availableQuizzes.value = [];
            return;
        }
        const response = await fetch('http://localhost:3000/api/quizzes/search?query=' + encodeURIComponent(searchText.value));
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        availableQuizzes.value = data;
    } catch (error) {
        console.error('Error fetching available quizzes:', error);
    }
};

const filteredQuizzes = computed(() => {
    if (!searchText.value) {
        return availableQuizzes.value;
    }
    return availableQuizzes.value.filter(quizz =>
        quizz.title.toLowerCase().includes(searchText.value.toLowerCase())
    );
});


</script>


<style scoped>
</style>