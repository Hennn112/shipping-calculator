// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  // CSS Framework
  css: ["~/assets/css/main.css"],

  // Runtime config for API base URL
  runtimeConfig: {
    public: {
      apiBase: "https://shipping-calculator-production.up.railway.app/api",
    },
  },

  // Modules
  modules: ["@nuxtjs/tailwindcss"],

  // Server-side rendering configuration
  ssr: true,

  // Nitro configuration for API proxy (optional)
  nitro: {
    devProxy: {
      "/api": {
        target: "https://shipping-calculator-production.up.railway.app/api",
        changeOrigin: true,
        pathRewrite: { "^/api": "" },
      },
    },
  },

  // App configuration
  app: {
    head: {
      title: "International Freight Calculator",
      meta: [
        { charset: "utf-8" },
        { name: "viewport", content: "width=device-width, initial-scale=1" },
        {
          name: "description",
          content: "Calculate international shipping costs to Indonesia",
        },
      ],
    },
  },
});