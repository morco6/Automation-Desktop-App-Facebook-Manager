/*
* Configuration file for electron GUI
*/

const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')
const ipcMain = require('electron').ipcMain

let mainWindow = null
let secondWindow = null

//create login window
const createWindow = () => {
  mainWindow = new BrowserWindow({
      width: 700, 
      height: 667, 
      resizable: false, 
      frame: false, 
      alwaysOnTop: true
    })
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, 'index.html'),
    protocol: 'file:',
    slashes: true
  }))
  //mainWindow.webContents.openDevTools()
  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})


//-----------communicate with renderer via ipcMain and ipcRenderer-------------

ipcMain.on('nextPage', (event) => { // synchronous function - creates a new window (the child window)
    secondWindow = new BrowserWindow({
        width: 1000, 
        height: 750, 
        resizable: false, 
        frame: true, 
        alwaysOnTop: true
    })
    secondWindow.loadURL(require('url').format({
        pathname: path.join(__dirname, 'home.html'),
        protocol: 'file:',
        slashes: true
    }))
    //when second window closed -> close app
    secondWindow.on('closed', () => {
        secondWindow = null
        app.quit()
    })
    secondWindow.show()
})



//-----------Open a communication with python api-------------

let pyProc = null
let pyPort = null

const selectPort = () => {
  pyPort = 4244
  return pyPort
}

/**
 * On startup - spawn python api.
 */
const createPyProc = () => {
  let port = '' + selectPort()
  let script = path.join(__dirname, 'Python', 'api.py')
  pyProc = require('child_process').spawn('python3', [script, port])
  if (pyProc != null) {
    console.log('child process success')
  }
}

const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)