/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // Paleta del Centro de Estudiantes
        cec: {
          primary: '#1d4ed8',
          secondary: '#0f172a',
          accent: '#facc15',
        },
      },
    },
  },
  plugins: [],
}
