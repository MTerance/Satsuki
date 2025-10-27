using System.Threading.Tasks;

namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les gestionnaires de messages
	/// </summary>
	public interface IMessageHandler
	{
		/// <summary>
		/// Traite un message re�u d'un client
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="message">Contenu du message</param>
		Task HandleMessage(string clientId, string message);
		
		/// <summary>
		/// Envoie un message � un client sp�cifique
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="message">Message � envoyer</param>
		/// <param name="encrypt">Si true, crypte le message</param>
		Task<bool> SendMessage(string clientId, string message, bool encrypt = true);
		
		/// <summary>
		/// Diffuse un message � tous les clients
		/// </summary>
		/// <param name="message">Message � diffuser</param>
		/// <param name="encrypt">Si true, crypte le message</param>
		Task BroadcastMessage(string message, bool encrypt = true);
	}
}
