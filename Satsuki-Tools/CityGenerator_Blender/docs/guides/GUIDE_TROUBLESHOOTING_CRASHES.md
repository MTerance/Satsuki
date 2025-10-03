# Guide de Dépannage Anti-Crash - City Block Generator

## Vue d'ensemble

Ce guide vous aide à éviter les crashes et résoudre les problèmes de performance avec l'addon City Block Generator.

## 🛡️ Configurations Sécurisées

### Limites Recommandées

| Paramètre | Minimum | Maximum Sûr | Maximum Absolu |
|-----------|---------|-------------|----------------|
| Largeur grille | 1 | 3 | 5 |
| Longueur grille | 1 | 3 | 5 |
| Étages maximum | 1 | 5 | 15 |
| Bâtiments/bloc | 1 | 1 | 2 |
| **Total blocs** | **1** | **9** | **25** |

### Configurations Testées

- ✅ **1x1** : Configuration minimale, toujours sûre
- ✅ **2x2** : Petite ville, performances excellentes
- ✅ **3x3** : Configuration optimale recommandée
- ⚠️ **4x4** : Attention aux performances
- ❌ **5x5+** : Risque de crash élevé

## 🚨 Signaux d'Alerte

### Dans l'Interface

L'interface affiche des avertissements automatiques :

- 🟢 **Configuration sûre** : Pas de message
- 🟡 **Attention Performance** : Plus de 35 bâtiments
- 🔴 **Configuration dangereuse** : Plus de 25 blocs

### Avant le Crash

Signes avant-coureurs :
- Blender devient lent
- Mémoire RAM élevée (>4GB pour Blender)
- Ventilateurs qui s'activent
- Interface qui ne répond plus

## 🔧 Solutions aux Problèmes

### Crash Pendant la Génération

**Symptôme** : Blender se ferme brutalement

**Solutions** :
1. Réduire la taille de la grille (3x3 max)
2. Utiliser 1 bâtiment par bloc uniquement
3. Limiter les étages à 5
4. Sauvegarder avant la génération
5. Fermer les autres applications

### Performance Lente

**Symptôme** : Génération très lente ou Blender qui rame

**Solutions** :
1. Utiliser des grilles 2x2 ou plus petites
2. Désactiver le mode organique temporairement
3. Réduire la variété des bâtiments
4. Augmenter la RAM disponible

### Erreurs de Mémoire

**Symptôme** : Messages d'erreur de mémoire

**Solutions** :
1. Fermer tous les autres programmes
2. Redémarrer Blender
3. Utiliser des configurations plus petites
4. Vérifier 8GB+ RAM disponible

## 🎯 Configurations Recommandées

### Pour Débuter
```
Largeur: 2
Longueur: 2
Étages max: 3
Bâtiments/bloc: 1
```

### Pour le Développement
```
Largeur: 3
Longueur: 3
Étages max: 5
Bâtiments/bloc: 1
```

### Pour la Production
```
Largeur: 1-2
Longueur: 1-2
Étages max: 3-5
Bâtiments/bloc: 1
```

## 🧪 Tests de Validation

### Avant Utilisation

Exécutez les tests automatiques :
```bash
cd tests/
python test_simple.py
```

### Vérifications Manuelles

1. **Test minimal** : Générez une grille 1x1
2. **Test normal** : Générez une grille 2x2
3. **Test limite** : Générez une grille 3x3
4. **Surveillance** : Observez l'usage mémoire

## 🔄 Procédure de Récupération

### Si Blender Crash

1. **Redémarrer Blender**
2. **Ouvrir le dernier fichier sauvegardé**
3. **Utiliser une configuration plus petite**
4. **Tester avec 1x1 d'abord**

### Si Performance Dégradée

1. **Sauvegarder le travail**
2. **Fermer et rouvrir Blender**
3. **Supprimer les objets inutiles**
4. **Utiliser des configurations plus petites**

## ⚙️ Optimisations Système

### Configuration Blender

- Fermer les autres fichiers Blender
- Désactiver les add-ons inutiles
- Augmenter la limite de mémoire
- Utiliser un projet vide

### Configuration Système

- Fermer les navigateurs web
- Fermer les applications lourdes
- Vérifier l'espace disque disponible
- Surveiller la température CPU

## 📊 Monitoring

### Indicateurs à Surveiller

- **RAM utilisée** : < 4GB pour Blender
- **CPU** : < 80% d'utilisation
- **Température** : < 70°C
- **Espace disque** : > 2GB libre

### Outils de Monitoring

- Gestionnaire des tâches Windows
- Moniteur de ressources
- HWiNFO64 pour température
- Blender Statistics (coin Blender)

## 🆘 Support et Aide

### Logs de Débogage

Les messages de débogage s'affichent dans :
- Console Python Blender (Window > Toggle System Console)
- Sortie standard lors des tests

### Informations Utiles pour Support

Lors d'un rapport de bug, inclure :
- Version Blender
- Configuration testée (grille, paramètres)
- Message d'erreur complet
- Configuration système (RAM, CPU)
- Étapes pour reproduire

### Tests Automatiques

Utiliser les scripts de test pour valider :
- `test_simple.py` : Tests de base
- `test_safe_configurations.py` : Tests détaillés
- `run_all_tests.py` : Suite complète

## 🔄 Mises à Jour

### Changements v6.13.7

- ✅ Limites de sécurité ajoutées
- ✅ Avertissements dans l'interface
- ✅ Gestion d'erreurs améliorée
- ✅ Optimisations de performance
- ✅ Tests automatiques

### Nouvelles Sécurités

- Limitation automatique à 5x5 maximum
- Validation des paramètres d'entrée
- Gestion d'erreurs dans toutes les fonctions critiques
- Limites de performance pour éviter surcharge
- Avertissements visuels dans l'interface

---

**Dernière mise à jour** : Version 6.13.7  
**Validé avec** : Blender 4.0+  
**Tests** : Suite complète passée ✅