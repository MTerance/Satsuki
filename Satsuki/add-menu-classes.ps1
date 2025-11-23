# Script pour ajouter les classes manquantes
$file = "C:\Users\sshom\source\repos\Satsuki\Satsuki\addons\decor_manager\DecorManagerTool.cs"

Write-Host "Ajout des classes MenuType, MenuRenderSurfaceData et ColorJsonConverter..." -ForegroundColor Cyan

# Lire le fichier
$content = Get-Content $file -Raw

# Classes à ajouter avant #endif
$addition = @"

public enum MenuType
{
	Title,
	MainMenu,
	Game
}

public class MenuRenderSurfaceData
{
	public string SurfaceName { get; set; }
	public string TexturePath { get; set; }
	public string MenuType { get; set; }
	public Color EmissionColor { get; set; }
	public float EmissionEnergy { get; set; }
}

public class ColorJsonConverter : JsonConverter<Color>
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
"@

# Remplacer #endif par les classes + #endif
$content = $content -replace '#endif$', ($addition + "`n#endif")

# Sauvegarder
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($file, $content, $utf8NoBom)

Write-Host "Classes ajoutees avec succes!" -ForegroundColor Green
