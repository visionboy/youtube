export const useAuth = () => {
    const token = useCookie('auth_token')
    const user = useState('auth_user', () => null)
    const config = useRuntimeConfig()

    const login = async (username, password) => {
        try {
            const { data, error } = await useFetch(`${config.public.apiBase}/api/auth/login`, {
                method: 'POST',
                body: { username, password }
            })

            if (error.value) throw error.value

            token.value = data.value.access_token
            return true
        } catch (e) {
            console.error('Login failed', e)
            throw e
        }
    }

    const register = async (username, password) => {
        try {
            const { data, error } = await useFetch(`${config.public.apiBase}/api/auth/register`, {
                method: 'POST',
                body: { username, password }
            })

            if (error.value) throw error.value

            token.value = data.value.access_token
            return true
        } catch (e) {
            console.error('Registration failed', e)
            throw e
        }
    }

    const logout = () => {
        token.value = null
        user.value = null
        navigateTo('/login')
    }

    return {
        token,
        user,
        login,
        register,
        logout,
        isAuthenticated: computed(() => !!token.value)
    }
}
