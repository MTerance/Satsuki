using Godot;
using System;

namespace Satsuki.Scenes.Locations
{
    /// <summary>
    /// Interface de base pour toutes les locations du jeu
    /// Définit les fonctionnalités communes que chaque location doit implémenter
    /// </summary>
    public interface ILocation
    {
        #region Identification
        /// <summary>
        /// Nom unique de la location
        /// </summary>
        string LocationName { get; }

        /// <summary>
        /// Type de location (intérieur, extérieur, spécial, etc.)
        /// </summary>
        LocationType Type { get; }

        /// <summary>
        /// Description de la location
        /// </summary>
        string Description { get; }

        /// <summary>
        /// ID unique de la location pour le système de jeu
        /// </summary>
        string LocationId { get; }
        #endregion

        #region État et Statut
        /// <summary>
        /// Indique si la location est actuellement chargée et prête
        /// </summary>
        bool IsLoaded { get; }

        /// <summary>
        /// Indique si la location est accessible au joueur
        /// </summary>
        bool IsAccessible { get; }

        /// <summary>
        /// Retourne l'état complet de la location
        /// </summary>
        /// <returns>Objet contenant toutes les informations d'état</returns>
        object GetLocationState();
        #endregion

        #region Cycle de Vie
        /// <summary>
        /// Initialise la location
        /// </summary>
        void Initialize();

        /// <summary>
        /// Charge les ressources et éléments de la location
        /// </summary>
        void LoadLocation();

        /// <summary>
        /// Décharge la location et libère les ressources
        /// </summary>
        void UnloadLocation();

        /// <summary>
        /// Active la location (rend visible, démarre les systèmes)
        /// </summary>
        void ActivateLocation();

        /// <summary>
        /// Désactive la location (cache, arrête les systèmes)
        /// </summary>
        void DeactivateLocation();
        #endregion

        #region Gestion des Joueurs
        /// <summary>
        /// Appelé quand un joueur entre dans la location
        /// </summary>
        /// <param name="playerId">ID du joueur</param>
        void OnPlayerEnter(string playerId);

        /// <summary>
        /// Appelé quand un joueur quitte la location
        /// </summary>
        /// <param name="playerId">ID du joueur</param>
        void OnPlayerExit(string playerId);

        /// <summary>
        /// Obtient la liste des joueurs présents dans la location
        /// </summary>
        /// <returns>Liste des IDs des joueurs présents</returns>
        string[] GetPlayersInLocation();
        #endregion

        #region Interactions
        /// <summary>
        /// Obtient les objets interactables de la location
        /// </summary>
        /// <returns>Liste des objets avec lesquels le joueur peut interagir</returns>
        IInteractable[] GetInteractables();

        /// <summary>
        /// Traite une interaction dans la location
        /// </summary>
        /// <param name="playerId">ID du joueur qui interagit</param>
        /// <param name="interactionId">ID de l'interaction</param>
        /// <param name="data">Données additionnelles de l'interaction</param>
        void ProcessInteraction(string playerId, string interactionId, object data = null);
        #endregion

        #region Événements
        /// <summary>
        /// Événement déclenché quand la location est chargée
        /// </summary>
        event Action<ILocation> LocationLoaded;

        /// <summary>
        /// Événement déclenché quand la location est déchargée
        /// </summary>
        event Action<ILocation> LocationUnloaded;

        /// <summary>
        /// Événement déclenché quand un joueur entre dans la location
        /// </summary>
        event Action<ILocation, string> PlayerEntered;

        /// <summary>
        /// Événement déclenché quand un joueur quitte la location
        /// </summary>
        event Action<ILocation, string> PlayerExited;

        /// <summary>
        /// Événement déclenché lors d'une interaction dans la location
        /// </summary>
        event Action<ILocation, string, string> InteractionOccurred;
        #endregion

        #region Navigation
        /// <summary>
        /// Obtient les points de spawn disponibles dans la location
        /// </summary>
        /// <returns>Liste des positions de spawn</returns>
        Vector3[] GetSpawnPoints();

