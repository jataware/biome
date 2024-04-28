
const { app, BrowserWindow, ipcMain, dialog, webContents } = require('electron');
const path = require('node:path');


function handleSetTitle (event, title) {
  const webContents = event.sender;
  // can also use win from local `win` variable (let win; below)
  const win = BrowserWindow.fromWebContents(webContents);
  win.setTitle(title);
}

async function handleFileOpen () {
  const { canceled, filePaths } = await dialog.showOpenDialog();
  if (!canceled) {
    return filePaths[0];
  }
  return null;
}

let win;
function createWindow() {
   win = new BrowserWindow({
    titleBarStyle: 'hidden', // TODO does this work in all OS?
    autoHideMenuBar: true, // TODO test this
    title: 'Koro Web Recorder',
    width: 1400,
    height: 1000,
     // https://www.electronjs.org/docs/latest/api/browser-window#new-browserwindowoptions
    webPreferences: {
      // nodeIntegration: true, // NOTE only allowed with ctx iso
      // nodeIntegrationInSubFrames: false, // enable node in subframes/child wins
      // preload always has access to node APIs where node int is on/off
      preload: path.join(__dirname, 'preload-local.js'),
      zoomFactor: 1.0, // default
      javascript: true,
      webSecurity: true,// would setting to false allow embedding webview w/o preload
      // insec content force to true if webSecurity is false:
      allowRunningInsecureContent: false,
      images: true, // allow showing images
      // enable webview...
      imageAnimationPolicy: 'animate', // default; can disable GIFs animation etc
      textAreasAreResizable: true, // default; can disable
      webgl: true,
      plugins: false,
      experimentalFeatures: false,
      scrollBounce: false, // default; for macos
      defaultFontSize: 16, // default
      minimumFontSize: 1, // default=0
      webviewTag: true, // !important
      // The Electron API will only be available in the preload script and not the loaded page. This option should be used when loading potentially untrusted remote content to ensure the loaded content cannot tamper with the preload script and any Electron APIs being used:
      contextIsolation: false, // for getWebContentsId(); comm with preload-view
      // boolean (optional) - Whether to enable DevTools. If it is set to false, can not use BrowserWindow.webContents.openDevTools() to open DevTools. Default is true.
      devTools: true,
      safeDialogs: false, // default; disable consecutive dialogs from websites
      // if we enable safe dialogs and it triggers:
      safeDialogsMessage: 'More consecutive dialog creation prevented',
      disableDialogs: false, // default
      navigateOnDragDrop: false,
      spellcheck: false, // default=true
      // titleBarOverlay // see docs; TODO see if this works in linux/OSX
    },
  });

  win.loadFile('index.html');
  // All web page related events and operations will be done via webcontents:
  win.webContents.openDevTools();

  // Only works in linux/windows:
  // win.removeMenu(); // TODO check this out if menu is bothersome

  // Only on macos for traffic light close/min/max icons:
  // win.setWindowButtonVisibility(true); // could set to false try out
}

app.whenReady().then(() => {

  createWindow();

  let webview;

  ipcMain.on('set-title', handleSetTitle);
  // ipcMain.handle('ping', () => 'pong');

  ipcMain.on('local-webview-ready', function(event, webViewID) {
    console.log('electron received webview', event, webViewID);
    webview = webContents.fromId(webViewID);
  });

  ipcMain.on('dialog:openFile', handleFileOpen);

  ipcMain.on('webview:scroll-action', (event, payload) => {
    console.log("webview:scroll-action", event, payload);
  });

  ipcMain.on('webview:click-action', (event, payload) => {
    console.log("webview:click-action", event, payload);
  });

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) {
      console.log('browser windows == 0, recreating');
      createWindow();
      // createLocalWindow();
    }
  });

  ipcMain.on('nav-editor', () => {
    console.log('electron nav to editor');
    win.loadURL('http://localhost:3000/editor'); // Load your React app
  });

  ipcMain.on('nav-recorder', () => {
    win.loadFile('index.html');
  });

  // Capture screenshot on rect bounds, by node/electron:
  ipcMain.on('screenshot', (rect) => {
    const promise = win.capturePage(rect);
    // TODO use promise and check where image is captured
  });

});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
