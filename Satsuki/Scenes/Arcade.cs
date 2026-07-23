using Godot;
using Satsuki.Interfaces;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes
{
	public partial class Arcade : Node, IScene
	{

		private void LoadStage()
		{ 
			int id = 1; // Example stage ID
			var stageResource = new Repositories.Loaders.LocationLoader().LoadStageRsc(id);
			var stageNode = new Repositories.Loaders.LocationLoader().LoadStage(stageResource);
			AddChild(stageNode);
		}

		private void LoadPlayers()
		{
			// Load players and their positions based on the SpawnPointData
			// This is a placeholder for actual player loading logic
		}

		private void LoadGameRecord()
		{
			// Load the GameRecord from the database or other storage
			// This is a placeholder for actual game record loading logic
		}

		private void LoadQuizz()
		{
			// Load the Quizz data from the database or other storage
			// This is a placeholder for actual quizz loading logic
		}

		public override void _Ready()
		{
			// Get the GameRecord 
			LoadGameRecord();
			// Load the StageInfo and SpawnPointData from the GameRecord
			LoadStage();
			LoadPlayers();
			// Load the Quizz data from the GameRecord
			LoadQuizz();
			base._Ready();
		}

		public override void _Process(double delta)
		{
			base._Process(delta);
		}

		public object GetSceneState()
		{
			return new
			{
				SceneInfo = new
				{
					SceneName = "Arcade",
					SceneType = "Game",
					StartTime = DateTime.UtcNow,
					ElapsedTime = 0.0,
					ElapsedTimeFormatted = "00:00"
				},
				Status = new
				{
					IsActive = true,
					IsPaused = false
				}
			};
		}
	}
}
