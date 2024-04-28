// const { ipcRenderer,
        // contextBridge
      // } = require('electron');

// NOTE File Unused for now
// will delete soon

// console.log('preload-local loaded...');

// const onClick = (element, fn) => {
//   element.addEventListener('click', fn);
// };

// document.addEventListener("DOMContentLoaded", function () {
//   // mini-browser setup

//   // const urlInput = document.getElementById('urlInput');
//   const webview = document.getElementById('local-webview');

//   if (webview) {

//     webview.addEventListener('dom-ready', () => {

//       // TODO check electron API on how to check if dev tools is openm
//       // TODO only open in "dev" mode, not prod
//       webview.openDevTools();

//       console.log(webview.getWebContentsId);
//       ipcRenderer.send('local-webview-ready', webview.getWebContentsId());
//     });

//     onClick(document.getElementById('nav-editor'), () => {
//       console.log('click nav editor');
//       ipcRenderer.send('nav-editor');
//     });

//   } else {
//     // editor + react app
//     console.log('no webview detected on this page, skipping');

//     // preload with contextIsolation disabled
//     window.eapi = {
//       setTitle: (title) => ipcRenderer.send('set-title', title),
//       goToRecorder: () => ipcRenderer.send('nav-recorder'),
//     };
//   }


// });

