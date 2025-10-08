using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
    public partial class SplashScreenModel
    {
        [Export] public string ImagePath { get; set; }
        [Export] public float FadeOutDuration { get; set; } = 1.0f;
        [Export] public float FadeInDuration { get; set; } = 1.0f;
        [Export] public float DisplayDuration { get; set; } = 2.0f;
        public Texture2D  Texture { get; set; }


        public void LoadTexture() {

            Texture = GD.Load<Texture2D>(this.ImagePath);
        }
    }
}
