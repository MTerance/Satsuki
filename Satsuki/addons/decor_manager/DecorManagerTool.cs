using Godot;
using Godot.Collections;
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
	private LineEdit _scenePathInput;
	private Button _loadSceneButton;
	private Button _loadStageAssetButton;
	private Button _addSpawnPointButton;
    private Label _statusLabel;
	
	// Gestion des points d'apparition
	private CheckBox _spawnPointModeCheckbox;
	private OptionButton _spawnPointTypeOption;
	private Button _saveConfigButton;
	private ItemList _spawnPointsList;
	private Button _removeSpawnPointButton;
	
	private Node3D _loadedScene;
	// private readonly Dictionary<string, Camera3D> _cameras = new Dictionary<string, Camera3D>();
	private readonly List<SpawnPointData> _spawnPoints = new List<SpawnPointData>();

    /**/

    private readonly System.Collections.Generic.Dictionary<Sprite3D, SpawnPointData> _markerToSpawnPoint = new();
    private readonly System.Collections.Generic.Dictionary<SpawnPointData, Sprite3D> _spawnPointToMarker = new();
    private readonly System.Collections.Generic.Dictionary<SpawnPointData, Label3D> _spawnPointToLabel = new();

    /**/

	private readonly System.Collections.Generic.Dictionary<SpawnPointData,Control> _spawnPointToUIControl = new();

    /**/
    private bool _isSpawnPointMode = false;
	private string _currentScenePath = "";

	public override void _EnterTree()
	{
		GD.Print("DecorManagerTool: Initialisation...");
		CreateDockPanel();
		AddControlToDock(DockSlot.RightUl, _dockPanel);
		GD.Print("DecorManagerTool: Dock ajoute");
	}

	private void Cleanup()
	{
        if (_dockPanel != null)
        {
			if (_loadStageAssetButton != null)
			{
				_loadStageAssetButton.Pressed -= OnLoadStageAssetButtonPressed;
				_loadStageAssetButton = null;
            }
            if (_addSpawnPointButton != null)
            {
                _addSpawnPointButton.Pressed -= OnSpawnPointButtonPressed;
                _addSpawnPointButton = null;
            }
            RemoveControlFromDocks(_dockPanel);
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

		SetuploadStageButton(control);
        CreateSpawnPointPanel(control);
        GD.Print("DecorManagerTool: VBoxContainer ajoute");
	}

	private void SetuploadStageButton(Control control)
	{
        _loadStageAssetButton = control.FindChild("LoadStageAssetButton", true, false) as Button;
        if (_loadStageAssetButton != null)
        {
            _loadStageAssetButton.Pressed += OnLoadStageAssetButtonPressed;
        }
        else
            GD.PrintErr("StageInfoContainer: LoadStageAssetButton introuvable");

    }

    private void CreateSpawnPointPanel(Control control)
	{
        _addSpawnPointButton = control.FindChild("AddPlayerSpawnButton", true, false) as Button;
		if (_addSpawnPointButton != null)
		{
			_addSpawnPointButton.Pressed += OnSpawnPointButtonPressed;
        }
		else
            GD.PrintErr("DecorManagerTool: AddSpawnPointButton trouve");

    }


	private T FindNodeByName<T>(Control parent, string nodeName) where T : Node
	{
		var node = parent.GetNodeOrNull<T>(nodeName);
		if (node == null)
		{
			GD.PrintErr($"DecorManagerTool: Noeud '{nodeName}' de type {typeof(T).Name} non trouve dans le control.");
		}
		else
		{
			GD.Print($"DecorManagerTool: Noeud '{nodeName}' de type {typeof(T).Name} trouve.");
		}
		return node;
    }


	private void AddNewSpawnPoint()
	{
        GD.Print("AddNewSpawnPoint: Begin");
        var spawnPoint = new SpawnPointData(GenerateStageId(), Vector3.Zero, Vector3.Zero, SpawnPointType.Standard_Idle);
		_spawnPoints.Add(spawnPoint);

		var spawnPointControlPath = "res://addons/decor_manager/Scenes/player_spawn_container.tscn";
        if (!ResourceLoader.Exists(spawnPointControlPath))
        {
            GD.PrintErr("ERROR");
            return;
        }
        PackedScene controlScene = GD.Load<PackedScene>(spawnPointControlPath);
        Control control = controlScene.Instantiate<Control>();
		var container = _dockPanel.FindChild("PlayersSpawnsContainer", true, false) as VBoxContainer;

		if (container != null)
		{
			GD.Print("AddNewSpawnPoint: Ajout du spawn point dans la liste");
            ((PlayerSpawnTemplate)control).InitPlayerSpawnTemplate(spawnPoint);
            container.AddChild(control);
            GD.Print("AddNewSpawnPoint: Spawn point ajoute dans la liste");	
        }
		else
			GD.PrintErr("AddNewSpawnPoint: Container pour les spawn points introuvable");
    }




	/*
    private void SetupLoadStageButton(Control control)
	{
		var controlNode = FindNodeByName<Button>(control, "UploadStageButton");
	}
	*/
	private Label3D CreateLabelForPointMarker(SpawnPointData spawnPoint)
	{
		var label = new Label3D();
		var labelText = $"SpawnPoint_{spawnPoint.Index}\nPos: {spawnPoint.Position}\nRot: {spawnPoint.Rotation}\n Type: {spawnPoint.Type}";
		label.Text = labelText;
		label.Position = spawnPoint.Position + new Vector3(0, 1.5f, 0); // Positionner le label au-dessus du marqueur
		label.FontSize = 24;
		label.NoDepthTest = true;

		return label;
	}

	private Sprite3D CreateSpawnPointMarker(SpawnPointData spawnPoint)
	{
		Sprite3D marker = new Sprite3D();
		marker.Name = $"SpawnPoint_{spawnPoint.Index}";
		marker.Texture = GD.Load<Texture2D>("res://addons/decor_manager/Assets/spawn_point_marker.png");
		marker.Scale = new Vector3(0.5f, 0.5f, 0.5f);
		marker.Position = spawnPoint.Position;
		marker.RotationDegrees = spawnPoint.Rotation;

		return marker;
	}

	private void UpdateLabelFromSpawnPoint(SpawnPointData spawnPoint)
	{
		if (!(_spawnPointToLabel.TryGetValue(spawnPoint, out var label)))
		{
			return;
		}
		var labelText = $"SpawnPoint_{spawnPoint.Index}\nPos: {spawnPoint.Position}\nRot: {spawnPoint.Rotation}\n Type: {spawnPoint.Type}";
		label.Text = labelText;
		label.Position = spawnPoint.Position + new Vector3(0, 1.5f, 0); // Positionner le label au-dessus du marqueur
    }


    private void UpdateSpawnPointFromMarker(Sprite3D sprite)
	{
        if (!(_markerToSpawnPoint.TryGetValue(sprite,out var spawnPoint)))
        {
			return;
        }

		spawnPoint.Position = sprite.Position;
		spawnPoint.Rotation = sprite.RotationDegrees;
		UpdateLabelFromSpawnPoint(spawnPoint);
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
            Id = GenerateStageId(),
            Name = Path.GetFileNameWithoutExtension(_currentScenePath),
            SceneName = Path.GetFileNameWithoutExtension(_currentScenePath),
            ScenePath = _currentScenePath,
            SpawnPoints = new Godot.Collections.Array<SpawnPointData>()
        };

        // Ajouter les spawn points
        foreach (var sp in _spawnPoints)
        {
            stageResource.SpawnPoints.Add(sp);
        }


        string savePath = $"res://Resources/Stages/{stageResource.Name}.tres";

        // Sauvegarder
        stageResource.Save(savePath);
    }

    private int GenerateStageId()
    {
        return (int)(DateTime.UtcNow.Ticks % int.MaxValue);
    }


    public override void _Process(double delta)
    {
        base._Process(delta);
		SyncSelectedMarkers();
    }

	private void SyncSelectedMarkers()
	{
        foreach (var kvp in _markerToSpawnPoint)
        {
            var marker = kvp.Key;
            var spawnPoint = kvp.Value;

            // Verifier si la position ou rotation a change
            if (marker.Position != spawnPoint.Position || marker.RotationDegrees != spawnPoint.Rotation)
            {
                UpdateSpawnPointFromMarker(marker);
            }
        }
    }

	private void OnSpawnPointButtonPressed()
	{
		GD.Print("DecorManagerTool: AddSpawnPointButton pousse");
		AddNewSpawnPoint();
        GD.Print("DecorManagerTool: Add NewSpawnPoint termine");
    }

    private void OnLoadStageAssetButtonPressed()
    {
        GD.Print("DecorManagerTool: UploadStageButton pousse");
        GD.PrintErr("DecorManagerTool: Fonction de chargement de stage non implementee");
    }

    private void _on_label_mouse_entered()
    {
        GD.Print("DecorManagerTool: Souris entre dans le label");
    }


    /*
	private void LoadCustomControl()
	{
		string controlPath = "res://addons/decor_manager/Scenes/control.tscn";
		if (!ResourceLoader.Exists(controlPath))
		{
			GD.PrintErr("ERROR");
			return;
		}
		PackedScene controlScene = GD.Load<PackedScene>(controlPath);
		Control control = controlScene.Instantiate<Control>();
		_mainContainer.AddChild(control);
		GD.Print("DecorManagerTool: Control personnalise ajoute");
	}
	*/

}







