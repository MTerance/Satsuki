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

	private SceneManager _sceneManager = SceneManager.Instance;


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
			SceneManager.Instance.AddNodeToScene(node);
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
			// _stageInfoContainer.LoadStageAssetRequested += OnLoadStageAssetRequested;
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

	/// <summary>
	/// Clears all data and state associated with the current workspace, resetting relevant containers to their default
	/// state.
	/// </summary>
	/// <remarks>Call this method to remove all workspace-specific information before loading a new workspace
	/// or when resetting the current session. This method does not affect global application state outside of the
	/// workspace context.</remarks>
	private void ClearCurrentWorkspace()
	{
		_lobbyMenuContainer.ClearSpawnPoints();
		_stageInfoContainer.ClearStageInfo();
		_generalInfoContainer.ClearGeneralInfo();
		//SceneManager.Instance.ClearLoadedScene();
	}

	private void OnNewStageResourceRequested()
	{
		// Reinitialiser la effacer les spanw points et le decor charge si il y en a un
		ClearCurrentWorkspace();
		GD.Print("DecorManagerTool: New stage resource requested");
	}

	public void LoadStageResource(string path)
	{
		var resource = StageResource.Load(path);
		if (resource != null)
		{
			ClearCurrentWorkspace();
			_generalInfoContainer.UpdateGeneralInfo(resource.Name, resource.ResourcePath);
			_stageInfoContainer.SetStageInfo(resource.ScenePath);
			_lobbyMenuContainer.SetLobbyInfo(resource.LobbyInfo);
			OnLoadStageAssetRequested(GD.Load<PackedScene>(resource.ScenePath));
			// Charger les spawn points dans le lobby menu container
		}
		else
		{
			GD.PrintErr("DecorManagerTool: Erreur lors du chargement de la StageResource");
		}
	}

	private void OnLoadFileSelected(string path, EditorFileDialog fileDialog)
	{
		LoadStageResource(path);
		fileDialog.QueueFree();
	}

	private void OnLoadStageResourceRequested()
	{
		GD.Print("DecorManagerTool: Load stage resource requested");
		var fileDialog = new EditorFileDialog();
		fileDialog.FileMode = EditorFileDialog.FileModeEnum.OpenFile;
		fileDialog.Filters = new string[] { "*.tres" };
		fileDialog.Access = EditorFileDialog.AccessEnum.Resources;
		fileDialog.CurrentDir = "res://Resources/Locations/";
		fileDialog.Title = "Charger une configuration de scene";
		fileDialog.FileSelected += (string path) =>
		{
			OnLoadFileSelected(path, fileDialog);
		};
		fileDialog.Canceled += () => fileDialog.QueueFree();
		EditorInterface.Singleton.GetBaseControl().AddChild(fileDialog);
		fileDialog.PopupCentered(new Vector2I(800, 600));
	}

	private void OnSaveStageResourceRequested()
	{
		GD.Print("DecorManagerTool: Save stage resource requested");
		var fileDialog = new EditorFileDialog();
		fileDialog.FileMode = EditorFileDialog.FileModeEnum.SaveFile;
		fileDialog.Filters = new string[] { "*.tres" };
		fileDialog.Access = EditorFileDialog.AccessEnum.Resources;
		fileDialog.CurrentDir = "res://Resources/Locations/";
		fileDialog.CurrentFile = $"{_generalInfoContainer.GetGeneralInfo().Item1}.tres";
		fileDialog.Title = "Sauvegarder la configuration de la scene";
		fileDialog.FileSelected += (string path) =>
		{
			OnSaveFileSelected(path,fileDialog);
		};
		fileDialog.Canceled += () => fileDialog.QueueFree();
		EditorInterface.Singleton.GetBaseControl().AddChild(fileDialog);
		fileDialog.PopupCentered(new Vector2I(800, 600));
	}

	public StageResource BuildStageResource(string path)
	{
		var generalInfo = _generalInfoContainer.GetGeneralInfo();
		var lobbyInfo = _lobbyMenuContainer.GetLobbyInfo();
		var stageInfo = _stageInfoContainer.GetStageInfo();
		var savedAt = DateTime.Now.ToString();
		var resource = new StageResource
		{
			Id = Satsuki.addons.decor_manager.Tools.Tool.GenerateStageId(),
			Name = generalInfo.Item1,
			SceneName = stageInfo.Item1,
			ScenePath = stageInfo.Item2,
			LobbyInfo = lobbyInfo,
			SavedAt = savedAt
		};

		return resource;
	}

	private void OnSaveFileSelected(string path,EditorFileDialog fileDialog)
	{
		fileDialog.QueueFree();

		var resource = BuildStageResource(path);
		if (resource == null)
			GD.PrintErr("DecorManagerTool: Erreur lors de la construction de la StageResource");

		if (ResourceLoader.Exists(path))
		{
			var cached = ResourceLoader.Load(path, "", ResourceLoader.CacheMode.Replace);
			cached?.Dispose();
		}

		if (resource.Save(path))
		{
			_generalInfoContainer.UpdateGeneralInfo(resource.Name, resource.ResourcePath);
		}
	}

	private void SetupRootSceneNode()
	{
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
			//            SpawnPoints = new Godot.Collections.Array<SpawnPointData>()
		};

		// Ajouter les spawn points
		/*
		foreach (var sp in _lobbyMenuContainer.GetSpawnsPoints())
		{
			stageResource.SpawnPoints.Add(sp);
		}
*/

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
