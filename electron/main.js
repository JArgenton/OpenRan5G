const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let backendProcess = null;

function startBackend() {
  const scriptPath = path.join(__dirname, '..', 'start.py');

  backendProcess = spawn('python', [scriptPath], {
    cwd: path.join(__dirname, '..'),
    shell: true,
    detached: true, // ← importante
    stdio: 'ignore' // ← não herda stdout, para permitir detach
  });

  backendProcess.unref(); // permite que o processo continue independente (mas a gente ainda pode matar)

  console.log('Backend iniciado. PID:', backendProcess.pid);
}

function stopBackend() {
  if (backendProcess && !backendProcess.killed) {
    try {
      console.log('Encerrando backend. PID:', backendProcess.pid);
      process.kill(-backendProcess.pid); // ← mata o grupo inteiro
    } catch (e) {
      console.error('Erro ao encerrar backend:', e);
    }
  }
}

function createWindow() {
  const win = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
    }
  });

  win.loadFile(path.join(__dirname, '..', 'frontend', 'dist', 'index.html'));

  win.setMenuBarVisibility(false);      // Oculta a barra de menu
    win.setMenu(null);                    // Remove o menu completamente


  win.on('closed', () => {
    stopBackend();
    app.quit();
  });
}

app.on('before-quit', stopBackend);
app.on('will-quit', stopBackend);
app.on('window-all-closed', () => {
  stopBackend();
  if (process.platform !== 'darwin') app.quit();
});

app.whenReady().then(() => {
  startBackend();
  createWindow();
});
