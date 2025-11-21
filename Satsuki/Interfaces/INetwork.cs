namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les composants réseau
	/// </summary>
	public interface INetwork
	{
		/// <summary>
		/// Démarre le serveur réseau
		/// </summary>
		/// <returns>True si le démarrage a réussi</returns>
		bool Start();
		
		/// <summary>
		/// Arrête le serveur réseau
		/// </summary>
		/// <returns>True si l'arrêt a réussi</returns>
		bool Stop();
	}
}