        /// <summary>
        /// Obtient la position de spawn par défaut
        /// </summary>
        /// <returns>Position par défaut où apparaître dans la location</returns>
        Vector3 GetDefaultSpawnPoint();

        /// <summary>
        /// Obtient les sorties disponibles de la location
        /// </summary>
        /// <returns>Dictionnaire des sorties (nom ? destination)</returns>
        System.Collections.Generic.Dictionary<string, string> GetExits();
        #endregion

        #region Configuration
        /// <summary>
        /// Configure la location avec des paramètres spécifiques
        /// </summary>
        /// <param name="config">Configuration à appliquer</param>
        void Configure(ILocationConfig config);

        /// <summary>
        /// Sauvegarde l'état actuel de la location
        /// </summary>
        /// <returns>Données d'état sérialisées</returns>
        object SaveLocationState();

        /// <summary>
        /// Restaure l'état de la location depuis des données sauvegardées
        /// </summary>
        /// <param name="stateData">Données d'état à restaurer</param>
        void RestoreLocationState(object stateData);
        #endregion
    }

    /// <summary>
    /// Énumération des types de locations
    /// </summary>
    public enum LocationType
    {
        /// <summary>
        /// Location d'intérieur (maison, bâtiment, etc.)
        /// </summary>
        Interior,

        /// <summary>
        /// Location d'extérieur (rue, parc, etc.)
        /// </summary>
        Exterior,

        /// <summary>
        /// Location spéciale (donjon, zone secrète, etc.)
        /// </summary>
        Special,

        /// <summary>
        /// Location de transition (couloir, ascenseur, etc.)
        /// </summary>
        Transition,

        /// <summary>
        /// Location de combat
        /// </summary>
        Combat,

        /// <summary>
        /// Location sociale (café, place publique, etc.)
        /// </summary>
        Social,

        /// <summary>
        /// Location de magasin/commerce
        /// </summary>
        Shop,

        /// <summary>
        /// Location de base/refuge du joueur
        /// </summary>
        Home
    }

    /// <summary>
    /// Interface pour les objets interactables dans une location
    /// </summary>
    public interface IInteractable
    {
        /// <summary>
        /// ID unique de l'objet interactable
        /// </summary>
        string InteractableId { get; }

        /// <summary>
        /// Nom affiché à l'utilisateur
        /// </summary>
        string DisplayName { get; }

        /// <summary>
        /// Description de l'interaction possible
        /// </summary>
        string InteractionDescription { get; }

        /// <summary>
        /// Indique si l'objet est actuellement interactable
        /// </summary>
        bool IsInteractable { get; }

        /// <summary>
        /// Position de l'objet dans la location
        /// </summary>
        Vector3 Position { get; }

        /// <summary>
        /// Exécute l'interaction avec l'objet
        /// </summary>
        /// <param name="playerId">ID du joueur qui interagit</param>
        /// <param name="data">Données additionnelles</param>
        /// <returns>Résultat de l'interaction</returns>
        object Interact(string playerId, object data = null);

        /// <summary>
        /// Événement déclenché lors d'une interaction
        /// </summary>
        event Action<IInteractable, string> Interacted;
    }

    /// <summary>
    /// Interface pour la configuration d'une location
    /// </summary>
    public interface ILocationConfig
    {
        /// <summary>
        /// Paramètres d'ambiance (éclairage, son, etc.)
        /// </summary>
        object AmbianceSettings { get; }

        /// <summary>
        /// Paramètres de gameplay spécifiques
        /// </summary>
        object GameplaySettings { get; }

        /// <summary>
        /// Ressources à précharger
        /// </summary>
        string[] PreloadResources { get; }

        /// <summary>
        /// Indique si la location doit être sauvegardée automatiquement
        /// </summary>
        bool AutoSave { get; }

        /// <summary>
        /// Capacité maximale de joueurs
        /// </summary>
        int MaxPlayers { get; }
    }
}