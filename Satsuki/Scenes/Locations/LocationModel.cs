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
        private bool _hasInitialized = false;

        public override void _Ready()
        {
            // Initialize the media screen setup with a delay to ensure everything is loaded
            CallDeferred(nameof(InitializeMediaScreen));
        }

        private void InitializeMediaScreen()
        {
            if (_hasInitialized) return;
            
            GD.Print("🎬 LocationModel: Initializing media screen...");
            
            // Try to set up the media screen
            var mediaScreen = FindMediaScreenNode();
            if (mediaScreen != null)
            {
                GD.Print($"📺 Found MediaScreen: {mediaScreen.Name}");
                SetupMediaScreenWithFallback(mediaScreen);
            }
            else
            {
                GD.Print("📺 No MediaScreen found in this location");
            }
            
            _hasInitialized = true;
        }

        private void SetupMediaScreenWithFallback(MeshInstance3D mediaScreen)
        {
            // First try to find a SubViewport
            var subViewport = GetSubViewportFromMainGameScene();
            
            if (subViewport != null)
            {
                // Success: Set up with viewport texture
                SetupMediaScreenWithViewport(mediaScreen, subViewport);
            }
            else
            {
                // Fallback: Set up with a default material
                SetupMediaScreenWithDefaultMaterial(mediaScreen);
            }
        }

        private void SetupMediaScreenWithViewport(MeshInstance3D mediaScreen, SubViewport subViewport)
        {
            try
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

                GD.Print($"✅ Viewport texture applied to MediaScreen: {mediaScreen.Name}");
                GD.Print($"🔗 SubViewport path: {subViewport.GetPath()}");
            }
            catch (Exception ex)
            {
                GD.PrintErr($"❌ Error setting up viewport texture: {ex.Message}");
                // Fallback to default material if viewport setup fails
                SetupMediaScreenWithDefaultMaterial(mediaScreen);
            }
        }

        private void SetupMediaScreenWithDefaultMaterial(MeshInstance3D mediaScreen)
        {
            try
            {
                // Create a default material for the media screen
                var material = new StandardMaterial3D();
                
                material.AlbedoColor = new Color(0.1f, 0.1f, 0.2f); // Dark blue
                material.EmissionEnabled = true;
                material.Emission = new Color(0.2f, 0.4f, 0.8f); // Blue glow
                material.Metallic = 0.1f;
                material.Roughness = 0.3f;

                // Apply the material as overlay
                mediaScreen.MaterialOverlay = material;

                GD.Print($"📺 Default material applied to MediaScreen: {mediaScreen.Name}");
                GD.Print("ℹ️ SubViewport not available - using fallback material");
            }
            catch (Exception ex)
            {
                GD.PrintErr($"❌ Error setting up default material: {ex.Message}");
            }
        }

        private SubViewport GetSubViewportFromMainGameScene()
        {
            try
            {
                // Get the MainGameScene node
                var mainGameScene = GetNodeOrNull<Node>("/root/MainGameScene");
                if (mainGameScene == null)
                {
                    GD.Print("ℹ️ MainGameScene not found at /root/MainGameScene");
                    return null;
                }

                // Search for SubViewport in MainGameScene
                return FindSubViewportRecursive(mainGameScene);
            }
            catch (Exception ex)
            {
                GD.PrintErr($"❌ Error searching for SubViewport: {ex.Message}");
                return null;
            }
        }

        private SubViewport FindSubViewportRecursive(Node node)
        {
            // Check if current node is a SubViewport
            if (node is SubViewport subViewport)
            {
                GD.Print($"🔍 Found SubViewport: {subViewport.Name}");
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
            // Check if current node is a MeshInstance3D with name ending in "_MediaScreen" or named "MediaScreen"
            if (node is MeshInstance3D meshInstance)
            {
                string nodeName = node.Name.ToString();
                if (nodeName.EndsWith("_MediaScreen") || nodeName == "MediaScreen")
                {
                    return meshInstance;
                }
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

        /// <summary>
        /// Public method to manually refresh the media screen texture
        /// Call this when a SubViewport becomes available
        /// </summary>
        public void RefreshMediaScreenTexture()
        {
            GD.Print("🔄 Refreshing media screen texture...");
            
            var mediaScreen = FindMediaScreenNode();
            if (mediaScreen != null)
            {
                SetupMediaScreenWithFallback(mediaScreen);
            }
            else
            {
                GD.PrintErr("❌ Cannot refresh: MediaScreen not found");
            }
        }

        /// <summary>
        /// Alternative method using GetNode with unique name (if you prefer the % syntax)
        /// </summary>
        public void SetupMediaScreenAlternative()
        {
            try
            {
                var mediaScreen = GetNodeOrNull<MeshInstance3D>("%MediaScreen");
                if (mediaScreen == null)
                {
                    GD.Print("ℹ️ MediaScreen with unique name not found, trying regular search...");
                    mediaScreen = FindMediaScreenNode();
                }

                if (mediaScreen != null)
                {
                    SetupMediaScreenWithFallback(mediaScreen);
                }
                else
                {
                    GD.PrintErr("❌ MediaScreen not found with any method");
                }
            }
            catch (Exception ex)
            {
                GD.PrintErr($"❌ Error in alternative method: {ex.Message}");
            }
        }

        /// <summary>
        /// Creates a SubViewport dynamically if needed
        /// </summary>
        public SubViewport CreateSubViewport(Vector2I size = default)
        {
            try
            {
                if (size == default)
                {
                    size = new Vector2I(512, 512);
                }

                var subViewport = new SubViewport();
                subViewport.Name = "DynamicSubViewport";
                subViewport.Size = size;
                subViewport.RenderTargetUpdateMode = SubViewport.UpdateMode.Always;
                
                // Add to the scene tree
                AddChild(subViewport);
                
                GD.Print($"✅ Created dynamic SubViewport: {size}");
                
                // Try to set up the media screen with this new viewport
                CallDeferred(nameof(RefreshMediaScreenTexture));
                
                return subViewport;
            }
            catch (Exception ex)
            {
                GD.PrintErr($"❌ Error creating SubViewport: {ex.Message}");
                return null;
            }
        }
    }
}
