using Godot;
using Satsuki.Networks;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Satsuki.Utils
{
    /// <summary>
    /// Utilitaires serveur pour l'envoi de messages, l'état du serveur et la gestion du cryptage.
    /// </summary>
    public static class ServerUtils
    {
        private static bool _debugMode = true;

        /// <summary>
        /// Active ou désactive le mode debug des logs serveur.
        /// </summary>
        public static void SetDebugMode(bool enabled)
        {
            _debugMode = enabled;
        }

        #region Client Communication
        /// <summary>
        /// Envoie un message à un client spécifique avec cryptage optionnel.
        /// </summary>
        public static async Task<bool> SendMessageToClient(string clientId, string message, bool encrypt = true)
        {
            bool success = await MessageReceiver.GetInstance.SendMessageToClient(clientId, message, encrypt);
            if (_debugMode)
            {
                if (!success)
                    GD.PrintErr($"ServerUtils: Échec envoi message à {clientId}");
                else if (encrypt)
                    GD.Print($"ServerUtils: Message crypté envoyé à {clientId}");
            }
            return success;
        }

        /// <summary>
        /// Diffuse un message à tous les clients avec cryptage optionnel.
        /// </summary>
        public static async Task BroadcastToAllClients(string message, bool encrypt = true)
        {
            await MessageReceiver.GetInstance.BroadcastMessage(message, encrypt);
            if (_debugMode)
            {
                string status = encrypt ? "crypté" : "clair";
                GD.Print($"ServerUtils: Message {status} diffusé: {message}");
            }
        }

        /// <summary>
        /// Diffuse un message à tous les clients sauf l'expéditeur avec cryptage optionnel.
        /// </summary>
        public static async Task BroadcastToOtherClients(string senderClientId, string message, bool encrypt = true)
        {
            var clients = MessageReceiver.GetInstance.GetConnectedClientIds();
            foreach (string clientId in clients)
            {
                if (clientId != senderClientId)
                {
                    await MessageReceiver.GetInstance.SendMessageToClient(clientId, message, encrypt);
                }
            }
            if (_debugMode)
            {
                string status = encrypt ? "crypté" : "clair";
                GD.Print($"ServerUtils: Message {status} diffusé à {Math.Max(0, clients.Count - 1)} autres clients");
            }
        }

        /// <summary>
        /// Déconnecte un client spécifique.
        /// </summary>
        public static async Task DisconnectClient(string clientId)
        {
            await MessageReceiver.GetInstance.RemoveClient(clientId);
            if (_debugMode)
            {
                GD.Print($"ServerUtils: Client {clientId} déconnecté");
            }
        }
        #endregion

        #region Server Information
        /// <summary>
        /// Obtient le nombre de clients connectés.
        /// </summary>
        public static int GetConnectedClientCount()
        {
            return MessageReceiver.GetInstance.GetConnectedClientIds().Count;
        }

        /// <summary>
        /// Obtient la liste des clients connectés.
        /// </summary>
        public static List<string> GetConnectedClientIds()
        {
            return MessageReceiver.GetInstance.GetConnectedClientIds();
        }

        /// <summary>
        /// Affiche la liste des clients connectés dans la sortie.
        /// </summary>
        public static void ListConnectedClients()
        {
            var clients = MessageReceiver.GetInstance.GetConnectedClientIds();
            GD.Print($"ServerUtils: Clients connectés: {string.Join(", ", clients)}");
        }

        /// <summary>
        /// Obtient l'état complet du serveur et des informations de la scène de jeu fournie.
        /// </summary>
        public static object GetCompleteGameState(Node gameScene)
        {
            var serverState = GetServerState();
            object gameSceneState = null;

            if (gameScene != null)
            {
                try
                {
                    gameSceneState = new
                    {
                        gameScene.Name,
                        Type = gameScene.GetType().Name,
                        ChildCount = gameScene.GetChildCount()
                    };
                }
                catch (Exception ex)
                {
                    GD.PrintErr($"ServerUtils: Erreur récupération état scène: {ex.Message}");
                    gameSceneState = new { Error = "Failed to get game scene state", Message = ex.Message };
                }
            }

            return new
            {
                ServerState = serverState,
                GameSceneState = gameSceneState,
                Timestamp = DateTime.UtcNow
            };
        }

        /// <summary>
        /// Obtient l'état complet du serveur.
        /// </summary>
        public static object GetServerState()
        {
            var stats = MessageReceiver.GetInstance.GetStatistics();
            var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
            var connectedClients = MessageReceiver.GetInstance.GetConnectedClientIds();
            var network = Network.GetInstance;

            return new
            {
                Server = new
                {
                    IsRunning = stats.isRunning,
                    ConnectedClients = stats.connectedClients,
                    PendingMessages = stats.pendingMessages
                },
                Encryption = new
                {
                    Enabled = stats.encryptionEnabled,
                    KeyPreview = encInfo.keyBase64?.Substring(0, Math.Min(10, encInfo.keyBase64?.Length ?? 0)) ?? "N/A",
                    IVPreview = encInfo.ivBase64?.Substring(0, Math.Min(10, encInfo.ivBase64?.Length ?? 0)) ?? "N/A"
                },
                Clients = connectedClients.Select(id => new
                {
                    Id = id,
                    Status = "Connected",
                    Type = network.GetClientType(id) ?? "UNKNOWN"
                }).ToList(),
                Debug = new
                {
                    DebugMode = _debugMode,
                    Timestamp = DateTime.UtcNow
                }
            };
        }
        #endregion

        #region Cryptography
        /// <summary>
        /// Bascule le cryptage des messages on/off.
        /// </summary>
        public static void ToggleEncryption()
        {
            var encInfo = MessageReceiver.GetInstance.GetEncryptionInfo();
            MessageReceiver.GetInstance.ConfigureEncryption(!encInfo.enabled);
            GD.Print($"ServerUtils: Cryptage basculé {(!encInfo.enabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");
        }

        /// <summary>
        /// Génère une nouvelle clé de cryptage.
        /// </summary>
        public static void GenerateNewEncryptionKey()
        {
            MessageReceiver.GetInstance.GenerateNewEncryptionKey();
            GD.Print("ServerUtils: Nouvelle clé de cryptage générée");
        }
        #endregion
    }
}
