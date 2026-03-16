import { ref, reactive } from 'vue';

class ProcessService {
    constructor() {
        // États réactifs
        this.isRunning = ref(false);
        this.processInfo = ref(null);
        this.lastCheck = ref(null);
        this.error = ref(null);
        this.isChecking = ref(false);
        
        // Monitoring
        this.monitoring = ref(false);
        this.monitoringInterval = null;
        this.monitoringCallbacks = [];
        
        // Statistiques
        this.stats = reactive({
            totalChecks: 0,
            successfulChecks: 0,
            failedChecks: 0,
            uptimeChecks: 0,
            lastSuccessfulCheck: null,
            averageCheckDuration: 0
        });
        
        // Configuration
        this.config = reactive({
            checkInterval: 5000, // 5 secondes par défaut
            autoStart: false,
            enableDetailedInfo: true
        });
    }

    /**
     * Vérifie si Satsuki.exe est en cours d'exécution
     * @returns {Promise<Object>}
     */
    async checkSatsukiProcess() {
        if (this.isChecking.value) {
            console.warn('Vérification déjà en cours...');
            return this.getCurrentState();
        }

        this.isChecking.value = true;
        this.error.value = null;
        const startTime = Date.now();
        
        try {
            // Vérifier si l'API est disponible
            if (!window.processChecker) {
                throw new Error('API processChecker non disponible. Vérifiez que l\'application Electron est correctement configurée.');
            }

            const result = await window.processChecker.checkSatsuki();
            
            // Mettre à jour les états
            this.isRunning.value = result.running;
            this.processInfo.value = result.processInfo;
            this.lastCheck.value = new Date().toISOString();
            this.error.value = result.error;
            
            // Mettre à jour les statistiques
            this.stats.totalChecks++;
            this.stats.successfulChecks++;
            if (result.running) {
                this.stats.uptimeChecks++;
            }
            this.stats.lastSuccessfulCheck = this.lastCheck.value;
            
            const duration = Date.now() - startTime;
            this.stats.averageCheckDuration = 
                (this.stats.averageCheckDuration * (this.stats.successfulChecks - 1) + duration) / this.stats.successfulChecks;
            
            // Notifier les callbacks de monitoring
            this._notifyMonitoringCallbacks(result);
            
            return result;
            
        } catch (error) {
            this.error.value = error.message;
            this.isRunning.value = false;
            this.processInfo.value = null;
            this.stats.totalChecks++;
            this.stats.failedChecks++;
            
            console.error('Erreur lors de la vérification du processus Satsuki:', error);
            
            const errorResult = {
                running: false,
                processInfo: null,
                error: error.message
            };
            
            this._notifyMonitoringCallbacks(errorResult);
            
            return errorResult;
        } finally {
            this.isChecking.value = false;
        }
    }

    /**
     * Obtient des informations détaillées sur le processus Satsuki
     * @returns {Promise<Object>}
     */
    async getDetailedProcessInfo() {
        if (!this.config.enableDetailedInfo) {
            console.warn('Les informations détaillées sont désactivées');
            return await this.checkSatsukiProcess();
        }

        this.isChecking.value = true;
        
        try {
            if (!window.processChecker) {
                throw new Error('API processChecker non disponible');
            }

            const result = await window.processChecker.getDetailedInfo();
            
            this.isRunning.value = result.running;
            this.processInfo.value = result.processInfo;
            this.lastCheck.value = new Date().toISOString();
            this.error.value = result.error;
            
            return result;
            
        } catch (error) {
            this.error.value = error.message;
            console.error('Erreur lors de l\'obtention des informations détaillées:', error);
            throw error;
        } finally {
            this.isChecking.value = false;
        }
    }

    /**
     * Obtient tous les processus Satsuki en cours
     * @returns {Promise<Array>}
     */
    async getAllSatsukiProcesses() {
        try {
            if (!window.processChecker) {
                throw new Error('API processChecker non disponible');
            }

            return await window.processChecker.getAllSatsukiProcesses();
            
        } catch (error) {
            console.error('Erreur lors de l\'obtention de tous les processus Satsuki:', error);
            throw error;
        }
    }

