# ? Après redémarrage - Checklist

**Utilisez cette checklist après avoir redémarré Windows**

---

## ?? ÉTAPES À SUIVRE

### ? 1. Vérifier que Windows est bien redémarré
- [ ] Windows a redémarré complètement
- [ ] Session utilisateur ouverte

### ? 2. Ouvrir Godot
- [ ] Double-clic sur l'icône Godot
- [ ] Ouvrir le projet "Satsuki"
- [ ] ? Attendre 30-60 secondes (régénération cache)

### ? 3. Activer le plugin
- [ ] Menu : Project ? Project Settings
- [ ] Onglet : Plugins
- [ ] Trouver : "Decor Manager"
- [ ] Cocher : ? la case
- [ ] Cliquer : OK

### ? 4. Vérifier le succès
- [ ] Dock "Decor Manager" visible à droite
- [ ] Console : "DecorManagerTool: Initialisation..."
- [ ] Console : "DecorManagerTool: Dock ajoute"
- [ ] **AUCUN message d'erreur**

---

## ? SI ÇA MARCHE

**FÉLICITATIONS ! Le problème est résolu !**

### Test rapide :
```
1. Dans le dock Decor Manager
2. Saisir : res://Scenes/Locations/Restaurant.tscn
3. Cliquer : "Charger la scene"
4. Vérifier : Caméras détectées
```

---

## ? SI L'ERREUR PERSISTE

**C'est extrêmement improbable après un redémarrage Windows.**

Si ça arrive quand même :

### Vérifier :
1. Windows a bien redémarré (pas juste mise en veille)
2. Godot est fermé complètement avant de rouvrir
3. Le projet Satsuki est bien celui dans `C:\Users\sshom\source\repos\Satsuki\Satsuki`

### Partager :
1. Screenshot de l'erreur exacte
2. Logs de la console Godot (Output ? Debugger)
3. Confirmer que Windows a été redémarré

---

## ?? Logs attendus (succès)

```
Godot Engine v4.x
OpenGL Renderer: ...
DecorManagerTool: Initialisation...
DecorManagerTool: Dock ajoute
```

**Si vous voyez ces logs ? ? SUCCÈS !**

---

*Date : 22 novembre 2025*  
*Action : Post-redémarrage*  
*Objectif : Vérifier que le plugin fonctionne*
