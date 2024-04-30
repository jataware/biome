const {
  contextBridge,  // To add to website window properties
  ipcRenderer,    // Communicate back to electron
} = require('electron');

// This re-runs each time that win.loadURL/File is loaded with new path/URL

let webview = null;

/* Helper fns */
const onClick = (element, fn) => {
  element.addEventListener('click', fn);
};
const byId = (idStr) => document.getElementById(idStr);


const clickHandler = (buttonId, eventName, args)  => {
  const button = document.getElementById(buttonId);

  if(!button) {
    console.log(`Element not found for ${buttonId}. Skipping`);
    return;
  }
  onClick(button, () => {
    ipcRenderer.send(eventName, args);
  });
};

document.addEventListener("DOMContentLoaded", function () {

  webview = document.getElementById('local-webview');

  if (webview) {

    clickHandler('nav-editor-button', 'recorder:nav-editor');

    clickHandler('toggle-recording-button', 'recorder:toggle-recording');

    clickHandler('inspect-button', 'webview:devtools');

    clickHandler('mark-button', 'webview:mark-page');

    clickHandler('reload-button', 'recorder:navigate-webview', 'reload');

    clickHandler('back-button', 'recorder:navigate-webview', 'back');

    clickHandler('forward-button', 'recorder:navigate-webview', 'forward');

    const urlInput = document.getElementById('urlInput');
    urlInput.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
        console.log('send enter, value:', urlInput.value);
        ipcRenderer.send('recorder:navigate-webview', 'load', urlInput.value);
      }
    });

  }

});

// Gets exposed to index.html javascripts (<script tag>) or to loadURL() for React App
// Does not get exposed on webview preload-view.js
contextBridge.exposeInMainWorld('eapi', {
  // NOTE invoke vs send...
  // send/on for one way from renderer to electron
  // invoke/handle for 2-way between renderer and electron
  setTitle: (title) => ipcRenderer.send('set-title', title),
  // NOTE invoke because openFile should return the value
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  ping: () => ipcRenderer.invoke('debug:ping'),
  goToRecorder: () => ipcRenderer.send('editor:nav-recorder'),
  inspectWebView: () => ipcRenderer.send('webview:devtools')
});

contextBridge.exposeInMainWorld('eapi-versions', {
  node: () => process.versions.node,
  chrome: () => process.versions.chrome,
  electron: () => process.versions.electron
  // we can also expose variables, not just functions..
});
