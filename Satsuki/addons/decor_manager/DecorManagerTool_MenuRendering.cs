using Godot;
using System;
using System.Collections.Generic;
using System.IO;

#if TOOLS
/// <summary>
/// Extension du DecorManager pour le Menu Rendering
/// Permet d'afficher les menus UI (Title, MainMenu, Game) sur des surfaces 3D
/// </summary>
public partial class DecorManagerTool
{
	// Champs pour menu rendering
	private CheckBox _menuRenderingModeCheckbox;
	private LineEdit _texturePathInput;
	private Button _browseTextureButton;
	private Button _applyTextureButton;
	private ItemList _renderSurfacesList;
	private ColorPickerButton _emissionColorPicker;
	private SpinBox _emissionEnergySpinBox;
	private OptionButton _menuTypeOption;
	private bool _isMenuRenderingMode = false;
	private readonly List<MenuRenderSurface> _menuRenderSurfaces = new List<MenuRenderSurface>();
	private Node3D _selectedSurface;
	
	/// <summary>
	/// Crée la section Menu Rendering dans l'interface
	/// </summary>
	private void CreateMovieRenderingSection()
	{
		var sectionLabel = new Label();
		sectionLabel.Text = "Menu Rendering (Affichage UI sur surfaces)";
		sectionLabel.AddThemeFontSizeOverride("font_size", 16);
		sectionLabel.AddThemeColorOverride("font_color", new Color(1.0f, 0.2f, 0.8f));
		_mainContainer.AddChild(sectionLabel);
		
		// Mode activation
		_menuRenderingModeCheckbox = new CheckBox();
		_menuRenderingModeCheckbox.Text = "Mode selection actif (cliquez sur une surface)";
		_menuRenderingModeCheckbox.Toggled += OnMenuRenderingModeToggled;
		_mainContainer.AddChild(_menuRenderingModeCheckbox);
		
		// Menu Type selection
		var menuTypeContainer = new HBoxContainer();
		_mainContainer.AddChild(menuTypeContainer);
		
		var menuTypeLabel = new Label();
		menuTypeLabel.Text = "Menu:";
		menuTypeLabel.CustomMinimumSize = new Vector2(80, 0);
		menuTypeContainer.AddChild(menuTypeLabel);
		
		_menuTypeOption = new OptionButton();
		_menuTypeOption.AddItem("Title", 0);
		_menuTypeOption.AddItem("MainMenu", 1);
		_menuTypeOption.AddItem("Game", 2);
		_menuTypeOption.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		menuTypeContainer.AddChild(_menuTypeOption);
		
		// Texture selection
		var textureContainer = new HBoxContainer();
		_mainContainer.AddChild(textureContainer);
		
		var textureLabel = new Label();
		textureLabel.Text = "Texture:";
		textureLabel.CustomMinimumSize = new Vector2(80, 0);
		textureContainer.AddChild(textureLabel);
		
		_texturePathInput = new LineEdit();
		_texturePathInput.PlaceholderText = "res://Assets/Textures/title_screen.png";
		_texturePathInput.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		textureContainer.AddChild(_texturePathInput);
		
		_browseTextureButton = new Button();
		_browseTextureButton.Text = "...";
		_browseTextureButton.Pressed += OnBrowseTexturePressed;
		textureContainer.AddChild(_browseTextureButton);
		
		// Emission settings
		var emissionContainer = new HBoxContainer();
		_mainContainer.AddChild(emissionContainer);
		
		var emissionLabel = new Label();
		emissionLabel.Text = "Emission:";
		emissionLabel.CustomMinimumSize = new Vector2(80, 0);
		emissionContainer.AddChild(emissionLabel);
		
		_emissionColorPicker = new ColorPickerButton();
		_emissionColorPicker.Color = Colors.White;
		_emissionColorPicker.CustomMinimumSize = new Vector2(100, 30);
		emissionContainer.AddChild(_emissionColorPicker);
		
		var energyLabel = new Label();
		energyLabel.Text = "Energy:";
		energyLabel.CustomMinimumSize = new Vector2(60, 0);
		emissionContainer.AddChild(energyLabel);
		
		_emissionEnergySpinBox = new SpinBox();
		_emissionEnergySpinBox.MinValue = 0;
		_emissionEnergySpinBox.MaxValue = 10;
		_emissionEnergySpinBox.Step = 0.1;
		_emissionEnergySpinBox.Value = 1.0;
		_emissionEnergySpinBox.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		emissionContainer.AddChild(_emissionEnergySpinBox);
		
		// Apply button
		_applyTextureButton = new Button();
		_applyTextureButton.Text = "Appliquer menu sur surface selectionnee";
		_applyTextureButton.Pressed += OnApplyTexturePressed;
		_mainContainer.AddChild(_applyTextureButton);
		
		// Liste des surfaces
		var listLabel = new Label();
		listLabel.Text = "Surfaces avec menu rendering:";
		_mainContainer.AddChild(listLabel);
		
		_renderSurfacesList = new ItemList();
		_renderSurfacesList.CustomMinimumSize = new Vector2(0, 120);
		_renderSurfacesList.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		_mainContainer.AddChild(_renderSurfacesList);
		
		// Buttons
		var buttonsContainer = new HBoxContainer();
		_mainContainer.AddChild(buttonsContainer);
		
		var removeSurfaceButton = new Button();
		removeSurfaceButton.Text = "Retirer menu";
		removeSurfaceButton.Pressed += OnRemoveTexturePressed;
		buttonsContainer.AddChild(removeSurfaceButton);
		
		var clearAllButton = new Button();
		clearAllButton.Text = "Tout effacer";
		clearAllButton.Pressed += OnClearAllTexturesPressed;
		buttonsContainer.AddChild(clearAllButton);
		
		var saveButton = new Button();
		saveButton.Text = "Sauvegarder dans JSON";
		saveButton.Pressed += OnSaveMenuRenderingConfig;
		buttonsContainer.AddChild(saveButton);
	}
	
