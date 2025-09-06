# Guide de résolution : Addon visible mais non activable

## 🎯 Problème identifié
L'addon "Add Mesh: City Block Generator" apparaît dans la liste des addons Blender mais :
- ❌ La case à cocher ne se coche pas
- ❌ L'addon ne s'active pas
- ❌ Le panneau n'apparaît pas dans la sidebar

## 🔧 Solutions par ordre de priorité

### Solution 1 : Test d'activation dans la console
1. **Ouvrir Blender** et aller dans le workspace **Scripting**
2. **Copier-coller** le contenu du fichier `test_activation_rapide.py` dans la console Python
3. **Appuyer sur Entrée** pour exécuter
4. **Lire les messages** pour identifier le problème exact

### Solution 2 : Activation manuelle forcée
```python
# À copier dans la console Blender
import addon_utils
addon_utils.enable("city_block_generator_6_12", default_set=True, persistent=True)
```

### Solution 3 : Réinstallation propre
1. **Désinstaller** l'addon actuel (si visible dans la liste)
2. **Redémarrer Blender** complètement
3. **Réinstaller** le fichier ZIP `city_block_generator_6_12_v6.21.1.zip`
4. **Cocher la case** dans Preferences > Add-ons

### Solution 4 : Diagnostic complet
1. **Copier** le contenu de `diagnostic_activation_blender.py`
2. **Coller** dans la console Python de Blender
3. **Analyser** le rapport détaillé
4. **Suivre** les recommandations spécifiques

## 🚨 Erreurs courantes et solutions

### Erreur : "Module not found"
**Cause** : Addon mal installé ou nom incorrect
**Solution** : Réinstaller le ZIP, vérifier le nom du dossier

### Erreur : "Registration failed"
**Cause** : Conflit avec autre addon ou erreur de syntaxe
**Solution** : Désactiver autres addons temporairement

### Erreur : "Properties not found"
**Cause** : Propriétés non enregistrées
**Solution** : Utiliser l'opérateur "Réinitialiser Paramètres"

## 📋 Checklist de vérification

- [ ] Blender 4.0+ installé
- [ ] ZIP installé via Install Add-on
- [ ] Addon visible dans la liste
- [ ] Test d'activation en console effectué
- [ ] Messages d'erreur identifiés
- [ ] Solutions appliquées dans l'ordre

## 🎯 Résultat attendu

Une fois l'addon activé :
1. ✅ Case cochée dans la liste des addons
2. ✅ Onglet "CityGen" dans la sidebar 3D (touche N)
3. ✅ Panneau avec paramètres de génération
4. ✅ Bouton "Générer Ville" fonctionnel

## 📞 Dernière solution

Si aucune solution ne fonctionne :
1. **Sauvegarder** vos fichiers Blender importants
2. **Réinitialiser** les préférences Blender
3. **Réinstaller** l'addon dans un Blender "propre"

---

**Version guide** : 6.21.1  
**Compatibilité** : Blender 4.0+  
**Dernière mise à jour** : Décembre 2024
