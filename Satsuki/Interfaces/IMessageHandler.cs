using System.Threading.Tasks;

namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les gestionnaires de messages
	/// </summary>
	public interface IMessageHandler
	{
		/// <summary>
		/// Traite un message reçu d'un client
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="message">Contenu du message</param>
		Task HandleMessage(string clientId, string message);
		
		/// <summary>
		/// Envoie un message à un client spécifique
		/// </summary>
		/// <param name="clientId">ID du client</param>
		/// <param name="message">Message à envoyer</param>
		/// <param name="encrypt">Si true, crypte le message</param>
		Task<bool> SendMessage(string clientId, string message, bool encrypt = true);
		
		/// <summary>
		/// Diffuse un message à tous les clients
		/// </summary>
		/// <param name="message">Message à diffuser</param>
		/// <param name="encrypt">Si true, crypte le message</param>
		Task BroadcastMessage(string message, bool encrypt = true);
	}
}
