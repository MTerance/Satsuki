const { screen } = require('electron');
const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

class ScreenManager {
  constructor() {
    this.displays = [];
  }

  /**
   * Obtient la liste de tous les écrans disponibles
   * @returns {Array} Liste des écrans avec leurs propriétés
   */
  getAllDisplays() {
    try {
      const displays = screen.getAllDisplays();
      
      this.displays = displays.map((display, index) => ({
        id: display.id,
        label: display.label || `Écran ${index + 1}`,
        bounds: display.bounds,
        workArea: display.workArea,
        scaleFactor: display.scaleFactor,
        rotation: display.rotation,
        isPrimary: display.bounds.x === 0 && display.bounds.y === 0,
        size: display.size,
        touchSupport: display.touchSupport,
        index: index
      }));

      return this.displays;
    } catch (error) {
      console.error('Erreur lors de l\'obtention des écrans:', error);
      return [];
    }
  }

  /**
   * Obtient l'écran principal
   * @returns {Object} Informations sur l'écran principal
   */
  getPrimaryDisplay() {
    try {
      const primaryDisplay = screen.getPrimaryDisplay();
      return {
        id: primaryDisplay.id,
        label: 'Écran Principal',
        bounds: primaryDisplay.bounds,
        workArea: primaryDisplay.workArea,
        scaleFactor: primaryDisplay.scaleFactor,
        rotation: primaryDisplay.rotation,
        isPrimary: true,
        size: primaryDisplay.size,
        touchSupport: primaryDisplay.touchSupport
      };
    } catch (error) {
      console.error('Erreur lors de l\'obtention de l\'écran principal:', error);
      return null;
    }
  }

  /**
   * Lance Satsuki.exe sur un écran spécifique
   * @param {number} displayId - ID de l'écran cible
   * @param {string} satsukiPath - Chemin vers Satsuki.exe (optionnel)
   * @returns {Promise<Object>} Résultat du lancement
   */
  async launchSatsukiOnDisplay(displayId, satsukiPath = null) {
    try {
      const targetDisplay = this.displays.find(display => display.id === displayId);
      
      if (!targetDisplay) {
        throw new Error(`Écran avec l'ID ${displayId} introuvable`);
      }

      // Chemins possibles pour Satsuki.exe
      const possiblePaths = [
        satsukiPath,
        'C:\\Program Files\\Satsuki\\Satsuki.exe',
        'C:\\Program Files (x86)\\Satsuki\\Satsuki.exe',
        'C:\\Games\\Satsuki\\Satsuki.exe',
        path.join(process.env.USERPROFILE || '', 'Desktop', 'Satsuki.exe'),
        path.join(process.env.USERPROFILE || '', 'Documents', 'Satsuki', 'Satsuki.exe')
      ].filter(Boolean);

      // Trouver le chemin valide
      let executablePath = null;
      for (const testPath of possiblePaths) {
        if (fs.existsSync(testPath)) {
          executablePath = testPath;
          break;
        }
      }

      if (!executablePath) {
        return {
          success: false,
          error: 'Satsuki.exe introuvable. Veuillez spécifier le chemin correct.',
          suggestedPaths: possiblePaths
        };
      }

      // Calculer la position de fenêtre pour l'écran cible
      const windowX = targetDisplay.bounds.x + 100;
      const windowY = targetDisplay.bounds.y + 100;
      const windowWidth = Math.min(1280, targetDisplay.workArea.width - 200);
      const windowHeight = Math.min(720, targetDisplay.workArea.height - 200);

      // Arguments pour positionner la fenêtre (dépend du programme)
      const args = [
        // Arguments génériques pour positioning (peut ne pas fonctionner avec tous les programmes)
        '--window-position', `${windowX},${windowY}`,
        '--window-size', `${windowWidth}x${windowHeight}`,
        '--display', displayId.toString()
      ];

      // Lancer le processus
      const childProcess = spawn(executablePath, args, {
        detached: true,
        stdio: 'ignore'
      });

      // Permettre au processus de continuer même si le parent se ferme
      childProcess.unref();

      return {
        success: true,
        processId: childProcess.pid,
        displayInfo: targetDisplay,
        executablePath,
        message: `Satsuki lancé sur ${targetDisplay.label} (PID: ${childProcess.pid})`
      };

    } catch (error) {
      console.error('Erreur lors du lancement de Satsuki:', error);
      return {
        success: false,
        error: error.message,
        displayId
      };
    }
  }