	private void OnMenuRenderingModeToggled(bool enabled)
	{
		_isMenuRenderingMode = enabled;
		
		// Désactiver spawn points si menu rendering est activé
		if (enabled && _isSpawnPointMode)
		{
			_isSpawnPointMode = false;
			_spawnPointModeCheckbox.ButtonPressed = false;
		}
		
		UpdateStatus(enabled ? "Mode menu rendering actif - Cliquez sur une surface" : "Mode menu rendering desactive", 
					enabled ? new Color(1.0f, 0.2f, 0.8f) : Colors.Gray);
	}
	
	private void OnBrowseTexturePressed()
	{
		var fileDialog = new EditorFileDialog();
		fileDialog.FileMode = EditorFileDialog.FileModeEnum.OpenFile;
		fileDialog.Filters = new string[] { "*.png,*.jpg ; Image Files" };
		fileDialog.Access = EditorFileDialog.AccessEnum.Resources;
		fileDialog.FileSelected += OnTextureFileSelected;
		fileDialog.PopupCentered(new Vector2I(800, 600));
		_dockPanel.AddChild(fileDialog);
	}
	
	private void OnTextureFileSelected(string path)
	{
		_texturePathInput.Text = path;
		GD.Print($"Texture selectionnee: {path}");
	}
	
	private void SelectRenderSurface(Node3D surface)
	{
		if (surface == null) return;
		
		_selectedSurface = surface;
		UpdateStatus($"Surface selectionnee: {surface.Name}", Colors.Cyan);
		GD.Print($"Surface selectionnee pour menu rendering: {surface.Name}");
	}
	
	private void OnApplyTexturePressed()
	{
		if (_selectedSurface == null)
		{
			UpdateStatus("Erreur: Aucune surface selectionnee", Colors.Red);
			return;
		}
		
		var texturePath = _texturePathInput.Text.Trim();
		if (string.IsNullOrEmpty(texturePath))
		{
			UpdateStatus("Erreur: Aucune texture specifiee", Colors.Red);
			return;
		}
		
		if (!ResourceLoader.Exists(texturePath))
		{
			UpdateStatus($"Erreur: Fichier introuvable - {texturePath}", Colors.Red);
			return;
		}
		
		try
		{
			var menuType = GetSelectedMenuType();
			ApplyMenuTexture(_selectedSurface, texturePath, menuType);
		}
		catch (Exception ex)
		{
			UpdateStatus($"Erreur application texture: {ex.Message}", Colors.Red);
			GD.PrintErr($"Erreur: {ex}");
		}
	}
	
	private MenuType GetSelectedMenuType()
	{
		switch (_menuTypeOption.Selected)
		{
			case 0: return MenuType.Title;
			case 1: return MenuType.MainMenu;
			case 2: return MenuType.Game;
			default: return MenuType.Title;
		}
	}
	
