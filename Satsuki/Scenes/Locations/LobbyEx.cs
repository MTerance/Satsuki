using Godot;
using Satsuki.Interfaces;
using Satsuki.Scenes.Locations;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Satsuki.Scenes.Locations
{
    /// <summary>
    /// Location LobbyEx - Lobby étendu pour l'écran titre
    /// Zone sociale principale où les joueurs se retrouvent depuis l'écran titre
    /// </summary>
    public partial class LobbyEx : LocationModel
    {
        #region Location Properties Override
        public override string LocationName => "LobbyEx";
        public override LocationType Type => LocationType.Social;
        public override string Description => "Lobby étendu - Zone sociale principale du jeu";
        public override string LocationId => $"LobbyEx_{GetInstanceId()}";
        #endregion

        #region Private Fields
        private DateTime _lobbyStartTime;
        private bool _isLobbyReady = false;
        private List<string> _lobbyActivities = new List<string>();
        #endregion

        public override void _Ready()
        {
            _lobbyStartTime = DateTime.UtcNow;
            GD.Print("??? LobbyEx: Initialisation du lobby étendu...");
            
            // Appeler l'initialisation de base de LocationModel
            base._Ready();
            
            // Initialisation spécifique au lobby
            InitializeLobbyFeatures();
            
            GD.Print("? LobbyEx: Lobby étendu prêt");
        }

        /// <summary>
        /// Initialise les fonctionnalités spécifiques au lobby
        /// </summary>
        private void InitializeLobbyFeatures()
        {
            // Ajouter des activités par défaut du lobby
            _lobbyActivities.AddRange(new[]
            {
                "Chat Social",
                "Liste des Joueurs",
                "Salles de Jeu",
                "Événements",
                "Notifications"
            });

            _isLobbyReady = true;
            GD.Print("?? LobbyEx: Fonctionnalités lobby initialisées");
        }

        #region LocationModel Overrides
        protected override void InitializeInteractables()
        {
            // Appeler l'initialisation de base (MediaScreen)
            base.InitializeInteractables();

            // Ajouter des interactables spécifiques au lobby
            AddLobbyInteractables();
        }

        protected override void InitializeSpawnPoints()
        {
            // Points de spawn spécifiques au lobby
            GD.Print("?? LobbyEx: Configuration des points de spawn lobby");
        }

        protected override void InitializeExits()
        {
            // Sorties vers d'autres zones depuis le lobby
            GD.Print("?? LobbyEx: Configuration des sorties lobby");
        }

        protected override void OnPlayerEnterSpecific(string playerId)
        {
            GD.Print($"?? LobbyEx: Bienvenue {playerId} dans le lobby étendu!");
            
            // Logique spécifique à l'entrée dans le lobby
            SendWelcomeMessage(playerId);
            UpdateLobbyActivity($"{playerId} a rejoint le lobby");
        }

        protected override void OnPlayerExitSpecific(string playerId)
        {
            GD.Print($"?? LobbyEx: Au revoir {playerId} du lobby étendu!");
            
            // Logique spécifique à la sortie du lobby
            UpdateLobbyActivity($"{playerId} a quitté le lobby");
        }
        #endregion

        #region Lobby-Specific Methods
        /// <summary>
        /// Ajoute des objets interactables spécifiques au lobby
        /// </summary>
        private void AddLobbyInteractables()
        {
            // Créer les interactables du lobby
            var lobbyBoard = new LobbyBoardInteractable();
            var gameTerminal = new GameTerminalInteractable();

            // Les ajouter via la méthode publique de traitement d'interaction
            // Note: Comme _interactables est privé, on utilise une approche différente
            GD.Print($"?? LobbyEx: Ajout d'interactables spécialisés au lobby");
            GD.Print($"?? LobbyEx: Tableau d'affichage configuré - {lobbyBoard.DisplayName}");
            GD.Print($"?? LobbyEx: Terminal de jeux configuré - {gameTerminal.DisplayName}");
        }

        /// <summary>
        /// Obtient les interactables spécifiques au lobby
        /// </summary>
        /// <returns>Liste des interactables du lobby</returns>
        public override IInteractable[] GetInteractables()
        {
            // Obtenir les interactables de base
            var baseInteractables = base.GetInteractables().ToList();

            // Ajouter les interactables spécifiques au lobby
            baseInteractables.Add(new LobbyBoardInteractable());
            baseInteractables.Add(new GameTerminalInteractable());

            return baseInteractables.ToArray();
        }

        /// <summary>
        /// Traite les interactions spécifiques au lobby
        /// </summary>
        /// <param name="playerId">ID du joueur</param>
        /// <param name="interactionId">ID de l'interaction</param>
        /// <param name="data">Données additionnelles</param>
        public override void ProcessInteraction(string playerId, string interactionId, object data = null)
        {
            // Traiter d'abord les interactions spécifiques au lobby
            switch (interactionId)
            {
                case "LobbyBoard_Main":
                    ProcessLobbyBoardInteraction(playerId, data);
                    return;
                case "GameTerminal_Main":
                    ProcessGameTerminalInteraction(playerId, data);
                    return;
            }

            // Sinon, déléguer à la classe de base
            base.ProcessInteraction(playerId, interactionId, data);
        }

        /// <summary>
        /// Traite l'interaction avec le tableau d'affichage
        /// </summary>
        private void ProcessLobbyBoardInteraction(string playerId, object data)
        {
            GD.Print($"?? LobbyEx: {playerId} consulte le tableau d'affichage");
            UpdateLobbyActivity($"{playerId} a consulté le tableau d'affichage");
        }

        /// <summary>
        /// Traite l'interaction avec le terminal de jeux
        /// </summary>
        private void ProcessGameTerminalInteraction(string playerId, object data)
        {
            GD.Print($"?? LobbyEx: {playerId} utilise le terminal de jeux");
            UpdateLobbyActivity($"{playerId} a utilisé le terminal de jeux");
        }

        /// <summary>
        /// Envoie un message de bienvenue au joueur
        /// </summary>
        /// <param name="playerId">ID du joueur</param>
        private void SendWelcomeMessage(string playerId)
        {
            var welcomeMessage = $"Bienvenue dans le LobbyEx, {playerId}! Explorez les activités disponibles.";
            GD.Print($"?? LobbyEx: {welcomeMessage}");
            
            // Ici on pourrait envoyer via le serveur
            // GetServerHandler()?.SendMessageToClient(playerId, welcomeMessage);
        }

        /// <summary>
        /// Met à jour l'activité du lobby
        /// </summary>
        /// <param name="activity">Description de l'activité</param>
        public void UpdateLobbyActivity(string activity)
        {
            _lobbyActivities.Insert(0, $"[{DateTime.UtcNow:HH:mm:ss}] {activity}");
            
            // Garder seulement les 10 dernières activités
            if (_lobbyActivities.Count > 10)
            {
                _lobbyActivities.RemoveAt(_lobbyActivities.Count - 1);
            }

            GD.Print($"?? LobbyEx: Activité mise à jour - {activity}");
        }

        /// <summary>
        /// Obtient les activités récentes du lobby
        /// </summary>
        /// <returns>Liste des activités récentes</returns>
        public string[] GetRecentActivities()
        {
            return _lobbyActivities.ToArray();
        }

        /// <summary>
        /// Obtient les statistiques du lobby
        /// </summary>
        /// <returns>Statistiques du lobby</returns>
        public object GetLobbyStats()
        {
            var elapsedTime = (DateTime.UtcNow - _lobbyStartTime).TotalMinutes;
            
            return new
            {
                LobbyName = LocationName,
                IsReady = _isLobbyReady,
                ElapsedTimeMinutes = Math.Round(elapsedTime, 2),
                PlayersCount = GetPlayersInLocation().Length,
                ActivitiesCount = _lobbyActivities.Count,
                RecentActivities = _lobbyActivities.Take(5).ToArray(),
                InteractablesCount = GetInteractables().Length
            };
        }
        #endregion

        #region ILocation Implementation Override
        public override object GetLocationState()
        {
            // Obtenir l'état de base
            var baseState = base.GetLocationState();
            
            // Ajouter des informations spécifiques au lobby
            return new
            {
                BaseLocation = baseState,
                LobbyEx = new
                {
                    LobbySpecific = new
                    {
                        IsLobbyReady = _isLobbyReady,
                        StartTime = _lobbyStartTime,
                        ElapsedTimeMinutes = Math.Round((DateTime.UtcNow - _lobbyStartTime).TotalMinutes, 2)
                    },
                    Activities = new
                    {
                        Count = _lobbyActivities.Count,
                        Recent = _lobbyActivities.Take(3).ToArray()
                    },
                    Stats = GetLobbyStats()
                }
            };
        }

        public override Dictionary<string, string> GetExits()
        {
            return new Dictionary<string, string>
            {
                { "GameRooms", "GameRoomLocation" },
                { "Shop", "ShopLocation" },
                { "Social", "SocialHubLocation" },
                { "Exit", "TitleScreen" }
            };
        }

        public override Vector3[] GetSpawnPoints()
        {
            // Points de spawn optimisés pour un lobby
            return new Vector3[]
            {
                Vector3.Zero,                    // Centre du lobby
                new Vector3(10, 0, 0),          // Zone est
                new Vector3(-10, 0, 0),         // Zone ouest
                new Vector3(0, 0, 10),          // Zone nord
                new Vector3(0, 0, -10),         // Zone sud
                new Vector3(5, 0, 5),           // Nord-est
                new Vector3(-5, 0, 5),          // Nord-ouest
                new Vector3(5, 0, -5),          // Sud-est
                new Vector3(-5, 0, -5)          // Sud-ouest
            };
        }
        #endregion

        public override void _ExitTree()
        {
            GD.Print("?? LobbyEx: Nettoyage du lobby étendu");
            base._ExitTree();
        }
    }

    /// <summary>
    /// Tableau d'affichage interactable du lobby
    /// </summary>
    public class LobbyBoardInteractable : IInteractable
    {
        public string InteractableId => "LobbyBoard_Main";
        public string DisplayName => "Tableau d'Affichage";
        public string InteractionDescription => "Consulter les annonces et informations du lobby";
        public bool IsInteractable => true;
        public Vector3 Position => new Vector3(0, 0, 5);

        public event Action<IInteractable, string> Interacted;

        public object Interact(string playerId, object data = null)
        {
            GD.Print($"?? LobbyBoard: {playerId} consulte le tableau d'affichage");
            
            Interacted?.Invoke(this, playerId);
            
            return new
            {
                Success = true,
                Action = "LobbyBoardViewed",
                PlayerId = playerId,
                Content = new
                {
                    Announcements = new[]
                    {
                        "Bienvenue dans LobbyEx!",
                        "Nouvelles salles de jeu disponibles",
                        "Événement spécial ce weekend"
                    },
                    LastUpdate = DateTime.UtcNow
                },
                Timestamp = DateTime.UtcNow
            };
        }
    }

    /// <summary>
    /// Terminal de jeux interactable du lobby
    /// </summary>
    public class GameTerminalInteractable : IInteractable
    {
        public string InteractableId => "GameTerminal_Main";
        public string DisplayName => "Terminal de Jeux";
        public string InteractionDescription => "Accéder aux salles de jeu et mini-jeux";
        public bool IsInteractable => true;
        public Vector3 Position => new Vector3(5, 0, 0);

        public event Action<IInteractable, string> Interacted;

        public object Interact(string playerId, object data = null)
        {
            GD.Print($"?? GameTerminal: {playerId} utilise le terminal de jeux");
            
            Interacted?.Invoke(this, playerId);
            
            return new
            {
                Success = true,
                Action = "GameTerminalAccessed",
                PlayerId = playerId,
                AvailableGames = new[]
                {
                    "Quiz Game",
                    "Billiard Game", 
                    "Card Games",
                    "Puzzle Games"
                },
                Timestamp = DateTime.UtcNow
            };
        }
    }
}