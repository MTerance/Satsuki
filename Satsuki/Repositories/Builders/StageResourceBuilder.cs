using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace Satsuki.Repositories.Builders
{
    public class StageResourceBuilder
    {
        public List<Tuple<int, string>> GetStages()
        {
            var stages = new List<Tuple<int, string>>();
            using (var dbManager = new SqliteDbManager())
            {
                dbManager.OpenConnection();
                using (var connection = dbManager.GetConnection())
                {
                    using (var command = connection.CreateCommand())
                    {
                        command.CommandText = "SELECT ID, NAME FROM Stages;";
                        using (var reader = command.ExecuteReader())
                        {
                            while (reader.Read())
                            {
                                int id = reader.GetInt32(0);
                                string name = reader.GetString(1);
                                stages.Add(new Tuple<int, string>(id, name));
                            }
                        }
                    }
                }
                dbManager.CloseConnection();
            }
            return stages;
        }

        public StageResourceBuilder()
        {

        }
    }
}
