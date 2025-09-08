# 🔢 SYSTÈME DE VERSIONING AUTOMATIQUE - TOKYO ADDON

## 📋 **CHECKLIST OBLIGATOIRE AVANT DÉPLOIEMENT**

### ✅ **À FAIRE À CHAQUE MODIFICATION** :

1. **📈 INCRÉMENTER LA VERSION** :
   - Modifier `bl_info["version"]` : `(1, 0, X)`
   - Modifier `bl_info["name"]` : `"Tokyo City Generator 1.0.X"`
   - Modifier `bl_label` : `"Tokyo City Generator 1.0.X"`
   - Modifier logs : `"🗾 Tokyo City Generator 1.0.X registered/unregistered!"`

2. **📝 METTRE À JOUR LA DESCRIPTION** :
   - Adapter `bl_info["description"]` selon les changements
   - Résumer les nouveautés principales

3. **🚀 DÉPLOYER** :
   - Exécuter `python DEPLOY_TOKYO_1_0.py`
   - Vérifier la taille du fichier

## 📊 **HISTORIQUE DES VERSIONS** :

- **1.0.1** : Version initiale Tokyo
- **1.0.2** : Corrections bugs de base
- **1.0.3** : Interface Blender 4.x compatible
- **1.0.4** : Routes et trottoirs ajoutés
- **1.0.5** : Variations réalistes (courbes x5)
- **1.0.6** : Révolution urbaine (blocs = trottoirs)
- **1.0.7** : Couverture complète (zéro espace vide)
- **1.0.8** : Géométrie propre (corrections bizarreries)
- **1.0.9** : **PROCHAINE VERSION** → À FAIRE

## 🔄 **SYSTÈME D'AUTO-REMINDER** :

### **AVANT CHAQUE `DEPLOY_TOKYO_1_0.py`** :
```
echo "⚠️  RAPPEL : As-tu mis à jour le numéro de version ?"
echo "📋 Vérifier : bl_info, bl_label, logs"
echo "📈 Version actuelle → Nouvelle version"
```

## 🎯 **CONVENTION DE VERSIONING** :

- **X.Y.Z** format
- **Z** : Corrections de bugs, petites améliorations
- **Y** : Nouvelles fonctionnalités majeures 
- **X** : Refonte complète

## 💡 **SUGGESTIONS D'AMÉLIORATION** :

1. **Script automatique** de mise à jour de version
2. **Fichier VERSION** séparé
3. **Validation** avant déploiement
4. **Changelog** automatique

---

🚨 **RAPPEL PERMANENT** : **TOUJOURS** mettre à jour la version avant déploiement ! 🚨
