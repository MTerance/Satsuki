using Godot;
using Satsuki.Repositories.Loaders;
using Satsuki.Scenes.GameModes.Arcade.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes.GameModes.Arcade.Builders
{
    public class ArcadeGameBuilder
    {
        private ArcadeGameRecord record;
        private LocationLoader locationLoader;
        private PlayerLoader playerLoader;
        //
        private Node stage;
        private Dictionary<int, Node> players;


        public ArcadeGameBuilder(ArcadeGameRecord record)
        {
            this.record = record;
            this.locationLoader = new LocationLoader();
            this.playerLoader = new PlayerLoader();
        }


        private void BuildStage()
        {
            var stageRsc = locationLoader.LoadStageRsc(record.IdStage);
            stage = locationLoader.LoadStage(stageRsc);
        }

        private void BuildPlayers()
        {
            foreach (var playerRecord in record.Players)
            {
                var player = playerLoader.LoadPlayerMesh();
                players.Add(playerRecord.Id, player);
                // Add player to the scene or perform other setup
            }
        }

        public Node Build()
        {
            BuildStage();
            BuildPlayers();
            /**/
            var stageRsc = locationLoader.LoadStageRsc(record.IdStage);
            /**/
            var nbPlayers = record.Players.Count;
          //  var positionMainScene = stageRsc.StageInfo.

            /**/
            return stage;

        }


    }
}
