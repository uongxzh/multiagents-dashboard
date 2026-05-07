/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        surface: {
          50: "#f8f9fc",
          100: "#f1f3f8",
          200: "#e2e6ef",
          300: "#c8cfdd",
          400: "#a3adc2",
          500: "#7a86a0",
          600: "#5f6b84",
          700: "#49536a",
          800: "#353d50",
          900: "#1e2332",
          950: "#121624",
        },
      },
    },
  },
  plugins: [],
};
