namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les composants r�seau
	/// </summary>
	public interface INetwork
	{
		/// <summary>
		/// D�marre le serveur r�seau
		/// </summary>
		/// <returns>True si le d�marrage a r�ussi</returns>
		bool Start();
		
		/// <summary>
		/// Arr�te le serveur r�seau
		/// </summary>
		/// <returns>True si l'arr�t a r�ussi</returns>
		bool Stop();
	}
}
