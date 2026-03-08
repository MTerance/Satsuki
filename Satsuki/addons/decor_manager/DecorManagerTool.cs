using Godot;
using Godot.Collections;
using Satsuki.addons.decor_manager;
using Satsuki.addons.decor_manager.Tools;
using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

#if TOOLS
/// <summary>
/// Outil Godot pour gerer les decors et cameras
/// Permet de charger des .tscn et configurer les cameras et points d'apparition
/// </summary>
[Tool]
public partial class DecorManagerTool : EditorPlugin
{
    private Control _dockPanel;
    private VBoxContainer _mainContainer;
    private StageInfoContainer _stageInfoContainer;
    private GeneralInfoContainer _generalInfoContainer;
    private LobbyMenuContainer _lobbyMenuContainer;

    //
    private SpawnPointGizmoPlugin _spawnPointGizmoPlugin;



    private Node3D _currentSceneRoot;

    // Gestion des points d'apparition
    private CheckBox _spawnPointModeCheckbox;
    private OptionButton _spawnPointTypeOption;
    private Button _saveConfigButton;
    private ItemList _spawnPointsList;
    private Button _removeSpawnPointButton;

    private Node3D _loadedScene;

    private bool _isSpawnPointMode = false;
    private string _currentScenePath = "";

    private SceneManager _sceneManager= SceneManager.Instance;


    public override void _EnterTree()
    {
        GD.Print("DecorManagerTool: Initialisation...");
        SetupRootSceneNode();
        CreateDockPanel();
        AddControlToDock(DockSlot.RightUl, _dockPanel);

        _spawnPointGizmoPlugin = new SpawnPointGizmoPlugin();
        AddNode3DGizmoPlugin(_spawnPointGizmoPlugin);

        GD.Print("DecorManagerTool: Dock ajoute");
    }

    private void Cleanup()
    {
        if (_spawnPointGizmoPlugin != null)
        {
            RemoveNode3DGizmoPlugin(_spawnPointGizmoPlugin);
            _spawnPointGizmoPlugin = null;
        }

        if (_dockPanel != null)
        {


            if (_generalInfoContainer != null)
            {
                _generalInfoContainer.NewStageResourceRequested -= OnNewStageResourceRequested;
                _generalInfoContainer.LoadStageResourceRequested -= OnLoadStageResourceRequested;
                _generalInfoContainer.SaveStageResourceRequested -= OnSaveStageResourceRequested;
                _generalInfoContainer = null;
            }

            RemoveControlFromDocks(_dockPanel);
            GetTree().Root.RemoveChild(_currentSceneRoot);
            _dockPanel.QueueFree();
        }
    }

    public override void _ExitTree()
    {
        Cleanup();
        GD.Print("DecorManagerTool: Nettoyage termine");
    }

    public override bool _Handles(GodotObject @object)
    {
        return (_isSpawnPointMode || _isMenuRenderingMode) && @object is Node3D;
    }

    private void CreateDockPanel()
    {
        _dockPanel = new Control();
        _dockPanel.Name = "Decor Manager";
        GD.Print("DecorManagerTool: Creation du panneau de dock...");
        string controlPath = "res://addons/decor_manager/Scenes/control.tscn";
        if (!ResourceLoader.Exists(controlPath))
        {
            GD.PrintErr("ERROR");
            return;
        }
        PackedScene controlScene = GD.Load<PackedScene>(controlPath);
        Control control = controlScene.Instantiate<Control>();
        _dockPanel.AddChild(control);

        SetupLobbyMenuContainer(control);
        SetupGeneralInfoContainer(control);
        SetupStageInfoContainer(control);
        GD.Print("DecorManagerTool: VBoxContainer ajoute");
    }

    private void SetupLobbyMenuContainer(Control control)
    {
        _lobbyMenuContainer = control.FindChild("LobbyMenuContainer", true, false) as LobbyMenuContainer;
        if (_lobbyMenuContainer != null)
        {
            _lobbyMenuContainer.SpawnPointCreated += OnSpawnPointCreated;
        }
        else
            GD.PrintErr("DecorManagerTool: LobbyMenuContainer introuvable");
    }

    private void OnSpawnPointCreated(Node3D node)
    {
        try
        {
            var editedSceneRoot = EditorInterface.Singleton.GetEditedSceneRoot();
            if (editedSceneRoot != null)
            {
                editedSceneRoot.AddChild(node);
                node.Owner = editedSceneRoot;
            }
            else
                _currentSceneRoot.AddChild(node);
        }
        catch (Exception ex)
        {
            GD.PrintErr($"DecorManagerTool: Erreur lors de l'ajout du spawn point: {ex.Message}");
        }
    }

