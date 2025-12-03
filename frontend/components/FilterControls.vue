<template>
  <div class="card p-4">
    <div class="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
      <!-- Left side: Filters -->
      <div class="flex flex-wrap gap-4">
        <!-- Order By -->
        <div class="flex items-center gap-2">
          <label class="text-sm text-vscode-textDim">Order:</label>
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
        
        <!-- Date Range (Radio) -->
        <div class="flex flex-col gap-1">
          <label class="text-sm text-vscode-textDim">Period:</label>
          <div class="flex flex-wrap gap-2">
            <label v-for="option in periodOptions" :key="option.value" class="flex items-center gap-1 cursor-pointer">
              <input 
                type="radio" 
                name="period"
                :value="option.value"
                :checked="filters.publishedAfter === option.value"
                @change="$emit('update:filters', { ...filters, publishedAfter: option.value })"
                class="accent-vscode-accent"
              >
              <span class="text-sm">{{ option.label }}</span>
            </label>
          </div>
        </div>

        <!-- Duration (Radio) -->
        <div class="flex flex-col gap-1">
          <label class="text-sm text-vscode-textDim">Length:</label>
          <div class="flex flex-wrap gap-2">
            <label v-for="option in durationOptions" :key="option.value" class="flex items-center gap-1 cursor-pointer">
              <input 
                type="radio" 
                name="duration"
                :value="option.value"
                :checked="filters.videoDuration === option.value"
                @change="$emit('update:filters', { ...filters, videoDuration: option.value })"
                class="accent-vscode-accent"
              >
              <span class="text-sm">{{ option.label }}</span>
            </label>
          </div>
        </div>

        <!-- New Filters Row -->
        <div class="flex flex-wrap gap-4 items-end w-full">
          <!-- Min Comments -->
          <div class="flex items-center gap-2">
            <label class="text-sm text-vscode-textDim">Min Comments:</label>
            <input 
              type="number"
              :value="filters.minComments"
              @input="$emit('update:filters', { ...filters, minComments: ($event.target as HTMLInputElement).value ? parseInt(($event.target as HTMLInputElement).value) : null })"
              class="input w-24"
              placeholder="0"
            >
          </div>

          <!-- Tag Filter -->
          <div class="flex items-center gap-2">
            <label class="text-sm text-vscode-textDim">Tag:</label>
            <input 
              type="text"
              :value="filters.tag"
              @input="$emit('update:filters', { ...filters, tag: ($event.target as HTMLInputElement).value })"
              class="input w-32"
              placeholder="e.g. vue"
            >
          </div>

          <!-- Ratio -->
          <div class="flex items-center gap-2">
            <label class="text-sm text-vscode-textDim">Ratio:</label>
            <select 
              :value="filters.minRatio || ''"
              @change="$emit('update:filters', { ...filters, minRatio: ($event.target as HTMLSelectElement).value ? parseFloat(($event.target as HTMLSelectElement).value) : null })"
              class="select"
            >
              <option value="">Any</option>
              <option :value="10">> 10% (High)</option>
              <option :value="50">> 50% (Very High)</option>
              <option :value="100">> 100% (Viral)</option>
              <option :value="500">> 500% (Mega)</option>
            </select>
          </div>
          
          <!-- Max Results -->
          <div class="flex items-center gap-2">
            <label class="text-sm text-vscode-textDim">Count:</label>
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

const periodOptions = [
  { label: '1 Month', value: '1m' },
  { label: '2 Months', value: '2m' },
  { label: '6 Months', value: '6m' },
  { label: '1 Year', value: '1y' },
  { label: 'All', value: 'all' }
]

const durationOptions = [
  { label: 'Short', value: 'short' },
  { label: 'Long', value: 'long' },
  { label: 'Any', value: 'any' }
]
</script>
