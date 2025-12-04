<template>
  <div class="min-h-screen flex flex-col">
    <!-- Header / Activity Bar -->
    <header class="bg-vscode-sidebar border-b border-vscode-border">
      <div class="container mx-auto px-4">
        <div class="flex items-center justify-between h-14">
          <!-- Logo -->
          <NuxtLink to="/" class="flex items-center gap-2 text-vscode-textBright font-semibold text-lg hover:text-vscode-accent transition-colors">
            <svg class="w-6 h-6 text-vscode-accent" fill="currentColor" viewBox="0 0 24 24">
              <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
            </svg>
            Social Video Analytics
          </NuxtLink>
          
          <!-- Navigation -->
          <nav class="flex items-center gap-1">
            <NuxtLink 
              to="/" 
              class="activity-item"
              active-class="active"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"/>
              </svg>
              <span class="hidden md:inline">Videos</span>
            </NuxtLink>
            
            <NuxtLink 
              to="/settings" 
              class="activity-item"
              active-class="active"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M11.49 3.17c-.38-1.56-2.6-1.56-2.98 0a1.532 1.532 0 01-2.286.948c-1.372-.836-2.942.734-2.106 2.106.54.886.061 2.042-.947 2.287-1.561.379-1.561 2.6 0 2.978a1.532 1.532 0 01.947 2.287c-.836 1.372.734 2.942 2.106 2.106a1.532 1.532 0 012.287.947c.379 1.561 2.6 1.561 2.978 0a1.533 1.533 0 012.287-.947c1.372.836 2.942-.734 2.106-2.106a1.533 1.533 0 01.947-2.287c1.561-.379 1.561-2.6 0-2.978a1.532 1.532 0 01-.947-2.287c.836-1.372-.734-2.942-2.106-2.106a1.532 1.532 0 01-2.287-.947zM10 13a3 3 0 100-6 3 3 0 000 6z" clip-rule="evenodd"/>
              </svg>
              <span class="hidden md:inline">Settings</span>
            </NuxtLink>
            <button 
              v-if="route.path !== '/login'"
              @click="logout" 
              class="activity-item"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
              <span class="hidden md:inline">Logout</span>
            </button>
          </nav>
        </div>
      </div>
    </header>
    
    <!-- Main Content -->
    <main class="flex-1">
      <slot />
    </main>
    
    <!-- Status Bar -->
    <footer class="status-bar flex items-center justify-between">
      <div class="flex items-center gap-4">
        <span>Social Video Analytics v1.0</span>
      </div>
      <div>
        <span>Powered by YouTube Data API v3</span>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { logout } = useAuth()
</script>
