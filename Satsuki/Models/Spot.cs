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
		public Vector3I Position { get; set; }
		public PlayerTypeSpot PlayerSpot { get; set; }
		public Spot(Vector3I position, PlayerTypeSpot playerSpot)
		{
			this.Position = position;
			this.PlayerSpot = playerSpot;
		}
	}
}
