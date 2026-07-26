using Godot;
using System;


#if TOOLS
[Tool]

public partial class Vector3dTextBox : HBoxContainer
{
	private Label _label;
	private TextBox _positionX;
	private TextBox _positionY;
	private TextBox _positionZ;

	public event EventHandler ValueChanged;

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		SetupComponents();
		GD.Print("Vector3dTextBox: Ready and components initialized.");
	}

	private void SetupComponents()
	{
		_label = FindChild("Label") as Label;
		_positionX = FindChild("PositionX") as TextBox;
		_positionY = FindChild("PositionY") as TextBox;
		_positionZ = FindChild("PositionZ") as TextBox;

		if (_positionX != null)
			_positionX.TextChanged += OnXTextChanged;
		if (_positionY != null)
			_positionY.TextChanged += OnYTextChanged;
		if (_positionZ != null)
			_positionZ.TextChanged += OnZTextChanged;

		if (_positionX != null)
			_positionX.SetLabelText("X");
		if (_positionY != null)
			_positionY.SetLabelText("Y");
		if (_positionZ != null)
			_positionZ.SetLabelText("Z");

		if (_positionX != null && _positionY != null && _positionZ != null)
			GD.Print("Vector3dTextBox: Components setup completed successfully.");
	}

	#region events LineEdit

	private void OnXTextChanged(object sender, EventArgs e)
	{
		OnValueChanged();
	}

	private void OnYTextChanged(object sender, EventArgs e)
	{
		OnValueChanged();
	}

	private void OnZTextChanged(object sender, EventArgs e)
	{
		OnValueChanged();
	}

	#endregion

	private void OnValueChanged()
	{
		ValueChanged?.Invoke(this, EventArgs.Empty);
	}

	public void SetValue(Vector3 vector)
	{
		_positionX.SetText(vector.X.ToString());
		_positionY.SetText(vector.Y.ToString());
		_positionZ.SetText(vector.Z.ToString());
	}

	public Vector3 GetValue()
	{
		return new Vector3(
			float.Parse(_positionX.GetText()),
			float.Parse(_positionY.GetText()),
			float.Parse(_positionZ.GetText()));
	}

	public void Setup(string text, Vector3 vector)
	{
		_label.Text = text;
		SetValue(vector);
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}

	public override void _ExitTree()
	{
		_positionX.TextChanged -= OnXTextChanged;
		_positionY.TextChanged -= OnYTextChanged;
		_positionZ.TextChanged -= OnZTextChanged;
		base._ExitTree();
	}
}

#endif
