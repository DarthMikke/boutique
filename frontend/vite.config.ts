import { defineConfig } from 'vite'

// https://vitejs.dev/config/
export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        scripts: 'src/main.ts',
        style: 'src/style.scss',
      },
      output: {
        dir: "../wsgi/app/static/assets",
        assetFileNames: "[name].[ext]",
        entryFileNames: "[name].js",
      }
    }
  }
})
