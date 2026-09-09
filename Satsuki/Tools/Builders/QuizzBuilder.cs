using Godot;
using Satsuki.Interfaces.Quizz;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Metadata;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Tools.Builders
{
    public class QuizzBuilder
    {
        public QuizzBuilder() { }

        private string GetQuizzType(string nameTypeQuizz)
        {
            String quizzType = string.Empty;
            using (var dbManager = new SqliteDbManager())
            {
                dbManager.OpenConnection();
                using (var connection = dbManager.GetConnection())
                {
                    using (var command = connection.CreateCommand())
                    {
                        command.CommandText = "SELECT Filename FROM TypeQuizz WHERE Name = @Name LIMIT 1"; 
                        command.Parameters.AddWithValue("@Name", nameTypeQuizz);
                        var result = command.ExecuteScalar();
                        if (result != null)
                        {
                            quizzType = result.ToString();
                            GD.Print($"Quizz Name: {nameTypeQuizz} -> Quizz Type: {quizzType}");
                        }
                        else
                        {
                            GD.Print($"No quizz type found in the database for quizz name: {nameTypeQuizz}");
                        }
                    }
                }
                dbManager.CloseConnection();
            }
            return quizzType;
        }


       public Node BuildQuizz(IQuizzBlueprint blueprint)
        {
            // Placeholder for actual quizz building logic
            // This method would create and return a Node representing the quizz based on the type and model provided
            // For now, it simply returns a new Node instance

            var quizzType = GetQuizzType(blueprint.TypeQuizz);
            if (string.IsNullOrEmpty(quizzType))
            {
                GD.PrintErr($"Failed to build quizz: No quizz type found for {blueprint.TypeQuizz}");
                return null;
            }
            var node = GD.Load<PackedScene>(quizzType);
            return node.Instantiate<Node>();
        }


    }
}
