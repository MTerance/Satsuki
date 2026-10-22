using Satsuki.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Repositories.Loaders
{
    public class LobbyScreenContentLoader
    {
        public static LobbyScreenContentLoader GetInstance()
        {
            if (_instance == null)
            {
                _instance = new LobbyScreenContentLoader();
            }
            return _instance;
        }
        
        private static LobbyScreenContentLoader _instance;

        private LobbyScreenContentLoader()
        {
            // Initialisation du gestionnaire de contenu de l'écran du lobby
        }

        public LobbyScreenContent GetLobbyScreenContent(string tagMode)
        {
            LobbyScreenContent content = new LobbyScreenContent();

            using (var dbManager = new SqliteDbManager())
            {
                dbManager.OpenConnection();
                using (var connection = dbManager.GetConnection())
                {
                    using (var command = connection.CreateCommand())
                    {
                     command.CommandText = "SELECT agm.LogoImgPath, agm.BgdImgPath FROM AssetGameMode agm JOIN GameMode gm ON agm.IdGameMode = gm.Id  WHERE gm.Tag = @Tag";
                     command.Parameters.AddWithValue("@TagQuizz", tagMode);
                        using (var reader = command.ExecuteReader())
                        {
                            if (reader.Read())
                            {
                                content.LogoImgPath = reader.GetString(0);
                                content.BackgroundImgPath = reader.GetString(1);
                            }
                        }
                    }
                }
                dbManager.CloseConnection();
            }
            return content;
        }
    }
}
