/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./components/**/*.{js,vue,ts}",
        "./layouts/**/*.vue",
        "./pages/**/*.vue",
        "./plugins/**/*.{js,ts}",
        "./app.vue",
    ],
    theme: {
        extend: {
            colors: {
                // VS Code color palette
                vscode: {
                    bg: '#1e1e1e',
                    sidebar: '#252526',
                    hover: '#2a2d2e',
                    border: '#3e3e42',
                    accent: '#007acc',
                    accentHover: '#1a8cd8',
                    orange: '#f9826c',
                    text: '#cccccc',
                    textBright: '#ffffff',
                    textDim: '#858585',
                    input: '#3c3c3c',
                    focusBorder: '#007acc',
                    button: '#0e639c',
                    buttonHover: '#1177bb',
                    link: '#3794ff',
                }
            },
            fontFamily: {
                sans: ['Inter', 'Segoe UI', 'system-ui', 'sans-serif'],
            },
            animation: {
                'fade-in': 'fadeIn 0.2s ease-in-out',
                'slide-up': 'slideUp 0.3s ease-out',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0' },
                    '100%': { opacity: '1' },
                },
                slideUp: {
                    '0%': { transform: 'translateY(10px)', opacity: '0' },
                    '100%': { transform: 'translateY(0)', opacity: '1' },
                },
            },
        },
    },
    plugins: [],
}
