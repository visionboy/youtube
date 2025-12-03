<template>
  <div class="overflow-x-auto">
    <div class="flex justify-end mb-4">
      <button 
        @click="exportToExcel" 
        class="btn btn-secondary flex items-center gap-2"
        :disabled="!videos.length"
      >
        <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M3 17a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm3.293-7.707a1 1 0 011.414 0L9 10.586V3a1 1 0 112 0v7.586l1.293-1.293a1 1 0 111.414 1.414l-3 3a1 1 0 01-1.414 0l-3-3a1 1 0 010-1.414z" clip-rule="evenodd"/>
        </svg>
        Export to Excel
      </button>
    </div>

    <table class="w-full text-left border-collapse">
      <thead>
        <tr class="border-b border-vscode-border text-vscode-textDim text-sm">
          <th class="p-3 font-medium">Video</th>
          <th class="p-3 font-medium">Channel</th>
          <th class="p-3 font-medium cursor-pointer hover:text-vscode-textBright" @click="$emit('sort', 'date')">Published</th>
          <th class="p-3 font-medium cursor-pointer hover:text-vscode-textBright" @click="$emit('sort', 'views')">Views</th>
          <th class="p-3 font-medium cursor-pointer hover:text-vscode-textBright" @click="$emit('sort', 'likes')">Likes</th>
          <th class="p-3 font-medium">Comments</th>
          <th class="p-3 font-medium">Subs</th>
          <th class="p-3 font-medium">Ratio</th>
          <th class="p-3 font-medium">Tags</th>
          <th class="p-3 font-medium">Description</th>
          <th class="p-3 font-medium">Action</th>
        </tr>
      </thead>
      <tbody class="text-vscode-text text-sm">
        <tr 
          v-for="video in videos" 
          :key="video.id"
          class="border-b border-vscode-border hover:bg-vscode-itemHover transition-colors group"
        >
          <td class="p-3">
            <div class="flex items-center gap-3">
              <img 
                :src="video.thumbnails.default.url" 
                class="w-24 h-14 object-cover rounded"
                :alt="video.title"
              />
              <span class="font-medium line-clamp-2 max-w-xs group-hover:text-vscode-accent" :title="video.title">{{ video.title }}</span>
            </div>
          </td>
          <td class="p-3 text-vscode-textDim">{{ video.channelTitle }}</td>
          <td class="p-3 text-vscode-textDim">{{ formatDate(video.publishedAt) }}</td>
          <td class="p-3">{{ formatNumber(video.statistics.viewCount) }}</td>
          <td class="p-3">{{ formatNumber(video.statistics.likeCount) }}</td>
          <td class="p-3">{{ formatNumber(video.statistics.commentCount) }}</td>
          <td class="p-3">{{ formatNumber(video.statistics.subscriberCount) }}</td>
          <td class="p-3">
            <span :class="getRatioColor(video.statistics.viewSubscriberRatio)">
              {{ video.statistics.viewSubscriberRatio }}%
            </span>
          </td>
          <td class="p-3">
            <div class="flex flex-wrap gap-1 max-w-[150px]">
              <span 
                v-for="tag in (video.tags || []).slice(0, 2)" 
                :key="tag"
                class="px-1.5 py-0.5 bg-vscode-badge text-[10px] rounded-full truncate max-w-full"
                :title="tag"
              >
                #{{ tag }}
              </span>
            </div>
          </td>
          <td class="p-3">
            <p class="text-xs text-vscode-textDim line-clamp-2 max-w-xs" :title="video.description">
              {{ video.description }}
            </p>
          </td>
          <td class="p-3">
            <button 
              @click="$emit('play', video)"
              class="p-1 hover:bg-vscode-accent hover:text-white rounded transition-colors"
              title="Play Video"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clip-rule="evenodd"/>
              </svg>
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import * as XLSX from 'xlsx'

const props = defineProps<{
  videos: any[]
}>()

defineEmits<{
  play: [video: any]
  sort: [field: string]
}>()

const formatNumber = (num: number) => {
  return new Intl.NumberFormat('en-US').format(num)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString()
}

const getRatioColor = (ratio: number) => {
  if (ratio >= 500) return 'text-purple-400'
  if (ratio >= 100) return 'text-red-400'
  if (ratio >= 50) return 'text-orange-400'
  if (ratio >= 10) return 'text-green-400'
  return 'text-vscode-textDim'
}

const exportToExcel = () => {
  const data = props.videos.map(v => ({
    Title: v.title,
    Description: v.description,
    Channel: v.channelTitle,
    Published: new Date(v.publishedAt).toLocaleDateString(),
    Views: v.statistics.viewCount,
    Likes: v.statistics.likeCount,
    Comments: v.statistics.commentCount,
    Subscribers: v.statistics.subscriberCount || 0,
    'Ratio (%)': v.statistics.viewSubscriberRatio || 0,
    Tags: (v.tags || []).join(', '),
    URL: `https://www.youtube.com/watch?v=${v.id}`
  }))

  const ws = XLSX.utils.json_to_sheet(data)
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, "Videos")
  
  // Auto-width columns
  const maxWidth = 50
  const wscols = Object.keys(data[0]).map(key => ({ wch: Math.min(maxWidth, Math.max(key.length, ...data.map(row => (row[key] ? row[key].toString().length : 0)))) }))
  ws['!cols'] = wscols

  XLSX.writeFile(wb, `youtube_analytics_export_${new Date().toISOString().slice(0,10)}.xlsx`)
}
</script>
