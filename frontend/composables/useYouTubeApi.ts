import axios from 'axios'
import { ref } from 'vue'

export const useYouTubeApi = () => {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const loading = ref(false)
    const error = ref<string | null>(null)

    const searchVideos = async (query: string, filters: any = {}) => {
        loading.value = true
        error.value = null

        try {
            const params = {
                q: query,
                maxResults: filters.maxResults || 25,
                order: filters.order || 'relevance'
            }

            const response = await axios.get(`${apiBase}/api/videos/search`, { params })
            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Failed to search videos'
            throw err
        } finally {
            loading.value = false
        }
    }

    const getVideoDetails = async (videoId: string) => {
        loading.value = true
        error.value = null

        try {
            const response = await axios.get(`${apiBase}/api/videos/${videoId}`)
            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Failed to get video details'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        loading,
        error,
        searchVideos,
        getVideoDetails
    }
}
