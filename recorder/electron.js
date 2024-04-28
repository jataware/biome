
const { app, BrowserWindow, ipcMain, dialog, webContents } = require('electron');
const path = require('node:path');


function eventToWindow(event) {
  return BrowserWindow.fromWebContents(event.sender);
}

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

const isDev = true;

let win;
function createWindow() {
   win = new BrowserWindow({
    // titleBarStyle: 'hidden', // TODO does this work in all OS?
    autoHideMenuBar: true, // hides linux/window File|Edit|View Menu
    title: 'Koro Web Recorder',
    width: 1400,
    height: 1000,
     // https://www.electronjs.org/docs/latest/api/browser-window#new-browserwindowoptions
    webPreferences: {
      // nodeIntegration: true, // NOTE only allowed with ctx iso
      // nodeIntegrationInSubFrames: true, // enable node in subframes/child wins
      // preload always has access to node APIs where node int is on/off
      preload: path.join(__dirname, 'preload.js'),
      zoomFactor: 1.0, // default
      javascript: true,
      webSecurity: true, // would setting to false allow embedding webview w/o preload
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
      contextIsolation: true, // for getWebContentsId(); comm with preload-view
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

  // TODO use on dev only:
  win.webContents.openDevTools(); // works for index.html contents

  // Only works in linux/windows:
  // win.removeMenu(); // TODO check this out if menu is bothersome

  // Only on macos for traffic light close/min/max icons:
  // win.setWindowButtonVisibility(true); // could set to false try out
}

app.whenReady().then(() => {

  let webviewContentsHandle = null;

  createWindow();

  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) {
      console.log('Browser windows == 0; recreating.');
      createWindow();
    }
  });

  // Get a permanent handle since it's hard to
  // know the webview ID by order
  ipcMain.on('webview:ready', (event, ...more) => {
    webviewContentsHandle = event.sender;
  });

  ipcMain.on('set-title', handleSetTitle);

  // ----------------------- RECORD STEP ------------------------------------

  ipcMain.on('recorder:nav-editor', () => {

    const startURL = isDev
          ? 'http://localhost:3000'
          : `file://${path.join(__dirname, '../build/index.html')}`;

    win.loadURL('http://localhost:3000/editor'); // Loads React app
  });

  ipcMain.on('recorder:mark-page', () => {
    webviewContentsHandle.send('mark-page');
  });

  // payload = 'reload', 'back', 'forward', 'load' (url)
  ipcMain.on('recorder:navigate-webview', (event, payload) => {
    webviewContentsHandle.send('navigate-webview', payload);
  });

  // ------------------- EVENTS FROM WEBVIEW --------------------------------

  // TODO do we handle per event on electron, or do we
  // capture in browser and send final actions then?
  // PoC that actions can be send to electron, regardless:
  ipcMain.on('webview:scroll-action', (event, payload) => {
    console.log("webview:scroll-action", event, payload);
  });
  ipcMain.on('webview:click-action', (event, payload) => {
    console.log("webview:click-action", event, payload);
  });

  // ----------------------- EDITOR STEP ------------------------------------
  ipcMain.on('editor:nav-recorder', () => {
    console.log('nav recorder');
    win.loadFile('index.html');
  });


  // --------------------------- PENDING -----------------------------------

  // Capture screenshot on rect bounds, by node/electron:
  ipcMain.on('screenshot', (rect) => {
    // TODO maybe we can scope this to webviewContentsHandle
    const promise = win.capturePage(rect);
    // TODO use promise and check where image is captured
  });

  // ---------------------------- DEBUG -------------------------------------

  ipcMain.handle('debug:ping', () => 'pong');

  ipcMain.on('dialog:openFile', handleFileOpen);

  ipcMain.on('webview:devtools', () => {
    // mainIndexPage contents in win... ID=1
    // const contents = win.webContents;
    // console.log(contents);

    // if getting all contents:
    // const allContents = webContents.getAllWebContents();
    // const [webviewContents, mainIndexPage] = allContents;
    // console.log(allContents);

    // or use webContents.fromId(x) if known IF
    // mainIndexPage.openDevTools(); // ID 1
    webviewContentsHandle.openDevTools();
    // webviewContents.openDevTools(); // ID 2 or 3,4... don't trust the ID No.
  });


});

app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit();
});
