using Godot;
using Satsuki.addons.decor_manager.Tools;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.addons.decor_manager
{
#if TOOLS
    [Tool]
    public class SceneManager
    {
        #region Singleton Implementation
        private static SceneManager _instance;
        private static readonly object _lock = new object();

        public static SceneManager Instance
        {
            get
            {
                lock (_lock)
                {
                    if (_instance == null)
                    {
                        _instance = new SceneManager();
                    }
                    return _instance;
                }
            }
        }

        #endregion

        private Node3D _currentSceneRoot;
        private Node3D _loadedScene;
        private SceneManager()
        {
            // Private constructor to prevent instantiation
        }

        public void SetupRootSceneNode()
        {
            var editedSceneNode = EditorInterface.Singleton.GetEditedSceneRoot() as Node3D;
            if (editedSceneNode != null)
            {
                _currentSceneRoot = editedSceneNode;
                editedSceneNode = null;
            }

            var currentSceneRoot = new Node3D();
            currentSceneRoot.Name = "DecorManagerSetup";
            currentSceneRoot.Position = Vector3.Zero;
            // ----------------

            var packedScene = new PackedScene();
            packedScene.Pack(currentSceneRoot);
            var tempScenePath = "res://addons/decor_manager/DecorManager.tscn";
            ResourceSaver.Save(packedScene, tempScenePath);
            EditorInterface.Singleton.OpenSceneFromPath(tempScenePath);

            // ----------------

            _currentSceneRoot = EditorInterface.Singleton.GetEditedSceneRoot() as Node3D;
        }

        public void AddNodeToScene(Node3D node)
        {
            var editedSceneRoot = EditorInterface.Singleton.GetEditedSceneRoot();
            if (editedSceneRoot != null)
            {
                editedSceneRoot.AddChild(node);
                node.Owner = editedSceneRoot;
            }
            else
                _currentSceneRoot.AddChild(node);
        }

        public void RemoveNodeFromScene(Node3D node)
        {
            var editedSceneRoot = EditorInterface.Singleton.GetEditedSceneRoot();
            if (editedSceneRoot != null)
            {
                editedSceneRoot.RemoveChild(node);
            }
            else
                _currentSceneRoot.RemoveChild(node);
            node.QueueFree();
            /*

            if (_currentSceneRoot == null 
                || _loadedScene == null)
            {
                GD.PrintErr("Current scene root is not set. Call SetupRootSceneNode() first.");
                return;
            }
            if (node.GetParent() == _loadedScene)
            {
                _loadedScene.RemoveChild(node);
                node.QueueFree();
            }
            else
            {
                GD.PrintErr("Node is not a child of the loaded scene.");
            }
            */
        }

        public void LoadMainStage(PackedScene scene)
        {
            if (scene == null)
            {
                GD.PrintErr("PackedScene is null. Cannot add to scene.");
                return;
            }
            SetupRootSceneNode();
            _loadedScene = scene.Instantiate<Node3D>();
            _currentSceneRoot.AddChild(_loadedScene);

        }

        public void ClearLoadedScene()
        {
            if (_loadedScene != null)
            {
                _currentSceneRoot.RemoveChild(_loadedScene);
                _loadedScene.QueueFree();
                _loadedScene = null;
            }
        }

        private void CleanupScene()
        {
            if (_currentSceneRoot != null)
            {
                _currentSceneRoot.QueueFree();
                _currentSceneRoot = null;
            }
        }

        public void ResetScene()
        {
            CleanupScene();
            SetupRootSceneNode();
        }

        public void LoadStageScene(string scenePath)
        {
            if (_currentSceneRoot == null)
            {
                GD.PrintErr("Current scene root is not set. Call SetupRootSceneNode() first.");
                return;
            }
            var packedScene = ResourceLoader.Load<PackedScene>(scenePath);
            if (packedScene == null)
            {
                GD.PrintErr($"Failed to load scene at path: {scenePath}");
                return;
            }
            _loadedScene = packedScene.Instantiate<Node3D>();
            if (_loadedScene == null)
            {
                GD.PrintErr($"Failed to instantiate scene from path: {scenePath}");
                return;
            }
            _currentSceneRoot.AddChild(_loadedScene);
        }
    }
#endif
}
