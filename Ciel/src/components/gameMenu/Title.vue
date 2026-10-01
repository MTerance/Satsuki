<template>
    <div>
        <h1>Title</h1>
        <button class="btn-base btn-secondary">Go to Lobby</button>
    </div>
</template>

<script setup lang="ts">
    import {onMounted, onUnmounted} from 'vue'; 
    import clientService from '@/services/clientService';


    onMounted(() => {
      // Logic to execute when the component is mounted
    });

    onUnmounted(() => {
      // Logic to execute when the component is unmounted
    });

    const GoToLobby = async () => {
        await clientService.sendOrder('GoToScene', 'Lobby');
    };

</script>