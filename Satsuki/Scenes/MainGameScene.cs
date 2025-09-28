using Godot;
using System;
using System.Threading.Tasks;

public partial class MainGameScene : Node
{

	public override void _Ready()
	{
		InitializeNetwork();
	}

	public async void ChangeScene()
	{
		GetTree().ChangeSceneToFile(
			"res://Scenes/OtherScene.tscn"
		);
	}

	private void InitializeNetwork()
	{

	}
}
