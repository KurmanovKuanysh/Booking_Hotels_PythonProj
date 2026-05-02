import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      fontFamily: {
        serif: ["'Playfair Display'", "Georgia", "serif"],
        sans: ["'DM Sans'", "sans-serif"],
        mono: ["'DM Mono'", "monospace"],
      },
      colors: {
        ink: {
          DEFAULT: "#0D0D0D",
          soft: "#1A1A2E",
        },
        cream: {
          DEFAULT: "#F5F0E8",
          dark: "#E8E0D0",
        },
        gold: {
          DEFAULT: "#C9A84C",
          light: "#E5C97A",
          dark: "#A07830",
        },
        stone: {
          50: "#FAFAF8",
          100: "#F0EDE8",
          200: "#DDD8CF",
          300: "#C4BDB0",
          400: "#A89E92",
          500: "#8B8074",
          600: "#6E6358",
          700: "#52483E",
          800: "#362E26",
          900: "#1A1410",
        },
      },
      backgroundImage: {
        "hero-pattern": "radial-gradient(ellipse at 20% 50%, rgba(201,168,76,0.15) 0%, transparent 60%), radial-gradient(ellipse at 80% 20%, rgba(201,168,76,0.08) 0%, transparent 50%)",
      },
      animation: {
        "fade-up": "fadeUp 0.6s ease forwards",
        "fade-in": "fadeIn 0.4s ease forwards",
        "slide-in": "slideIn 0.5s ease forwards",
      },
      keyframes: {
        fadeUp: {
          from: { opacity: "0", transform: "translateY(20px)" },
          to: { opacity: "1", transform: "translateY(0)" },
        },
        fadeIn: {
          from: { opacity: "0" },
          to: { opacity: "1" },
        },
        slideIn: {
          from: { opacity: "0", transform: "translateX(-20px)" },
          to: { opacity: "1", transform: "translateX(0)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
