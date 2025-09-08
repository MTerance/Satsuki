# TEXTURE ROUTES - Mode d'emploi simple

## 🛣️ Comment utiliser les textures de routes

### 1. Préparation des fichiers

Créez un dossier `roads` dans votre dossier de textures :
```
[Votre dossier textures]/
├── buildings/          (pour les bâtiments)
└── roads/             (NOUVEAU - pour les routes)
    ├── asphalt_quad.jpg      (texture principale 4 zones)
    ├── asphalt_normal.jpg    (normal map - optionnel)
    └── asphalt_specular.jpg  (specular map - optionnel)
```

### 2. Format de la texture principale

La texture `asphalt_quad.jpg` doit contenir **4 zones disposées ainsi** :

```
┌─────────────────┬─────────────────┐
│   TROTTOIR      │   CENTRE        │
│   BÉTON         │   ROUTE         │
│  (Haut droite)  │  (Haut gauche)  │
├─────────────────┼─────────────────┤
│   TROTTOIR      │   BORDS         │
│   CARRELAGE     │   ROUTE         │
│  (Bas gauche)   │  (Bas droite)   │
└─────────────────┴─────────────────┘
```

**Important** : Les lignes blanches des bords de route doivent être **parallèles aux trottoirs** !

### 3. Dans Blender

1. **Installer l'addon** v1.5.0
2. **Activer "Advanced Texture System"** ✅
3. **Définir votre "Texture Base Path"** 📁
4. **Cliquer "🛣️ Test Routes"** pour voir le résultat

### 4. Résultat

L'addon créera automatiquement :
- ✅ **Centre de route** → Zone haut gauche de votre texture
- ✅ **Bords de route** → Zone bas droite (lignes blanches)  
- ✅ **Trottoir béton** → Zone haut droite
- ✅ **Trottoir carrelage** → Zone bas gauche

## 🎨 Conseils pour créer votre texture

### Dimensions recommandées
- **2048x2048** pixels (qualité standard)
- **4096x4096** pixels (haute qualité)

### Contenu de chaque zone (1024x1024 chacune)
1. **Haut gauche (Centre route)** : Asphalte gris uniforme
2. **Bas droite (Bords route)** : Asphalte + ligne blanche horizontale
3. **Haut droite (Trottoir béton)** : Texture béton gris clair
4. **Bas gauche (Trottoir carrelage)** : Motif carreaux/pavés

### Astuces
- Gardez les **bordures de zones compatibles** pour éviter les coupures
- La **ligne blanche** doit être **horizontale** dans votre image
- Utilisez des **couleurs réalistes** (gris foncé route, gris clair trottoir)

## 🔧 Dépannage rapide

### "Mes textures n'apparaissent pas"
1. Vérifiez le chemin : `[Base Path]/roads/asphalt_quad.jpg`
2. Utilisez "🔍 Diagnostic Textures" pour débugger
3. Assurez-vous que le fichier fait moins de 50MB

### "Le mapping est incorrect"
- L'addon gère automatiquement le mapping UV
- Ne modifiez pas manuellement les coordonnées UV
- Chaque surface utilisera automatiquement sa zone

### "Performance lente"
- Utilisez des textures 2K au lieu de 4K
- Les normal/specular maps sont optionnelles

---

**Créé avec Tokyo City Generator v1.5.0** 🏙️
