using Godot;
using Godot.Collections;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
    public partial class StageResource : Resource
    {
        public int Id { get; set; }
        [Export]
        public string Name { get; set; }
        [Export]
        public string SceneName { get; set; }
        [Export]
        public string ScenePath { get; set; }
        [Export]
        public Godot.Collections.Array<SpawnPointData> SpawnPoints { get; set; }
        [Export]
        public string SavedAt { get; set; }

        public bool Save(string path)
        {
            try
            {
                var error = ResourceSaver.Save(this, path);

                if (error == Error.Ok)
                {
                    GD.Print($"StageResource sauvegardée: {path}");
                    return true;
                }
                else
                {
                    GD.PrintErr($"Erreur sauvegarde StageResource: {error}");
                    return false;
                }
            }
            catch (Exception ex)
            {
                GD.PrintErr($"Exception sauvegarde: {ex.Message}");
                return false;
            }
        }

        public static StageResource Load(string path)
        {
            try
            {
                if (!ResourceLoader.Exists(path))
                {
                    GD.PrintErr($"Fichier introuvable: {path}");
                    return null;
                }

                var resource = GD.Load<StageResource>(path);
                GD.Print($"StageResource chargée: {path}");
                return resource;
            }
            catch (Exception ex)
            {
                GD.PrintErr($"Exception chargement: {ex.Message}");
                return null;
            }
        }
    }
}
