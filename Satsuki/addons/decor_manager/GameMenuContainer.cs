using Godot;
using Satsuki.Models;
using System;


#if TOOLS
[Tool]

public partial class GameMenuContainer : VBoxContainer
{

	CameraPlacementTemplate _cameraPlacementPanel;

	public override void _Ready()
	{
		base._Ready();
	}

	public StageInfo GetStageInfo()
	{
		return new StageInfo();
    }
}
#endif
