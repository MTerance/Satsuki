#!/bin/bash

# Script pour packager l'addon City Block Generator
# Supprime l'ancien ZIP et crée un nouveau package

echo "=== PACKAGING CITY BLOCK GENERATOR ADDON ==="
echo ""

# Nom du fichier ZIP
ZIP_NAME="city_block_generator_6_12.zip"
ADDON_DIR="city_block_generator_6_12"

# Vérifier si le dossier de l'addon existe
if [ ! -d "$ADDON_DIR" ]; then
    echo "❌ ERREUR: Le dossier '$ADDON_DIR' n'existe pas!"
    echo "   Assurez-vous d'être dans le bon répertoire."
    exit 1
fi

echo "📁 Dossier source trouvé: $ADDON_DIR"

# Supprimer l'ancien fichier ZIP s'il existe
if [ -f "$ZIP_NAME" ]; then
    echo "🗑️  Suppression de l'ancien fichier: $ZIP_NAME"
    rm "$ZIP_NAME"
    if [ $? -eq 0 ]; then
        echo "   ✓ Ancien ZIP supprimé avec succès"
    else
        echo "   ❌ Erreur lors de la suppression"
        exit 1
    fi
else
    echo "ℹ️  Aucun ancien ZIP à supprimer"
fi

# Créer le nouveau fichier ZIP
echo ""
echo "📦 Création du nouveau package..."
echo "   Source: $ADDON_DIR/"
echo "   Destination: $ZIP_NAME"

# Utiliser zip pour créer l'archive (exclure les fichiers temporaires)
zip -r "$ZIP_NAME" "$ADDON_DIR/" \
    -x "*.pyc" \
    -x "*/__pycache__/*" \
    -x "*.tmp" \
    -x "*.bak" \
    -x "*~" \
    -x ".DS_Store"

# Vérifier le succès de la création
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SUCCÈS! Package créé: $ZIP_NAME"
    
    # Afficher les informations du fichier
    if [ -f "$ZIP_NAME" ]; then
        FILE_SIZE=$(du -h "$ZIP_NAME" | cut -f1)
        echo "   📊 Taille du fichier: $FILE_SIZE"
        
        echo ""
        echo "📋 Contenu de l'archive:"
        unzip -l "$ZIP_NAME" | head -20
        
        echo ""
        echo "🎯 PRÊT POUR L'INSTALLATION:"
        echo "   1. Ouvrez Blender"
        echo "   2. Edit > Preferences > Add-ons"
        echo "   3. Install > Sélectionnez $ZIP_NAME"
        echo "   4. Activez 'City Block Generator'"
    fi
else
    echo ""
    echo "❌ ERREUR lors de la création du package!"
    exit 1
fi

echo ""
echo "=== PACKAGING TERMINÉ ==="
