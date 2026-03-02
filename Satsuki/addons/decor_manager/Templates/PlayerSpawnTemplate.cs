using Godot;
using Microsoft.VisualBasic.FileIO;
using Satsuki.Models;
using System;

#if TOOLS
[Tool]
#endif
public partial class PlayerSpawnTemplate : Control
{

	private Button _deleteButton;
	private Label IdSpawnDataLabel;

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		GD.Print("Test PlayerSpawnTemplate");
        _deleteButton = FindChild("DeleteButton") as Button;
        _deleteButton.Pressed += OnDeleteButtonPressed;
    }

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}

	public void InitPlayerSpawnTemplate(SpawnPointData spawnPoint)
	{
		GD.Print("PlayerSpawnTemplate:  InitPlayerSpawnTemplate");
        IdSpawnDataLabel = FindChild("IdSpawnPoint") as Label;
		IdSpawnDataLabel.Text = spawnPoint.Index.ToString();
		_deleteButton = FindChild("DeleteButton") as Button;
		_deleteButton.Pressed += OnDeleteButtonPressed;
	}

	public void OnDeleteButtonPressed()
	{
		DeleteSpawnPoint();
	}


	private void DeleteSpawnPoint()
	{
		var parent = GetParent() as VBoxContainer;
		if (parent != null)
		{
			parent.RemoveChild(this);
			this.QueueFree();
		}
	}


}
