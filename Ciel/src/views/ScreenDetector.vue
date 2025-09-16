<template>
  <div class="screen-detector">
    <h1>Screen Detector</h1>
    <div class="screen-info">
      <p><strong>Screen Width:</strong> {{ screenWidth }}px</p>
      <p><strong>Screen Height:</strong> {{ screenHeight }}px</p>
      <p><strong>Window Width:</strong> {{ windowWidth }}px</p>
      <p><strong>Window Height:</strong> {{ windowHeight }}px</p>
      <p><strong>Device Pixel Ratio:</strong> {{ devicePixelRatio }}</p>
      <p><strong>Screen Type:</strong> {{ screenType }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const screenWidth = ref(0)
const screenHeight = ref(0)
const windowWidth = ref(0)
const windowHeight = ref(0)
const devicePixelRatio = ref(0)
const screenType = ref('')

const updateScreenInfo = () => {
  screenWidth.value = screen.width
  screenHeight.value = screen.height
  windowWidth.value = window.innerWidth
  windowHeight.value = window.innerHeight
  devicePixelRatio.value = window.devicePixelRatio
  
  // Determine screen type based on width
  if (windowWidth.value < 640) {
    screenType.value = 'Mobile'
  } else if (windowWidth.value < 1024) {
    screenType.value = 'Tablet'
  } else {
    screenType.value = 'Desktop'
  }
}

onMounted(() => {
  updateScreenInfo()
  window.addEventListener('resize', updateScreenInfo)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateScreenInfo)
})
</script>

<style scoped>
.screen-detector {
  padding: 2rem;
  max-width: 600px;
  margin: 0 auto;
}

.screen-info {
  background: #f5f5f5;
  padding: 1.5rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.screen-info p {
  margin: 0.5rem 0;
  font-family: monospace;
}

h1 {
  color: #333;
  text-align: center;
  margin-bottom: 1rem;
}
</style>
