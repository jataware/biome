
const {
  contextBridge,
  ipcRenderer
} = require('electron');

let webview = null;

function inspectWebView() {
  console.log('inspecting web view in preload');

  console.log('preload: dom loaded, webview:', webview, webview.querySelector, webview.history);

  console.log('webview ready...');
  console.log('dom loaded, webview location:', webview.location);

  const content = webview.webContent;
  console.log('content', content);

  // TODO check if devtools open API and in "dev" mode only
  const webToolsResult = webview.openDevTools();

  console.log('keys', Object.keys(webview));
  console.log('contents', webview.webcontents);
}

document.addEventListener("DOMContentLoaded", function () {

  // TODO get as ref from js to ensure react rendered? (timing!)
  webview = document.getElementById('webview');
  console.log('preload: dom loaded, webview:', webview, webview.querySelector, webview.history);

  console.log('preload: checking if webview');
  if (webview) {
    console.log('preload: inside if webview');

    webview.addEventListener('dom-ready', () => {
      console.log('preload: webview dom ready');
      inspectWebView();
    });
  }

});

// MOCK
// const contextBridge = {
//   exposeInMainWorld: () => false
// };

contextBridge.exposeInMainWorld('eapi', {
  // TODO NOTE invoke vs send...
  // send/on for one way from renderer to electron
  // invoke/handle for 2-way between renderer and electron
  // TODO setTitle could use send instead of invoke
  setTitle: (title) => ipcRenderer.send('set-title', title),
  // NOTE invoke because openFile should return the value
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  // NOTE invoke because server responds back with pong and client receives that result
  ping: () => ipcRenderer.invoke('ping'),
  // navNext: () => ipcRenderer.invoke('next'),

  // overrides webview from above...? NOTE dangerous?
  // clientSetWebView: (webViewRerefence) => {
  //   console.log('client set web view called but ignoring for now', webViewRerefence);
  // webview = webViewRerefence;
  // },
  // getWebView: () => webview,
  // inspectWebView,
});

// ipcRenderer.send('setWebView', webViewRerefence)

// in preload-view on gptV-act, maybe we can use it from elsewhere?
// ipcRenderer.on('navigate-webview', (event, action, payload) => {
//     switch (action) {
//         case 'goBack':
//             if (window.history.length > 1) {
//                 window.history.back();
//             }
//             break;
//         case 'goForward':
//             if (window.history.length > 1) {
//                 window.history.forward();
//             }
//             break;
//         case 'reload':
//             window.location.reload();
//             break;
//         case 'loadURL':
//             window.location.href = payload;
//             break;
//     }
// });
