using Godot;
using System;

public partial class QuestionAswerQuizzScene : Control
{
	private Label questionLabel;
	private Label answerLabel;
	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		GD.Print("QuestionAswerQuizzScene ready");
		questionLabel = this.GetNode<Label>("QuizzVBoxContainer/QuestionMarginContainer/QuestionLabel");
		answerLabel = this.GetNode<Label>("QuizzVBoxContainer/AnswerMarginContainer/AnswerLabel");
		if (questionLabel == null || answerLabel == null)
		{
			GD.PrintErr("Labels not found!");
			return;
		}
		questionLabel.Text = "What is the capital of France?";
		answerLabel.Text = "The capital of France is Paris.";
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}
}
