namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les sc�nes qui peuvent recevoir des messages r�seau
	/// </summary>
	public interface INetworkScene : IScene
	{
		/// <summary>
		/// Traite un order BACKEND destin� � la sc�ne
		/// </summary>
		/// <param name="clientId">ID du client BACKEND</param>
		/// <param name="order">Type d'order</param>
		/// <param name="jsonData">Donn�es JSON compl�tes</param>
		void HandleSceneOrder(string clientId, string order, string jsonData);
		
		/// <summary>
		/// Traite une request client destin�e � la sc�ne
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="request">Type de request</param>
		/// <param name="jsonData">Donn�es JSON compl�tes</param>
		void HandleSceneRequest(string clientId, string request, string jsonData);
	}
}
