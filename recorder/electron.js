
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

function createWindow() {
  const win = new BrowserWindow({
    width: 1400,
    height: 1000,
    webPreferences: {
      nodeIntegration: true, // NOTE ? check
      preload: path.join(__dirname, 'preload.js'),
      // enable webview...
      webviewTag: true, // TODO
    },
  });

  // mainWindow.loadFile('index.html')
  win.loadURL('http://localhost:3000'); // Load your React app
}

app.whenReady().then(() => {
  ipcMain.on('set-title', handleSetTitle);

  ipcMain.on('clientSetWebView', function(webViewReference) {
    console.log('electron received webview', webViewRerefence);
  });

  ipcMain.handle('dialog:openFile', handleFileOpen);

  ipcMain.handle('ping', () => 'pong');

  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });

});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
});
