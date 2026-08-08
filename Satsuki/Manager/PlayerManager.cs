using Satsuki.Models;
using System;
using System.Collections.Generic;
using Godot;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Manager
{
    public class PlayerManager
    {
        private Dictionary<PlayerInfo, Node3D> players;

        public PlayerManager()
        {
            players = new Dictionary<PlayerInfo, Node3D>();
        }

        public void AddPlayer(PlayerInfo playerInfo, Node3D playerNode)
        {
            if (!players.ContainsKey(playerInfo))
            {
                players.Add(playerInfo, playerNode);
            }
        }

        public Node3D GetPlayerNode(PlayerInfo playerInfo)
        {
            if (players.TryGetValue(playerInfo, out var playerNode))
            {
                return playerNode as Node3D;
            }
            return null;
        }
    }
}