	private void ApplyMenuTexture(Node3D surface, string texturePath, MenuType menuType)
	{
		// Trouver le MeshInstance3D
		MeshInstance3D meshInstance = null;
		
		if (surface is MeshInstance3D mesh)
		{
			meshInstance = mesh;
		}
		else
		{
			// Chercher un MeshInstance3D enfant
			foreach (Node child in surface.GetChildren())
			{
				if (child is MeshInstance3D childMesh)
				{
					meshInstance = childMesh;
					break;
				}
			}
		}
		
		if (meshInstance == null)
		{
			UpdateStatus($"Erreur: Pas de MeshInstance3D trouve sur {surface.Name}", Colors.Red);
			return;
		}
		
		// Créer le matériau avec la texture
		var material = new StandardMaterial3D();
		
		// Charger la texture
		var texture = GD.Load<Texture2D>(texturePath);
		if (texture != null)
		{
			material.AlbedoTexture = texture;
		}
		
		// Configurer l'émission
		material.EmissionEnabled = true;
		material.Emission = _emissionColorPicker.Color;
		material.EmissionEnergyMultiplier = (float)_emissionEnergySpinBox.Value;
		material.EmissionTexture = material.AlbedoTexture;
		
		// Appliquer le matériau
		meshInstance.MaterialOverride = material;
		
		// Enregistrer dans la liste
		var renderSurface = new MenuRenderSurface
		{
			Surface = meshInstance,
			SurfaceName = meshInstance.Name,
			TexturePath = texturePath,
			MenuType = menuType,
			EmissionColor = _emissionColorPicker.Color,
			EmissionEnergy = (float)_emissionEnergySpinBox.Value
		};
		
		// Vérifier si la surface existe déjà, si oui, la remplacer
		var existingIndex = _menuRenderSurfaces.FindIndex(s => s.SurfaceName == meshInstance.Name);
		if (existingIndex >= 0)
		{
			_menuRenderSurfaces[existingIndex] = renderSurface;
		}
		else
		{
			_menuRenderSurfaces.Add(renderSurface);
		}
		
		UpdateRenderSurfacesList();
		
		UpdateStatus($"Menu {menuType} applique sur {meshInstance.Name}", Colors.Green);
		
		// Marquer la scène comme modifiée
		var editorInterface = EditorInterface.Singleton;
		editorInterface.MarkSceneAsUnsaved();
	}
	
	private void UpdateRenderSurfacesList()
	{
		_renderSurfacesList.Clear();
		for (int i = 0; i < _menuRenderSurfaces.Count; i++)
		{
			var rs = _menuRenderSurfaces[i];
			var text = $"{i}: {rs.SurfaceName} - {rs.MenuType} ({Path.GetFileName(rs.TexturePath)})";
			_renderSurfacesList.AddItem(text);
		}
	}
	
	private void OnRemoveTexturePressed()
	{
		var selected = _renderSurfacesList.GetSelectedItems();
		if (selected.Length == 0) return;
		
		int index = selected[0];
		if (index >= 0 && index < _menuRenderSurfaces.Count)
		{
			var renderSurface = _menuRenderSurfaces[index];
			
			// Retirer le matériau
			if (renderSurface.Surface != null && IsInstanceValid(renderSurface.Surface))
			{
				renderSurface.Surface.MaterialOverride = null;
			}
			
			_menuRenderSurfaces.RemoveAt(index);
			UpdateRenderSurfacesList();
			UpdateStatus($"Menu retire de {renderSurface.SurfaceName}", Colors.Orange);
		}
	}
	
	private void OnClearAllTexturesPressed()
	{
		foreach (var rs in _menuRenderSurfaces)
		{
			if (rs.Surface != null && IsInstanceValid(rs.Surface))
			{
				rs.Surface.MaterialOverride = null;
			}
		}
		
		_menuRenderSurfaces.Clear();
		UpdateRenderSurfacesList();
		UpdateStatus("Tous les menus retires", Colors.Orange);
	}
	
	private void OnSaveMenuRenderingConfig()
	{
		if (string.IsNullOrEmpty(_currentScenePath))
		{
			UpdateStatus("Erreur: Aucune scene chargee", Colors.Red);
			return;
		}
		
		try
		{
			// Charger ou créer la configuration
			var sceneName = Path.GetFileNameWithoutExtension(_currentScenePath);
			var jsonFileName = $"{sceneName}_config.json";
			var jsonPath = Path.Combine(ProjectSettings.GlobalizePath("res://"), "Configs", jsonFileName);
			
			DecorConfiguration config;
			
			// Charger config existante si elle existe
			if (File.Exists(jsonPath))
			{
				var json = File.ReadAllText(jsonPath);
				var options = new System.Text.Json.JsonSerializerOptions
				{
					Converters = { new Vector3JsonConverter() }
				};
				config = System.Text.Json.JsonSerializer.Deserialize<DecorConfiguration>(json, options);
			}
			else
			{
				config = new DecorConfiguration
				{
					ScenePath = _currentScenePath,
					SceneName = sceneName,
					SpawnPoints = new List<SpawnPointData>(),
					SavedAt = DateTime.UtcNow
				};
			}
			
			// Ajouter/mettre à jour les surfaces de menu rendering
			config.MenuRenderSurfaces = _menuRenderSurfaces.ConvertAll(rs => new MenuRenderSurfaceData
			{
				SurfaceName = rs.SurfaceName,
				TexturePath = rs.TexturePath,
				MenuType = rs.MenuType.ToString(),
				EmissionColor = rs.EmissionColor,
				EmissionEnergy = rs.EmissionEnergy
			});
			
			config.SavedAt = DateTime.UtcNow;
			
			// Créer le dossier Configs s'il n'existe pas
			var configDir = Path.GetDirectoryName(jsonPath);
			if (!Directory.Exists(configDir))
			{
				Directory.CreateDirectory(configDir);
			}
			
			// Sérialiser en JSON
			var saveOptions = new System.Text.Json.JsonSerializerOptions
			{
				WriteIndented = true,
				Converters = { new Vector3JsonConverter(), new ColorJsonConverter() }
			};
			var jsonContent = System.Text.Json.JsonSerializer.Serialize(config, saveOptions);
			
			// Sauvegarder
			File.WriteAllText(jsonPath, jsonContent);
			
			UpdateStatus($"Configuration menu rendering sauvegardee: {jsonFileName}", Colors.Green);
			GD.Print($"Menu rendering sauvegarde dans: {jsonPath}");
		}
		catch (Exception ex)
		{
			UpdateStatus($"Erreur sauvegarde: {ex.Message}", Colors.Red);
			GD.PrintErr($"Erreur: {ex}");
		}
	}
	
