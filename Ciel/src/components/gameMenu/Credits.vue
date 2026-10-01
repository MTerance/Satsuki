<template>
    <div>
        <h1>Credits</h1>
        <p>Game developed by MTerance.</p>

        <button class="btn-base btn-secondary">Go to Title</button>
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


    const GoToTitle = async () => {
      //clientService.  // Logic to navigate to the Title page
      await clientService.sendOrder('GoToScene', 'Title');
    };

</script>