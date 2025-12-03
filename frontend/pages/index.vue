<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Search Bar -->
    <div class="mb-6">
      <SearchBar 
        v-model="searchQuery"
        @search="handleSearch"
      />
    </div>
    
    <!-- Filter Controls -->
    <div class="mb-6">
      <FilterControls
        :filters="filters"
        :sort-by="sortBy"
        :sort-direction="sortDirection"
        @update:filters="filters = $event"
        @sort="handleSort"
        @toggle-direction="toggleSortDirection"
      />
    </div>
    
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center py-20">
      <div class="text-center">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-4 border-vscode-accent border-t-transparent"></div>
        <p class="mt-4 text-vscode-textDim">Loading videos...</p>
      </div>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="card p-6 text-center">
      <svg class="w-16 h-16 mx-auto text-red-500 mb-4" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
      </svg>
      <h3 class="text-xl font-semibold text-vscode-textBright mb-2">Error</h3>
      <p class="text-vscode-text mb-4">{{ error }}</p>
      <NuxtLink to="/settings" class="btn btn-primary">
        Configure API Key
      </NuxtLink>
    </div>
    
    <!-- Empty State -->
    <div v-else-if="!videos.length && searchQuery" class="card p-12 text-center">
      <svg class="w-20 h-20 mx-auto text-vscode-textDim mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/>
      </svg>
      <h3 class="text-xl font-semibold text-vscode-textBright mb-2">No videos found</h3>
      <p class="text-vscode-textDim">Try adjusting your search query or filters</p>
    </div>
    
    <!-- Welcome State -->
    <div v-else-if="!videos.length" class="card p-12 text-center">
      <svg class="w-20 h-20 mx-auto text-vscode-accent mb-4" fill="currentColor" viewBox="0 0 24 24">
        <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>
      </svg>
      <h3 class="text-xl font-semibold text-vscode-textBright mb-2">Welcome to YouTube Analytics</h3>
      <p class="text-vscode-textDim mb-4">Start by searching for videos above</p>
    </div>
    
    <!-- Video Grid -->
    <div v-else>
      <div class="mb-4 text-sm text-vscode-textDim">
        Found {{ videos.length }} videos
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <VideoCard
          v-for="video in sortedVideos"
          :key="video.id"
          :video="video"
          @click="openVideoPlayer"
        />
      </div>
    </div>
    
    <!-- Video Player Modal -->
    <VideoPlayer
      :video-id="selectedVideoId"
      :show="showPlayer"
      @close="closeVideoPlayer"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const { searchVideos, loading, error } = useYouTubeApi()

const searchQuery = ref('')
const filters = ref({
  order: 'relevance',
  maxResults: 25
})
const videos = ref<any[]>([])
const sortBy = ref('')
const sortDirection = ref<'asc' | 'desc'>('desc')
const selectedVideoId = ref('')
const showPlayer = ref(false)

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return
  
  try {
    const result = await searchVideos(searchQuery.value, filters.value)
    videos.value = result.videos
  } catch (err) {
    console.error('Search failed:', err)
  }
}

const handleSort = (field: string) => {
  if (sortBy.value === field) {
    toggleSortDirection()
  } else {
    sortBy.value = field
    sortDirection.value = 'desc'
  }
}

const toggleSortDirection = () => {
  sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
}

const sortedVideos = computed(() => {
  if (!sortBy.value) return videos.value
  
  const sorted = [...videos.value].sort((a, b) => {
    let aVal, bVal
    
    switch (sortBy.value) {
      case 'views':
        aVal = a.statistics.viewCount
        bVal = b.statistics.viewCount
        break
      case 'likes':
        aVal = a.statistics.likeCount
        bVal = b.statistics.likeCount
        break
      case 'date':
        aVal = new Date(a.publishedAt).getTime()
        bVal = new Date(b.publishedAt).getTime()
        break
      default:
        return 0
    }
    
    return sortDirection.value === 'asc' ? aVal - bVal : bVal - aVal
  })
  
  return sorted
})

const openVideoPlayer = (video: any) => {
  selectedVideoId.value = video.id
  showPlayer.value = true
}

const closeVideoPlayer = () => {
  showPlayer.value = false
  selectedVideoId.value = ''
}
</script>
