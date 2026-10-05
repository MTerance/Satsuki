const { exec } = require('child_process');
const os = require('os');
const util = require('util');

const execAsync = util.promisify(exec);

class ProcessChecker {
  constructor() {
    this.processName = 'Satsuki.exe';
    this.isWindows = os.platform() === 'win32';
    // Patterns des exécutables à détecter : Satsuki.exe ou Godot_*.exe
    this.processPatterns = [
      /^Satsuki\.exe$/i,
      /^Godot_.*\.exe$/i
    ];
  }

  /**
   * Vérifie si un nom de processus correspond aux patterns surveillés
   * @param {string} name - Nom de l'exécutable (ex: "Godot_v4.2.exe")
   * @returns {boolean}
   */
  _matchesProcessName(name) {
    if (!name) return false;
    return this.processPatterns.some(pattern => pattern.test(name.trim()));
  }

  /**
   * Vérifie si le processus Satsuki.exe (ou un Godot_*.exe) est en cours d'exécution
   * @returns {Promise<{running: boolean, processInfo: Object|null, error: string|null}>}
   */
  async checkSatsukiProcess() {
    try {
      let command;
      
      if (this.isWindows) {
        // tasklist ne supporte pas les jokers dans IMAGENAME : on liste tout
        // et on filtre côté JS avec les patterns (Satsuki.exe, Godot_*.exe)
        command = 'tasklist /FO CSV /NH';
      } else {
        // Commande Unix/Linux/macOS
        command = 'pgrep -f "Satsuki|Godot_"';
      }

      const { stdout, stderr } = await execAsync(command);
      
      if (this.isWindows) {
        return this._parseWindowsTasklist(stdout);
      } else {
        return this._parseUnixPgrep(stdout);
      }
      
    } catch (error) {
      console.error('Erreur lors de la vérification du processus Satsuki:', error);
      return {
        running: false,
        processInfo: null,
        error: error.message
      };
    }
  }

