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
    <div v-if="loading && !videos.length" class="flex items-center justify-center py-20">
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
    
    <!-- Results Container -->
    <div v-else>
      <!-- View Toggle & Results Count -->
      <div class="flex items-center justify-between mb-4">
        <div class="text-sm text-vscode-textDim">
          Found {{ totalResults }} videos
        </div>
        <div class="flex bg-vscode-itemHover rounded p-1">
          <button 
            @click="viewMode = 'grid'"
            class="p-2 rounded transition-colors"
            :class="{ 'bg-vscode-accent text-white': viewMode === 'grid', 'text-vscode-textDim hover:text-vscode-text': viewMode !== 'grid' }"
            title="Grid View"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
            </svg>
          </button>
          <button 
            @click="viewMode = 'table'"
            class="p-2 rounded transition-colors"
            :class="{ 'bg-vscode-accent text-white': viewMode === 'table', 'text-vscode-textDim hover:text-vscode-text': viewMode !== 'table' }"
            title="Table View"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Video Grid -->
      <div v-if="viewMode === 'grid'">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          <VideoCard
            v-for="video in sortedVideos"
            :key="video.id"
            :video="video"
            @click="openVideoPlayer"
          />
        </div>
      </div>

      <!-- Video Table -->
      <div v-else>
        <VideoTable 
          :videos="sortedVideos"
          @play="openVideoPlayer"
          @sort="handleSort"
        />
      </div>

      <!-- Load More -->
      <div v-if="nextPageToken" class="flex justify-center mt-8 pb-8">
        <button 
          @click="loadMore"
          :disabled="loading"
          class="px-6 py-2 bg-vscode-button hover:bg-vscode-buttonHover text-white rounded disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2 transition-colors"
        >
          <span v-if="loading" class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
          {{ loading ? 'Loading...' : 'Load More' }}
        </button>
      </div>
    </div> <!-- End Results Container -->
    
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
  maxResults: 10,
  publishedAfter: '1m',
  videoDuration: 'short',
  minRatio: null as number | null,
  minComments: null as number | null,
  tag: ''
})
const videos = ref<any[]>([])
const nextPageToken = ref<string | null>(null)
const totalResults = ref(0)
const viewMode = ref<'grid' | 'table'>('grid')
const sortBy = ref('')
const sortDirection = ref<'asc' | 'desc'>('desc')
const selectedVideoId = ref('')
const showPlayer = ref(false)

const handleSearch = async () => {
  if (!searchQuery.value.trim()) return
  
  // Reset state for new search
  videos.value = []
  nextPageToken.value = null
  
  try {
    const result = await searchVideos(searchQuery.value, filters.value)
    videos.value = result.videos
    nextPageToken.value = result.nextPageToken
    totalResults.value = result.total // Note: API might return total for page, not global
  } catch (err) {
    console.error('Search failed:', err)
  }
}

const loadMore = async () => {
  if (!nextPageToken.value) return
  
  try {
    const result = await searchVideos(searchQuery.value, {
      ...filters.value,
      pageToken: nextPageToken.value
    })
    videos.value = [...videos.value, ...result.videos]
    nextPageToken.value = result.nextPageToken
  } catch (err) {
    console.error('Load more failed:', err)
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
