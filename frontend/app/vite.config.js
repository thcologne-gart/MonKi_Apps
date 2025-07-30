// Plugins
import vue from '@vitejs/plugin-vue'
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'

// Utilities
import { defineConfig } from 'vite'
import { fileURLToPath, URL } from 'node:url'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue({ 
      template: { transformAssetUrls
    }
    }),
    // https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vite-plugin
    vuetify({
      autoImport: true,
      styles: {
        configFile: 'src/styles/settings.scss',
      },
    }),
  ],
  define: { 'process.env': {} },
  resolve: {
    alias: {
      find: './runtimeConfig',
      replacement: './runtimeConfig.browser',
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
    extensions: [
      '.js',
      '.json',
      '.jsx',
      '.mjs',
      '.ts',
      '.tsx',
      '.vue',
    ],
  },
  server: {
    port: 3000,
    proxy: {
      /*
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
      */
     '/awsBackend': {
        target: 'https://svmiv1rcci.execute-api.us-east-1.amazonaws.com',
        //target: 'http://backend1-env.eba-qq8c86yd.us-east-1.elasticbeanstalk.com',
        //target: 'https://d38a0dijjqq41h.cloudfront.net',
        //target: 'http://139.6.140.49:5000/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/awsBackend/, ''),
     }, 
      '/awsNlpEndpoints': {
        target: 'http://3.95.230.131:8003/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/awsNlpEndpoints/, ''),
      },
      '/nlpEndpoints': {
        // TH
        //target: 'http://139.6.140.196:8003/',
        // Zu Hause
        target: 'http://192.168.178.49:8003/',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/nlpEndpoints/, ''),
      },
      '/startNlp': {
        target: 'http://localhost:8003',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/startNlp/, ''),
      }
    }
  },
})
