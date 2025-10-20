using Godot;
using Satsuki.Networks;
using Satsuki.Utils;
using System;
using System.Threading.Tasks;

public partial class ServerManager : Node
{
	private Network _network;
	private bool _isServerRunning = false;

	[Signal] public delegate void ServerStartedEventHandler();
	[Signal] public delegate void ServerStoppedEventHandler();
	[Signal] public delegate void ServerErrorEventHandler(string error);

	public override void _Ready()
	{
		GD.Print("Server Manager: Initialisation du serveur Satsuki...");
		
		// Demarrer le serveur automatiquement au lancement du jeu
		CallDeferred(nameof(StartServerAsync));
		
		// Gerer la fermeture propre du serveur
		GetTree().AutoAcceptQuit = false;
	}

	private async void StartServerAsync()
	{
		try
		{
			GD.Print("Demarrage du serveur reseau...");
			
			_network = Network.GetInstance;
			
			if (_network.Start())
			{
				_isServerRunning = true;
				GD.Print("Serveur Satsuki demarre avec succes!");
				GD.Print("Serveur TCP: 127.0.0.1:80");
				GD.Print("Systeme de cryptage: Active");
				
				EmitSignal(SignalName.ServerStarted);
				
				// Envoyer un message d'etat initial aux clients connectes
				await Task.Delay(1000); // Attendre que le serveur soit completement initialise
				await _network.BroadcastMessage("SERVER_READY: Serveur Satsuki en ligne");
			}
			else
			{
				var error = "Echec du demarrage du serveur reseau";
				GD.PrintErr(error);
				EmitSignal(SignalName.ServerError, error);
			}
		}
		catch (Exception ex)
		{
			var error = $"Erreur lors du demarrage du serveur: {ex.Message}";
			GD.PrintErr(error);
			EmitSignal(SignalName.ServerError, error);
		}
	}

	public override void _Notification(int what)
	{
		if (what == NotificationWMCloseRequest || what == NotificationApplicationPaused)
		{
			OnQuitRequest();
		}
	}

	private async void OnQuitRequest()
	{
		GD.Print("Arret du serveur en cours...");
		
		if (_isServerRunning && _network != null)
		{
			try
			{
				// Notifier les clients de la fermeture
				await _network.BroadcastMessage("SERVER_SHUTDOWN: Le serveur Satsuki va se fermer");
				await Task.Delay(2000); // Attendre que les messages soient envoyes
				
				_network.Stop();
				_isServerRunning = false;
				EmitSignal(SignalName.ServerStopped);
				
				GD.Print("Serveur arrete proprement");
			}
			catch (Exception ex)
			{
				GD.PrintErr($"Erreur lors de l'arret du serveur: {ex.Message}");
			}
		}
	}

	public bool IsServerRunning()
	{
		return _isServerRunning;
	}

	public Network GetNetwork()
	{
		return _network;
	}

	public async Task<bool> SendServerMessage(string message)
	{
		if (_network != null && _isServerRunning)
		{
			await _network.BroadcastMessage(message);
			return true;
		}
		return false;
	}

	public int GetConnectedClientsCount()
	{
		if (_network != null)
		{
			var stats = _network.GetNetworkStatistics();
			return stats.connectedClients;
		}
		return 0;
	}

	public void LogServerStatus()
	{
		if (_network != null)
		{
			var stats = _network.GetNetworkStatistics();
			GD.Print($"Statut serveur - Clients: {stats.connectedClients}, Messages en attente: {stats.pendingMessages}");
		}
	}
}
