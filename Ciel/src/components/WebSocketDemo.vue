<template>
  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">WebSocket Client Demo</h2>
      
      <!-- Connection Status -->
      <div class="alert" :class="connectionStatus.connected ? 'alert-success' : 'alert-warning'">
        <div>
          <span>Status: {{ connectionStatus.connected ? 'Connected' : 'Disconnected' }}</span>
          <span v-if="connectionStatus.url" class="ml-2 text-sm opacity-70">
            ({{ connectionStatus.url }})
          </span>
        </div>
      </div>

      <!-- Connection Form -->
      <div class="form-control w-full">
        <label class="label">
          <span class="label-text">WebSocket URL</span>
        </label>
        <div class="join">
          <input 
            v-model="wsUrl" 
            type="text" 
            placeholder="ws://localhost:8080 or wss://echo.websocket.org"
            class="input input-bordered join-item flex-1"
            :disabled="connectionStatus.connected"
          />
          <button 
            @click="connectionStatus.connected ? disconnect() : connect()" 
            class="btn join-item"
            :class="connectionStatus.connected ? 'btn-error' : 'btn-primary'"
          >
            {{ connectionStatus.connected ? 'Disconnect' : 'Connect' }}
          </button>
        </div>
      </div>

      <!-- Message Form -->
      <div class="form-control w-full" v-if="connectionStatus.connected">
        <label class="label">
          <span class="label-text">Send Message</span>
        </label>
        <div class="join">
          <input 
            v-model="messageToSend" 
            type="text" 
            placeholder="Enter message to send"
            class="input input-bordered join-item flex-1"
            @keyup.enter="sendMessage"
          />
          <button @click="sendMessage" class="btn btn-primary join-item">
            Send
          </button>
        </div>
      </div>

      <!-- Messages Log -->
      <div class="form-control w-full">
        <label class="label">
          <span class="label-text">Messages Log</span>
          <button @click="clearMessages" class="btn btn-sm btn-ghost">Clear</button>
        </label>
        <div class="mockup-code max-h-64 overflow-y-auto">
          <div v-if="messages.length === 0" class="px-4 py-2 text-gray-500">
            No messages yet...
          </div>
          <div v-for="(message, index) in messages" :key="index" class="px-4 py-1">
            <span class="text-success">[{{ message.timestamp }}]</span>
            <span :class="message.type === 'sent' ? 'text-info' : 'text-warning'">
              {{ message.type === 'sent' ? '→' : '←' }}
            </span>
            <span class="ml-2">{{ message.content }}</span>
          </div>
        </div>
      </div>

      <!-- Error Display -->
      <div v-if="error" class="alert alert-error">
        <div>
          <span>Error: {{ error }}</span>
          <button @click="error = ''" class="btn btn-sm btn-ghost ml-2">×</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

// Reactive state
const wsUrl = ref('wss://echo.websocket.org')
const messageToSend = ref('')
const messages = ref<Array<{
  type: 'sent' | 'received',
  content: string,
  timestamp: string
}>>([])
const connectionStatus = ref({
  connected: false,
  url: null as string | null
})
const error = ref('')

// Helper function to format timestamp
const formatTimestamp = () => {
  return new Date().toLocaleTimeString()
}

// Add message to log
const addMessage = (type: 'sent' | 'received', content: string) => {
  messages.value.push({
    type,
    content,
    timestamp: formatTimestamp()
  })
}

// Connect to WebSocket
const connect = async () => {
  if (!wsUrl.value) {
    error.value = 'Please enter a WebSocket URL'
    return
  }

  try {
    const result = await (window as any).websocket.connect(wsUrl.value)
    if (!result.success) {
      error.value = result.message
    }
  } catch (err) {
    error.value = `Connection failed: ${err}`
  }
}

// Disconnect from WebSocket
const disconnect = async () => {
  try {
    const result = await (window as any).websocket.disconnect()
    if (!result.success) {
      error.value = result.message
    }
  } catch (err) {
    error.value = `Disconnect failed: ${err}`
  }
}

// Send message
const sendMessage = async () => {
  if (!messageToSend.value.trim()) {
    return
  }

  try {
    const result = await (window as any).websocket.send(messageToSend.value)
    if (result.success) {
      addMessage('sent', messageToSend.value)
      messageToSend.value = ''
    } else {
      error.value = result.message
    }
  } catch (err) {
    error.value = `Send failed: ${err}`
  }
}

// Clear messages
const clearMessages = () => {
  messages.value = []
}

// Check initial status
const checkStatus = async () => {
  try {
    const status = await (window as any).websocket.getStatus()
    connectionStatus.value = status
  } catch (err) {
    console.error('Failed to get WebSocket status:', err)
  }
}

// Set up event listeners
onMounted(() => {
  checkStatus()

  // Listen for WebSocket messages
  ;(window as any).websocket.onMessage((data: string) => {
    addMessage('received', data)
  })

  // Listen for connection status changes
  ;(window as any).websocket.onStatus((status: any) => {
    connectionStatus.value = status
  })

  // Listen for errors
  ;(window as any).websocket.onError((errorMsg: string) => {
    error.value = errorMsg
  })
})

// Clean up event listeners
onUnmounted(() => {
  ;(window as any).websocket.removeAllListeners()
})
</script>