    private void SetupStageInfoContainer(Control control)
    {
        _stageInfoContainer = control.FindChild("StageInfoContainer", true, false) as StageInfoContainer;
        if (_stageInfoContainer != null)
        {
            _stageInfoContainer.LoadStageAssetRequested += OnLoadStageAssetRequested;
            GD.Print("DecorManagerTool: StageInfoContainer trouve et evenement connecte");
        }
        else
            GD.PrintErr("DecorManagerTool: StageInfoContainer introuvable");
    }

    private void OnLoadStageAssetRequested(PackedScene scene)
    {
        if ((scene != null))
        {
            SetupRootSceneNode();
            _loadedScene = scene.Instantiate<Node3D>();
            _currentSceneRoot.AddChild(_loadedScene);
            GD.Print($"DecorManagerTool: Scene chargee");
        }
        else
            GD.PrintErr("DecorManagerTool: Scene a charger est null");
    }

    private void SetupGeneralInfoContainer(Control control)
    {
        _generalInfoContainer = control.FindChild("GeneralInfoContainer", true, false) as GeneralInfoContainer;
        if (_generalInfoContainer != null)
        {
            _generalInfoContainer.NewStageResourceRequested += OnNewStageResourceRequested;
            _generalInfoContainer.LoadStageResourceRequested += OnLoadStageResourceRequested;
            _generalInfoContainer.SaveStageResourceRequested += OnSaveStageResourceRequested;
        }
        else
            GD.PrintErr("DecorManagerTool: GeneralInfoContainer introuvable");
    }

    private void OnNewStageResourceRequested()
    {
        // Reinitialiser la effacer les spanw points et le decor charge si il y en a un
        _lobbyMenuContainer.ClearSpawnPoints();
        GD.Print("DecorManagerTool: New stage resource requested");
    }
     
    private void OnLoadStageResourceRequested()
    {
        _lobbyMenuContainer.ClearSpawnPoints();
        GD.Print("DecorManagerTool: Load stage resource requested");
    }

    private void OnSaveStageResourceRequested()
    {
        GD.Print("DecorManagerTool: Save stage resource requested");
    }

    private void SetupRootSceneNode()
    {
        /*
        var editedSceneRoot = EditorInterface.Singleton.GetEditedSceneRoot() as Node3D;

        if (editedSceneRoot != null)
        {
            _currentSceneRoot = editedSceneRoot;
            GD.Print("DecorManagerTool: Noeud racine deja existant, suppression du noeud existant");
            editedSceneRoot = null;
        }
        var currentSceneRoot = new Node3D();
        currentSceneRoot.Name = "DecorManagerSetup";
        currentSceneRoot.Position = Vector3.Zero;

        // Sauvegarder et ouvrir la scène dans l'éditeur
        var packedScene = new PackedScene();
        packedScene.Pack(currentSceneRoot);

        var tempScenePath = "res://addons/decor_manager/DecorManager.tscn";
        ResourceSaver.Save(packedScene, tempScenePath);
        EditorInterface.Singleton.OpenSceneFromPath(tempScenePath);

        // Récupérer la référence après ouverture
        _currentSceneRoot = EditorInterface.Singleton.GetEditedSceneRoot() as Node3D;
        GD.Print("DecorManagerTool: Noeud racine pour le decor manager cree");
        */
        _sceneManager.SetupRootSceneNode();
    }

    private void ResetRootSceneNode()
    {
        if (_currentSceneRoot != null)
        {
            _currentSceneRoot.QueueFree();
        }
        SetupRootSceneNode();
    }

    private void SaveStageResource()
    {
        if (string.IsNullOrEmpty(_currentScenePath))
        {
            GD.PrintErr("Aucune scene chargee");
            return;
        }

        // Creer la resource
        var stageResource = new StageResource
        {
            Id = Satsuki.addons.decor_manager.Tools.Tool.GenerateStageId(),
            Name = Path.GetFileNameWithoutExtension(_currentScenePath),
            SceneName = Path.GetFileNameWithoutExtension(_currentScenePath),
            ScenePath = _currentScenePath,
            SpawnPoints = new Godot.Collections.Array<SpawnPointData>()
        };

        // Ajouter les spawn points
        foreach (var sp in _lobbyMenuContainer.GetSpawnsPoints())
        {
            stageResource.SpawnPoints.Add(sp);
        }


        string savePath = $"res://Resources/Stages/{stageResource.Name}.tres";

        // Sauvegarder
        stageResource.Save(savePath);
    }

    public override void _Process(double delta)
    {
        base._Process(delta);

    }
}
#endif
