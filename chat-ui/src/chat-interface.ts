import { createApp } from 'vue';
import PrimeVue from 'primevue/config';
import Tooltip from 'primevue/tooltip';
import ToastService from 'primevue/toastservice';
import FocusTrap from 'primevue/focustrap';

import BeakerThemePlugin from 'beaker-vue/src/plugins/theme';
import ChatInterface from './ChatInterface.vue';
import { vKeybindings } from 'beaker-vue/src/directives/keybindings';

import 'primeicons/primeicons.css';
import 'beaker-vue/src/index.scss';

import { PageConfig, URLExt } from '@jupyterlab/coreutils';

const baseUrl = PageConfig.getBaseUrl();

(async () => {

  let config;
  if (process.env.NODE_ENV === "development") {
    config = {
      baseUrl: baseUrl,
      appUrl: baseUrl,
      wsUrl: baseUrl.replace("http", "ws"),
      token: "89f73481102c46c0bc13b2998f9a4fce",
    }
  }
  else {
    const confUrl = URLExt.join(baseUrl, '/config')
    const configResponse = await fetch(confUrl);
    config = await configResponse.json();
  }

  const app = createApp(ChatInterface, {config});

  app.use(PrimeVue);
  app.use(ToastService);
  app.use(BeakerThemePlugin as any);
  app.directive('tooltip', Tooltip);
  app.directive('focustrap', FocusTrap);
  app.directive('keybindings', vKeybindings as any);
  app.mount('#app');
})();