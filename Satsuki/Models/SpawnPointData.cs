using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
	[GlobalClass]
	public partial class SpawnPointData : Resource
	{
		[Export]
		public int Index { get; set; }
		[Export]
		public Vector3 Position { get; set; }
		[Export]
		public Vector3 Rotation { get; set; }
		[Export]
		public SpawnPointType Type { get; set; }

		public SpawnPointData()
		{
			Index = 0;
			Position = Vector3.Zero;
			Rotation = Vector3.Zero;
			Type = SpawnPointType.Standard_Idle;
		}

		public SpawnPointData(int index, Vector3 position, Vector3 rotation, SpawnPointType type)
		{
			Index = index;
			Position = position;
			Rotation = rotation;
			Type = type;
		}
	}

    public class SpawnPointDataResource
    {
        public int Index { get; set; }
        public Tuple<float, float, float> Position { get; set; }
        public Tuple<float, float, float> Rotation { get; set; }
        public SpawnPointType Type { get; set; }
        public SpawnPointDataResource()
        {
            Index = 0;
            Position = Tuple.Create(0f, 0f, 0f);
            Rotation = Tuple.Create(0f, 0f, 0f);
            Type = SpawnPointType.Standard_Idle;
        }
        public SpawnPointDataResource(int index, Vector3 position, Vector3 rotation, SpawnPointType type)
        {
            Index = index;
            Position = Tuple.Create(position.X, position.Y, position.Z);
            Rotation = Tuple.Create(rotation.X, rotation.Y, rotation.Z);
            Type = type;
        }
    }
}
