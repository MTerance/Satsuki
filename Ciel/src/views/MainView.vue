<template>

<div v-if="!isReady">
    <p> Loading...</p>
    <router-view/>
</div>

</template>

<script lang="ts">
import { onMounted, onUnmounted, ref } from 'vue';
import clientService from '../services/clientService.js';

export default {
    setup() {
        return {
            isReady
        };
    }
};

const isReady = ref(false);


const handleConnection = () => {
    
};

setTimeout(() => {
    handleConnection();
    }, 1000
);

onMounted(() => {

});

onUnmounted(() => {

});

</script>