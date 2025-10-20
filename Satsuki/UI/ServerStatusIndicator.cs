using Godot;
using System;

public partial class ServerStatusIndicator : Control
{
    private Label _statusLabel;
    private ColorRect _statusDot;
    private ServerManager _serverManager;
    private Timer _updateTimer;

    public override void _Ready()
    {
        SetupUI();
        
        _serverManager = GetNode<ServerManager>("/root/ServerManager");
        if (_serverManager != null)
        {
            _serverManager.ServerStarted += OnServerStarted;
            _serverManager.ServerStopped += OnServerStopped;
            _serverManager.ServerError += OnServerError;
            
            // Timer pour mettre à jour le nombre de clients
            _updateTimer = new Timer();
            _updateTimer.WaitTime = 2.0f;
            _updateTimer.Timeout += UpdateClientCount;
            _updateTimer.Autostart = true;
            AddChild(_updateTimer);
        }
        
        // État initial
        UpdateStatus("Démarrage...", Colors.Yellow);
    }

    private void SetupUI()
    {
        // Conteneur horizontal
        var hbox = new HBoxContainer();
        AddChild(hbox);

        // Point de couleur pour le statut
        _statusDot = new ColorRect();
        _statusDot.CustomMinimumSize = new Vector2(12, 12);
        _statusDot.Color = Colors.Yellow;
        hbox.AddChild(_statusDot);

        // Espacement
        var spacer = new Control();
        spacer.CustomMinimumSize = new Vector2(8, 1);
        hbox.AddChild(spacer);

        // Label de statut
        _statusLabel = new Label();
        _statusLabel.Text = "Serveur: Démarrage...";
        _statusLabel.AddThemeStyleboxOverride("normal", new StyleBoxFlat());
        hbox.AddChild(_statusLabel);
    }

    private void OnServerStarted()
    {
        UpdateStatus("En ligne", Colors.Green);
        UpdateClientCount();
    }

    private void OnServerStopped()
    {
        UpdateStatus("Arrêté", Colors.Red);
    }

    private void OnServerError(string error)
    {
        UpdateStatus($"Erreur: {error}", Colors.Orange);
    }

    private void UpdateStatus(string status, Color color)
    {
        if (_statusLabel != null)
            _statusLabel.Text = $"Serveur: {status}";
        
        if (_statusDot != null)
            _statusDot.Color = color;
    }

    private void UpdateClientCount()
    {
        if (_serverManager != null && _serverManager.IsServerRunning())
        {
            int clientCount = _serverManager.GetConnectedClientsCount();
            if (_statusLabel != null)
            {
                _statusLabel.Text = $"Serveur: En ligne ({clientCount} client{(clientCount > 1 ? "s" : "")})";
            }
        }
    }

    public override void _ExitTree()
    {
        if (_serverManager != null)
        {
            _serverManager.ServerStarted -= OnServerStarted;
            _serverManager.ServerStopped -= OnServerStopped;
            _serverManager.ServerError -= OnServerError;
        }
        
        _updateTimer?.QueueFree();
    }
}