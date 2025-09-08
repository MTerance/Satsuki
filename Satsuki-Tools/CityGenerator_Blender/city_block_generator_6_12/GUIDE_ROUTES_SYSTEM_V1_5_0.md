# GUIDE SYSTÈME DE TEXTURES ROUTES - Tokyo City Generator v1.5.0

## 🛣️ NOUVEAUTÉ: Système de Routes et Trottoirs

La version 1.5.0 introduit un système avancé de textures pour les routes avec mapping UV par quadrants.

## 📊 Architecture du Système

### Fichier de Texture Principal
Le système utilise une **texture principale divisée en 4 quadrants** :

```
+-------------------+-------------------+
|                   |                   |
|   TROTTOIR        |   CENTRE          |
|   BÉTON           |   ROUTE           |
|   (Haut droite)   |   (Haut gauche)   |
|                   |                   |
+-------------------+-------------------+
|                   |                   |
|   TROTTOIR        |   BORDS           |
|   CARRELAGE       |   ROUTE           |
|   (Bas gauche)    |   (Bas droite)    |
|                   |                   |
+-------------------+-------------------+
```

### Types de Surfaces Supportés

1. **Centre Route (`road_center`)**
   - Zone: Haut gauche de la texture
   - Usage: Surface principale asphalte
   - Coordonnées UV: (0.0, 0.5) avec échelle (0.5, 0.5)

2. **Bords Route (`road_border`)**
   - Zone: Bas droite de la texture
   - Usage: Lignes blanches parallèles aux trottoirs
   - Coordonnées UV: (0.5, 0.0) avec échelle (0.5, 0.5)

3. **Trottoir Béton (`sidewalk_concrete`)**
   - Zone: Haut droite de la texture
   - Usage: Trottoirs en béton
   - Coordonnées UV: (0.5, 0.5) avec échelle (0.5, 0.5)

4. **Trottoir Carrelage (`sidewalk_tiles`)**
   - Zone: Bas gauche de la texture
   - Usage: Trottoirs carrelés
   - Coordonnées UV: (0.0, 0.0) avec échelle (0.5, 0.5)

## 📁 Structure des Fichiers Requis

Placez les fichiers dans : `[Texture Base Path]/roads/`

### Fichiers Obligatoires :
- `asphalt_quad.jpg` - Texture principale avec 4 zones
- `asphalt_normal.jpg` - Normal map (optionnel)
- `asphalt_specular.jpg` - Specular map (optionnel)

### Recommandations :
- **Taille**: 2048x2048 ou 4096x4096 pixels
- **Format**: JPG, PNG, ou EXR
- **Qualité**: Haute résolution pour détails fins

## 🎛️ Interface Utilisateur

### Nouvel Opérateur : Test Routes
Le bouton **"🛣️ Test Routes"** dans le panneau Tokyo crée :

1. **4 sections de test** séparées montrant chaque quadrant
2. **1 route complète** de démonstration  
3. **Bâtiments de contexte** pour simulation urbaine
4. **Labels 3D** pour identifier chaque section

### Accès au Test :
1. Activer "Advanced Texture System"
2. Définir "Texture Base Path"
3. Cliquer "🛣️ Test Routes"

## ⚙️ Configuration Technique

### Propriétés Matériau Route :
- **Roughness**: 0.9 (asphalte rugueux)
- **Specular**: 0.2 (légère réflexion)
- **Metallic**: 0.0 (non métallique)

### Propriétés Matériau Trottoir :
- **Roughness**: 0.8 (béton/carrelage)
- **Specular**: 0.3 (plus réfléchissant)
- **Metallic**: 0.0 (non métallique)

## 🔧 API de Développement

### Classe `TokyoRoadTextureSystem`

```python
# Créer une instance
road_system = TokyoRoadTextureSystem(texture_base_path)

# Créer un matériau de route
material = road_system.create_road_material(
    road_type="road_center",  # ou "road_border", "sidewalk_concrete", "sidewalk_tiles"
    material_name="My_Road"
)

# Créer un matériau de trottoir spécifique
sidewalk_mat = road_system.create_sidewalk_material("concrete")
```

### Méthodes Disponibles :

- `create_road_material(road_type, material_name)` - Matériau route principal
- `create_sidewalk_material(sidewalk_type)` - Matériau trottoir
- `setup_road_texture_folders()` - Créer structure de dossiers

## 🚀 Migration depuis v1.4.1

### Changements :
1. **Nouvelle classe** : `TokyoRoadTextureSystem` ajoutée
2. **Nouveau bouton** : "🛣️ Test Routes" dans l'interface  
3. **Import étendu** : `from .texture_system import TokyoRoadTextureSystem`
4. **Version** : 1.4.1 → 1.5.0

### Compatibilité :
- **Rétrocompatible** : Système de bâtiments inchangé
- **Nouveau dossier** : `/roads/` ajouté automatiquement
- **Interface** : Bouton test uniquement si "Advanced Texture" activé

## 🎨 Guide de Création de Textures

### Préparation de la Texture Quadrant :

1. **Créer un canvas 2048x2048**
2. **Diviser en 4 zones égales** (1024x1024 chacune)
3. **Placer les textures** selon le schéma ci-dessus
4. **Assurer la continuité** aux bordures
5. **Exporter en haute qualité**

### Conseils Artistiques :
- **Centre route** : Asphalte uniforme, traces d'usure
- **Bords route** : Lignes blanches nettes, marquages routiers
- **Trottoir béton** : Surface rugueuse, joints de dilatation
- **Trottoir carrelage** : Motifs répétitifs, joints apparents

## 🐛 Dépannage

### Problèmes Courants :

1. **Textures non appliquées**
   - Vérifier le chemin : `[Base Path]/roads/asphalt_quad.jpg`
   - Utiliser "🔍 Diagnostic Textures" pour debug

2. **Mapping incorrect**
   - Coordonnées UV automatiques, pas de modification manuelle
   - Chaque quadrant est mappé automatiquement

3. **Performance**
   - Textures 4K peuvent ralentir sur machines anciennes
   - Utiliser 2K pour équilibre qualité/performance

### Debug :
- Le système utilise des **fallbacks procéduraux** si fichiers manquants
- Messages d'erreur détaillés dans la console Blender
- Test visuel avec cubes démo pour validation

## 🏗️ Roadmap Future

### Prochaines Versions :
- **Intersections complexes** avec textures spécialisées
- **Marquage routier** procédural (flèches, passages piétons)
- **Usure dynamique** basée sur trafic simulé
- **Intégration OSM** pour routes réelles

---

**Tokyo City Generator v1.5.0**  
*Système de textures routes et trottoirs*  
Développé par Tokyo Urban Designer
