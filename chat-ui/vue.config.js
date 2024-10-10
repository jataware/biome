const { defineConfig } = require('@vue/cli-service')
const path = require('path');

module.exports = defineConfig({
  pages: {
    index: 'src/chat-interface.ts',
    notebook: 'src/notebook-interface.ts'
  },
  assetsDir: "static/",
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      symlinks: false,
      alias: {
          vue: path.resolve("./node_modules/vue"),
      },
    },
  },
  devServer: {
    proxy: {
      '^/stats': {
        target: 'http://jupyter:8888',
        changeOrigin: true,
      },
      '^/api': {
        target: 'http://jupyter:8888',
        ws: true,
        changeOrigin: true,
      },
      '^/upload': {
        target: 'http://jupyter:8888',
        changeOrigin: true,
      },
      '^/download': {
        target: 'http://jupyter:8888',
        changeOrigin: true,
      },
      '^/contexts': {
        target: 'http://jupyter:8888',
        changeOrigin: true,
      },
      '^/config': {
        target: 'http://jupyter:8888',
        changeOrigin: true,
      },
      '^/summary': {
        target: 'http://jupyter:8888',
        changeOrigin: true,
      }
    },
  }
})
