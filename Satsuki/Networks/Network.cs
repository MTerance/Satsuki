using Godot;
using Satsuki.Utils;
using Satsuki.Networks;
using System;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

public class Network : SingletonBase<Network>, INetwork, IDisposable
{
	private TcpListener _server;
	private TcpClient _client;
	private NetworkStream _stream;
	private bool _isRunning = false;
	private CancellationTokenSource _cancellationTokenSource;
	private Task _messageListeningTask;

    public Network()
	{
		_server = null;
		_client = null;
		_stream = null;
		_cancellationTokenSource = new CancellationTokenSource();
	}

	public void Dispose()
	{
		Stop();
		_cancellationTokenSource?.Dispose();
	}

	public bool Stop()
	{
		if (_isRunning)
		{
			_isRunning = false;
			_cancellationTokenSource?.Cancel();
		}

		if (_stream != null)
		{
			_stream.Close();
			_stream.Dispose();
			_stream = null;
		}
		if (_client != null)
		{
			_client.Close();
			_client.Dispose();
			_client = null;
		}
		if (_server != null)
		{
			_server.Stop();
			_server = null;
		}
		return true;
	}

	public bool Start()	
	{
		if (!_isRunning)
		{
			_server = new TcpListener(IPAddress.Parse("127.0.0.1"), 80);
			_server.Start();
			Console.WriteLine("Server has started on {0}:{1}, Waiting for a connection…", "127.0.0.1", 80);

			_client = _server.AcceptTcpClient();
			Console.WriteLine("A client connected.");
			_stream = _client.GetStream();
			_isRunning = true;

			// Démarre le MessageHandler avec cryptage activé
			MessageHandler.GetInstance.StartMessageProcessing();
			
			// Affiche les informations de cryptage
			var encInfo = MessageHandler.GetInstance.GetEncryptionInfo();
			Console.WriteLine($"Cryptage: {(encInfo.enabled ? "ACTIVÉ" : "DÉSACTIVÉ")}");

			// Démarre l'écoute des messages en arrière-plan
			_messageListeningTask = Task.Run(ListenForMessages, _cancellationTokenSource.Token);
        }
		return _isRunning;
	}

	/// <summary>
	/// Configure le cryptage pour les messages
	/// </summary>
	/// <param name="enabled">Active ou désactive le cryptage</param>
	/// <param name="generateNewKey">Génère une nouvelle clé aléatoire</param>
	public void ConfigureEncryption(bool enabled, bool generateNewKey = false)
	{
		if (generateNewKey)
		{
			MessageHandler.GetInstance.GenerateNewEncryptionKey();
		}
		
		MessageHandler.GetInstance.ConfigureEncryption(enabled);
		
		var encInfo = MessageHandler.GetInstance.GetEncryptionInfo();
		Console.WriteLine($"Network: Cryptage {(encInfo.enabled ? "activé" : "désactivé")}");
	}

	/// <summary>
	/// Écoute les messages entrants des clients en continu
	/// </summary>
	private async Task ListenForMessages()
	{
		byte[] buffer = new byte[4096];
		
		try
		{
			while (_isRunning && !_cancellationTokenSource.Token.IsCancellationRequested)
			{
				if (_stream != null && _stream.CanRead && _client.Connected)
				{
					try
					{
						int bytesRead = await _stream.ReadAsync(buffer, 0, buffer.Length, _cancellationTokenSource.Token);
						
						if (bytesRead > 0)
						{
							string receivedData = Encoding.UTF8.GetString(buffer, 0, bytesRead);
							Console.WriteLine($"Données reçues: {receivedData.Length} bytes");
							
							// Vérifie si les données reçues sont déjà cryptées
							if (MessageCrypto.IsEncrypted(receivedData))
							{
								Console.WriteLine("Message crypté reçu du client");
								MessageHandler.GetInstance.AddEncryptedMessage(receivedData);
							}
							else
							{
								Console.WriteLine("Message en clair reçu du client");
								MessageHandler.GetInstance.AddReceivedMessage(receivedData);
							}
						}
						else
						{
							// Client déconnecté
							Console.WriteLine("Client déconnecté.");
							break;
						}
					}
					catch (Exception ex) when (ex is ObjectDisposedException || ex is InvalidOperationException)
					{
						// Stream fermé ou client déconnecté
						Console.WriteLine("Connexion fermée.");
						break;
					}
				}
				else
				{
					// Pas de client connecté, attendre un peu
					await Task.Delay(100, _cancellationTokenSource.Token);
				}
			}
		}
		catch (OperationCanceledException)
		{
			Console.WriteLine("Écoute des messages annulée.");
		}
		catch (Exception ex)
		{
			Console.WriteLine($"Erreur lors de l'écoute des messages: {ex.Message}");
		}
	}

	/// <summary>
	/// Envoie un message au client connecté (crypté automatiquement)
	/// </summary>
	/// <param name="message">Message à envoyer</param>
	/// <param name="encrypt">Force le cryptage du message (true par défaut)</param>
	public async Task<bool> SendMessage(string message, bool encrypt = true)
	{
		if (_stream != null && _stream.CanWrite && !string.IsNullOrEmpty(message))
		{
			try
			{
				string dataToSend = message;
				
				// Crypte le message si demandé
				if (encrypt)
				{
					dataToSend = MessageCrypto.Encrypt(message);
					Console.WriteLine($"Envoi message crypté: {dataToSend.Length} bytes");
				}
				else
				{
					Console.WriteLine($"Envoi message en clair: {message}");
				}

				byte[] data = Encoding.UTF8.GetBytes(dataToSend);
				await _stream.WriteAsync(data, 0, data.Length);
				await _stream.FlushAsync();
				return true;
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Erreur lors de l'envoi du message: {ex.Message}");
				return false;
			}
		}
		return false;
	}

	/// <summary>
	/// Envoie un message Message déjà créé
	/// </summary>
	/// <param name="message">Objet Message à envoyer</param>
	/// <param name="sendEncrypted">Envoie la version cryptée si disponible</param>
	public async Task<bool> SendMessage(Satsuki.Message message, bool sendEncrypted = true)
	{
		if (message == null)
			return false;

		string contentToSend;
		
		if (sendEncrypted && message.IsEncrypted)
		{
			// Envoie directement le contenu crypté
			contentToSend = message.Content;
			Console.WriteLine("Envoi du message déjà crypté");
		}
		else if (sendEncrypted && !message.IsEncrypted)
		{
			// Crypte avant envoi sans modifier l'original
			var encryptedCopy = message.CreateEncryptedCopy();
			contentToSend = encryptedCopy.Content;
			Console.WriteLine("Envoi du message avec cryptage à la volée");
		}
		else
		{
			// Envoie en clair ou décrypte avant envoi
			contentToSend = message.IsEncrypted ? message.GetDecryptedContent() : message.Content;
			Console.WriteLine("Envoi du message en clair");
		}

		return await SendMessage(contentToSend, false); // false car déjà traité
	}

	/// <summary>
	/// Obtient les statistiques de cryptage
	/// </summary>
	/// <returns>Informations sur l'état du cryptage</returns>
	public (bool enabled, string keyInfo, string ivInfo) GetEncryptionStatus()
	{
		return MessageHandler.GetInstance.GetEncryptionInfo();
	}
}
