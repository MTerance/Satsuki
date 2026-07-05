using Godot;
using Satsuki.Repositories.Builders;
using System;
using System.Collections.Generic;
using System.Linq;

#if TOOLS
[Tool]
#endif

public partial class StageListContainer : Control
{
	private StageResourceBuilder StageResourceBuilder { get; set; }
	private ItemList _stageInfoList;
	private Button _loadButton;
	private Button _cancelButton;
	private List<int> _listIndexStage;


	[Signal]
	public delegate void StageResourceSelectedEventHandler(int stageId);
	[Signal]
	public delegate void CloseStageSelectorWindowEventHandler();


	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		StageResourceBuilder = new StageResourceBuilder();

		_stageInfoList = FindChild("StageInfoList") as ItemList;
		_loadButton = FindChild("LoadButton") as Button;
		_cancelButton = FindChild("CancelButton") as Button;
		_loadButton.Pressed += _loadButton_Pressed;
		_cancelButton.Pressed += _cancelButton_Pressed;
		_loadButton.Disabled = true;

		_listIndexStage = new List<int>();
		_stageInfoList.ItemSelected += OnStageInfoListItemSelected;
		GeStageList();
	}

	private void _loadButton_Pressed()
	{
		EmitSignal(SignalName.StageResourceSelected, _listIndexStage[(int)_stageInfoList.GetSelectedItems().First()]);
	}

	private void _cancelButton_Pressed()
	{
		EmitSignal(SignalName.CloseStageSelectorWindow);
	}


	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}

	private void GeStageList()
	{
		StageResourceBuilder.GetStages().ForEach(stage =>
		{
			_listIndexStage.Add(stage.Item1);
			_stageInfoList.AddItem(stage.Item2,null,true);
		});
	}

	private void OnStageInfoListItemSelected(long index)
	{
		_loadButton.Disabled = false;
	}

	private void OnStageInfoListItemDeselected(long index)
	{
		EmitSignal("StageResourceDeselected", index);
	}
}
