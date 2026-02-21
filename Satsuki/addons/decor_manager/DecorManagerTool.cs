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
		return (_isSpawnPointMode || _isMenuRenderingMode) && @object is Node3D;
	}

	private void CreateDockPanel()
	{
		_dockPanel = new Control();
		_dockPanel.Name = "Decor Manager";
		GD.Print("DecorManagerTool: Creation du panneau de dock...");
        var scrollContainer = new ScrollContainer();
		scrollContainer.SizeFlagsHorizontal = Control.SizeFlags.Fill;
		scrollContainer.SizeFlagsVertical = Control.SizeFlags.Fill;
		_dockPanel.AddChild(scrollContainer);
		GD.Print("DecorManagerTool: ScrollContainer ajoute");
		_mainContainer = new VBoxContainer();
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
