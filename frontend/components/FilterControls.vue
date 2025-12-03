<template>
  <div class="card p-4">
    <div class="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
      <!-- Left side: Order and Max Results -->
      <div class="flex flex-wrap gap-4">
        <!-- Order By -->
        <div class="flex items-center gap-2">
          <label class="text-sm text-vscode-textDim">Order by:</label>
          <select 
            :value="filters.order"
            @change="$emit('update:filters', { ...filters, order: ($event.target as HTMLSelectElement).value })"
            class="select"
          >
            <option value="relevance">Relevance</option>
            <option value="date">Date</option>
            <option value="viewCount">View Count</option>
            <option value="rating">Rating</option>
          </select>
        </div>
        
        <!-- Max Results -->
        <div class="flex items-center gap-2">
          <label class="text-sm text-vscode-textDim">Results:</label>
          <select 
            :value="filters.maxResults"
            @change="$emit('update:filters', { ...filters, maxResults: parseInt(($event.target as HTMLSelectElement).value) })"
            class="select"
          >
            <option :value="10">10</option>
            <option :value="25">25</option>
            <option :value="50">50</option>
          </select>
        </div>
      </div>
      
      <!-- Right side: Sort Controls -->
      <div class="flex items-center gap-2">
        <span class="text-sm text-vscode-textDim">Sort:</span>
        <div class="flex gap-2">
          <button
            @click="$emit('sort', 'views')"
            class="btn btn-secondary text-sm"
            :class="{ 'bg-vscode-accent text-white': sortBy === 'views' }"
          >
            Views
          </button>
          <button
            @click="$emit('sort', 'likes')"
            class="btn btn-secondary text-sm"
            :class="{ 'bg-vscode-accent text-white': sortBy === 'likes' }"
          >
            Likes
          </button>
          <button
            @click="$emit('sort', 'date')"
            class="btn btn-secondary text-sm"
            :class="{ 'bg-vscode-accent text-white': sortBy === 'date' }"
          >
            Date
          </button>
          <button
            @click="$emit('toggleDirection')"
            class="btn btn-secondary text-sm"
            title="Toggle sort direction"
          >
            <svg 
              class="w-4 h-4 transition-transform"
              :class="{ 'rotate-180': sortDirection === 'asc' }"
              fill="currentColor" 
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  filters: any
  sortBy: string
  sortDirection: 'asc' | 'desc'
}>()

defineEmits<{
  'update:filters': [filters: any]
  sort: [field: string]
  toggleDirection: []
}>()
</script>
