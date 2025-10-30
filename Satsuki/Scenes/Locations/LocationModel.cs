using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes.Locations
{
    public partial class LocationModel : Node3D
    {
        private void getMediaScreen()
        {
            // Find MeshInstance3D with name ending in "_MediaScreen"
            var mediaScreen = FindMediaScreenNode();

            if (mediaScreen != null)
            {
                // Get the SubViewport from MainGameScene
                var subViewport = GetSubViewportFromMainGameScene();

                if (subViewport != null)
                {
                    // Create or modify the MaterialOverlay with ViewportTexture
                    var material = new StandardMaterial3D();

                    // Use the SubViewport as texture
                    var viewportTexture = new ViewportTexture();
                    viewportTexture.ViewportPath = subViewport.GetPath();

                    material.AlbedoTexture = viewportTexture;
                    material.AlbedoColor = Colors.White;
                    material.Metallic = 0.0f;
                    material.Roughness = 0.5f;
                    material.EmissionEnabled = true;
                    material.Emission = Colors.White * 0.1f; // Slight glow effect

                    // Apply the material as overlay
                    mediaScreen.MaterialOverlay = material;

                    GD.Print($"Viewport texture applied to MediaScreen: {mediaScreen.Name}");
                    GD.Print($"SubViewport path: {subViewport.GetPath()}");
                }
                else
                {
                    GD.PrintErr("SubViewport not found in MainGameScene");
                }
            }
            else
            {
                GD.PrintErr("No MeshInstance3D with name ending in '_MediaScreen' found");
            }
        }

        private SubViewport GetSubViewportFromMainGameScene()
        {
            // Get the MainGameScene node
            var mainGameScene = GetNode<Node>("/root/MainGameScene");
            if (mainGameScene == null)
            {
                GD.PrintErr("MainGameScene not found at /root/MainGameScene");
                return null;
            }

            // Search for SubViewport in MainGameScene
            return FindSubViewportRecursive(mainGameScene);
        }

        private SubViewport FindSubViewportRecursive(Node node)
        {
            // Check if current node is a SubViewport
            if (node is SubViewport subViewport)
            {
                GD.Print($"Found SubViewport: {subViewport.Name}");
                return subViewport;
            }

            // Search through children
            foreach (Node child in node.GetChildren())
            {
                var result = FindSubViewportRecursive(child);
                if (result != null)
                    return result;
            }

            return null;
        }

        private MeshInstance3D FindMediaScreenNode()
        {
            // Search through all children recursively
            return FindMediaScreenRecursive(this);
        }

        private MeshInstance3D FindMediaScreenRecursive(Node node)
        {
            // Check if current node is a MeshInstance3D with name ending in "_MediaScreen"
            if (node is MeshInstance3D meshInstance && node.Name.ToString().EndsWith("_MediaScreen"))
            {
                return meshInstance;
            }

            // Search through children
            foreach (Node child in node.GetChildren())
            {
                var result = FindMediaScreenRecursive(child);
                if (result != null)
                    return result;
            }

            return null;
        }

        // Alternative method using GetNode with unique name (if you prefer the % syntax)
        private void getMediaScreenAlternative()
        {
            try
            {
                var mediaScreen = GetNode<MeshInstance3D>("%_MediaScreen");
                var subViewport = GetSubViewportFromMainGameScene();

                if (subViewport != null)
                {
                    // Create and configure material with viewport texture
                    var material = new StandardMaterial3D();

                    var viewportTexture = new ViewportTexture();
                    viewportTexture.ViewportPath = subViewport.GetPath();

                    material.AlbedoTexture = viewportTexture;
                    material.AlbedoColor = Colors.White;
                    material.EmissionEnabled = true;
                    material.Emission = Colors.White * 0.2f;

                    // Apply material overlay
                    mediaScreen.MaterialOverlay = material;

                    GD.Print($"Alternative: Viewport texture applied to MediaScreen: {mediaScreen.Name}");
                }
            }
            catch (Exception ex)
            {
                GD.PrintErr($"Error in alternative method: {ex.Message}");
            }
        }

        // Method to refresh the viewport texture (useful for dynamic updates)
        public void RefreshMediaScreenTexture()
        {
            getMediaScreen();
        }

    }
}
