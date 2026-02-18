using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
	public partial class LocationModel : Node3D
	{
		[Export]
		public LocationResourceModel LocationResource { get; set; }

    }

	public partial class LocationResourceModel : Resource
    {
		public enum PlayerSpot
		{
			Occupied,
			Vacant,
		}

		[Export]
		public string Name { get; set; }
        [Export]
        public string Description { get; set; }
        [Export]
        public List<Tuple<Vector3I,PlayerSpot>> QuizzSpots { get; set; }
        [Export]
        public List<Tuple<Vector3I, PlayerSpot>> LobbySpots{ get; set; }

		public LocationResourceModel () : this(null,null,
			new List<Tuple<Vector3I, PlayerSpot>>(),
			new List<Tuple<Vector3I, PlayerSpot>>())
		{}

		public LocationResourceModel (string name, string description,
			List<Tuple<Vector3I, PlayerSpot>> quizzSpots,
			List<Tuple<Vector3I, PlayerSpot>> lobbySpots)
		{
			this.Name = name;
			this.Description = description;
			this.QuizzSpots = quizzSpots;
			this.LobbySpots = lobbySpots;
        }

    }
}
