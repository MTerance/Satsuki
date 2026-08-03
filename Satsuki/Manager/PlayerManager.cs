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
        private Dictionary<PlayerInfo, Node> players;

        public PlayerManager()
        {
            players = new Dictionary<PlayerInfo, Node>();
        }

        public void AddPlayer(PlayerInfo playerInfo, Node playerNode)
        {
            if (!players.ContainsKey(playerInfo))
            {
                players.Add(playerInfo, playerNode);
            }
        }

        public Node GetPlayerNode(PlayerInfo playerInfo)
        {
            if (players.TryGetValue(playerInfo, out var playerNode))
            {
                return playerNode;
            }
            return null;
        }
    }
}
