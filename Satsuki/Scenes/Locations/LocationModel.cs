using Godot;
using Satsuki.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Satsuki.Scenes.Locations
{
    /// <summary>
    /// Modèle de base pour les locations du jeu
    /// Implémente ILocation et IScene pour une intégration complète
    /// </summary>
    public partial class LocationModel : Node3D, ILocation, IScene
    {
        #region Private Fields
        private bool _hasInitialized = false;
        private bool _isLoaded = false;
        private bool _isAccessible = true;
        private DateTime _loadTime;
        private List<string> _playersInLocation = new List<string>();
        private List<IInteractable> _interactables = new List<IInteractable>();
        #endregion

        #region ILocation Properties
        /// <summary>
        /// Nom unique de la location
        /// </summary>
        public virtual string LocationName => GetType().Name;

        /// <summary>
        /// Type de location
        /// </summary>
        public virtual LocationType Type => LocationType.Special;

        /// <summary>
        /// Description de la location
        /// </summary>
        public virtual string Description => "Location de base du jeu";

        /// <summary>
        /// ID unique de la location
        /// </summary>
        public virtual string LocationId => $"{LocationName}_{GetInstanceId()}";

        /// <summary>
        /// Indique si la location est chargée
        /// </summary>
        public bool IsLoaded => _isLoaded;

        /// <summary>
        /// Indique si la location est accessible
        /// </summary>
        public bool IsAccessible => _isAccessible;
        #endregion

        #region ILocation Events
        public event Action<ILocation> LocationLoaded;
        public event Action<ILocation> LocationUnloaded;
        public event Action<ILocation, string> PlayerEntered;
        public event Action<ILocation, string> PlayerExited;
        public event Action<ILocation, string, string> InteractionOccurred;
        #endregion

        #region Godot Lifecycle
        public override void _Ready()
        {
            _loadTime = DateTime.UtcNow;
            
            GD.Print($"🏗️ LocationModel: Initialisation de {LocationName}...");
            
            // Initialiser la location
            Initialize();
            
            // Charger la location
            LoadLocation();
            
            // Setup spécifique MediaScreen (code existant)
            CallDeferred(nameof(InitializeMediaScreen));
        }

        public override void _ExitTree()
        {
            // Décharger la location
            UnloadLocation();
            
            GD.Print($"🧹 LocationModel: Nettoyage de {LocationName} terminé");
        }
        #endregion

        #region ILocation Implementation - Cycle de Vie
        /// <summary>
        /// Initialise la location
        /// </summary>
        public virtual void Initialize()
        {
            if (_hasInitialized) return;

            GD.Print($"🔧 {LocationName}: Initialisation...");

            // Initialiser les systèmes de base
            InitializeInteractables();
            InitializeSpawnPoints();
            InitializeExits();

            _hasInitialized = true;
            GD.Print($"✅ {LocationName}: Initialisé");
        }

        /// <summary>
        /// Charge la location
        /// </summary>
        public virtual void LoadLocation()
        {
            if (_isLoaded) return;

            GD.Print($"📦 {LocationName}: Chargement...");

            // Charger les ressources
            LoadResources();
            
            // Activer les systèmes
            ActivateLocation();

            _isLoaded = true;
            LocationLoaded?.Invoke(this);
            
            GD.Print($"✅ {LocationName}: Chargé");
        }

        /// <summary>
        /// Décharge la location
        /// </summary>
        public virtual void UnloadLocation()
        {
            if (!_isLoaded) return;

            GD.Print($"🗑️ {LocationName}: Déchargement...");

            // Désactiver les systèmes
            DeactivateLocation();

            // Nettoyer les joueurs
            var playersToRemove = _playersInLocation.ToArray();
            foreach (var playerId in playersToRemove)
            {
                OnPlayerExit(playerId);
            }

            _isLoaded = false;
            LocationUnloaded?.Invoke(this);
            
            GD.Print($"🧹 {LocationName}: Déchargé");
        }

        /// <summary>
        /// Active la location
        /// </summary>
        public virtual void ActivateLocation()
        {
            GD.Print($"⚡ {LocationName}: Activation...");
            
            // Activer les objets interactables
            foreach (var interactable in _interactables)
            {
                // Logique d'activation si nécessaire
            }

            // Rendre visible
            Visible = true;
            ProcessMode = ProcessModeEnum.Inherit;
        }

        /// <summary>
        /// Désactive la location
        /// </summary>
        public virtual void DeactivateLocation()
        {
            GD.Print($"💤 {LocationName}: Désactivation...");
            
            // Désactiver les systèmes actifs
            // Cacher la location
            Visible = false;
            ProcessMode = ProcessModeEnum.Disabled;
        }
        #endregion

        #region ILocation Implementation - Gestion des Joueurs
        /// <summary>
        /// Appelé quand un joueur entre dans la location
        /// </summary>
        public virtual void OnPlayerEnter(string playerId)
        {
            if (_playersInLocation.Contains(playerId)) return;

            GD.Print($"👤 {LocationName}: Joueur {playerId} entre");
            
            _playersInLocation.Add(playerId);
            PlayerEntered?.Invoke(this, playerId);

            // Logique spécifique à l'entrée du joueur
            OnPlayerEnterSpecific(playerId);
        }

        /// <summary>
        /// Appelé quand un joueur quitte la location
        /// </summary>
        public virtual void OnPlayerExit(string playerId)
        {
            if (!_playersInLocation.Contains(playerId)) return;

            GD.Print($"👤 {LocationName}: Joueur {playerId} sort");
            
            _playersInLocation.Remove(playerId);
            PlayerExited?.Invoke(this, playerId);

            // Logique spécifique à la sortie du joueur
            OnPlayerExitSpecific(playerId);
        }

        /// <summary>
        /// Obtient les joueurs dans la location
        /// </summary>
        public virtual string[] GetPlayersInLocation()
        {
            return _playersInLocation.ToArray();
        }
        #endregion

        #region ILocation Implementation - Interactions
        /// <summary>
        /// Obtient les objets interactables
        /// </summary>
        public virtual IInteractable[] GetInteractables()
        {
            return _interactables.ToArray();
        }

        /// <summary>
        /// Traite une interaction
        /// </summary>
        public virtual void ProcessInteraction(string playerId, string interactionId, object data = null)
        {
            GD.Print($"🤝 {LocationName}: Interaction {interactionId} par {playerId}");

            var interactable = _interactables.FirstOrDefault(i => i.InteractableId == interactionId);
            if (interactable != null && interactable.IsInteractable)
            {
                var result = interactable.Interact(playerId, data);
                InteractionOccurred?.Invoke(this, playerId, interactionId);

                // Traiter le résultat de l'interaction
                ProcessInteractionResult(playerId, interactionId, result);
            }
            else
            {
                GD.PrintErr($"❌ {LocationName}: Interaction {interactionId} introuvable ou non disponible");
            }
        }
        #endregion

        #region ILocation Implementation - Navigation
        /// <summary>
        /// Obtient les points de spawn
        /// </summary>
        public virtual Vector3[] GetSpawnPoints()
        {
            // Points de spawn par défaut
            return new Vector3[]
            {
                Vector3.Zero,
                new Vector3(5, 0, 0),
                new Vector3(-5, 0, 0),
                new Vector3(0, 0, 5),
                new Vector3(0, 0, -5)
            };
        }

        /// <summary>
        /// Obtient le point de spawn par défaut
        /// </summary>
        public virtual Vector3 GetDefaultSpawnPoint()
        {
            return Vector3.Zero;
        }

        /// <summary>
        /// Obtient les sorties de la location
        /// </summary>
        public virtual Dictionary<string, string> GetExits()
        {
            return new Dictionary<string, string>
            {
                { "North", "NorthLocation" },
                { "South", "SouthLocation" },
                { "East", "EastLocation" },
                { "West", "WestLocation" }
            };
        }
        #endregion

        #region ILocation Implementation - Configuration
        /// <summary>
        /// Configure la location
        /// </summary>
        public virtual void Configure(ILocationConfig config)
        {
            if (config == null) return;

            GD.Print($"⚙️ {LocationName}: Application de la configuration");

            // Appliquer les paramètres d'ambiance
            ApplyAmbianceSettings(config.AmbianceSettings);

            // Appliquer les paramètres de gameplay
            ApplyGameplaySettings(config.GameplaySettings);

            // Précharger les ressources
            PreloadResources(config.PreloadResources);
        }

        /// <summary>
        /// Sauvegarde l'état de la location
        /// </summary>
        public virtual object SaveLocationState()
        {
            return new
            {
                LocationId = LocationId,
                LocationName = LocationName,
                Type = Type.ToString(),
                IsLoaded = _isLoaded,
                IsAccessible = _isAccessible,
                LoadTime = _loadTime,
                PlayersInLocation = _playersInLocation.ToArray(),
                InteractablesState = SaveInteractablesState(),
                Timestamp = DateTime.UtcNow
            };
        }

        /// <summary>
        /// Restaure l'état de la location
        /// </summary>
        public virtual void RestoreLocationState(object stateData)
        {
            if (stateData == null) return;

            GD.Print($"🔄 {LocationName}: Restauration de l'état");

            // Logique de restauration spécifique
            // À implémenter selon les besoins
        }
        #endregion

        #region ILocation Implementation - État
        /// <summary>
        /// Retourne l'état de la location
        /// </summary>
        public virtual object GetLocationState()
        {
            var elapsedTime = (DateTime.UtcNow - _loadTime).TotalSeconds;

            return new
            {
                Location = new
                {
                    Id = LocationId,
                    Name = LocationName,
                    Type = Type.ToString(),
                    Description = Description,
                    IsLoaded = _isLoaded,
                    IsAccessible = _isAccessible,
                    LoadTime = _loadTime,
                    ElapsedTime = Math.Round(elapsedTime, 2)
                },
                Players = new
                {
                    Count = _playersInLocation.Count,
                    PlayerIds = _playersInLocation.ToArray()
                },
                Interactables = new
                {
                    Count = _interactables.Count,
                    Available = _interactables.Count(i => i.IsInteractable)
                },
                Navigation = new
                {
                    SpawnPoints = GetSpawnPoints().Length,
                    DefaultSpawn = GetDefaultSpawnPoint(),
                    ExitCount = GetExits().Count
                },
                Status = new
                {
                    Initialized = _hasInitialized,
                    Timestamp = DateTime.UtcNow
                }
            };
        }
        #endregion

        #region IScene Implementation (existing)
        /// <summary>
        /// Implémentation IScene - délègue à GetLocationState
        /// </summary>
        public object GetSceneState()
        {
            return GetLocationState();
        }
        #endregion

        #region MediaScreen Code (existing - preserved)
        private void InitializeMediaScreen()
        {
            if (_hasInitialized) return;
            
            GD.Print("🎬 LocationModel: Initializing media screen...");
            
            // Try to set up the media screen
            var mediaScreen = FindMediaScreenNode();
            if (mediaScreen != null)
            {
                GD.Print($"📺 Found MediaScreen: {mediaScreen.Name}");
                SetupMediaScreenWithFallback(mediaScreen);
            }
            else
            {
                GD.Print("📺 No MediaScreen found in this location");
            }
        }

        private void SetupMediaScreenWithFallback(MeshInstance3D mediaScreen)
        {
            // First try to find a SubViewport
            var subViewport = GetSubViewportFromMainGameScene();
            
            if (subViewport != null)
            {
                // Success: Set up with viewport texture
                SetupMediaScreenWithViewport(mediaScreen, subViewport);
            }
            else
            {
                // Fallback: Set up with a default material
                SetupMediaScreenWithDefaultMaterial(mediaScreen);
            }
        }

        private void SetupMediaScreenWithViewport(MeshInstance3D mediaScreen, SubViewport subViewport)
        {
            try
            {
                // Create or modify the MaterialOverlay with ViewportTexture
                var material = new StandardMaterial3D();

                // Use the SubViewport as texture
                var viewportTexture = new ViewportTexture();
                viewportTexture.ViewportPath = subViewport.GetPath();

                material.AlbedoTexture = viewportTexture;
                material.AlbedoColor = Colors.White;
                material.Metallic = 0.0f;
                material.Roughness = 0.5f;
                material.EmissionEnabled = true;
                material.Emission = Colors.White * 0.1f; // Slight glow effect

                // Apply the material as overlay
                mediaScreen.MaterialOverlay = material;

                GD.Print($"✅ Viewport texture applied to MediaScreen: {mediaScreen.Name}");
                GD.Print($"🔗 SubViewport path: {subViewport.GetPath()}");
            }
            catch (Exception ex)
            {
                GD.PrintErr($"❌ Error setting up viewport texture: {ex.Message}");
                // Fallback to default material if viewport setup fails
                SetupMediaScreenWithDefaultMaterial(mediaScreen);
            }
        }

        private void SetupMediaScreenWithDefaultMaterial(MeshInstance3D mediaScreen)
        {
            try
            {
                // Create a default material for the media screen
                var material = new StandardMaterial3D();
                
                material.AlbedoColor = new Color(0.1f, 0.1f, 0.2f); // Dark blue
                material.EmissionEnabled = true;
                material.Emission = new Color(0.2f, 0.4f, 0.8f); // Blue glow
                material.Metallic = 0.1f;
                material.Roughness = 0.3f;

                // Apply the material as overlay
                mediaScreen.MaterialOverlay = material;

                GD.Print($"📺 Default material applied to MediaScreen: {mediaScreen.Name}");
                GD.Print("ℹ️ SubViewport not available - using fallback material");
            }
            catch (Exception ex)
            {
                GD.PrintErr($"❌ Error setting up default material: {ex.Message}");
            }
        }

        private SubViewport GetSubViewportFromMainGameScene()
        {
            try
            {
                // Get the MainGameScene node
                var mainGameScene = GetNodeOrNull<Node>("/root/MainGameScene");
                if (mainGameScene == null)
                {
                    GD.Print("ℹ️ MainGameScene not found at /root/MainGameScene");
                    return null;
                }

                // Search for SubViewport in MainGameScene
                return FindSubViewportRecursive(mainGameScene);
            }
            catch (Exception ex)
            {
                GD.PrintErr($"❌ Error searching for SubViewport: {ex.Message}");
                return null;
            }
        }

        private SubViewport FindSubViewportRecursive(Node node)
        {
            // Check if current node is a SubViewport
            if (node is SubViewport subViewport)
            {
                GD.Print($"🔍 Found SubViewport: {subViewport.Name}");
                return subViewport;
            }

            // Search through children
            foreach (Node child in node.GetChildren())
            {
                var result = FindSubViewportRecursive(child);
                if (result != null)
                    return result;
            }

            return null;
        }

        private MeshInstance3D FindMediaScreenNode()
        {
            // Search through all children recursively
            return FindMediaScreenRecursive(this);
        }

        private MeshInstance3D FindMediaScreenRecursive(Node node)
        {
            // Check if current node is a MeshInstance3D with name ending in "_MediaScreen" or named "MediaScreen"
            if (node is MeshInstance3D meshInstance)
            {
                string nodeName = node.Name.ToString();
                if (nodeName.EndsWith("_MediaScreen") || nodeName == "MediaScreen")
                {
                    return meshInstance;
                }
            }

            // Search through children
            foreach (Node child in node.GetChildren())
            {
                var result = FindMediaScreenRecursive(child);
                if (result != null)
                    return result;
            }

            return null;
        }

        /// <summary>
        /// Public method to manually refresh the media screen texture
        /// Call this when a SubViewport becomes available
        /// </summary>
        public void RefreshMediaScreenTexture()
        {
            GD.Print("🔄 Refreshing media screen texture...");
            
            var mediaScreen = FindMediaScreenNode();
            if (mediaScreen != null)
            {
                SetupMediaScreenWithFallback(mediaScreen);
            }
            else
            {
                GD.PrintErr("❌ Cannot refresh: MediaScreen not found");
            }
        }

        /// <summary>
        /// Creates a SubViewport dynamically if needed
        /// </summary>
        public SubViewport CreateSubViewport(Vector2I size = default)
        {
            try
            {
                if (size == default)
                {
                    size = new Vector2I(512, 512);
                }

                var subViewport = new SubViewport();
                subViewport.Name = "DynamicSubViewport";
                subViewport.Size = size;
                subViewport.RenderTargetUpdateMode = SubViewport.UpdateMode.Always;
                
                // Add to the scene tree
                AddChild(subViewport);
                
                GD.Print($"✅ Created dynamic SubViewport: {size}");
                
                // Try to set up the media screen with this new viewport
                CallDeferred(nameof(RefreshMediaScreenTexture));
                
                return subViewport;
            }
            catch (Exception ex)
            {
                GD.PrintErr($"❌ Error creating SubViewport: {ex.Message}");
                return null;
            }
        }
        #endregion

        #region Protected Virtual Methods (for inheritance)
        /// <summary>
        /// Initialise les objets interactables spécifiques à cette location
        /// </summary>
        protected virtual void InitializeInteractables()
        {
            // Rechercher automatiquement les MediaScreen comme interactables
            var mediaScreen = FindMediaScreenNode();
            if (mediaScreen != null)
            {
                var mediaScreenInteractable = new MediaScreenInteractable(mediaScreen);
                _interactables.Add(mediaScreenInteractable);
                GD.Print($"📺 MediaScreen ajouté comme interactable: {mediaScreenInteractable.InteractableId}");
            }
        }

        /// <summary>
        /// Initialise les points de spawn spécifiques
        /// </summary>
        protected virtual void InitializeSpawnPoints()
        {
            // À override dans les classes dérivées
        }

        /// <summary>
        /// Initialise les sorties spécifiques
        /// </summary>
        protected virtual void InitializeExits()
        {
            // À override dans les classes dérivées
        }

        /// <summary>
        /// Charge les ressources spécifiques à la location
        /// </summary>
        protected virtual void LoadResources()
        {
            // À override dans les classes dérivées
        }

        /// <summary>
        /// Logique spécifique quand un joueur entre
        /// </summary>
        protected virtual void OnPlayerEnterSpecific(string playerId)
        {
            // À override dans les classes dérivées
        }

        /// <summary>
        /// Logique spécifique quand un joueur sort
        /// </summary>
        protected virtual void OnPlayerExitSpecific(string playerId)
        {
            // À override dans les classes dérivées
        }

        /// <summary>
        /// Traite le résultat d'une interaction
        /// </summary>
        protected virtual void ProcessInteractionResult(string playerId, string interactionId, object result)
        {
            GD.Print($"📊 {LocationName}: Résultat interaction {interactionId}: {result}");
        }

        /// <summary>
        /// Applique les paramètres d'ambiance
        /// </summary>
        protected virtual void ApplyAmbianceSettings(object settings)
        {
            // À override dans les classes dérivées
        }

        /// <summary>
        /// Applique les paramètres de gameplay
        /// </summary>
        protected virtual void ApplyGameplaySettings(object settings)
        {
            // À override dans les classes dérivées
        }

        /// <summary>
        /// Précharge les ressources spécifiées
        /// </summary>
        protected virtual void PreloadResources(string[] resources)
        {
            if (resources == null) return;

            foreach (var resource in resources)
            {
                GD.Print($"📦 {LocationName}: Préchargement de {resource}");
                // Logique de préchargement
            }
        }

        /// <summary>
        /// Sauvegarde l'état des interactables
        /// </summary>
        protected virtual object SaveInteractablesState()
        {
            return _interactables.Select(i => new
            {
                Id = i.InteractableId,
                IsInteractable = i.IsInteractable,
                Position = i.Position
            }).ToArray();
        }
        #endregion
    }

    /// <summary>
    /// Implémentation d'un MediaScreen comme objet interactable
    /// </summary>
    public class MediaScreenInteractable : IInteractable
    {
        private readonly MeshInstance3D _mediaScreen;

        public MediaScreenInteractable(MeshInstance3D mediaScreen)
        {
            _mediaScreen = mediaScreen;
        }

        public string InteractableId => $"MediaScreen_{_mediaScreen.GetInstanceId()}";
        public string DisplayName => "Écran Média";
        public string InteractionDescription => "Interagir avec l'écran média";
        public bool IsInteractable => _mediaScreen != null && _mediaScreen.IsInsideTree();
        public Vector3 Position => _mediaScreen?.GlobalPosition ?? Vector3.Zero;

        public event Action<IInteractable, string> Interacted;

        public object Interact(string playerId, object data = null)
        {
            GD.Print($"📺 MediaScreen: Interaction par {playerId}");
            
            Interacted?.Invoke(this, playerId);
            
            return new
            {
                Success = true,
                Action = "MediaScreenInteraction",
                PlayerId = playerId,
                Timestamp = DateTime.UtcNow
            };
        }
    }
}
