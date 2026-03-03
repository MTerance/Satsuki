using Godot;
using System;

#if TOOLS
[Tool]
#endif
public partial class StageInfoContainer : Control
{
	private Button _loadStageAssetButton;
	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		GD.Print("Test ready Stageinfo container");
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}


}