public class DecorConfiguration
{
	public string ScenePath { get; set; }
	public string SceneName { get; set; }
	public List<SpawnPointData> SpawnPoints { get; set; }
	public List<MenuRenderSurfaceData> MenuRenderSurfaces { get; set; }
	public DateTime SavedAt { get; set; }
}

public class Vector3JsonConverter : JsonConverter<Vector3>
{
	public override Vector3 Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
	{
		if (reader.TokenType != JsonTokenType.StartObject)
			throw new JsonException();

		float x = 0, y = 0, z = 0;

		while (reader.Read())
		{
			if (reader.TokenType == JsonTokenType.EndObject)
				return new Vector3(x, y, z);

			if (reader.TokenType == JsonTokenType.PropertyName)
			{
				string propertyName = reader.GetString();
				reader.Read();
				
				switch (propertyName)
				{
					case "x":
					case "X":
						x = (float)reader.GetDouble();
						break;
					case "y":
					case "Y":
						y = (float)reader.GetDouble();
						break;
					case "z":
					case "Z":
						z = (float)reader.GetDouble();
						break;
				}
			}
		}

		throw new JsonException();
	}

	public override void Write(Utf8JsonWriter writer, Vector3 value, JsonSerializerOptions options)
	{
		writer.WriteStartObject();
		writer.WriteNumber("x", value.X);
		writer.WriteNumber("y", value.Y);
		writer.WriteNumber("z", value.Z);
		writer.WriteEndObject();
	}
}
#endif
