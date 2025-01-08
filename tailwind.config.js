/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // Asegúrate de que Tailwind escanee tus archivos HTML
    "./static/js/**/*.js",    // Si tienes archivos JavaScript que usan Tailwind
  ],
  theme: {
    extend: {
      // Aquí puedes agregar tus personalizaciones de tema
      fontFamily: {
        sans: ['Poppins', 'sans-serif'], // Establece Poppins como la fuente sans por defecto
      },
      colors: {
        'color-primario': '#082f49', // Ejemplo de color personalizado
        'color-secundario': '#374151',
        'color-tres': '#a3a3a3',
        'color-base': '#e5e5e5',

        'blue': {
        '50': '#f1f5fd',
        '100': '#e0eaf9',
        '200': '#c7daf6',
        '300': '#a1c3ef',
        '400': '#74a2e6',
        '500': '#5382de',
        '600': '#3f67d1',
        '700': '#3554c0',
        '800': '#31459c',
        '900': '#2c3d7c',
        '950': '#252f5b',
    },
    
      },
      spacing: {
        '128': '32rem', // Ejemplo de espaciado personalizado
      },
    },
  },
  plugins: [],
}
