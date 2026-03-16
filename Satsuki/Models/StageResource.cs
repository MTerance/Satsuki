using Godot;
using Godot.Collections;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
    [GlobalClass]
    public partial class StageResource : Resource
    {
        [Export]
        public int Id { get; set; }
        [Export]
        public string Name { get; set; }
        [Export]
        public string SceneName { get; set; }
        [Export]
        public string ScenePath { get; set; }
        [Export]
        public LobbyInfo LobbyInfo { get; set; } = new LobbyInfo();
        [Export]
        public string SavedAt { get; set; }

        public bool Save(string path)
        {
            try
            {
                ResourcePath = path;
                var error = ResourceSaver.Save(this, path, ResourceSaver.SaverFlags.ChangePath);

                if (error == Error.Ok)
                {
                    GD.Print($"StageResource sauvegardee: {path}");
                    var file = FileAccess.Open(path, FileAccess.ModeFlags.Read);
                    if (file != null)
                    {
                        var firstLine = file.GetLine();
                        file.Close();
                        GD.Print($"DEBUG: Premiere ligne du fichier sauvegarde: '{firstLine}'");
                    }
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

                var raw = ResourceLoader.Load(path, "", ResourceLoader.CacheMode.Ignore);
                if (raw is StageResource resource)
                {
                    return resource;
                }
                return null;
            }
            catch (Exception ex)
            {
                GD.PrintErr($"Exception chargement: {ex.Message}");
                return null;
            }
        }
    }
}
