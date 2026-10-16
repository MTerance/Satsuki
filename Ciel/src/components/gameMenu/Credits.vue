<template>
    <div>
        <h1>Credits</h1>
  
        <button class="btn-base btn-secondary" @click="GoToTitle">Go to Title</button>
    </div>
</template>

<script setup lang="ts">

    import {onMounted, onUnmounted} from 'vue';
    import clientService, { OrderTarget } from '@/services/clientService';


    onMounted(() => {
      // Logic to execute when the component is mounted
    });

    onUnmounted(() => {
      // Logic to execute when the component is unmounted
    });


    const GoToTitle = async () => {
      //clientService.  // Logic to navigate to the Title page
      await clientService.sendOrder('GoToScene', 'Title',OrderTarget.SYSTEM);
    };

</script>