    /**
     * Démarre la surveillance périodique du processus Satsuki
     * @param {number} interval - Intervalle en millisecondes (optionnel)
     * @param {Function} callback - Fonction appelée à chaque vérification (optionnel)
     */
    startMonitoring(interval = null, callback = null) {
        if (this.monitoring.value) {
            console.warn('La surveillance est déjà en cours');
            return;
        }

        const checkInterval = interval || this.config.checkInterval;
        
        if (callback && typeof callback === 'function') {
            this.monitoringCallbacks.push(callback);
        }

        this.monitoring.value = true;
        
        // Première vérification immédiate
        this.checkSatsukiProcess();
        
        // Démarrer la surveillance périodique
        this.monitoringInterval = setInterval(() => {
            this.checkSatsukiProcess();
        }, checkInterval);
        
        console.log(`Surveillance Satsuki démarrée (intervalle: ${checkInterval}ms)`);
    }

    /**
     * Arrête la surveillance périodique
     */
    stopMonitoring() {
        if (!this.monitoring.value) {
            console.warn('Aucune surveillance en cours');
            return;
        }

        if (this.monitoringInterval) {
            clearInterval(this.monitoringInterval);
            this.monitoringInterval = null;
        }
        
        this.monitoring.value = false;
        console.log('Surveillance Satsuki arrêtée');
    }

    /**
     * Ajoute un callback de surveillance
     * @param {Function} callback - Fonction appelée à chaque vérification
     */
    addMonitoringCallback(callback) {
        if (typeof callback === 'function') {
            this.monitoringCallbacks.push(callback);
        }
    }

    /**
     * Supprime un callback de surveillance
     * @param {Function} callback - Fonction à supprimer
     */
    removeMonitoringCallback(callback) {
        const index = this.monitoringCallbacks.indexOf(callback);
        if (index > -1) {
            this.monitoringCallbacks.splice(index, 1);
        }
    }

    /**
     * Notifie tous les callbacks de surveillance
     * @private
     */
    _notifyMonitoringCallbacks(result) {
        this.monitoringCallbacks.forEach(callback => {
            try {
                callback(result);
            } catch (error) {
                console.error('Erreur dans le callback de surveillance:', error);
            }
        });
    }

    /**
     * Obtient l'état actuel du service
     * @returns {Object}
     */
    getCurrentState() {
        return {
            running: this.isRunning.value,
            processInfo: this.processInfo.value,
            lastCheck: this.lastCheck.value,
            error: this.error.value,
            isChecking: this.isChecking.value,
            monitoring: this.monitoring.value,
            stats: { ...this.stats },
            config: { ...this.config }
        };
    }

    /**
     * Réinitialise les statistiques
     */
    resetStats() {
        this.stats.totalChecks = 0;
        this.stats.successfulChecks = 0;
        this.stats.failedChecks = 0;
        this.stats.uptimeChecks = 0;
        this.stats.lastSuccessfulCheck = null;
        this.stats.averageCheckDuration = 0;
    }

    /**
     * Met à jour la configuration
     * @param {Object} newConfig - Nouvelle configuration
     */
    updateConfig(newConfig) {
        Object.assign(this.config, newConfig);
        
        // Si la surveillance est en cours et l'intervalle a changé, redémarrer
        if (this.monitoring.value && newConfig.checkInterval && newConfig.checkInterval !== this.config.checkInterval) {
            this.stopMonitoring();
            this.startMonitoring(newConfig.checkInterval);
        }
    }

    /**
     * Obtient des informations de diagnostic sur le service
     * @returns {Object}
     */
    getDiagnosticInfo() {
        return {
            serviceState: this.getCurrentState(),
            apiAvailable: !!window.processChecker,
            browserInfo: {
                userAgent: navigator.userAgent,
                platform: navigator.platform
            },
            timestamps: {
                serviceCreated: new Date().toISOString(),
                lastCheck: this.lastCheck.value
            }
        };
    }
}

// Export singleton instance
export default new ProcessService();