using Godot;
using System;

#if TOOLS
[Tool]

public partial class TextBox : HBoxContainer
{
	private Label _label;
	private LineEdit _lineEdit;
	public event EventHandler TextChanged;

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		SetupComponents();
		GD.Print("TextBox: Ready called, components set up.");
	}

	private void SetupComponents()
	{
		_label = FindChild("Label") as Label;
		_lineEdit = FindChild("LineEdit") as LineEdit;

		if (_lineEdit != null)
		{
			_lineEdit.TextChanged += OnTextChanged;
		}
	}

	private void OnTextChanged(string newText)
	{
		TextChanged?.Invoke(this, EventArgs.Empty);
	}

	public void SetText(string text)
	{
		if (_lineEdit != null && IsInstanceValid(_lineEdit))
		{
			_lineEdit.Text = text;
		}
	}

	public string GetText()
	{
		if (_lineEdit != null && IsInstanceValid(_lineEdit))
		{
			return _lineEdit.Text;
		}
		return string.Empty;
	}

	public void SetLabelText(string text)
	{
		if (_label != null && IsInstanceValid(_label))
		{
			_label.Text = text;
		}
	}


	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}

	public override void _ExitTree()
	{
		if (_lineEdit != null && IsInstanceValid(_lineEdit))
		{
			_lineEdit.TextChanged -= OnTextChanged;
		}
		base._ExitTree();
	}
}

#endif
