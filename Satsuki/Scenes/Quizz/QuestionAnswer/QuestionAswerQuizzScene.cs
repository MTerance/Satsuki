using Godot;
using Godot.Collections;
using System;
using System.Collections;
using System.Collections.Generic;


public class MediaModel
{
	public enum MediaType
	{
		Image,
		Audio,
		Video
	}
	public MediaType Type { get; set; }
	public string Path { get; set; } // Path to media file
	public MediaModel(MediaType type, string path)
	{
		Type = type;
		Path = path;
	}
}

public class QuestionAnswerQuizzModel
{
	public enum ShowStateMedia
	{
		BeforeQuestion,
		BeforeAnswer,
		DuringQuestion,
		DuringAnswer,
		AfterAnswer
	}

	public string Question { get; set; }
	public string Answer { get; set; }
	public System.Collections.Generic.Dictionary<ShowStateMedia, MediaModel> Medias{ get; set; } // Path to media file (image, audio, video)
	public QuestionAnswerQuizzModel(string question, string answer, System.Collections.Generic.Dictionary<ShowStateMedia, MediaModel> medias = null)
	{
		Question = question;
		Answer = answer;
		Medias = medias ?? new System.Collections.Generic.Dictionary<ShowStateMedia, MediaModel>();
	}
}

public partial class QuestionAswerQuizzScene : Control
{
	private Label questionLabel;
	private Label answerLabel;
	private GameState currentState;
	private enum GameState 
	{
		Beginning,
		ShowMediaBeforeQuestion,
		ShowingQuestion,
		PickUpAnswer,
		ShowMediaBeforeAnswer,
		ShowingAnswer,
		End
	}

	private void StartGame()
	{
		currentState = GameState.Beginning;
		this.questionLabel.Visible = false;
		this.answerLabel.Visible = false;
		NextStateGame();
	}

	private void ShowAnswer()
	{
		this.answerLabel.Visible = true;
	}

	private void PickUpPlayerAnswer()
	{

	}

	private void ShowMedia()
	{

	}


	private void ShowQuestion()
	{
		this.questionLabel.Visible = true;
	}

	private void EndGame()
	{
		GD.Print("Game Ended");
	}

	private void NextStateGame()
	{
		switch (currentState)
		{
			case GameState.Beginning:
				currentState = GameState.ShowMediaBeforeQuestion;
				break;
			case GameState.ShowMediaBeforeQuestion:
				currentState = GameState.ShowingQuestion;
				break;
			case GameState.ShowingQuestion:
				currentState = GameState.PickUpAnswer;
				break;
			case GameState.PickUpAnswer:
				currentState = GameState.ShowMediabeforeAnswer;
				break;
			case GameState.ShowMediabeforeAnswer:
				currentState = GameState.ShowingAnswer;
				break;
			case GameState.ShowingAnswer:
				currentState = GameState.End;
				break;

			case GameState.End:
			default:
				break;
		}
	}

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		GD.Print("QuestionAswerQuizzScene ready");
		questionLabel = this.GetNode<Label>("QuizzVBoxContainer/QuestionMarginContainer/QuestionLabel");
		answerLabel = this.GetNode<Label>("QuizzVBoxContainer/AnswerMarginContainer/AnswerLabel");
		currentState = GameState.Beginning;
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
