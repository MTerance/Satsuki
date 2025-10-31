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
		/// D�finit le type d'un client
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="clientType">Type � assigner</param>
		/// <returns>True si l'op�ration r�ussit</returns>
		bool SetClientType(string clientId, string clientType);
		
		/// <summary>
		/// Obtient tous les clients d'un type sp�cifique
		/// </summary>
		/// <param name="clientType">Type de clients recherch�</param>
		/// <returns>Liste des IDs de clients</returns>
		List<string> GetClientsByType(string clientType);
		
		/// <summary>
		/// Obtient tous les clients connect�s
		/// </summary>
		/// <returns>Liste des IDs de clients</returns>
		List<string> GetAllClients();
		
		/// <summary>
		/// D�connecte un client
		/// </summary>
		/// <param name="clientId">ID du client � d�connecter</param>
		void DisconnectClient(string clientId);
	}
}
