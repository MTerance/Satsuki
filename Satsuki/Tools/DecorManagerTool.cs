using Godot;
using System;
using System.Collections.Generic;

#if TOOLS
namespace Satsuki.Tools
{
	/// <summary>
	/// Outil Godot pour gerer les decors et cameras
	/// Permet de charger des .tscn et configurer les cameras
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
		
		private Node3D _loadedScene;
		private readonly Dictionary<string, Camera3D> _cameras = new Dictionary<string, Camera3D>();

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

			// Titre
			var titleLabel = new Label();
			titleLabel.Text = "DECOR MANAGER";
			titleLabel.AddThemeFontSizeOverride("font_size", 20);
			_mainContainer.AddChild(titleLabel);

			AddSeparator();

			// Section chargement de scene
			CreateSceneLoadingSection();

			AddSeparator();

			// Label de statut
			_statusLabel = new Label();
			_statusLabel.Text = "Aucune scene chargee";
			_statusLabel.AddThemeColorOverride("font_color", new Color(0.7f, 0.7f, 0.7f));
			_mainContainer.AddChild(_statusLabel);

			AddSeparator();

			// Panels de configuration des cameras
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

			// Champ de chemin
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

			// Bouton browse
			var browseButton = new Button();
			browseButton.Text = "...";
			browseButton.Pressed += OnBrowsePressed;
			pathContainer.AddChild(browseButton);

			// Bouton charger
			_loadSceneButton = new Button();
			_loadSceneButton.Text = "Charger la scene";
			_loadSceneButton.Pressed += OnLoadScenePressed;
			_mainContainer.AddChild(_loadSceneButton);
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
				// Decharger la scene precedente
				if (_loadedScene != null)
				{
					_loadedScene.QueueFree();
					_loadedScene = null;
					_cameras.Clear();
				}

				// Charger la nouvelle scene
				var sceneResource = GD.Load<PackedScene>(scenePath);
				_loadedScene = sceneResource.Instantiate<Node3D>();
				
				// Ajouter a l'arbre de l'editeur
				var editorInterface = GetEditorInterface();
				var editedSceneRoot = editorInterface.GetEditedSceneRoot();
				
				if (editedSceneRoot != null)
				{
					editedSceneRoot.AddChild(_loadedScene);
					_loadedScene.Owner = editedSceneRoot;
				}

				// Scanner les cameras
				ScanCameras(_loadedScene);
				
				UpdateStatus($"Scene chargee: {scenePath}", Colors.Green);
				UpdateCameraPanels();
			}
			catch (Exception ex)
			{
				UpdateStatus($"Erreur de chargement: {ex.Message}", Colors.Red);
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
				// Appliquer les changements
				if (!string.IsNullOrEmpty(newName) && newName != cameraName)
				{
					camera.Name = newName;
					_cameras.Remove(cameraName);
					_cameras[newName] = camera;
				}

				camera.GlobalPosition = position;
				camera.GlobalRotation = rotation;

				UpdateStatus($"Camera {cameraName} mise a jour", Colors.Green);
				
				// Marquer la scene comme modifiee
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

	/// <summary>
	/// Panel de configuration pour une camera
	/// </summary>
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
			// Header
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

			// Nom
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

			// Position
			AddChild(new Label { Text = "Position:" });
			var posContainer = new HBoxContainer();
			AddChild(posContainer);

			_posXInput = CreateSpinBox("X:", -1000, 1000);
			_posYInput = CreateSpinBox("Y:", -1000, 1000);
			_posZInput = CreateSpinBox("Z:", -1000, 1000);

			posContainer.AddChild(_posXInput);
			posContainer.AddChild(_posYInput);
			posContainer.AddChild(_posZInput);

			// Rotation
			AddChild(new Label { Text = "Rotation (degres):" });
			var rotContainer = new HBoxContainer();
			AddChild(rotContainer);

			_rotXInput = CreateSpinBox("X:", -180, 180);
			_rotYInput = CreateSpinBox("Y:", -180, 180);
			_rotZInput = CreateSpinBox("Z:", -180, 180);

			rotContainer.AddChild(_rotXInput);
			rotContainer.AddChild(_rotYInput);
			rotContainer.AddChild(_rotZInput);

			// Boutons
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
}
#endif
