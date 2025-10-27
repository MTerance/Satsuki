using System.Collections.Generic;

namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les gestionnaires de clients
	/// </summary>
	public interface IClientManager
	{
		/// <summary>
		/// Obtient le type d'un client
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <returns>Type du client (BACKEND, PLAYER, OTHER) ou null</returns>
		string GetClientType(string clientId);
		
		/// <summary>
		/// Définit le type d'un client
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="clientType">Type à assigner</param>
		/// <returns>True si l'opération réussit</returns>
		bool SetClientType(string clientId, string clientType);
		
		/// <summary>
		/// Obtient tous les clients d'un type spécifique
		/// </summary>
		/// <param name="clientType">Type de clients recherché</param>
		/// <returns>Liste des IDs de clients</returns>
		List<string> GetClientsByType(string clientType);
		
		/// <summary>
		/// Obtient tous les clients connectés
		/// </summary>
		/// <returns>Liste des IDs de clients</returns>
		List<string> GetAllClients();
		
		/// <summary>
		/// Déconnecte un client
		/// </summary>
		/// <param name="clientId">ID du client à déconnecter</param>
		void DisconnectClient(string clientId);
	}
}
