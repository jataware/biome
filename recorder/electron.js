
const { app, BrowserWindow, ipcMain, dialog, webContents } = require('electron');
const path = require('node:path');


function handleSetTitle (event, title) {
  const webContents = event.sender;
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
    titleBarStyle: 'hidden',
    width: 1400,
    height: 1000,
    webPreferences: {
      // nodeIntegration: true, // NOTE only allowed with ctx iso
      preload: path.join(__dirname, 'preload-local.js'),
      // enable webview...
      webviewTag: true,
      contextIsolation: false // for getWebContentsId()
    },
  });

  win.loadFile('index.html');
  // win.loadURL('http://localhost:3000'); // Load your React app
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

});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
