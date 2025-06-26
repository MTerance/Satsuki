<template>
  <div class="database-demo p-6 max-w-4xl mx-auto">
    <h2 class="text-3xl font-bold mb-6 text-center">SQLite Database Demo</h2>
    
    <!-- Add User Form -->
    <div class="card bg-base-100 shadow-xl mb-6">
      <div class="card-body">
        <h3 class="card-title">Add New User</h3>
        <form @submit.prevent="addUser" class="space-y-4">
          <div class="form-control">
            <label class="label">
              <span class="label-text">Name</span>
            </label>
            <input 
              v-model="newUser.name" 
              type="text" 
              placeholder="Enter name" 
              class="input input-bordered w-full" 
              required 
            />
          </div>
          <div class="form-control">
            <label class="label">
              <span class="label-text">Email</span>
            </label>
            <input 
              v-model="newUser.email" 
              type="email" 
              placeholder="Enter email" 
              class="input input-bordered w-full" 
              required 
            />
          </div>
          <div class="form-control">
            <button type="submit" class="btn btn-primary" :disabled="loading">
              <span v-if="loading" class="loading loading-spinner"></span>
              {{ loading ? 'Adding...' : 'Add User' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Users List -->
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <div class="flex justify-between items-center mb-4">
          <h3 class="card-title">Users List</h3>
          <button @click="fetchUsers" class="btn btn-outline btn-sm">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Refresh
          </button>
        </div>
        
        <div v-if="users.length === 0" class="text-center py-8 text-gray-500">
          No users found. Add some users to get started!
        </div>
        
        <div v-else class="overflow-x-auto">
          <table class="table table-zebra">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id">
                <td>{{ user.id }}</td>
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ formatDate(user.created_at) }}</td>
                <td>
                  <button 
                    @click="deleteUser(user.id)" 
                    class="btn btn-error btn-sm"
                    :disabled="loading"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Status Messages -->
    <div v-if="message" class="alert mt-4" :class="messageType === 'error' ? 'alert-error' : 'alert-success'">
      <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" v-if="messageType === 'success'" />
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" v-else />
      </svg>
      <span>{{ message }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

// Declare global database API for TypeScript
declare global {
  interface Window {
    database: {
      addUser: (userData: { name: string; email: string }) => Promise<any>
      getUsers: () => Promise<any[]>
      deleteUser: (userId: number) => Promise<any>
    }
  }
}

const users = ref<any[]>([])
const loading = ref(false)
const message = ref('')
const messageType = ref<'success' | 'error'>('success')

const newUser = ref({
  name: '',
  email: ''
})

const showMessage = (msg: string, type: 'success' | 'error' = 'success') => {
  message.value = msg
  messageType.value = type
  setTimeout(() => {
    message.value = ''
  }, 5000)
}

const fetchUsers = async () => {
  try {
    loading.value = true
    users.value = await window.database.getUsers()
  } catch (error) {
    console.error('Error fetching users:', error)
    showMessage('Error fetching users', 'error')
  } finally {
    loading.value = false
  }
}

const addUser = async () => {
  if (!newUser.value.name || !newUser.value.email) {
    showMessage('Please fill in all fields', 'error')
    return
  }

  try {
    loading.value = true
    await window.database.addUser({
      name: newUser.value.name,
      email: newUser.value.email
    })
    
    newUser.value.name = ''
    newUser.value.email = ''
    
    showMessage('User added successfully!', 'success')
    await fetchUsers()
  } catch (error) {
    console.error('Error adding user:', error)
    showMessage('Error adding user. Email might already exist.', 'error')
  } finally {
    loading.value = false
  }
}

const deleteUser = async (userId: number) => {
  if (!confirm('Are you sure you want to delete this user?')) {
    return
  }

  try {
    loading.value = true
    await window.database.deleteUser(userId)
    showMessage('User deleted successfully!', 'success')
    await fetchUsers()
  } catch (error) {
    console.error('Error deleting user:', error)
    showMessage('Error deleting user', 'error')
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleString()
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.database-demo {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding-top: 2rem;
}
</style>
