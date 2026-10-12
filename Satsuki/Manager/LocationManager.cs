using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Manager
{
	public class LocationManager
	{

		public static LocationManager GetInstance()
		{
			if (_instance == null)
			{
				_instance = new LocationManager();
			}
			return _instance;
		}
		private static LocationManager _instance;

		private LocationManager()
		{
			// Initialisation du gestionnaire de localisation
		}

		//public

	}
}
