using Godot;
using Godot.Collections;
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

		[Export]
		public string Name { get; set; }
		[Export]
		public string Description { get; set; }
		[Export]
		public Array<Spot> QuizzSpots { get; set; }
		[Export]
		public Array<Spot> LobbySpots{ get; set; }

		public LocationResourceModel () : this(null,null,
			new Array<Spot>(),
			new Array<Spot>())
		{}

		public LocationResourceModel (string name, string description,
			Array<Spot> quizzSpots,
			Array<Spot> lobbySpots)
		{
			this.Name = name;
			this.Description = description;
			this.QuizzSpots = quizzSpots;
			this.LobbySpots = lobbySpots;
		}

	}
}