	/// <summary>
	/// Extension de _Forward3DGuiInput pour gérer le mode menu rendering
	/// À appeler depuis la méthode principale
	/// </summary>
	private int HandleMenuRenderingInput(Camera3D camera, InputEvent @event)
	{
		if (!_isMenuRenderingMode || _isSpawnPointMode)
			return (int)EditorPlugin.AfterGuiInput.Pass;
		
		if (@event is InputEventMouseButton mouseButton && mouseButton.Pressed && mouseButton.ButtonIndex == MouseButton.Left)
		{
			var from = camera.ProjectRayOrigin(mouseButton.Position);
			var to = from + camera.ProjectRayNormal(mouseButton.Position) * 1000;
			
			var spaceState = camera.GetWorld3D().DirectSpaceState;
			var query = PhysicsRayQueryParameters3D.Create(from, to);
			var result = spaceState.IntersectRay(query);
			
			if (result.Count > 0)
			{
				var collider = result["collider"].As<Node3D>();
				SelectRenderSurface(collider);
				return (int)EditorPlugin.AfterGuiInput.Stop;
			}
		}
		
		return (int)EditorPlugin.AfterGuiInput.Pass;
	}
}

/// <summary>
/// Type de menu à afficher
/// </summary>
public enum MenuType
{
	Title,
	MainMenu,
	Game
}

/// <summary>
/// Données pour une surface avec menu rendering (runtime)
/// </summary>
public class MenuRenderSurface
{
	public MeshInstance3D Surface { get; set; }
	public string SurfaceName { get; set; }
	public string TexturePath { get; set; }
	public MenuType MenuType { get; set; }
	public Color EmissionColor { get; set; }
	public float EmissionEnergy { get; set; }
}

/// <summary>
/// Données pour une surface avec menu rendering (serialization)
/// </summary>
public class MenuRenderSurfaceData
{
	public string SurfaceName { get; set; }
	public string TexturePath { get; set; }
	public string MenuType { get; set; }
	public Color EmissionColor { get; set; }
	public float EmissionEnergy { get; set; }
}

/// <summary>
/// Convertisseur JSON pour Color
/// </summary>
public class ColorJsonConverter : System.Text.Json.Serialization.JsonConverter<Color>
{
	public override Color Read(ref System.Text.Json.Utf8JsonReader reader, Type typeToConvert, System.Text.Json.JsonSerializerOptions options)
	{
		if (reader.TokenType != System.Text.Json.JsonTokenType.StartObject)
			throw new System.Text.Json.JsonException();

		float r = 0, g = 0, b = 0, a = 1;

		while (reader.Read())
		{
			if (reader.TokenType == System.Text.Json.JsonTokenType.EndObject)
				return new Color(r, g, b, a);

			if (reader.TokenType == System.Text.Json.JsonTokenType.PropertyName)
			{
				string propertyName = reader.GetString();
				reader.Read();
				
				switch (propertyName)
				{
					case "r":
					case "R":
						r = (float)reader.GetDouble();
						break;
					case "g":
					case "G":
						g = (float)reader.GetDouble();
						break;
					case "b":
					case "B":
						b = (float)reader.GetDouble();
						break;
					case "a":
					case "A":
						a = (float)reader.GetDouble();
						break;
				}
			}
		}

		throw new System.Text.Json.JsonException();
	}

	public override void Write(System.Text.Json.Utf8JsonWriter writer, Color value, System.Text.Json.JsonSerializerOptions options)
	{
		writer.WriteStartObject();
		writer.WriteNumber("r", value.R);
		writer.WriteNumber("g", value.G);
		writer.WriteNumber("b", value.B);
		writer.WriteNumber("a", value.A);
		writer.WriteEndObject();
	}
}
#endif