  /**
   * Lance Satsuki.exe de manière simple (écran par défaut)
   * @param {string} satsukiPath - Chemin vers Satsuki.exe (optionnel)
   * @returns {Promise<Object>} Résultat du lancement
   */
  async launchSatsuki(satsukiPath = null) {
    const primaryDisplay = this.getPrimaryDisplay();
    return await this.launchSatsukiOnDisplay(primaryDisplay.id, satsukiPath);
  }

  /**
   * Obtient des informations détaillées sur les capacités d'écran
   * @returns {Object} Informations système sur les écrans
   */
  getDisplayCapabilities() {
    const displays = this.getAllDisplays();
    
    return {
      totalDisplays: displays.length,
      primaryDisplay: displays.find(d => d.isPrimary),
      totalScreenArea: displays.reduce((total, display) => {
        return total + (display.bounds.width * display.bounds.height);
      }, 0),
      maxResolution: displays.reduce((max, display) => {
        const resolution = display.bounds.width * display.bounds.height;
        return resolution > max.resolution ? {
          resolution,
          display: display
        } : max;
      }, { resolution: 0, display: null }),
      touchScreens: displays.filter(d => d.touchSupport === 'available').length,
      highDPIScreens: displays.filter(d => d.scaleFactor > 1).length
    };
  }

  /**
   * Surveille les changements d'écrans
   * @param {Function} callback - Fonction appelée lors des changements
   * @returns {Function} Fonction pour arrêter la surveillance
   */
  watchDisplayChanges(callback) {
    const handleDisplayChange = () => {
      const newDisplays = this.getAllDisplays();
      callback({
        displays: newDisplays,
        timestamp: new Date().toISOString(),
        capabilities: this.getDisplayCapabilities()
      });
    };

    // Écouter les événements de changement d'écran
    screen.on('display-added', handleDisplayChange);
    screen.on('display-removed', handleDisplayChange);
    screen.on('display-metrics-changed', handleDisplayChange);

    // Retourner une fonction pour arrêter la surveillance
    return () => {
      screen.removeListener('display-added', handleDisplayChange);
      screen.removeListener('display-removed', handleDisplayChange);
      screen.removeListener('display-metrics-changed', handleDisplayChange);
    };
  }

  /**
   * Trouve le meilleur écran pour lancer Satsuki
   * @param {Object} preferences - Préférences d'écran
   * @returns {Object} Écran recommandé
   */
  getBestDisplayForSatsuki(preferences = {}) {
    const displays = this.getAllDisplays();
    
    if (displays.length === 0) {
      return null;
    }

    // Préférences par défaut
    const prefs = {
      preferPrimary: false,
      minWidth: 1024,
      minHeight: 768,
      preferLargeScreen: true,
      preferHighDPI: false,
      ...preferences
    };

    // Filtrer les écrans compatibles
    let compatibleDisplays = displays.filter(display => {
      return display.workArea.width >= prefs.minWidth && 
             display.workArea.height >= prefs.minHeight;
    });

    if (compatibleDisplays.length === 0) {
      compatibleDisplays = displays; // Fallback vers tous les écrans
    }

    // Appliquer les préférences
    if (prefs.preferPrimary) {
      const primaryDisplay = compatibleDisplays.find(d => d.isPrimary);
      if (primaryDisplay) return primaryDisplay;
    }

    if (prefs.preferLargeScreen) {
      return compatibleDisplays.reduce((largest, current) => {
        const currentArea = current.workArea.width * current.workArea.height;
        const largestArea = largest.workArea.width * largest.workArea.height;
        return currentArea > largestArea ? current : largest;
      });
    }

    if (prefs.preferHighDPI) {
      const highDPIDisplays = compatibleDisplays.filter(d => d.scaleFactor > 1);
      if (highDPIDisplays.length > 0) {
        return highDPIDisplays[0];
      }
    }

    return compatibleDisplays[0];
  }
}

// Export singleton instance
module.exports = new ScreenManager();