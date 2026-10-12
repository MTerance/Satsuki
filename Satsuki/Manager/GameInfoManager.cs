using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.Json.Nodes;
using System.Threading.Tasks;

namespace Satsuki.Manager
{
    public class GameInfoManager
    {

        static public GameInfoManager Instance { get; private set; } = new GameInfoManager();
        private Dictionary<string,JsonObject> _gameInfos = new Dictionary<string, JsonObject>();
        private GameInfoManager()
        {
            LoadDefaultGameInfo();
        }

        private void LoadDefaultGameInfo()
        {
            // Load default game info here
            using (var dbManager = new SqliteDbManager())
            {
                dbManager.OpenConnection();
                using (var connection = dbManager.GetConnection())
                {
                    using (var command = connection.CreateCommand())
                    {
                        command.CommandText = "SELECT Key, Value FROM GameInfo";
                        using (var reader = command.ExecuteReader())
                        {
                            while (reader.Read())
                            {
                                string key = reader.GetString(0);
                                string value = reader.GetString(1);
                                JsonObject jsonValue = JsonNode.Parse(value).AsObject();
                                _gameInfos[key] = jsonValue;
                            }
                        }
                    }
                }
                dbManager.CloseConnection();
            }
        }

        public void SetGameInfo(string key, JsonObject value)
        {
            if (_gameInfos.ContainsKey(key))
            {
                _gameInfos[key] = value;
            }
            else
            {
                _gameInfos.Add(key, value);
            }
        }

        public JsonObject GetGameInfo(string key)
        {
            if (_gameInfos.ContainsKey(key))
            {
                return _gameInfos[key];
            }
            else
            {
                return null;
            }
        }

    }
}
