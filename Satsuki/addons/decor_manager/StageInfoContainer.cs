using Godot;
using Satsuki.addons.decor_manager;
using Satsuki.Models;
using System;

#if TOOLS
[Tool]
#endif
public partial class StageInfoContainer : Control
{
	private Button _loadStageAssetButton;
	private LineEdit _stageNameLineEdit;
	private LineEdit _pathStageAssetLineEdit;

	/*
	[Signal]
	public delegate void LoadStageAssetRequestedEventHandler(PackedScene scene);
	*/
	private string _stageAssetPath;
	private string _stageName;

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		GD.Print("Test ready Stageinfo container");
		_loadStageAssetButton = FindChild("LoadStageAssetButton") as Button;
		_stageNameLineEdit = FindChild("StageNameLineEdit") as LineEdit;
		_pathStageAssetLineEdit = FindChild("PathStageAssetLineEdit") as LineEdit;
		if (_loadStageAssetButton != null)
		{
			_loadStageAssetButton.Pressed += OnLoadStageAssetButtonPressed;
		}
		else
			GD.PrintErr("LoadStageAssetButton not found in StageInfoContainer");
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}
	
	public Tuple<string,string> GetStageInfo()
	{
		var info = new Tuple<string, string>(_stageNameLineEdit.Text, _pathStageAssetLineEdit.Text);
		return info;
	}

	public void ClearStageInfo()
	{
		_stageNameLineEdit.Text = string.Empty;
		_pathStageAssetLineEdit.Text = string.Empty;
		ClearLoadedStage();
	}

	private void ClearLoadedStage()
	{
		SceneManager.Instance.ClearLoadedScene();
	}


	private void OnLoadStageAssetButtonPressed()
	{
		OpenFileLoadStageScene();
	}

	private void OpenFileLoadStageScene()
	{
		var fileDialog = new EditorFileDialog();
		fileDialog.FileMode = EditorFileDialog.FileModeEnum.OpenFile;
		fileDialog.Filters = new string[] { "*.tscn" };
		fileDialog.Access = EditorFileDialog.AccessEnum.Resources;
		fileDialog.CurrentDir = "res://Scenes/Locations/";
		fileDialog.Title = "Charger une scene";

		fileDialog.FileSelected += OnStageFileSelected;
		fileDialog.Canceled += () => fileDialog.QueueFree();
		EditorInterface.Singleton.GetBaseControl().AddChild(fileDialog);
		fileDialog.PopupCentered(new Vector2I(800, 600));

	}

	private PackedScene LoadStageScene(string path)
	{
		if (!ResourceLoader.Exists(path))
		{
			GD.PrintErr("Stage scene not found: " + path);
			return null;
		}
		var scene = GD.Load<PackedScene>(path);
		return scene;
		//var currentScene = EditorInterface.Singleton.GetEditedSceneRoot();
	}

	private string GetStageNameFromPath(string path)
	{
		_stageName = System.IO.Path.GetFileNameWithoutExtension(path);
		_stageNameLineEdit.Text = _stageName;
		return _stageName;
	}

	public void SetStageInfo(string path)
	{
		var scene = LoadStageScene(path);

		if (scene != null)
		{
			var stageName = GetStageNameFromPath(path);
			_stageNameLineEdit.Text = stageName;
			_pathStageAssetLineEdit.Text = path;
			SceneManager.Instance.LoadMainStage(scene);
			// EmitSignal(SignalName.LoadStageAssetRequested,scene);   // Do something with the loaded scene
		}

	}

	private void OnStageFileSelected(string path)
	{
		SetStageInfo(path);
	}





}
