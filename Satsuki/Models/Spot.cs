using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
	public enum PlayerTypeSpot
	{
		Occupied,
		Vacant,
	}

	// Spot doit hériter de GodotObject pour être compatible Variant
	public partial class Spot : GodotObject
	{
		public int Id { get; set; }
		public Vector3 Position { get; set; }
		public PlayerTypeSpot PlayerSpot { get; set; }

		public SpawnPointData SpawnPoint { get; set; }

		public Spot(Vector3 position, PlayerTypeSpot playerSpot, SpawnPointData spawnPoint)
		{
			this.Id = new Random().Next(1, 1000000); // Génère un ID aléatoire pour le spot
            this.Position = position;
			this.PlayerSpot = playerSpot;
			this.SpawnPoint = spawnPoint;
		}

		public Spot()
		{
			this.Id = new Random().Next(1, 1000000); // Génère un ID aléatoire pour le spot
            this.Position = Vector3.Zero;
			this.PlayerSpot = PlayerTypeSpot.Vacant;
			this.SpawnPoint = null;
		}
	}
}
