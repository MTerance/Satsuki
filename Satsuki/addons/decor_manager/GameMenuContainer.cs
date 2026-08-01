using Godot;
using Satsuki.Models;
using System;


#if TOOLS
[Tool]

public partial class GameMenuContainer : VBoxContainer
{

	CameraPlacementTemplate _cameraPlacementPanel;
	PlayerZonePlacementContainer _playerZonePlacementContainer;

	public override void _Ready()
	{
		/*
		string controlPath = "res://addons/decor_manager/Scenes/player_zone_placement_container.tscn";
		if (!ResourceLoader.Exists(controlPath))
		{
			GD.PrintErr($"Resource not found: {controlPath}");
			return;
		}
		PackedScene controlScene = ResourceLoader.Load<PackedScene>(controlPath);
		Control control = controlScene.Instantiate<Control>();
		AddChild(control);
		*/
		_cameraPlacementPanel = FindChild("CameraPlacementContainer", true, false) as CameraPlacementTemplate;
		if (_cameraPlacementPanel == null)
			GD.PrintErr("CameraPlacementContainer node not found.");
		_cameraPlacementPanel.Init("GameMainScene");
		_playerZonePlacementContainer = FindChild("PlayerZonePlacementContainer", true, false) as PlayerZonePlacementContainer;
		if (_playerZonePlacementContainer == null)
			GD.PrintErr("PlayerZonePlacementContainer node not found.");
	}

	public void SetStageInfo(StageInfo stageInfo)
	{
		// Implémentation pour définir les informations de la scène
		_cameraPlacementPanel.Load(stageInfo.CameraPlacement);
		_playerZonePlacementContainer.Load(stageInfo.PositionZonePlayer, stageInfo.RotationZonePlayer, stageInfo.SizeZonePlayer);
	}

	public StageInfo GetStageInfo()
	{
		CameraPlacement camera = null;
		_cameraPlacementPanel.GetCameraPlacementInfo(out camera);

		var stageInfo = new StageInfo()
		{
			CameraPlacement = camera,
			PositionMainCamera = camera.Position,
			PositionZonePlayer = _playerZonePlacementContainer.GetPlayerZonePosition(),
			RotationZonePlayer = _playerZonePlacementContainer.GetPlayerZoneRotation(),
			SizeZonePlayer = _playerZonePlacementContainer.GetPlayerZoneSize(),
		};
		return stageInfo;
	}
}
#endif
