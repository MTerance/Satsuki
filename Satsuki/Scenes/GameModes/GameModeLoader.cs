using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes.GameModes
{
    public class GameModeLoader
    {

        private string GetGameModePathFromDb(string gameModeName)
        {
           String pathGameMode = string.Empty;

            using (var dbManager = new SqliteDbManager())
            {
                dbManager.OpenConnection();
                using (var connection = dbManager.GetConnection())
                {
                    using (var command = connection.CreateCommand())
                    {
                        command.CommandText = "SELECT Path FROM GameMode WHERE Name = @GameModeName LIMIT 1";
                        command.Parameters.AddWithValue("@GameModeName", gameModeName);
                        var result = command.ExecuteScalar();
                        if (result != null)
                        {
                            pathGameMode = result.ToString();
                            GD.Print($"Game Mode found in DB: {pathGameMode}");
                        }
                        else
                        {
                            GD.Print($"No game mode found in the database for name: {gameModeName}");
                            pathGameMode = string.Empty; // or handle as needed
                        }
                    }
                }
                dbManager.CloseConnection();
            }
            return pathGameMode;
        }
        
        private string GetFilePathMode(string gameModeName)
        {
            var pathGameMode = GetGameModePathFromDb(gameModeName);
            return pathGameMode;
        }



        public bool IsGameExist(string gameModeName)
        {

            // Implement logic to check if the game mode exists
            // For example, check if a file or resource with the given name exists
            return true; // Placeholder return value
        }

        public Node LoadGameMode(string gameModeName)
        {
            var pathGameMode = GetFilePathMode(gameModeName);
            var gameNode = GD.Load<PackedScene>(pathGameMode);
            return gameNode.Instantiate<Node>();
        }

    }
}
