using Godot;
using Satsuki.Models;
using Satsuki.Repositories.Loaders;
using Satsuki.Scenes.GameModes.Arcade.Models;
using Satsuki.Tools.Converters;
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

		private ArcadeBuildResult result = new ArcadeBuildResult();

        //
        //private Node stage;
		//private Dictionary<int, Node3D> players;


		public ArcadeGameBuilder(ArcadeGameRecord record)
		{
			this.record = record;
			this.locationLoader = new LocationLoader();
			this.playerLoader = new PlayerLoader();
		}


		private void BuildStage()
		{
			var stageRsc = locationLoader.LoadStageRsc(record.IdStage);
			result.Stage = locationLoader.LoadStage(stageRsc);
		}

		private void BuildPlayers()
		{
			foreach (var playerRecord in record.Players)
			{
				var player = playerLoader.LoadPlayerMesh();
				result.Players.Add(playerRecord.Id, player);
				// Add player to the scene or perform other setup
			}
		}

		private List<Vector3> GetSpawnPositionsForPlayers(StageInfoResource rsc, int nbPlayers)
		{
			int MaxPlayerPerLine = 4;
			int nbLines = 1;

			float length = rsc.SizeZonePlayer;
			float width = rsc.SizeZonePlayer / 2f;

			float startX = 0;
			float startZ = 0;

			List<Vector3> spawnPositions = new List<Vector3>();

			while (nbPlayers / nbLines > MaxPlayerPerLine)
			{
				nbLines++;
			}
			int nbColumns = (int)Math.Ceiling(nbPlayers / (float)nbLines);

			float columnSpacing = nbColumns > 1 ? length / (nbColumns - 1) : 0f;

			float lineSpacing = nbLines > 1 ? width / (nbLines - 1) : 0f;

			startX = -length / 2f;
			startZ = -width / 2f;

			for (int line = 0; line < nbLines; line++)
			{
				for (int column = 0; column < nbColumns; column++)
				{
					float x = startX + column * columnSpacing;
					float y = 0;
					float z = startZ + line * lineSpacing;
					spawnPositions.Add(new Vector3(x, y, z));
				}
			}
			return spawnPositions;
		}

		private void SetPlayersPositionsForMainScene(List<Vector3> spawnPositions)
		{
			int count = 0;
            foreach (var player in result.Players)
            {
				player.Value.Position = spawnPositions[count];
                count++;
            }
        }

		public ArcadeBuildResult Build()
		{
			BuildStage();
			BuildPlayers();
			var stageRsc = StageInfoConverter.ConvertFrom(locationLoader.LoadStageRsc(record.IdStage).StageInfo);
			var nbPlayers = record.Players.Count;
			var listSpots = GetSpawnPositionsForPlayers(stageRsc, nbPlayers);
			SetPlayersPositionsForMainScene(listSpots);
			// TODO : set mainCamera
            return result;
		}
	}
}
