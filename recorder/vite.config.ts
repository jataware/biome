import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
// import {join} from 'node:path';

// const PACKAGE_ROOT = __dirname;

// https://vitejs.dev/config/
const config = defineConfig({
  plugins: [react()],
  base: './',
});

console.log('vite config:', JSON.stringify(config, null, 2));

export default config;
