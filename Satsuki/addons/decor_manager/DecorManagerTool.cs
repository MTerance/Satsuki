using Godot;
using System;
using System.Collections.Generic;
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
	private Label _statusLabel;
	
	// Conteneurs pour chaque camera
	private CameraConfigPanel _titleCameraPanel;
	private CameraConfigPanel _lobbyCameraPanel;
	private CameraConfigPanel _gameCameraPanel;
	
	// Gestion des points d'apparition
	private CheckBox _spawnPointModeCheckbox;
	private OptionButton _spawnPointTypeOption;
	private Button _saveConfigButton;
	private ItemList _spawnPointsList;
	private Button _removeSpawnPointButton;
	
	private Node3D _loadedScene;
	private readonly Dictionary<string, Camera3D> _cameras = new Dictionary<string, Camera3D>();
	private readonly List<SpawnPointData> _spawnPoints = new List<SpawnPointData>();
	private bool _isSpawnPointMode = false;
	private string _currentScenePath = "";

	public override void _EnterTree()
	{
		GD.Print("DecorManagerTool: Initialisation...");
		CreateDockPanel();
		AddControlToDock(DockSlot.RightUl, _dockPanel);
		GD.Print("DecorManagerTool: Dock ajoute");
	}

	public override void _ExitTree()
	{
		if (_dockPanel != null)
		{
			RemoveControlFromDocks(_dockPanel);
			_dockPanel.QueueFree();
		}
		GD.Print("DecorManagerTool: Nettoyage termine");
	}
	
	public override bool _Handles(GodotObject @object)
	{
		return _isSpawnPointMode && @object is Node3D;
	}
	
	public override int _Forward3DGuiInput(Camera3D camera, InputEvent @event)
	{
		if (!_isSpawnPointMode) return (int)EditorPlugin.AfterGuiInput.Pass;
		
		if (@event is InputEventMouseButton mouseButton && mouseButton.Pressed && mouseButton.ButtonIndex == MouseButton.Left)
		{
			var from = camera.ProjectRayOrigin(mouseButton.Position);
			var to = from + camera.ProjectRayNormal(mouseButton.Position) * 1000;
			
			var spaceState = camera.GetWorld3D().DirectSpaceState;
			var query = PhysicsRayQueryParameters3D.Create(from, to);
			var result = spaceState.IntersectRay(query);
			
			if (result.Count > 0)
			{
				var position = (Vector3)result["position"];
				AddSpawnPoint(position);
				return (int)EditorPlugin.AfterGuiInput.Stop;
			}
		}
		
		return (int)EditorPlugin.AfterGuiInput.Pass;
	}

	private void CreateDockPanel()
	{
		_dockPanel = new Control();
		_dockPanel.Name = "Decor Manager";

		var scrollContainer = new ScrollContainer();
		scrollContainer.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		scrollContainer.SizeFlagsVertical = Control.SizeFlags.Fill;
		_dockPanel.AddChild(scrollContainer);

		_mainContainer = new VBoxContainer();
		_mainContainer.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		scrollContainer.AddChild(_mainContainer);

		var titleLabel = new Label();
		titleLabel.Text = "DECOR MANAGER";
		titleLabel.AddThemeFontSizeOverride("font_size", 20);
		_mainContainer.AddChild(titleLabel);

		AddSeparator();

		CreateSceneLoadingSection();

		AddSeparator();

		_statusLabel = new Label();
		_statusLabel.Text = "Aucune scene chargee";
		_statusLabel.AddThemeColorOverride("font_color", new Color(0.7f, 0.7f, 0.7f));
		_mainContainer.AddChild(_statusLabel);

		AddSeparator();
		
		CreateSpawnPointsSection();
		
		AddSeparator();

		_titleCameraPanel = CreateCameraConfigPanel("Title_Camera3D", new Color(1.0f, 0.5f, 0.0f));
		_lobbyCameraPanel = CreateCameraConfigPanel("Lobby_Camera3D", new Color(0.2f, 0.8f, 1.0f));
		_gameCameraPanel = CreateCameraConfigPanel("Game_Camera3D", new Color(0.2f, 1.0f, 0.2f));

		_mainContainer.AddChild(_titleCameraPanel);
		AddSeparator();
		_mainContainer.AddChild(_lobbyCameraPanel);
		AddSeparator();
		_mainContainer.AddChild(_gameCameraPanel);
	}

	private void CreateSceneLoadingSection()
	{
		var sectionLabel = new Label();
		sectionLabel.Text = "Charger une scene";
		sectionLabel.AddThemeFontSizeOverride("font_size", 16);
		_mainContainer.AddChild(sectionLabel);

		var pathContainer = new HBoxContainer();
		_mainContainer.AddChild(pathContainer);

		var pathLabel = new Label();
		pathLabel.Text = "Chemin .tscn:";
		pathLabel.CustomMinimumSize = new Vector2(100, 0);
		pathContainer.AddChild(pathLabel);

		_scenePathInput = new LineEdit();
		_scenePathInput.PlaceholderText = "res://Scenes/Locations/Restaurant.tscn";
		_scenePathInput.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		pathContainer.AddChild(_scenePathInput);

		var browseButton = new Button();
		browseButton.Text = "...";
		browseButton.Pressed += OnBrowsePressed;
		pathContainer.AddChild(browseButton);

		_loadSceneButton = new Button();
		_loadSceneButton.Text = "Charger la scene";
		_loadSceneButton.Pressed += OnLoadScenePressed;
		_mainContainer.AddChild(_loadSceneButton);
	}
	
	private void CreateSpawnPointsSection()
	{
		var sectionLabel = new Label();
		sectionLabel.Text = "Points d'apparition des joueurs";
		sectionLabel.AddThemeFontSizeOverride("font_size", 16);
		sectionLabel.AddThemeColorOverride("font_color", new Color(0.2f, 1.0f, 0.5f));
		_mainContainer.AddChild(sectionLabel);
		
		_spawnPointModeCheckbox = new CheckBox();
		_spawnPointModeCheckbox.Text = "Mode placement actif (cliquez dans la scene 3D)";
		_spawnPointModeCheckbox.Toggled += OnSpawnPointModeToggled;
		_mainContainer.AddChild(_spawnPointModeCheckbox);
		
		var typeContainer = new HBoxContainer();
		_mainContainer.AddChild(typeContainer);
		
		var typeLabel = new Label();
		typeLabel.Text = "Type:";
		typeLabel.CustomMinimumSize = new Vector2(80, 0);
		typeContainer.AddChild(typeLabel);
		
		_spawnPointTypeOption = new OptionButton();
		_spawnPointTypeOption.AddItem("Standard_Idle", 0);
		_spawnPointTypeOption.AddItem("Seated_Idle", 1);
		_spawnPointTypeOption.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		typeContainer.AddChild(_spawnPointTypeOption);
		
		var listLabel = new Label();
		listLabel.Text = "Points enregistres:";
		_mainContainer.AddChild(listLabel);
		
		_spawnPointsList = new ItemList();
		_spawnPointsList.CustomMinimumSize = new Vector2(0, 150);
		_spawnPointsList.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		_mainContainer.AddChild(_spawnPointsList);
		
		var buttonsContainer = new HBoxContainer();
		_mainContainer.AddChild(buttonsContainer);
		
		_removeSpawnPointButton = new Button();
		_removeSpawnPointButton.Text = "Supprimer selectionne";
		_removeSpawnPointButton.Pressed += OnRemoveSpawnPoint;
		buttonsContainer.AddChild(_removeSpawnPointButton);
		
		var clearButton = new Button();
		clearButton.Text = "Tout effacer";
		clearButton.Pressed += OnClearSpawnPoints;
		buttonsContainer.AddChild(clearButton);
		
		_saveConfigButton = new Button();
		_saveConfigButton.Text = "Sauvegarder configuration JSON";
		_saveConfigButton.Pressed += OnSaveConfiguration;
		_mainContainer.AddChild(_saveConfigButton);
	}

	private CameraConfigPanel CreateCameraConfigPanel(string cameraName, Color accentColor)
	{
		return new CameraConfigPanel(cameraName, accentColor, this);
	}

	private void AddSeparator()
	{
		var separator = new HSeparator();
		separator.CustomMinimumSize = new Vector2(0, 10);
		_mainContainer.AddChild(separator);
	}

	private void OnBrowsePressed()
	{
		var fileDialog = new EditorFileDialog();
		fileDialog.FileMode = EditorFileDialog.FileModeEnum.OpenFile;
		fileDialog.Filters = new string[] { "*.tscn ; Scene Files" };
		fileDialog.Access = EditorFileDialog.AccessEnum.Resources;
		fileDialog.FileSelected += OnFileSelected;
		fileDialog.PopupCentered(new Vector2I(800, 600));
		_dockPanel.AddChild(fileDialog);
	}

	private void OnFileSelected(string path)
	{
		_scenePathInput.Text = path;
		GD.Print($"Fichier selectionne: {path}");
	}

	private void OnLoadScenePressed()
	{
		string scenePath = _scenePathInput.Text.Trim();
		
		if (string.IsNullOrEmpty(scenePath))
		{
			UpdateStatus("Erreur: Chemin vide", Colors.Red);
			return;
		}

		if (!ResourceLoader.Exists(scenePath))
		{
			UpdateStatus($"Erreur: Fichier introuvable - {scenePath}", Colors.Red);
			return;
		}

		try
		{
			if (_loadedScene != null)
			{
				_loadedScene.QueueFree();
				_loadedScene = null;
				_cameras.Clear();
			}

			var sceneResource = GD.Load<PackedScene>(scenePath);
			_loadedScene = sceneResource.Instantiate<Node3D>();
			
			var editorInterface = GetEditorInterface();
			var editedSceneRoot = editorInterface.GetEditedSceneRoot();
			
			if (editedSceneRoot != null)
			{
				editedSceneRoot.AddChild(_loadedScene);
				_loadedScene.Owner = editedSceneRoot;
			}

			// Enregistrer le chemin de la scene
			_currentScenePath = scenePath;

			ScanCameras(_loadedScene);
			
			UpdateStatus($"Scene chargee: {scenePath}", Colors.Green);
			UpdateCameraPanels();
			
			// Charger la configuration existante si elle existe
			LoadExistingConfiguration();
		}
		catch (Exception ex)
		{
			UpdateStatus($"Erreur de chargement: {ex.Message}", Colors.Red);
			GD.PrintErr($"Erreur: {ex}");
		}
	}
	
	private void LoadExistingConfiguration()
	{
		try
		{
			var sceneName = Path.GetFileNameWithoutExtension(_currentScenePath);
			var jsonFileName = $"{sceneName}_config.json";
			var jsonPath = Path.Combine(ProjectSettings.GlobalizePath("res://"), "Configs", jsonFileName);
			
			if (File.Exists(jsonPath))
			{
				var json = File.ReadAllText(jsonPath);
				var options = new JsonSerializerOptions
				{
					Converters = { new Vector3JsonConverter() }
				};
				var config = JsonSerializer.Deserialize<DecorConfiguration>(json, options);
				
				if (config != null && config.SpawnPoints != null)
				{
					_spawnPoints.Clear();
					_spawnPoints.AddRange(config.SpawnPoints);
					UpdateSpawnPointsList();
					
					// Recréer les marqueurs visuels
					foreach (var sp in _spawnPoints)
					{
						CreateSpawnPointMarker(sp);
					}
					
					UpdateStatus($"Configuration chargee: {_spawnPoints.Count} points", Colors.Cyan);
				}
			}
		}
		catch (Exception ex)
		{
			GD.Print($"Aucune configuration existante: {ex.Message}");
		}
	}
	
	private void OnSpawnPointModeToggled(bool enabled)
	{
		_isSpawnPointMode = enabled;
		UpdateStatus(enabled ? "Mode placement actif - Cliquez dans la scene 3D" : "Mode placement desactive", 
					enabled ? new Color(0.2f, 1.0f, 0.5f) : Colors.Gray);
	}
	
	private void AddSpawnPoint(Vector3 position)
	{
		var spawnType = _spawnPointTypeOption.Selected == 0 ? SpawnPointType.Standard_Idle : SpawnPointType.Seated_Idle;
		var spawnPoint = new SpawnPointData
		{
			Position = position,
			Type = spawnType,
			Index = _spawnPoints.Count
		};
		
		_spawnPoints.Add(spawnPoint);
		UpdateSpawnPointsList();
		UpdateStatus($"Point d'apparition ajoute: {spawnType} a {position}", Colors.Green);
		
		CreateSpawnPointMarker(spawnPoint);
	}
	
	private void CreateSpawnPointMarker(SpawnPointData spawnPoint)
	{
		if (_loadedScene == null) return;
		
		var marker = new MeshInstance3D();
		marker.Name = $"SpawnPoint_{spawnPoint.Index}_{spawnPoint.Type}";
		
		var sphereMesh = new SphereMesh();
		sphereMesh.Radius = 0.3f;
		sphereMesh.Height = 0.6f;
		marker.Mesh = sphereMesh;
		
		var material = new StandardMaterial3D();
		material.AlbedoColor = spawnPoint.Type == SpawnPointType.Standard_Idle ? Colors.Green : Colors.Blue;
		material.EmissionEnabled = true;
		material.Emission = spawnPoint.Type == SpawnPointType.Standard_Idle ? Colors.Green : Colors.Blue;
		marker.MaterialOverride = material;
		
		marker.GlobalPosition = spawnPoint.Position;
		_loadedScene.AddChild(marker);
		marker.Owner = _loadedScene;
		
		var editorInterface = GetEditorInterface();
		editorInterface.MarkSceneAsUnsaved();
	}
	
	private void UpdateSpawnPointsList()
	{
		_spawnPointsList.Clear();
		for (int i = 0; i < _spawnPoints.Count; i++)
		{
			var sp = _spawnPoints[i];
			var text = $"{i}: {sp.Type} - ({sp.Position.X:F2}, {sp.Position.Y:F2}, {sp.Position.Z:F2})";
			_spawnPointsList.AddItem(text);
		}
	}
	
	private void OnRemoveSpawnPoint()
	{
		var selected = _spawnPointsList.GetSelectedItems();
		if (selected.Length == 0) return;
		
		int index = selected[0];
		if (index >= 0 && index < _spawnPoints.Count)
		{
			var spawnPoint = _spawnPoints[index];
			_spawnPoints.RemoveAt(index);
			
			if (_loadedScene != null)
			{
				var markerName = $"SpawnPoint_{spawnPoint.Index}_{spawnPoint.Type}";
				var marker = _loadedScene.FindChild(markerName, true, false);
				if (marker != null)
				{
					marker.QueueFree();
				}
			}
			
			for (int i = 0; i < _spawnPoints.Count; i++)
			{
				_spawnPoints[i].Index = i;
			}
			
			UpdateSpawnPointsList();
			UpdateStatus($"Point d'apparition {index} supprime", Colors.Orange);
		}
	}
	
	private void OnClearSpawnPoints()
	{
		_spawnPoints.Clear();
		
		if (_loadedScene != null)
		{
			foreach (Node child in _loadedScene.GetChildren())
			{
				if (child.Name.ToString().StartsWith("SpawnPoint_"))
				{
					child.QueueFree();
				}
			}
		}
		
		UpdateSpawnPointsList();
		UpdateStatus("Tous les points d'apparition supprimes", Colors.Orange);
	}
	
	private void OnSaveConfiguration()
	{
		if (string.IsNullOrEmpty(_currentScenePath))
		{
			UpdateStatus("Erreur: Aucune scene chargee", Colors.Red);
			return;
		}
		
		try
		{
			var config = new DecorConfiguration
			{
				ScenePath = _currentScenePath,
				SceneName = Path.GetFileNameWithoutExtension(_currentScenePath),
				SpawnPoints = _spawnPoints,
				SavedAt = DateTime.UtcNow
			};
			
			var jsonFileName = $"{config.SceneName}_config.json";
			var jsonPath = Path.Combine(ProjectSettings.GlobalizePath("res://"), "Configs", jsonFileName);
			
			var configDir = Path.GetDirectoryName(jsonPath);
			if (!Directory.Exists(configDir))
			{
				Directory.CreateDirectory(configDir);
			}
			
			var options = new JsonSerializerOptions
			{
				WriteIndented = true,
				Converters = { new Vector3JsonConverter() }
			};
			var json = JsonSerializer.Serialize(config, options);
			
			File.WriteAllText(jsonPath, json);
			
			UpdateStatus($"Configuration sauvegardee: {jsonFileName}", Colors.Green);
			GD.Print($"Configuration sauvegardee dans: {jsonPath}");
		}
		catch (Exception ex)
		{
			UpdateStatus($"Erreur sauvegarde: {ex.Message}", Colors.Red);
			GD.PrintErr($"Erreur: {ex}");
		}
	}

	private void ScanCameras(Node node)
	{
		if (node is Camera3D camera)
		{
			string cameraName = node.Name;
			if (cameraName == "Title_Camera3D" || cameraName == "Lobby_Camera3D" || cameraName == "Game_Camera3D")
			{
				_cameras[cameraName] = camera;
				GD.Print($"Camera trouvee: {cameraName}");
			}
		}

		foreach (Node child in node.GetChildren())
		{
			ScanCameras(child);
		}
	}

	private void UpdateCameraPanels()
	{
		_titleCameraPanel.UpdateFromCamera(_cameras.GetValueOrDefault("Title_Camera3D"));
		_lobbyCameraPanel.UpdateFromCamera(_cameras.GetValueOrDefault("Lobby_Camera3D"));
		_gameCameraPanel.UpdateFromCamera(_cameras.GetValueOrDefault("Game_Camera3D"));
	}

	private void UpdateStatus(string message, Color color)
	{
		_statusLabel.Text = message;
		_statusLabel.AddThemeColorOverride("font_color", color);
		GD.Print($"Status: {message}");
	}

	public void ApplyCameraChanges(string cameraName, string newName, Vector3 position, Vector3 rotation)
	{
		if (!_cameras.ContainsKey(cameraName))
		{
			UpdateStatus($"Erreur: Camera {cameraName} non trouvee", Colors.Red);
			return;
		}

		var camera = _cameras[cameraName];
		
		try
		{
			if (!string.IsNullOrEmpty(newName) && newName != cameraName)
			{
				camera.Name = newName;
				_cameras.Remove(cameraName);
				_cameras[newName] = camera;
			}

			camera.GlobalPosition = position;
			camera.GlobalRotation = rotation;

			UpdateStatus($"Camera {cameraName} mise a jour", Colors.Green);
			
			var editorInterface = GetEditorInterface();
			editorInterface.MarkSceneAsUnsaved();
		}
		catch (Exception ex)
		{
			UpdateStatus($"Erreur lors de la mise a jour: {ex.Message}", Colors.Red);
			GD.PrintErr($"Erreur: {ex}");
		}
	}

	public void CreateCamera(string cameraName)
	{
		if (_loadedScene == null)
		{
			UpdateStatus("Erreur: Aucune scene chargee", Colors.Red);
			return;
		}

		try
		{
			var newCamera = new Camera3D();
			newCamera.Name = cameraName;
			newCamera.GlobalPosition = Vector3.Zero;
			newCamera.GlobalRotation = Vector3.Zero;

			_loadedScene.AddChild(newCamera);
			newCamera.Owner = _loadedScene;

			_cameras[cameraName] = newCamera;
			UpdateCameraPanels();
			UpdateStatus($"Camera {cameraName} creee", Colors.Green);

			var editorInterface = GetEditorInterface();
			editorInterface.MarkSceneAsUnsaved();
		}
		catch (Exception ex)
		{
			UpdateStatus($"Erreur lors de la creation: {ex.Message}", Colors.Red);
			GD.PrintErr($"Erreur: {ex}");
		}
	}
}

