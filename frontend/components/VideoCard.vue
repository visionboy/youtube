<template>
  <div 
    class="card card-hover cursor-pointer overflow-hidden group"
    @click="$emit('click', video)"
  >
    <!-- Thumbnail -->
    <div class="relative overflow-hidden">
      <img 
        :src="video.thumbnails.medium.url" 
        :alt="video.title"
        class="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
      />
      <div class="absolute bottom-2 right-2 bg-black/80 px-2 py-1 rounded text-xs text-white">
        {{ formatDate(video.publishedAt) }}
      </div>
    </div>
    
    <!-- Content -->
    <div class="p-4">
      <h3 class="text-vscode-textBright font-semibold mb-2 line-clamp-2 group-hover:text-vscode-accent transition-colors">
        {{ video.title }}
      </h3>
      
      <div class="mb-3">
        <p class="text-vscode-textDim text-sm transition-all duration-300" :class="{ 'line-clamp-2': !expanded, 'line-clamp-none': expanded }">
          {{ video.description }}
        </p>
        <button 
          v-if="video.description && video.description.length > 100"
          @click.stop="expanded = !expanded" 
          class="text-xs text-vscode-accent hover:underline mt-1"
        >
          {{ expanded ? 'Show less' : 'Show more' }}
        </button>
      </div>

      <!-- Tags -->
      <div v-if="video.tags && video.tags.length" class="flex flex-wrap gap-1 mb-3">
        <span 
          v-for="tag in video.tags.slice(0, 3)" 
          :key="tag"
          class="px-2 py-0.5 bg-vscode-badge text-vscode-text text-xs rounded-full"
        >
          #{{ tag }}
        </span>
      </div>
      
      <p class="text-sm text-vscode-textDim mb-3 font-medium">
        {{ video.channelTitle }}
      </p>
      
      <!-- Statistics -->
      <div class="flex items-center gap-4 text-sm text-vscode-text">
        <div class="flex items-center gap-1">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/>
            <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd"/>
          </svg>
          <span>{{ formatNumber(video.statistics.viewCount) }}</span>
        </div>
        
        <div class="flex items-center gap-1">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path d="M2 10.5a1.5 1.5 0 113 0v6a1.5 1.5 0 01-3 0v-6zM6 10.333v5.43a2 2 0 001.106 1.79l.05.025A4 4 0 008.943 18h5.416a2 2 0 001.962-1.608l1.2-6A2 2 0 0015.56 8H12V4a2 2 0 00-2-2 1 1 0 00-1 1v.667a4 4 0 01-.8 2.4L6.8 7.933a4 4 0 00-.8 2.4z"/>
          </svg>
          <span>{{ formatNumber(video.statistics.likeCount) }}</span>
        </div>
        
        <div class="flex items-center gap-1" title="Comments">
          <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z" clip-rule="evenodd"/>
          </svg>
          <span>{{ formatNumber(video.statistics.commentCount) }}</span>
        </div>
      </div>
      
      <!-- Advanced Stats -->
      <div v-if="video.statistics.subscriberCount" class="mt-2 pt-2 border-t border-vscode-border flex items-center justify-between text-xs text-vscode-textDim">
        <div title="Subscribers">
          <span class="font-medium text-vscode-text">{{ formatNumber(video.statistics.subscriberCount) }}</span> subs
        </div>
        <div title="Views/Subscriber Ratio" :class="getRatioColor(video.statistics.viewSubscriberRatio)">
          <span class="font-medium">{{ video.statistics.viewSubscriberRatio }}%</span> ratio
        </div>
      </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  video: any
}>()

defineEmits<{
  click: [video: any]
}>()

const expanded = ref(false)

const formatNumber = (num: number) => {
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1) + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'K'
  }
  return num.toString()
}

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 1) return 'Today'
  if (diffDays < 7) return `${diffDays}d ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)}w ago`
  if (diffDays < 365) return `${Math.floor(diffDays / 30)}mo ago`
  return `${Math.floor(diffDays / 365)}y ago`
}

const getRatioColor = (ratio: number) => {
  if (ratio >= 500) return 'text-purple-400'
  if (ratio >= 100) return 'text-red-400'
  if (ratio >= 50) return 'text-orange-400'
  if (ratio >= 10) return 'text-green-400'
  return 'text-vscode-textDim'
}
</script>
