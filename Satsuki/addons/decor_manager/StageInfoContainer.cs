using Godot;
using System;

public partial class StageInfoContainer : Control
{
	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}


	private  void _on_load_stage_asset_button_pressed()
	{
		GD.Print("DecorManagerTool: UploadStageButton pousse");
		GD.PrintErr("DecorManagerTool: Fonction de chargement de stage non implementee");
	}

	private  void _on_label_mouse_entered()
	{
		GD.Print("DecorManagerTool: Souris entre dans le label");
	}
}