public partial class CameraConfigPanel : VBoxContainer
{
	private readonly string _cameraName;
	private readonly Color _accentColor;
	private readonly DecorManagerTool _tool;

	private LineEdit _nameInput;
	private SpinBox _posXInput;
	private SpinBox _posYInput;
	private SpinBox _posZInput;
	private SpinBox _rotXInput;
	private SpinBox _rotYInput;
	private SpinBox _rotZInput;
	private Button _applyButton;
	private Button _createButton;
	private Label _statusLabel;

	private Camera3D _camera;

	public CameraConfigPanel(string cameraName, Color accentColor, DecorManagerTool tool)
	{
		_cameraName = cameraName;
		_accentColor = accentColor;
		_tool = tool;

		CreateUI();
	}

	private void CreateUI()
	{
		var headerContainer = new HBoxContainer();
		AddChild(headerContainer);

		var titleLabel = new Label();
		titleLabel.Text = _cameraName;
		titleLabel.AddThemeFontSizeOverride("font_size", 14);
		titleLabel.AddThemeColorOverride("font_color", _accentColor);
		headerContainer.AddChild(titleLabel);

		_statusLabel = new Label();
		_statusLabel.Text = " (Non trouvee)";
		_statusLabel.AddThemeColorOverride("font_color", Colors.Gray);
		headerContainer.AddChild(_statusLabel);

		var nameContainer = new HBoxContainer();
		AddChild(nameContainer);

		var nameLabel = new Label();
		nameLabel.Text = "Nom:";
		nameLabel.CustomMinimumSize = new Vector2(80, 0);
		nameContainer.AddChild(nameLabel);

		_nameInput = new LineEdit();
		_nameInput.PlaceholderText = _cameraName;
		_nameInput.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		nameContainer.AddChild(_nameInput);

		AddChild(new Label { Text = "Position:" });
		var posContainer = new HBoxContainer();
		AddChild(posContainer);

		_posXInput = CreateSpinBox("X:", -1000, 1000);
		_posYInput = CreateSpinBox("Y:", -1000, 1000);
		_posZInput = CreateSpinBox("Z:", -1000, 1000);

		posContainer.AddChild(_posXInput);
		posContainer.AddChild(_posYInput);
		posContainer.AddChild(_posZInput);

		AddChild(new Label { Text = "Rotation (degres):" });
		var rotContainer = new HBoxContainer();
		AddChild(rotContainer);

		_rotXInput = CreateSpinBox("X:", -180, 180);
		_rotYInput = CreateSpinBox("Y:", -180, 180);
		_rotZInput = CreateSpinBox("Z:", -180, 180);

		rotContainer.AddChild(_rotXInput);
		rotContainer.AddChild(_rotYInput);
		rotContainer.AddChild(_rotZInput);

		var buttonContainer = new HBoxContainer();
		AddChild(buttonContainer);

		_applyButton = new Button();
		_applyButton.Text = "Appliquer";
		_applyButton.Pressed += OnApplyPressed;
		_applyButton.Disabled = true;
		buttonContainer.AddChild(_applyButton);

		_createButton = new Button();
		_createButton.Text = "Creer";
		_createButton.Pressed += OnCreatePressed;
		_createButton.Visible = false;
		buttonContainer.AddChild(_createButton);
	}

