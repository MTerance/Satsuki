using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.addons.decor_manager.Tools
{
#if TOOLS
    [Tool]

    public partial class SpawnPointGizmoPlugin : EditorNode3DGizmoPlugin
    {
        public SpawnPointGizmoPlugin()
        {
            CreateMaterial("main", new Color(0.2f, 0.6f, 1.0f), false,true);
            CreateHandleMaterial("handles");
        }

        public override string _GetGizmoName()
        {
            return "SpawnPointGizmo";
        }

        public override int _GetPriority()
        {
            return 1; // Priorité haute pour s'assurer que le gizmo est utilisé
        }

        public override bool _HasGizmo(Node3D forNode3D)
        {
            // Le gizmo s'affiche pour les nodes dont le nom commence par "SpawnPoint"
            var result = forNode3D.Name.ToString().StartsWith("gizmo_inter_");
            if (result)
                GD.Print($"SpawnPointGizmoPlugin: Gizmo detecte pour {forNode3D.Name}");
            return result;
        }

        public override void _Redraw(EditorNode3DGizmo gizmo)
        {
            gizmo.Clear();

            var node = gizmo.GetNode3D();
            if (node == null)
                return;

            var material = GetMaterial("main", gizmo);
            if (material == null)
                return;

            var lines = new Vector3[]
            {
                // Carré au sol
                new Vector3(-0.5f, 0, -0.5f), new Vector3(0.5f, 0, -0.5f),
                new Vector3(0.5f, 0, -0.5f), new Vector3(0.5f, 0, 0.5f),
                new Vector3(0.5f, 0, 0.5f), new Vector3(-0.5f, 0, 0.5f),
                new Vector3(-0.5f, 0, 0.5f), new Vector3(-0.5f, 0, -0.5f),
                // Flèche vers le haut
                new Vector3(0, 0, 0), new Vector3(0, 1.5f, 0),
                // Croix au sol
                new Vector3(-0.3f, 0, 0), new Vector3(0.3f, 0, 0),
                new Vector3(0, 0, -0.3f), new Vector3(0, 0, 0.3f),
            };

            gizmo.AddLines(lines, material,false);
            GD.Print($"SpawnPointGizmoPlugin: Redraw pour {node.Name}");
        }
    }
#endif
}
