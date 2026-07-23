import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import Icons from 'unplugin-icons/vite'
import IconsResolve from 'unplugin-icons/resolver'
import Components from 'unplugin-vue-components/vite'

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [IconsResolve()],
      dts: false,
    }),
    Icons({
      compiler: 'vue3',
      autoInstall: true,
    }),
  ],
  optimizeDeps: {
  include: [
    'feather-icons',
    'highlight.js',
    'highlight.js/lib/core',
    'interactjs',
    'debug',
  ],
  force: true,
},
  server: {
    port: 8080,
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/app': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      '/socket.io': {
          target: 'http://127.0.0.1:9000',
          ws: true,
          changeOrigin: true,
        },
      },
    },
  build: {
    outDir: '../construction_management/public/frontend',
    emptyOutDir: true,
    target: 'es2015',
  },
})