<template>
  <div class="container mx-auto px-4 py-8 max-w-4xl">
    <!-- API Key Status -->
    <div class="card p-6 mb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold text-vscode-textBright">API Key Status</h2>
        <div 
          class="px-3 py-1 rounded text-sm font-medium"
          :class="apiKeyStatus.configured ? 'bg-green-600 text-white' : 'bg-vscode-orange text-white'"
        >
          {{ apiKeyStatus.configured ? 'Configured' : 'Not Configured' }}
        </div>
      </div>
      
      <div v-if="apiKeyStatus.configured && apiKeyStatus.maskedKey" class="text-sm text-vscode-text">
        Current key: <code class="bg-vscode-bg px-2 py-1 rounded">{{ apiKeyStatus.maskedKey }}</code>
      </div>
    </div>
    
    <!-- API Key Form -->
    <div class="card p-6 mb-6">
      <h2 class="text-xl font-semibold text-vscode-textBright mb-4">
        {{ apiKeyStatus.configured ? 'Update' : 'Configure' }} API Key
      </h2>
      
      <form @submit.prevent="handleSaveApiKey">
        <div class="mb-4">
          <label for="apiKey" class="block text-sm font-medium text-vscode-text mb-2">
            YouTube Data API v3 Key
          </label>
          <input
            id="apiKey"
            v-model="apiKey"
            type="text"
            placeholder="Enter your API key"
            class="input"
            required
          />
        </div>
        
        <div class="flex gap-3">
          <button 
            type="submit" 
            class="btn btn-primary"
            :disabled="settingsLoading"
          >
            <span v-if="settingsLoading">Saving...</span>
            <span v-else>Save API Key</span>
          </button>
          
          <button 
            v-if="apiKeyStatus.configured"
            type="button"
            @click="handleDeleteApiKey"
            class="btn btn-danger"
            :disabled="settingsLoading"
          >
            Delete Key
          </button>
        </div>
      </form>
      
      <!-- Success/Error Messages -->
      <div v-if="successMessage" class="mt-4 p-3 bg-green-600/20 border border-green-600 rounded text-green-400">
        {{ successMessage }}
      </div>
      <div v-if="settingsError" class="mt-4 p-3 bg-red-600/20 border border-red-600 rounded text-red-400">
        {{ settingsError }}
      </div>
    </div>
    
    <!-- Instructions -->
    <div class="card p-6">
      <h2 class="text-xl font-semibold text-vscode-textBright mb-4">How to Get an API Key</h2>
      
      <ol class="space-y-3 text-vscode-text">
        <li class="flex gap-3">
          <span class="flex-shrink-0 w-6 h-6 rounded-full bg-vscode-accent text-white flex items-center justify-center text-sm font-semibold">1</span>
          <div>
            <p>Go to the <a href="https://console.cloud.google.com/" target="_blank" class="text-vscode-accent hover:underline">Google Cloud Console</a></p>
          </div>
        </li>
        
        <li class="flex gap-3">
          <span class="flex-shrink-0 w-6 h-6 rounded-full bg-vscode-accent text-white flex items-center justify-center text-sm font-semibold">2</span>
          <div>
            <p>Create a new project or select an existing one</p>
          </div>
        </li>
        
        <li class="flex gap-3">
          <span class="flex-shrink-0 w-6 h-6 rounded-full bg-vscode-accent text-white flex items-center justify-center text-sm font-semibold">3</span>
          <div>
            <p>Enable the <strong class="text-vscode-textBright">YouTube Data API v3</strong></p>
          </div>
        </li>
        
        <li class="flex gap-3">
          <span class="flex-shrink-0 w-6 h-6 rounded-full bg-vscode-accent text-white flex items-center justify-center text-sm font-semibold">4</span>
          <div>
            <p>Go to <strong class="text-vscode-textBright">Credentials</strong> and create an API key</p>
          </div>
        </li>
        
        <li class="flex gap-3">
          <span class="flex-shrink-0 w-6 h-6 rounded-full bg-vscode-accent text-white flex items-center justify-center text-sm font-semibold">5</span>
          <div>
            <p>Copy the API key and paste it above</p>
          </div>
        </li>
      </ol>
      
      <div class="mt-6 p-4 bg-vscode-bg rounded border border-vscode-border">
        <p class="text-sm text-vscode-textDim">
          <strong class="text-vscode-orange">Note:</strong> The free tier has a quota limit of 10,000 units per day. 
          Each search request costs approximately 100 units.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const { getApiKeyStatus, saveApiKey, deleteApiKey, loading: settingsLoading, error: settingsError } = useSettings()

const apiKey = ref('')
const apiKeyStatus = ref({ configured: false, maskedKey: null })
const successMessage = ref('')

onMounted(async () => {
  await loadApiKeyStatus()
})

const loadApiKeyStatus = async () => {
  try {
    apiKeyStatus.value = await getApiKeyStatus()
  } catch (err) {
    console.error('Failed to load API key status:', err)
  }
}

const handleSaveApiKey = async () => {
  successMessage.value = ''
  
  try {
    await saveApiKey(apiKey.value)
    successMessage.value = 'API key saved successfully!'
    apiKey.value = ''
    await loadApiKeyStatus()
    
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err) {
    console.error('Failed to save API key:', err)
  }
}

const handleDeleteApiKey = async () => {
  if (!confirm('Are you sure you want to delete the API key?')) return
  
  successMessage.value = ''
  
  try {
    await deleteApiKey()
    successMessage.value = 'API key deleted successfully!'
    await loadApiKeyStatus()
    
    setTimeout(() => {
      successMessage.value = ''
    }, 3000)
  } catch (err) {
    console.error('Failed to delete API key:', err)
  }
}
</script>
