/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        fantasy: {
          dark: '#1a1423',
          card: '#2d2438',
          accent: '#c9a227', // Gold-ish
          text: '#e6e1e8',
          danger: '#8b2635',
          success: '#2b7a4b',
        }
      }
    },
  },
  plugins: [],
}

