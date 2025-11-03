using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
	public class LocationModel
	{
		public enum PlayerPlace
		{
			Occupied,
			Vacant,
		}

		public string Name { get; set; }
		public string Description { get; set; }
		public List<Tuple<Vector3I,PlayerPlace>> QuizzSeats { get; set; }
		public List<Tuple<Vector3I, PlayerPlace>> LobbySeats{ get; set; }
	}
}
