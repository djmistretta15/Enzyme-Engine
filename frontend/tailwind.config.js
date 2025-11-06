/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'eab-primary': '#284C3B',
        'eab-secondary': '#C79A4B',
        'eab-accent': '#C2C1BA',
      },
    },
  },
  plugins: [],
}
