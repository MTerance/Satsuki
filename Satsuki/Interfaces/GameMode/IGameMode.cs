using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Interfaces.GameMode
{
    public interface IGameMode : IScene
    {
        [Signal]
        delegate void GameModeRequestedEventHandler(string newGameMode);
    }
}
