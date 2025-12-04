export default defineNuxtConfig({
    compatibilityDate: '2025-12-03',
    devtools: { enabled: true },

    modules: ['@nuxtjs/tailwindcss'],

    css: ['~/assets/css/main.css'],

    runtimeConfig: {
        public: {
            apiBase: process.env.API_BASE_URL || 'http://localhost:8000'
        }
    },

    app: {
        head: {
            title: 'Social Video Analytics',
            meta: [
                { charset: 'utf-8' },
                { name: 'viewport', content: 'width=device-width, initial-scale=1' },
                { name: 'description', content: 'Social video search and analytics platform' }
            ],
            link: [
                { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
                { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
                { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap' }
            ]
        }
    }
})
