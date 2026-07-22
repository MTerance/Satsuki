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
        { }


        public override void _Ready()
        {
            // Get the GameRecord 
            // Load the StageInfo and SpawnPointData from the GameRecord
            LoadStage();
            // Load the players and their positions based on the SpawnPointData

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
