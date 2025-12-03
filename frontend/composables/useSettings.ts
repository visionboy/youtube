import axios from 'axios'
import { ref } from 'vue'

export const useSettings = () => {
    const config = useRuntimeConfig()
    const apiBase = config.public.apiBase

    const loading = ref(false)
    const error = ref<string | null>(null)

    const getApiKeyStatus = async () => {
        loading.value = true
        error.value = null

        try {
            const response = await axios.get(`${apiBase}/api/settings/api-key`)
            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Failed to get API key status'
            throw err
        } finally {
            loading.value = false
        }
    }

    const saveApiKey = async (apiKey: string) => {
        loading.value = true
        error.value = null

        try {
            const response = await axios.post(`${apiBase}/api/settings/api-key`, { apiKey })
            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Failed to save API key'
            throw err
        } finally {
            loading.value = false
        }
    }

    const deleteApiKey = async () => {
        loading.value = true
        error.value = null

        try {
            const response = await axios.delete(`${apiBase}/api/settings/api-key`)
            return response.data
        } catch (err: any) {
            error.value = err.response?.data?.detail || 'Failed to delete API key'
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        loading,
        error,
        getApiKeyStatus,
        saveApiKey,
        deleteApiKey
    }
}
