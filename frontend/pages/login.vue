<template>
  <div class="min-h-screen flex items-center justify-center bg-vscode-bg text-vscode-text">
    <div class="w-full max-w-md p-8 bg-vscode-sidebar rounded-lg border border-vscode-border shadow-xl">
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-vscode-textBright">Welcome Back</h1>
        <p class="text-sm text-gray-400 mt-2">Sign in to continue to Social Video Analytics</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label class="block text-sm font-medium mb-2">Username</label>
          <input 
            v-model="username"
            type="text" 
            class="w-full px-4 py-2 bg-vscode-input border border-vscode-border rounded focus:outline-none focus:border-vscode-focusBorder text-vscode-text"
            placeholder="Enter your username"
            required
          />
        </div>

        <div>
          <label class="block text-sm font-medium mb-2">Password</label>
          <input 
            v-model="password"
            type="password" 
            class="w-full px-4 py-2 bg-vscode-input border border-vscode-border rounded focus:outline-none focus:border-vscode-focusBorder text-vscode-text"
            placeholder="Enter your password"
            required
          />
        </div>

        <div v-if="error" class="p-3 bg-red-900/50 border border-red-700 rounded text-red-200 text-sm">
          {{ error }}
        </div>

        <button 
          type="submit"
          :disabled="loading"
          class="w-full py-2 px-4 bg-vscode-button hover:bg-vscode-buttonHover text-white font-medium rounded transition-colors disabled:opacity-50"
        >
          {{ loading ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>
      
      <div class="mt-6 text-center text-sm text-gray-400">
        <p>Don't have an account? <a href="#" @click.prevent="handleRegister" class="text-vscode-link hover:underline">Register</a></p>
      </div>
    </div>
  </div>
</template>

<script setup>
const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const { login, register } = useAuth()

const handleLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    await login(username.value, password.value)
    navigateTo('/')
  } catch (e) {
    error.value = e.data?.detail || 'Invalid credentials'
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  loading.value = true
  error.value = ''
  try {
    await register(username.value, password.value)
    navigateTo('/')
  } catch (e) {
    error.value = e.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>
