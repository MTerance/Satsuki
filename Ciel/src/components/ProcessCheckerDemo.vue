<template>
  <div class="process-checker-demo p-6 bg-white rounded-lg shadow-lg">
    <h2 class="text-2xl font-bold mb-6 text-gray-800">
      🔍 Vérification de Processus Satsuki
    </h2>

    <!-- État actuel -->
    <div class="status-section mb-6">
      <h3 class="text-lg font-semibold mb-3">État Actuel</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <!-- Statut de fonctionnement -->
        <div class="status-card p-4 rounded-lg border">
          <div class="flex items-center">
            <div 
              :class="[
                'w-3 h-3 rounded-full mr-2',
                processService.isRunning.value ? 'bg-green-500' : 'bg-red-500'
              ]"
            ></div>
            <span class="font-medium">
              {{ processService.isRunning.value ? 'En cours' : 'Arrêté' }}
            </span>
          </div>
          <p class="text-sm text-gray-600 mt-1">
            Satsuki.exe
          </p>
        </div>

        <!-- Dernière vérification -->
        <div class="status-card p-4 rounded-lg border">
          <div class="text-sm">
            <span class="font-medium">Dernière vérif:</span>
            <p class="text-gray-600">
              {{ formatTime(processService.lastCheck.value) }}
            </p>
          </div>
        </div>

        <!-- Surveillance -->
        <div class="status-card p-4 rounded-lg border">
          <div class="flex items-center">
            <div 
              :class="[
                'w-3 h-3 rounded-full mr-2',
                processService.monitoring.value ? 'bg-blue-500 animate-pulse' : 'bg-gray-400'
              ]"
            ></div>
            <span class="font-medium">
              {{ processService.monitoring.value ? 'Surveillance ON' : 'Surveillance OFF' }}
            </span>
          </div>
        </div>

        <!-- Erreur -->
        <div class="status-card p-4 rounded-lg border" v-if="processService.error.value">
          <div class="text-red-600">
            <span class="font-medium">Erreur:</span>
            <p class="text-sm">{{ processService.error.value }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Actions -->
    <div class="actions-section mb-6">
      <h3 class="text-lg font-semibold mb-3">Actions</h3>
      <div class="flex flex-wrap gap-3">
        <button 
          @click="checkProcess"
          :disabled="processService.isChecking.value"
          class="btn btn-primary"
        >
          {{ processService.isChecking.value ? 'Vérification...' : 'Vérifier maintenant' }}
        </button>

        <button 
          @click="getDetailedInfo"
          :disabled="processService.isChecking.value"
          class="btn btn-secondary"
        >
          Infos détaillées
        </button>

        <button 
          @click="getAllProcesses"
          class="btn btn-outline"
        >
          Tous les processus
        </button>

        <button 
          @click="toggleMonitoring"
          :class="[
            'btn',
            processService.monitoring.value ? 'btn-error' : 'btn-success'
          ]"
        >
          {{ processService.monitoring.value ? 'Arrêter surveillance' : 'Démarrer surveillance' }}
        </button>
      </div>
    </div>

    <!-- Informations du processus -->
    <div class="process-info-section mb-6" v-if="processService.processInfo.value">
      <h3 class="text-lg font-semibold mb-3">Informations du Processus</h3>
      <div class="bg-gray-50 p-4 rounded-lg">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div v-for="(value, key) in processService.processInfo.value" :key="key" class="info-item">
            <span class="font-medium text-gray-700">{{ formatKey(key) }}:</span>
            <span class="text-gray-900 ml-2">{{ formatValue(value) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Liste de tous les processus -->
    <div class="all-processes-section mb-6" v-if="allProcesses.length > 0">
      <h3 class="text-lg font-semibold mb-3">
        Tous les Processus Satsuki ({{ allProcesses.length }})
      </h3>
      <div class="overflow-x-auto">
        <table class="table table-zebra w-full">
          <thead>
            <tr>
              <th>PID</th>
              <th>Nom</th>
              <th>Mémoire</th>
              <th>Session</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="process in allProcesses" :key="process.pid || Math.random()">
              <td>{{ process.pid || 'N/A' }}</td>
              <td>{{ process.imageName || process.processName || 'Satsuki.exe' }}</td>
              <td>{{ process.memoryUsage || 'N/A' }}</td>
              <td>{{ process.sessionName || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Statistiques -->
    <div class="stats-section mb-6">
      <h3 class="text-lg font-semibold mb-3">Statistiques</h3>
      <div class="stats shadow">
        <div class="stat">
          <div class="stat-title">Vérifications totales</div>
          <div class="stat-value">{{ processService.stats.totalChecks }}</div>
          <div class="stat-desc">
            {{ processService.stats.successfulChecks }} réussies, 
            {{ processService.stats.failedChecks }} échouées
          </div>
        </div>

        <div class="stat">
          <div class="stat-title">Disponibilité</div>
          <div class="stat-value">{{ uptimePercentage }}%</div>
          <div class="stat-desc">
            {{ processService.stats.uptimeChecks }}/{{ processService.stats.totalChecks }} vérifications
          </div>
        </div>

        <div class="stat">
          <div class="stat-title">Temps moyen</div>
          <div class="stat-value">{{ avgDuration }}ms</div>
          <div class="stat-desc">Temps de vérification moyen</div>
        </div>
      </div>
    </div>

    <!-- Configuration -->
    <div class="config-section">
      <h3 class="text-lg font-semibold mb-3">Configuration</h3>
      <div class="form-control">
        <label class="label">
          <span class="label-text">Intervalle de surveillance (ms)</span>
        </label>
        <input 
          type="number" 
          v-model.number="configInterval"
          @change="updateInterval"
          min="1000"
          max="60000"
          step="1000"
          class="input input-bordered w-full max-w-xs"
        >
      </div>

      <div class="form-control mt-4">
        <label class="cursor-pointer label">
          <span class="label-text">Informations détaillées</span>
          <input 
            type="checkbox" 
            v-model="processService.config.enableDetailedInfo"
            class="checkbox"
          >
        </label>
      </div>

      <button 
        @click="resetStats" 
        class="btn btn-outline btn-sm mt-4"
      >
        Réinitialiser les stats
      </button>
    </div>

    <!-- Log des événements -->
    <div class="events-log mt-6" v-if="eventLog.length > 0">
      <h3 class="text-lg font-semibold mb-3">
        Journal des Événements 
        <button @click="clearLog" class="btn btn-xs btn-outline ml-2">Effacer</button>
      </h3>
      <div class="bg-black text-green-400 p-4 rounded-lg max-h-64 overflow-y-auto font-mono text-sm">
        <div v-for="event in eventLog.slice(-20)" :key="event.id" class="mb-1">
          <span class="text-gray-500">[{{ formatTime(event.timestamp) }}]</span>
          <span :class="getEventClass(event.type)">{{ event.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import processService from '@/services/processService.js';

export default {
  name: 'ProcessCheckerDemo',
  setup() {
    const allProcesses = ref([]);
    const configInterval = ref(processService.config.checkInterval);
    const eventLog = ref([]);
    let eventIdCounter = 0;

    // Computed properties
    const uptimePercentage = computed(() => {
      if (processService.stats.totalChecks === 0) return 0;
      return Math.round((processService.stats.uptimeChecks / processService.stats.totalChecks) * 100);
    });

    const avgDuration = computed(() => {
      return Math.round(processService.stats.averageCheckDuration);
    });

    // Methods
    const addLogEvent = (type, message) => {
      eventLog.value.push({
        id: ++eventIdCounter,
        timestamp: new Date().toISOString(),
        type,
        message
      });
    };

    const checkProcess = async () => {
      addLogEvent('info', 'Démarrage de la vérification du processus...');
      try {
        const result = await processService.checkSatsukiProcess();
        addLogEvent(
          result.running ? 'success' : 'warning', 
          `Processus ${result.running ? 'trouvé' : 'non trouvé'}`
        );
        if (result.error) {
          addLogEvent('error', `Erreur: ${result.error}`);
        }
      } catch (error) {
        addLogEvent('error', `Erreur lors de la vérification: ${error.message}`);
      }
    };

    const getDetailedInfo = async () => {
      addLogEvent('info', 'Récupération des informations détaillées...');
      try {
        const result = await processService.getDetailedProcessInfo();
        addLogEvent('success', 'Informations détaillées récupérées');
      } catch (error) {
        addLogEvent('error', `Erreur: ${error.message}`);
      }
    };

    const getAllProcesses = async () => {
      addLogEvent('info', 'Récupération de tous les processus Satsuki...');
      try {
        const processes = await processService.getAllSatsukiProcesses();
        allProcesses.value = processes;
        addLogEvent('success', `${processes.length} processus trouvés`);
      } catch (error) {
        addLogEvent('error', `Erreur: ${error.message}`);
      }
    };

    const toggleMonitoring = () => {
      if (processService.monitoring.value) {
        processService.stopMonitoring();
        addLogEvent('warning', 'Surveillance arrêtée');
      } else {
        // Callback pour logger les événements de surveillance
        const monitoringCallback = (result) => {
          const status = result.running ? 'actif' : 'inactif';
          addLogEvent('info', `Surveillance: Satsuki.exe ${status}`);
        };
        
        processService.startMonitoring(configInterval.value, monitoringCallback);
        addLogEvent('success', 'Surveillance démarrée');
      }
    };

    const updateInterval = () => {
      processService.updateConfig({ checkInterval: configInterval.value });
      addLogEvent('info', `Intervalle mis à jour: ${configInterval.value}ms`);
    };

    const resetStats = () => {
      processService.resetStats();
      addLogEvent('warning', 'Statistiques réinitialisées');
    };

    const clearLog = () => {
      eventLog.value = [];
    };

    // Utility functions
    const formatTime = (isoString) => {
      if (!isoString) return 'Jamais';
      return new Date(isoString).toLocaleTimeString();
    };

    const formatKey = (key) => {
      const keyMap = {
        imageName: 'Nom d\'image',
        pid: 'PID',
        sessionName: 'Session',
        sessionNumber: 'N° Session',
        memoryUsage: 'Mémoire',
        processName: 'Processus',
        creationDate: 'Date création',
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

    const getEventClass = (type) => {
      const classes = {
        success: 'text-green-400',
        error: 'text-red-400',
        warning: 'text-yellow-400',
        info: 'text-blue-400'
      };
      return classes[type] || 'text-gray-400';
    };

    // Lifecycle
    onMounted(() => {
      addLogEvent('info', 'Composant ProcessChecker initialisé');
      // Vérification initiale
      checkProcess();
    });

    onUnmounted(() => {
      // S'assurer que la surveillance est arrêtée
      if (processService.monitoring.value) {
        processService.stopMonitoring();
      }
    });

    return {
      // Data
      processService,
      allProcesses,
      configInterval,
      eventLog,
      
      // Computed
      uptimePercentage,
      avgDuration,
      
      // Methods
      checkProcess,
      getDetailedInfo,
      getAllProcesses,
      toggleMonitoring,
      updateInterval,
      resetStats,
      clearLog,
      formatTime,
      formatKey,
      formatValue,
      getEventClass
    };
  }
};
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed;
}

.btn-secondary {
  @apply bg-gray-600 text-white hover:bg-gray-700;
}

.btn-success {
  @apply bg-green-600 text-white hover:bg-green-700;
}

.btn-error {
  @apply bg-red-600 text-white hover:bg-red-700;
}

.btn-outline {
  @apply border border-gray-400 text-gray-600 hover:bg-gray-50;
}

.status-card {
  @apply transition-all duration-200 hover:shadow-md;
}

.table {
  @apply w-full border-collapse;
}

.table th {
  @apply bg-gray-100 p-3 text-left font-semibold text-gray-700;
}

.table td {
  @apply p-3 border-t border-gray-200;
}

.table-zebra tbody tr:nth-child(even) {
  @apply bg-gray-50;
}

.stats {
  @apply bg-white border rounded-lg overflow-hidden;
}

.stat {
  @apply p-4 border-r border-gray-200 last:border-r-0 text-center;
}

.stat-title {
  @apply text-sm text-gray-600 font-medium;
}

.stat-value {
  @apply text-2xl font-bold text-gray-900 mt-1;
}

.stat-desc {
  @apply text-xs text-gray-500 mt-1;
}

.form-control {
  @apply mb-4;
}

.label {
  @apply flex justify-between items-center mb-2;
}

.label-text {
  @apply text-sm font-medium text-gray-700;
}

.input {
  @apply border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500;
}

.checkbox {
  @apply w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500;
}
</style>