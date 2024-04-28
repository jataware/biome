const {
  contextBridge,  // To add to website window properties
  ipcRenderer,    // Communicate back to electron
} = require('electron');

// This re-runs each time
// win.loadURL/File is loaded with new path/URL

let webview = null;

/* Helper Fn to simplify code*/
const onClick = (element, fn) => {
  element.addEventListener('click', fn);
};
const byId = (idStr) => document.getElementById(idStr);

document.addEventListener("DOMContentLoaded", function () {

  webview = document.getElementById('local-webview');

  if (webview) {
    const navEditorButton = document.getElementById('nav-editor-button');
      onClick(navEditorButton, () => {
        ipcRenderer.send('recorder:nav-editor');
      });

    const inspectButton = document.getElementById('inspect-button');
      onClick(inspectButton, () => {
        ipcRenderer.send('webview:devtools');
      });

    const markPageButton = document.getElementById('mark-button');
    onClick(markPageButton, () => {
      ipcRenderer.send('recorder:mark-page');
    });

    const reloadButton = document.getElementById('reload-button');
    onClick(reloadButton, () => {
      ipcRenderer.send('recorder:navigate-webview', 'reload');
    });
  }

});

// Without context isolation..
// window.eapi = {
//   goToRecorder: () => ipcRenderer.send('editor:nav-recorder'),
//   setTitle: () => "TODO"
// };

// Gets exposed to index.html javascripts (<script tag>) or to loadURL() for React App
// Does not get exposed on webview preload-view.js
contextBridge.exposeInMainWorld('eapi', {
  // TODO NOTE invoke vs send...
  // send/on for one way from renderer to electron
  // invoke/handle for 2-way between renderer and electron
  // TODO setTitle could use send instead of invoke
  setTitle: (title) => ipcRenderer.send('set-title', title),
  // NOTE invoke because openFile should return the value
  openFile: () => ipcRenderer.invoke('dialog:openFile'),
  // NOTE invoke because server responds back with pong and client receives that result
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
