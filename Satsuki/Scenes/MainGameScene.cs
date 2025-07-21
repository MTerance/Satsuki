using Godot;
using System;

public partial class MainGameScene : Node
{
	
	
	public async void ChangeScene()
	{
		GetTree().ChangeSceneToFile(
			"res://Scenes/OtherScene.tscn"
		);
	}	
}
