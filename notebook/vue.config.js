const { defineConfig } = require('@vue/cli-service')
const path = require('path');

module.exports = defineConfig({
  // publicPath: "/dev_ui/",
  pages: {
    index: 'src/main.ts',
    // admin: 'src/admin.ts',
  },
  assetsDir: "static/",
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        "beaker-vue": path.resolve(__dirname, "./beaker-kernel-link/beaker-vue/src/")
      }
    }
  },
  devServer: {
    proxy: {
      '^/stats': {
        target: 'http://beaker:8888',
        changeOrigin: true,
      },
      '^/api': {
        target: 'http://beaker:8888',
        ws: true,
        changeOrigin: true,
      },
      '^/upload': {
        target: 'http://beaker:8888',
        changeOrigin: true,
      },
      '^/download': {
        target: 'http://beaker:8888',
        changeOrigin: true,
      },
      '^/contexts': {
        target: 'http://beaker:8888',
        changeOrigin: true,
      },
      '^/sources_api': {
        target: 'http://sources_api:8082',
        changeOrigin: true,
        pathRewrite: { '^/sources_api': ''},
      },
      '^/config': {
        target: 'http://beaker:8888',
        changeOrigin: true,
      },
    },
  }
})
