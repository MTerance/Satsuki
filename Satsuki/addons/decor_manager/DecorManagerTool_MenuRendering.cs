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
