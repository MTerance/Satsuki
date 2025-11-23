using Godot;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Satsuki.Tools
{
	/// <summary>
	/// Classe utilitaire pour charger les configurations de décor
	/// </summary>
	public static class DecorLoader
	{
		public static DecorConfiguration LoadConfiguration(string tscnPath)
		{
			if (string.IsNullOrEmpty(tscnPath))
			{
				GD.PrintErr("DecorLoader: Chemin .tscn vide");
				return null;
			}

			try
			{
				var sceneName = Path.GetFileNameWithoutExtension(tscnPath);
				var jsonFileName = $"{sceneName}_config.json";
				var jsonPath = GetConfigPath(jsonFileName);
				
				if (!File.Exists(jsonPath))
				{
					GD.Print($"DecorLoader: Aucune configuration trouvee pour {sceneName}");
					return null;
				}

				var json = File.ReadAllText(jsonPath);
				var options = new JsonSerializerOptions
				{
					Converters = { new Vector3Converter(), new ColorConverter() }
				};
				var config = JsonSerializer.Deserialize<DecorConfiguration>(json, options);
				
				GD.Print($"DecorLoader: Configuration {sceneName} chargee ({config?.SpawnPoints?.Count ?? 0} spawn points, {config?.MenuRenderSurfaces?.Count ?? 0} menu surfaces)");
				
				return config;
			}
			catch (Exception ex)
			{
				GD.PrintErr($"DecorLoader: Erreur chargement configuration - {ex.Message}");
				return null;
			}
		}

		public static (Node3D scene, DecorConfiguration config) LoadDecorWithConfig(string tscnPath)
		{
			if (string.IsNullOrEmpty(tscnPath))
			{
				GD.PrintErr("DecorLoader: Chemin .tscn vide");
				return (null, null);
			}

			if (!ResourceLoader.Exists(tscnPath))
			{
				GD.PrintErr($"DecorLoader: Fichier introuvable - {tscnPath}");
				return (null, null);
			}

			try
			{
				GD.Print($"DecorLoader: Chargement de {tscnPath}");
				var sceneResource = GD.Load<PackedScene>(tscnPath);
				var scene = sceneResource.Instantiate<Node3D>();
				
				var config = LoadConfiguration(tscnPath);
				
				GD.Print($"DecorLoader: Decor charge - Scene: {scene.Name}, Config: {(config != null ? "OK" : "Aucune")}");
				
				return (scene, config);
			}
			catch (Exception ex)
			{
				GD.PrintErr($"DecorLoader: Erreur chargement decor - {ex.Message}");
				return (null, null);
			}
		}

		public static bool HasConfiguration(string tscnPath)
		{
			if (string.IsNullOrEmpty(tscnPath))
				return false;

			var sceneName = Path.GetFileNameWithoutExtension(tscnPath);
			var jsonFileName = $"{sceneName}_config.json";
			var jsonPath = GetConfigPath(jsonFileName);
			
			return File.Exists(jsonPath);
		}

		public static List<SpawnPointData> GetSpawnPoints(string tscnPath)
		{
			var config = LoadConfiguration(tscnPath);
			return config?.SpawnPoints ?? new List<SpawnPointData>();
		}

		public static List<SpawnPointData> GetSpawnPointsByType(string tscnPath, SpawnPointType type)
		{
			var allPoints = GetSpawnPoints(tscnPath);
			return allPoints.FindAll(sp => sp.Type == type);
		}

		public static SpawnPointData GetRandomSpawnPoint(string tscnPath, SpawnPointType? type = null)
		{
			var points = type.HasValue 
				? GetSpawnPointsByType(tscnPath, type.Value) 
				: GetSpawnPoints(tscnPath);
			
			if (points.Count == 0)
				return null;
			
			var random = new Random();
			return points[random.Next(points.Count)];
		}
		
		public static List<MenuRenderSurfaceData> GetMenuRenderSurfaces(string tscnPath)
		{
			var config = LoadConfiguration(tscnPath);
			return config?.MenuRenderSurfaces ?? new List<MenuRenderSurfaceData>();
		}
		
		public static List<MenuRenderSurfaceData> GetMenuRenderSurfacesByType(string tscnPath, string menuType)
		{
			var allSurfaces = GetMenuRenderSurfaces(tscnPath);
			return allSurfaces.FindAll(s => s.MenuType == menuType);
		}

		public static bool SaveConfiguration(DecorConfiguration config)
		{
			if (config == null || string.IsNullOrEmpty(config.SceneName))
			{
				GD.PrintErr("DecorLoader: Configuration invalide");
				return false;
			}

			try
			{
				var jsonFileName = $"{config.SceneName}_config.json";
				var jsonPath = GetConfigPath(jsonFileName);
				
				var configDir = Path.GetDirectoryName(jsonPath);
				if (!Directory.Exists(configDir))
				{
					Directory.CreateDirectory(configDir);
				}
				
				var options = new JsonSerializerOptions
				{
					WriteIndented = true,
					Converters = { new Vector3Converter(), new ColorConverter() }
				};
				var json = JsonSerializer.Serialize(config, options);
				
				File.WriteAllText(jsonPath, json);
				
				GD.Print($"DecorLoader: Configuration sauvegardee - {jsonFileName}");
				return true;
			}
			catch (Exception ex)
			{
				GD.PrintErr($"DecorLoader: Erreur sauvegarde - {ex.Message}");
				return false;
			}
		}

		private static string GetConfigPath(string fileName)
		{
			return Path.Combine(ProjectSettings.GlobalizePath("res://"), "Configs", fileName);
		}

		public static List<string> ListConfiguredDecors()
		{
			var result = new List<string>();
			
			try
			{
				var configDir = Path.Combine(ProjectSettings.GlobalizePath("res://"), "Configs");
				
				if (!Directory.Exists(configDir))
					return result;
				
				var jsonFiles = Directory.GetFiles(configDir, "*_config.json");
				
				foreach (var jsonFile in jsonFiles)
				{
					var config = LoadConfiguration($"res://Scenes/Locations/{Path.GetFileNameWithoutExtension(jsonFile).Replace("_config", "")}.tscn");
					if (config != null && !string.IsNullOrEmpty(config.ScenePath))
					{
						result.Add(config.ScenePath);
					}
				}
				
				GD.Print($"DecorLoader: {result.Count} decors configures trouves");
			}
			catch (Exception ex)
			{
				GD.PrintErr($"DecorLoader: Erreur liste decors - {ex.Message}");
			}
			
			return result;
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
	
	public class MenuRenderSurfaceData
	{
		public string SurfaceName { get; set; }
		public string TexturePath { get; set; }
		public string MenuType { get; set; }
		public Color EmissionColor { get; set; }
		public float EmissionEnergy { get; set; }
	}

	public class DecorConfiguration
	{
		public string ScenePath { get; set; }
		public string SceneName { get; set; }
		public List<SpawnPointData> SpawnPoints { get; set; }
		public List<MenuRenderSurfaceData> MenuRenderSurfaces { get; set; }
		public DateTime SavedAt { get; set; }
	}

	public class Vector3Converter : JsonConverter<Vector3>
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
	
	public class ColorConverter : JsonConverter<Color>
	{
		public override Color Read(ref Utf8JsonReader reader, Type typeToConvert, JsonSerializerOptions options)
		{
			if (reader.TokenType != JsonTokenType.StartObject)
				throw new JsonException();

			float r = 0, g = 0, b = 0, a = 1;

			while (reader.Read())
			{
				if (reader.TokenType == JsonTokenType.EndObject)
					return new Color(r, g, b, a);

				if (reader.TokenType == JsonTokenType.PropertyName)
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

			throw new JsonException();
		}

		public override void Write(Utf8JsonWriter writer, Color value, JsonSerializerOptions options)
		{
			writer.WriteStartObject();
			writer.WriteNumber("r", value.R);
			writer.WriteNumber("g", value.G);
			writer.WriteNumber("b", value.B);
			writer.WriteNumber("a", value.A);
			writer.WriteEndObject();
		}
	}
}
