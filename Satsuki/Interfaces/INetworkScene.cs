namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les scènes qui peuvent recevoir des messages réseau
	/// </summary>
	public interface INetworkScene : IScene
	{
		/// <summary>
		/// Traite un order BACKEND destiné à la scène
		/// </summary>
		/// <param name="clientId">ID du client BACKEND</param>
		/// <param name="order">Type d'order</param>
		/// <param name="jsonData">Données JSON complètes</param>
		void HandleSceneOrder(string clientId, string order, string jsonData);
		
		/// <summary>
		/// Traite une request client destinée à la scène
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="request">Type de request</param>
		/// <param name="jsonData">Données JSON complètes</param>
		void HandleSceneRequest(string clientId, string request, string jsonData);
	}
}
