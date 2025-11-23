# Instructions pour intégrer Movie Rendering dans DecorManagerTool

**Fichier** : `addons/decor_manager/DecorManagerTool.cs`

---

## Modifications à effectuer

### 1. Dans la méthode `CreateDockPanel()`, ligne ~124-126

**Avant** :
```csharp
		CreateSpawnPointsSection();
		
		AddSeparator();

		_titleCameraPanel = CreateCameraConfigPanel("Title_Camera3D", new Color(1.0f, 0.5f, 0.0f));
```

**Après** :
```csharp
		CreateSpawnPointsSection();
		
		AddSeparator();
		
		CreateMovieRenderingSection();
		
		AddSeparator();

		_titleCameraPanel = CreateCameraConfigPanel("Title_Camera3D", new Color(1.0f, 0.5f, 0.0f));
```

---

## Fichier créé

Le fichier `addons/decor_manager/DecorManagerTool_MovieRendering.cs` contient :
- La méthode `CreateMovieRenderingSection()`
- La méthode `HandleMovieRenderingInput()` 
- Toutes les méthodes pour gérer le movie rendering
- La classe `MovieRenderSurface`

Ces méthodes sont définies comme `partial` de `DecorManagerTool`.

---

## Vérification

Après modification, vérifier que :
1. Le fichier compile sans erreur
2. Le dock affiche la section "Movie Rendering" 
3. Les modes spawn points et movie rendering sont mutuellement exclusifs

---

## Build

```bash
dotnet build
```

Doit réussir sans erreur.
