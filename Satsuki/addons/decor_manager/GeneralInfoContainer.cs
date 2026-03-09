using Godot;
using System;

#if TOOLS
[Tool]
#endif
public partial class GeneralInfoContainer : Control
{

	private Button NewResourceInfoButton;
	private Button LoadResourceInfoButton;
	private Button SaveResourceInfoButton;
	private LineEdit NameInfoLineEdit;
	private LineEdit PathResourceLineEdit;


	[Signal]
	public delegate void NewStageResourceRequestedEventHandler();
	[Signal]
	public delegate void LoadStageResourceRequestedEventHandler();
	[Signal]
	public delegate void SaveStageResourceRequestedEventHandler();

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		GD.Print("Test ready general info container");
		NewResourceInfoButton = FindChild("NewResourceInfoButton") as Button;
		LoadResourceInfoButton = FindChild("LoadResourceInfoButton") as Button;
		SaveResourceInfoButton = FindChild("SaveResourceInfoButton") as Button;
		NameInfoLineEdit = FindChild("NameInfoLineEdit") as LineEdit;
		PathResourceLineEdit = FindChild("PathResourceLineEdit") as LineEdit;

		NewResourceInfoButton.Pressed += OnNewResourceInfoButtonPressed;
		LoadResourceInfoButton.Pressed += OnLoadResourceInfoButtonPressed;
		SaveResourceInfoButton.Pressed += OnSaveResourceInfoButtonPressed;
		GD.Print("General info container ready, buttons connected");
	}

	public void UpdateGeneralInfo(string name, string path)
	{
		NameInfoLineEdit.Text = name;
		PathResourceLineEdit.Text = path;
    }

	public void ClearGeneralInfo()
	{
		NameInfoLineEdit.Text = string.Empty;
		PathResourceLineEdit.Text = string.Empty;
    }

    // Called every frame. 'delta' is the elapsed time since the previous frame.
    public override void _Process(double delta)
	{
	}


	public void NewStageResource()
	{
		EmitSignal(SignalName.NewStageResourceRequested);
	}

	public void SaveStageResourceInfo()
	{
		EmitSignal(SignalName.SaveStageResourceRequested);
	}

	public void LoadStageResourceInfo()
	{
		EmitSignal(SignalName.LoadStageResourceRequested);
	}

	public void OnNewResourceInfoButtonPressed()
	{
		NewStageResource();
	}

	public void OnLoadResourceInfoButtonPressed()
	{
		LoadStageResourceInfo();
	}

	public void OnSaveResourceInfoButtonPressed()
	{
		SaveStageResourceInfo();
	}
}
