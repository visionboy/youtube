<template>
  <Teleport to="body">
    <Transition name="modal">
      <div 
        v-if="show" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80"
        @click.self="$emit('close')"
      >
        <div class="relative w-full max-w-5xl bg-vscode-sidebar border border-vscode-border rounded-lg shadow-2xl animate-slide-up">
          <!-- Header -->
          <div class="flex items-center justify-between p-4 border-b border-vscode-border">
            <h3 class="text-lg font-semibold text-vscode-textBright">Video Player</h3>
            <button 
              @click="$emit('close')"
              class="p-2 hover:bg-vscode-hover rounded transition-colors"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>
          </div>
          
          <!-- Video Player -->
          <div class="relative" style="padding-bottom: 56.25%;">
            <iframe
              :src="`https://www.youtube.com/embed/${videoId}?autoplay=1`"
              class="absolute inset-0 w-full h-full"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
defineProps<{
  videoId: string
  show: boolean
}>()

defineEmits<{
  close: []
}>()
</script>

<style scoped>
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