	private SpinBox CreateSpinBox(string label, double minValue, double maxValue)
	{
		var container = new VBoxContainer();
		container.SizeFlagsHorizontal = Control.SizeFlags.Fill;

		var labelNode = new Label();
		labelNode.Text = label;
		container.AddChild(labelNode);

		var spinBox = new SpinBox();
		spinBox.MinValue = minValue;
		spinBox.MaxValue = maxValue;
		spinBox.Step = 0.1;
		spinBox.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		container.AddChild(spinBox);

		return spinBox;
	}

	public void UpdateFromCamera(Camera3D camera)
	{
		_camera = camera;

		if (camera != null)
		{
			_nameInput.Text = camera.Name;
			_posXInput.Value = camera.GlobalPosition.X;
			_posYInput.Value = camera.GlobalPosition.Y;
			_posZInput.Value = camera.GlobalPosition.Z;
			_rotXInput.Value = Mathf.RadToDeg(camera.GlobalRotation.X);
			_rotYInput.Value = Mathf.RadToDeg(camera.GlobalRotation.Y);
			_rotZInput.Value = Mathf.RadToDeg(camera.GlobalRotation.Z);

			_statusLabel.Text = " (Trouvee)";
			_statusLabel.AddThemeColorOverride("font_color", Colors.Green);
			_applyButton.Disabled = false;
			_createButton.Visible = false;
		}
		else
		{
			_nameInput.Text = "";
			_posXInput.Value = 0;
			_posYInput.Value = 0;
			_posZInput.Value = 0;
			_rotXInput.Value = 0;
			_rotYInput.Value = 0;
			_rotZInput.Value = 0;

			_statusLabel.Text = " (Non trouvee)";
			_statusLabel.AddThemeColorOverride("font_color", Colors.Gray);
			_applyButton.Disabled = true;
			_createButton.Visible = true;
		}
	}

	private void OnApplyPressed()
	{
		if (_camera == null) return;

		string newName = string.IsNullOrEmpty(_nameInput.Text) ? _cameraName : _nameInput.Text;
		var position = new Vector3(
			(float)_posXInput.Value,
			(float)_posYInput.Value,
			(float)_posZInput.Value
		);
		var rotation = new Vector3(
			Mathf.DegToRad((float)_rotXInput.Value),
			Mathf.DegToRad((float)_rotYInput.Value),
			Mathf.DegToRad((float)_rotZInput.Value)
		);

		_tool.ApplyCameraChanges(_cameraName, newName, position, rotation);
	}

	private void OnCreatePressed()
	{
		_tool.CreateCamera(_cameraName);
	}
}

public enum SpawnPointType
{
	Standard_Idle,
	Seated_Idle
}

public class SpawnPointData
{
	public Vector3 Position { get; set; }
	public SpawnPointType Type { get; set; }
	public int Index { get; set; }
}

public class DecorConfiguration
{
	public string ScenePath { get; set; }
	public string SceneName { get; set; }
	public List<SpawnPointData> SpawnPoints { get; set; }
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