  /**
   * Parse la sortie de tasklist Windows
   * @private
   */
  _parseWindowsTasklist(stdout) {
    const lines = stdout.split('\n').filter(line => line.trim());
    
    // Rechercher les lignes correspondant aux patterns surveillés
    // (Satsuki.exe ou Godot_*.exe)
    const processLines = lines.filter(line => {
      const imageName = line.replace(/"/g, '').split(',')[0];
      return this._matchesProcessName(imageName);
    });

    if (processLines.length === 0) {
      return {
        running: false,
        processInfo: null,
        error: null
      };
    }

    // Parser les informations du premier processus trouvé
    const processInfo = this._parseProcessLine(processLines[0]);
    
    return {
      running: true,
      processInfo,
      error: null
    };
  }

  /**
   * Parse la sortie de pgrep Unix
   * @private
   */
  _parseUnixPgrep(stdout) {
    const pids = stdout.trim().split('\n').filter(pid => pid.trim());
    
    if (pids.length === 0) {
      return {
        running: false,
        processInfo: null,
        error: null
      };
    }

    return {
      running: true,
      processInfo: {
        pid: parseInt(pids[0]),
        processName: this.processName,
        count: pids.length
      },
      error: null
    };
  }

  /**
   * Parse une ligne de processus CSV de tasklist
   * @private
   */
  _parseProcessLine(line) {
    try {
      // Supprimer les guillemets et diviser par virgule
      const parts = line.replace(/"/g, '').split(',');
      
      if (parts.length >= 5) {
        return {
          imageName: parts[0].trim(),
          pid: parseInt(parts[1].trim()),
          sessionName: parts[2].trim(),
          sessionNumber: parseInt(parts[3].trim()) || 0,
          memoryUsage: parts[4].trim()
        };
      }
      
      return {
        raw: line,
        processName: parts[0]?.trim() || this.processName
      };
      
    } catch (error) {
      console.error('Erreur lors du parsing de la ligne de processus:', error);
      return {
        raw: line,
        processName: this.processName,
        parseError: error.message
      };
    }
  }

  /**
   * Obtient des informations détaillées sur le processus Satsuki
   * @returns {Promise<Object>}
   */
  async getDetailedProcessInfo() {
    try {
      const basicCheck = await this.checkSatsukiProcess();
      
      if (!basicCheck.running) {
        return basicCheck;
      }

      if (this.isWindows && basicCheck.processInfo?.pid) {
        // Obtenir des informations supplémentaires avec wmic
        const wmicCommand = `wmic process where "ProcessId=${basicCheck.processInfo.pid}" get Name,ProcessId,PageFileUsage,WorkingSetSize,CreationDate /format:csv`;
        
        try {
          const { stdout } = await execAsync(wmicCommand);
          const detailedInfo = this._parseWmicOutput(stdout);
          
          return {
            running: true,
            processInfo: {
              ...basicCheck.processInfo,
              ...detailedInfo
            },
            error: null
          };
        } catch (wmicError) {
          // Si wmic échoue, retourner les infos de base
          console.warn('Impossible d\'obtenir les infos détaillées via wmic:', wmicError.message);
          return basicCheck;
        }
      }
      
      return basicCheck;
      
    } catch (error) {
      console.error('Erreur lors de l\'obtention des infos détaillées:', error);
      return {
        running: false,
        processInfo: null,
        error: error.message
      };
    }
  }

  /**
   * Parse la sortie de wmic
   * @private
   */
  _parseWmicOutput(stdout) {
    try {
      const lines = stdout.split('\n').filter(line => line.trim() && !line.startsWith('Node'));
      
      if (lines.length >= 2) {
        const dataLine = lines[1].split(',');
        
        return {
          creationDate: dataLine[1]?.trim(),
          name: dataLine[2]?.trim(),
          pageFileUsage: dataLine[3]?.trim(),
          processId: parseInt(dataLine[4]?.trim()) || null,
          workingSetSize: dataLine[5]?.trim()
        };
      }
      
      return {};
    } catch (error) {
      console.error('Erreur lors du parsing wmic:', error);
      return {};
    }
  }

  /**
   * Surveille périodiquement le processus Satsuki
   * @param {number} interval - Intervalle en millisecondes (défaut: 5000ms)
   * @param {Function} callback - Fonction appelée à chaque vérification
   * @returns {Object} - Objet avec une méthode stop() pour arrêter la surveillance
   */
  startMonitoring(interval = 5000, callback) {
    if (typeof callback !== 'function') {
      throw new Error('Un callback est requis pour la surveillance');
    }

    const intervalId = setInterval(async () => {
      try {
        const result = await this.checkSatsukiProcess();
        callback(result);
      } catch (error) {
        callback({
          running: false,
          processInfo: null,
          error: error.message
        });
      }
    }, interval);

    return {
      stop: () => {
        clearInterval(intervalId);
      }
    };
  }

  /**
   * Obtient la liste de tous les processus Satsuki/Godot en cours
   * @returns {Promise<Array>}
   */
  async getAllSatsukiProcesses() {
    try {
      if (this.isWindows) {
        // On liste tout et on filtre par patterns (Satsuki.exe, Godot_*.exe)
        const command = 'tasklist /FO CSV /NH';
        const { stdout } = await execAsync(command);
        
        const lines = stdout.split('\n').filter(line => {
          if (!line.trim()) return false;
          const imageName = line.replace(/"/g, '').split(',')[0];
          return this._matchesProcessName(imageName);
        });
        
        return lines.map(line => this._parseProcessLine(line));
      } else {
        const command = 'pgrep -f "Satsuki|Godot_"';
        const { stdout } = await execAsync(command);
        const pids = stdout.trim().split('\n').filter(pid => pid.trim());
        
        return pids.map(pid => ({
          pid: parseInt(pid),
          processName: this.processName
        }));
      }
      
    } catch (error) {
      console.error('Erreur lors de l\'obtention de tous les processus Satsuki:', error);
      return [];
    }
  }
}

// Export singleton instance
module.exports = new ProcessChecker();