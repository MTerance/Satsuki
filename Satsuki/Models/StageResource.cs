using Godot;
using Godot.Collections;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
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
        public StageInfo StageInfo { get; set; } = new StageInfo();

        [Export]
        public string SavedAt { get; set; }


        private void SaveInDb()
        {
            using (var dbManager = new SqliteDbManager())
            {
                dbManager.OpenConnection();
                using (var connection = dbManager.GetConnection())
                {
                    using (var command = connection.CreateCommand())
                    {
                        var LobbyRsc = JsonSerializer.Serialize(this.LobbyInfo);
                        var StageRsc = JsonSerializer.Serialize(this.StageInfo);


                        command.CommandText =
                       $@"INSERT INTO Stages (ID,NAME,SCENE_NAME,SCENE_PATH,LOBBY_RSC,STAGE_RSC)
                        VALUES (
                        CASE WHEN {this.Id} = 0 THEN NULL ELSE {this.Id} END,
                        '{this.Name}','{this.SceneName}','{this.ScenePath}','{LobbyRsc}','{StageRsc}')
                        ON CONFLICT(ID)
                        DO UPDATE SET
                            NAME = excluded.NAME,
                            SCENE_NAME = excluded.SCENE_NAME,
                            SCENE_PATH = excluded.SCENE_PATH,
                            LOBBY_RSC = excluded.LOBBY_RSC,
                            STAGE_RSC = excluded.STAGE_RSC;";
                        command.ExecuteNonQuery();
                    }
                }

                    dbManager.CloseConnection();
            }
        }


        public StageResource GetStageById(int id)
        {
            using (var dbManager = new SqliteDbManager())
            {
                dbManager.OpenConnection();
                using (var connection = dbManager.GetConnection())
                {
                    using (var command = connection.CreateCommand())
                    {
                        command.CommandText = $"SELECT ID,NAME,SCENE_NAME,SCENE_PATH,LOBBY_RSC,STAGE_RSC FROM Stages WHERE ID = {id};";
                        using (var reader = command.ExecuteReader())
                        {
                            if (reader.Read())
                            {
                                var stageResource = new StageResource
                                {
                                    Id = reader.GetInt32(0),
                                    Name = reader.GetString(1),
                                    SceneName = reader.GetString(2),
                                    ScenePath = reader.GetString(3),
                                    LobbyInfo = JsonSerializer.Deserialize<LobbyInfo>(reader.GetString(4)),
                                    StageInfo = JsonSerializer.Deserialize<StageInfo>(reader.GetString(5))
                                };
                                return stageResource;
                            }
                        }
                    }
                }
                dbManager.CloseConnection();
            }
            return null;
        }

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
