<template>
  <div class="satsuki-launcher min-h-screen bg-gradient-to-br from-blue-900 via-purple-900 to-indigo-900">
    <!-- Loading Screen -->
    <div v-if="isInitializing" class="flex items-center justify-center min-h-screen">
      <div class="text-center">
        <div class="loading loading-spinner loading-lg mb-4 text-blue-400"></div>
        <h2 class="text-2xl font-bold text-white mb-2">Initialisation de Satsuki Launcher</h2>
        <p class="text-blue-200">{{ initializationStatus }}</p>
      </div>
    </div>

    <!-- Main Content -->
    <div v-else class="container mx-auto px-6 py-8">
      <!-- Header -->
      <div class="text-center mb-12">
        <h1 class="text-6xl font-bold text-white mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-400">
          🎮 Satsuki Launcher
        </h1>
        <p class="text-xl text-blue-200">Gestionnaire d'instances de jeu multi-écrans</p>
      </div>

      <!-- Status Bar -->
      <div class="bg-black/30 backdrop-blur-sm rounded-xl p-6 mb-8 border border-white/10">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="flex items-center">
              <div :class="['w-4 h-4 rounded-full mr-3', satsukiRunning ? 'bg-green-400 animate-pulse' : 'bg-red-400']"></div>
              <span class="text-white font-semibold">
                Satsuki: {{ satsukiRunning ? 'En cours' : 'Arrêté' }}
              </span>
            </div>
            <div class="text-blue-300">
              Écrans détectés: {{ displays.length }}
            </div>
            <div v-if="lastProcessCheck" class="text-gray-300 text-sm">
              Dernière vérification: {{ formatTime(lastProcessCheck) }}
            </div>
          </div>
          <button 
            @click="refreshStatus" 
            :disabled="isRefreshing"
            class="btn btn-sm btn-outline text-blue-300 border-blue-300 hover:bg-blue-300 hover:text-black"
          >
            <span v-if="isRefreshing" class="loading loading-spinner loading-xs mr-2"></span>
            Actualiser
          </button>
        </div>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="alert alert-error mb-8">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <div>
          <h3 class="font-bold">Erreur détectée</h3>
          <div class="text-xs">{{ error }}</div>
        </div>
        <button @click="clearError" class="btn btn-sm btn-ghost">×</button>
      </div>

      <!-- Satsuki is Running - Connection Section -->
      <div v-if="satsukiRunning" class="space-y-8">
        <div class="bg-green-900/30 backdrop-blur-sm rounded-xl p-8 border border-green-400/30">
          <div class="text-center">
            <div class="text-6xl mb-4">✅</div>
            <h2 class="text-3xl font-bold text-green-300 mb-4">Satsuki est en cours d'exécution</h2>
            <p class="text-green-200 mb-6">{{ runningProcesses.length }} instance(s) détectée(s)</p>
            
            <!-- Process Details -->
            <div v-if="runningProcesses.length > 0" class="bg-black/20 rounded-lg p-4 mb-6">
              <h3 class="text-lg font-semibold text-white mb-4">Instances actives</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <div v-for="process in runningProcesses" :key="process.pid" 
                     class="bg-green-800/30 rounded-lg p-4 border border-green-500/30">
                  <div class="text-white font-medium">PID: {{ process.pid }}</div>
                  <div class="text-green-200 text-sm">{{ process.imageName || 'Satsuki.exe' }}</div>
                  <div v-if="process.memoryUsage" class="text-green-300 text-xs">
                    Mémoire: {{ process.memoryUsage }}
                  </div>
                </div>
              </div>
            </div>

            <div class="space-y-4">
              <button 
                @click="connectToRunningInstance" 
                :disabled="isConnecting"
                class="btn btn-lg btn-success text-black font-bold px-8 py-4"
              >
                <span v-if="isConnecting" class="loading loading-spinner loading-md mr-2"></span>
                🔌 Se connecter à cette instance de jeu
              </button>
              
              <div class="text-sm text-green-300">
                Cliquez pour vous connecter à l'instance Satsuki en cours d'exécution
              </div>
            </div>
          </div>
        </div>

        <!-- Advanced Options -->
        <div class="bg-black/20 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <h3 class="text-xl font-semibold text-white mb-4">Options avancées</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button 
              @click="launchNewInstance" 
              class="btn btn-outline btn-primary"
            >
              🚀 Lancer une nouvelle instance
            </button>
            <button 
              @click="showProcessDetails = !showProcessDetails" 
              class="btn btn-outline btn-secondary"
            >
              📊 {{ showProcessDetails ? 'Masquer' : 'Afficher' }} les détails
            </button>
          </div>
          
          <!-- Process Details -->
          <div v-if="showProcessDetails && processDetails" class="mt-6 bg-black/40 rounded-lg p-4">
            <h4 class="text-lg font-medium text-white mb-3">Détails du processus</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div v-for="(value, key) in processDetails.processInfo" :key="key" class="flex justify-between">
                <span class="text-gray-300">{{ formatKey(key) }}:</span>
                <span class="text-white">{{ formatValue(value) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Satsuki is NOT Running - Launch Options -->
      <div v-else class="space-y-8">
        <div class="bg-orange-900/30 backdrop-blur-sm rounded-xl p-8 border border-orange-400/30">
          <div class="text-center">
            <div class="text-6xl mb-4">🎮</div>
            <h2 class="text-3xl font-bold text-orange-300 mb-4">Satsuki n'est pas en cours d'exécution</h2>
            <p class="text-orange-200 mb-6">Choisissez un écran pour lancer le jeu</p>
          </div>
        </div>

        <!-- Quick Launch -->
        <div class="bg-black/20 backdrop-blur-sm rounded-xl p-6 border border-white/10 mb-8">
          <h3 class="text-xl font-semibold text-white mb-4">🚀 Lancement rapide</h3>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button 
              @click="launchOnBestScreen" 
              :disabled="isLaunching"
              class="btn btn-lg btn-primary"
            >
              <span v-if="isLaunching" class="loading loading-spinner loading-md mr-2"></span>
              ⚡ Lancer sur le meilleur écran
            </button>
            <button 
              @click="launchOnPrimaryScreen" 
              :disabled="isLaunching"
              class="btn btn-lg btn-secondary"
            >
              <span v-if="isLaunching" class="loading loading-spinner loading-md mr-2"></span>
              🖥️ Lancer sur l'écran principal
            </button>
          </div>
        </div>

        <!-- Screen Selection -->
        <div class="bg-black/20 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <h3 class="text-xl font-semibold text-white mb-6">🖼️ Sélectionner un écran spécifique</h3>
          
          <div v-if="displays.length === 0" class="text-center py-8">
            <div class="text-4xl mb-4">⚠️</div>
            <p class="text-yellow-300">Aucun écran détecté</p>
            <button @click="refreshDisplays" class="btn btn-outline btn-warning mt-4">
              Actualiser les écrans
            </button>
          </div>

          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="display in displays" :key="display.id" 
                 class="screen-card bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl p-6 border border-gray-600 hover:border-blue-400 transition-all duration-300 hover:scale-105">
              
              <!-- Screen Preview -->
              <div class="relative mb-4">
                <div class="aspect-video bg-black rounded-lg border-2 border-gray-600 flex items-center justify-center relative overflow-hidden">
                  <div class="text-white text-2xl">🖥️</div>
                  <div v-if="display.isPrimary" class="absolute top-2 right-2">
                    <span class="badge badge-primary badge-sm">Principal</span>
                  </div>
                  <div v-if="display.touchSupport === 'available'" class="absolute top-2 left-2">
                    <span class="badge badge-secondary badge-sm">Touch</span>
                  </div>
                </div>
              </div>

              <!-- Screen Info -->
              <div class="space-y-2 mb-4">
                <h4 class="text-lg font-bold text-white">{{ display.label }}</h4>
                <div class="text-sm text-gray-300 space-y-1">
                  <div>📐 {{ display.bounds.width }}×{{ display.bounds.height }}</div>
                  <div>📍 Position: ({{ display.bounds.x }}, {{ display.bounds.y }})</div>
                  <div>🔍 Échelle: {{ display.scaleFactor }}x</div>
                  <div v-if="display.rotation !== 0">🔄 Rotation: {{ display.rotation }}°</div>
                </div>
              </div>

              <!-- Action Button -->
              <button 
                @click="launchOnScreen(display)" 
                :disabled="isLaunching"
                class="btn btn-block btn-primary"
              >
                <span v-if="isLaunching && launchingScreenId === display.id" class="loading loading-spinner loading-sm mr-2"></span>
                🚀 Lancer sur cet écran
              </button>

              <!-- Screen Stats -->
              <div class="mt-3 text-xs text-gray-400 text-center">
                Surface: {{ formatScreenArea(display.bounds.width * display.bounds.height) }}
              </div>
            </div>
          </div>
        </div>

        <!-- Custom Path Section -->
        <div class="bg-black/20 backdrop-blur-sm rounded-xl p-6 border border-white/10">
          <h3 class="text-xl font-semibold text-white mb-4">⚙️ Options avancées</h3>
          
          <div class="form-control mb-4">
            <label class="label">
              <span class="label-text text-white">Chemin personnalisé vers Satsuki.exe (optionnel)</span>
            </label>
            <div class="flex space-x-2">
              <input 
                v-model="customSatsukiPath" 
                type="text" 
                placeholder="C:\Program Files\Satsuki\Satsuki.exe"
                class="input input-bordered flex-1 bg-black/40 text-white border-gray-600 focus:border-blue-400"
              >
              <button @click="browseSatsukiPath" class="btn btn-outline btn-secondary">
                📁 Parcourir
              </button>
            </div>
            <label class="label">
              <span class="label-text-alt text-gray-400">Laissez vide pour utiliser la détection automatique</span>
            </label>
          </div>

          <!-- Launch Preferences -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="form-control">
              <label class="cursor-pointer label">
                <span class="label-text text-white">Préférer l'écran principal</span>
                <input type="checkbox" v-model="launchPreferences.preferPrimary" class="checkbox checkbox-primary">
              </label>
            </div>
            <div class="form-control">
              <label class="cursor-pointer label">
                <span class="label-text text-white">Préférer les grands écrans</span>
                <input type="checkbox" v-model="launchPreferences.preferLargeScreen" class="checkbox checkbox-primary">
              </label>
            </div>
          </div>
        </div>
      </div>

      <!-- System Information -->
      <div class="bg-black/20 backdrop-blur-sm rounded-xl p-6 border border-white/10 mt-8">
        <h3 class="text-xl font-semibold text-white mb-4">📊 Informations système</h3>
        <div v-if="displayCapabilities" class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
          <div class="stat">
            <div class="stat-title text-gray-300">Écrans totaux</div>
            <div class="stat-value text-blue-400">{{ displayCapabilities.totalDisplays }}</div>
          </div>
          <div class="stat">
            <div class="stat-title text-gray-300">Écrans tactiles</div>
            <div class="stat-value text-green-400">{{ displayCapabilities.touchScreens }}</div>
          </div>
          <div class="stat">
            <div class="stat-title text-gray-300">Haute résolution</div>
            <div class="stat-value text-purple-400">{{ displayCapabilities.highDPIScreens }}</div>
          </div>
          <div class="stat">
            <div class="stat-title text-gray-300">Surface totale</div>
            <div class="stat-value text-orange-400 text-lg">{{ formatScreenArea(displayCapabilities.totalScreenArea) }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted, onUnmounted } from 'vue';
import processService from '@/services/processService.js';

export default {
  name: 'SatsukiLauncher',
  setup() {
    // State
    const isInitializing = ref(true);
    const initializationStatus = ref('Vérification de Satsuki...');
    const satsukiRunning = ref(false);
    const displays = ref([]);
    const displayCapabilities = ref(null);
    const runningProcesses = ref([]);
    const processDetails = ref(null);
    const error = ref('');
    const isRefreshing = ref(false);
    const isLaunching = ref(false);
    const launchingScreenId = ref(null);
    const isConnecting = ref(false);
    const customSatsukiPath = ref('');
    const lastProcessCheck = ref(null);
    const showProcessDetails = ref(false);

    // Preferences
    const launchPreferences = reactive({
      preferPrimary: false,
      preferLargeScreen: true,
      preferHighDPI: false,
      minWidth: 1024,
      minHeight: 768
    });

    // Methods
    const checkSatsukiStatus = async () => {
      try {
        const result = await processService.checkSatsukiProcess();
        satsukiRunning.value = result.running;
        lastProcessCheck.value = new Date().toISOString();
        
        if (result.running) {
          // Get all processes for detailed info
          runningProcesses.value = await processService.getAllSatsukiProcesses();
          processDetails.value = await processService.getDetailedProcessInfo();
        } else {
          runningProcesses.value = [];
          processDetails.value = null;
        }
        
        if (result.error) {
          error.value = result.error;
        }
      } catch (err) {
        error.value = `Erreur lors de la vérification: ${err.message}`;
        console.error('Erreur vérification Satsuki:', err);
      }
    };

    const loadDisplays = async () => {
      try {
        if (!window.screenManager) {
          throw new Error('API screenManager non disponible');
        }
        
        displays.value = await window.screenManager.getAllDisplays();
        displayCapabilities.value = await window.screenManager.getCapabilities();
      } catch (err) {
        error.value = `Erreur lors du chargement des écrans: ${err.message}`;
        console.error('Erreur chargement écrans:', err);
      }
    };

    const initialize = async () => {
      try {
        initializationStatus.value = 'Vérification de Satsuki...';
        await checkSatsukiStatus();
        
        initializationStatus.value = 'Détection des écrans...';
        await loadDisplays();
        
        initializationStatus.value = 'Initialisation terminée';
        
        // Small delay for UX
        setTimeout(() => {
          isInitializing.value = false;
        }, 1000);
        
      } catch (err) {
        error.value = `Erreur d'initialisation: ${err.message}`;
        isInitializing.value = false;
      }
    };

    const refreshStatus = async () => {
      isRefreshing.value = true;
      try {
        await Promise.all([
          checkSatsukiStatus(),
          loadDisplays()
        ]);
      } finally {
        isRefreshing.value = false;
      }
    };

    const refreshDisplays = async () => {
      await loadDisplays();
    };

    const launchOnScreen = async (display) => {
      isLaunching.value = true;
      launchingScreenId.value = display.id;
      
      try {
        if (!window.screenManager) {
          throw new Error('API screenManager non disponible');
        }
        
        const result = await window.screenManager.launchSatsukiOnDisplay(
          display.id, 
          customSatsukiPath.value || null
        );
        
        if (result.success) {
          // Wait a bit then check status
          setTimeout(async () => {
            await checkSatsukiStatus();
          }, 2000);
        } else {
          error.value = result.error || 'Échec du lancement';
        }
        
      } catch (err) {
        error.value = `Erreur lors du lancement: ${err.message}`;
      } finally {
        isLaunching.value = false;
        launchingScreenId.value = null;
      }
    };

    const launchOnBestScreen = async () => {
      try {
        if (!window.screenManager) {
          throw new Error('API screenManager non disponible');
        }
        
        const bestDisplay = await window.screenManager.getBestDisplay(launchPreferences);
        if (bestDisplay) {
          await launchOnScreen(bestDisplay);
        } else {
          error.value = 'Aucun écran approprié trouvé';
        }
      } catch (err) {
        error.value = `Erreur: ${err.message}`;
      }
    };

    const launchOnPrimaryScreen = async () => {
      try {
        if (!window.screenManager) {
          throw new Error('API screenManager non disponible');
        }
        
        const primaryDisplay = await window.screenManager.getPrimaryDisplay();
        if (primaryDisplay) {
          await launchOnScreen(primaryDisplay);
        } else {
          error.value = 'Écran principal non trouvé';
        }
      } catch (err) {
        error.value = `Erreur: ${err.message}`;
      }
    };

    const launchNewInstance = async () => {
      await launchOnBestScreen();
    };

    const connectToRunningInstance = async () => {
      isConnecting.value = true;
      
      try {
        // Simulate connection logic
        await new Promise(resolve => setTimeout(resolve, 1500));
        
        // Here you would implement the actual connection logic
        // For now, we'll just show a success message
        alert('Connexion à l\'instance Satsuki réussie !');
        
      } catch (err) {
        error.value = `Erreur de connexion: ${err.message}`;
      } finally {
        isConnecting.value = false;
      }
    };

    const browseSatsukiPath = () => {
      // This would open a file dialog in a real implementation
      // For now, we'll just show an alert
      alert('Fonctionnalité de parcours de fichiers à implémenter');
    };

    const clearError = () => {
      error.value = '';
    };

    // Utility functions
    const formatTime = (isoString) => {
      if (!isoString) return 'Jamais';
      return new Date(isoString).toLocaleTimeString();
    };

    const formatKey = (key) => {
      const keyMap = {
        imageName: 'Image',
        pid: 'PID',
        sessionName: 'Session',
        sessionNumber: 'N° Session',
        memoryUsage: 'Mémoire',
        processName: 'Processus',
        creationDate: 'Création',
        pageFileUsage: 'Fichier page',
        workingSetSize: 'Working Set'
      };
      return keyMap[key] || key;
    };

    const formatValue = (value) => {
      if (value === null || value === undefined) return 'N/A';
      if (typeof value === 'number') return value.toLocaleString();
      return value.toString();
    };

    const formatScreenArea = (area) => {
      if (area > 1000000) {
        return `${(area / 1000000).toFixed(1)}M px`;
      }
      return `${(area / 1000).toFixed(0)}K px`;
    };

    // Lifecycle
    onMounted(() => {
      initialize();
      
      // Set up periodic status checking
      const statusInterval = setInterval(checkSatsukiStatus, 10000); // Every 10 seconds
      
      // Cleanup on unmount
      onUnmounted(() => {
        clearInterval(statusInterval);
      });
    });

    return {
      // State
      isInitializing,
      initializationStatus,
      satsukiRunning,
      displays,
      displayCapabilities,
      runningProcesses,
      processDetails,
      error,
      isRefreshing,
      isLaunching,
      launchingScreenId,
      isConnecting,
      customSatsukiPath,
      lastProcessCheck,
      showProcessDetails,
      launchPreferences,
      
      // Methods
      checkSatsukiStatus,
      refreshStatus,
      refreshDisplays,
      launchOnScreen,
      launchOnBestScreen,
      launchOnPrimaryScreen,
      launchNewInstance,
      connectToRunningInstance,
      browseSatsukiPath,
      clearError,
      formatTime,
      formatKey,
      formatValue,
      formatScreenArea
    };
  }
};
</script>

<style scoped>
.screen-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
}

.loading {
  display: inline-block;
}

.stat {
  padding: 1rem;
  text-align: center;
}

.stat-title {
  font-size: 0.75rem;
  opacity: 0.7;
  font-weight: 500;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 700;
  margin-top: 0.25rem;
}

.btn {
  transition: all 0.2s ease-in-out;
}

.btn:hover {
  transform: translateY(-1px);
}

.alert {
  border-radius: 0.75rem;
}

.form-control {
  margin-bottom: 1rem;
}

.label-text {
  font-weight: 500;
}

.input {
  transition: border-color 0.2s ease-in-out;
}

.checkbox {
  accent-color: theme('colors.blue.500');
}

.badge {
  font-size: 0.75rem;
  font-weight: 600;
}
</style>