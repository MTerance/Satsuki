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
	public System.Collections.Generic.Dictionary<ShowStateMedia, MediaModel> Medias { get; set; } // Path to media file (image, audio, video)
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
	private TextureRect mediaDisplay;

	private QuestionAnswerQuizzModel currentQuizz;

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

	public override void _UnhandledKeyInput(InputEvent @event)
	{
		if (@event is InputEventKey eventKey)
		{
			if (eventKey.IsReleased() && eventKey.Keycode == Key.Enter)
			{
				GD.Print("Enter key pressed");
				NextStateGame();
				return;
			}
		}
	}

	private void TEST_SetNewQuizz()
	{
		var medias = new System.Collections.Generic.Dictionary<QuestionAnswerQuizzModel.ShowStateMedia, MediaModel>
		{
			{ QuestionAnswerQuizzModel.ShowStateMedia.DuringQuestion, new MediaModel(MediaModel.MediaType.Image, "res://Assets/Img/drapeau-france-2.png") },
			{ QuestionAnswerQuizzModel.ShowStateMedia.DuringAnswer, new MediaModel(MediaModel.MediaType.Image, "res://Assets/Img/La_Tour_Eiffel.webp") }
		};
		currentQuizz = new QuestionAnswerQuizzModel("What is the capital of France?", "The capital of France is Paris.", medias);
	}


	private void StartGame()
	{
		currentState = GameState.Beginning;
		this.questionLabel.Visible = false;
		this.answerLabel.Visible = false;
	}

	private void ShowAnswer()
	{
		this.answerLabel.Text = currentQuizz.Answer;
		this.answerLabel.Visible = true;
		if (!(bool)(currentQuizz.Medias?.ContainsKey(QuestionAnswerQuizzModel.ShowStateMedia.DuringAnswer)))
			NextStateGame();
		else
		{
			var currentMedia = currentQuizz.Medias.TryGetValue(QuestionAnswerQuizzModel.ShowStateMedia.DuringAnswer, out MediaModel media);
			ShowMedia(media);
		}
	}

	private void PickUpPlayerAnswer()
	{

	}

	private void ShowMedia(MediaModel media)
	{
		switch (media.Type)
		{
			case MediaModel.MediaType.Image:
				GD.Print("Show Image: " + media.Path);
				mediaDisplay.Texture = GD.Load<Texture2D>(media.Path);
				mediaDisplay.Visible = true;
				break;
			case MediaModel.MediaType.Audio:
				GD.Print("Play Audio: " + media.Path);				
				break;
			case MediaModel.MediaType.Video:
				GD.Print("Play Video: " + media.Path);
				break;
			default:
				GD.PrintErr("Unknown media type");
				break;
		}
	}

	private void ShowQuestion()
	{
		if ((bool)currentQuizz.Medias?.ContainsKey(QuestionAnswerQuizzModel.ShowStateMedia.DuringQuestion))
			ShowMedia(currentQuizz.Medias[QuestionAnswerQuizzModel.ShowStateMedia.DuringQuestion]);
		this.questionLabel.Text = currentQuizz.Question;
		this.questionLabel.Visible = true;
	}

	private void EndGame()
	{
		this.answerLabel.Visible = false;
		this.questionLabel.Visible = false;
		GD.Print("Game Ended");
	}

	private void NextStateGame()
	{
		GD.Print("Old State: " + currentState.ToString());
		switch (currentState)
		{
			case GameState.Beginning:
				currentState = GameState.ShowMediaBeforeQuestion;
				if (!(bool)(currentQuizz.Medias?.ContainsKey(QuestionAnswerQuizzModel.ShowStateMedia.BeforeQuestion)))
					NextStateGame();
				else
				{
					var currentMedia = currentQuizz.Medias.TryGetValue(QuestionAnswerQuizzModel.ShowStateMedia.BeforeQuestion, out MediaModel media);
					ShowMedia(media);
				}
				break;
			case GameState.ShowMediaBeforeQuestion:
				currentState = GameState.ShowingQuestion;
				ShowQuestion();
				break;
			case GameState.ShowingQuestion:
				currentState = GameState.PickUpAnswer;
				break;
			case GameState.PickUpAnswer:
				currentState = GameState.ShowMediaBeforeAnswer;
				if (!(bool)(currentQuizz.Medias?.ContainsKey(QuestionAnswerQuizzModel.ShowStateMedia.BeforeAnswer)))
					NextStateGame();
				break;
			case GameState.ShowMediaBeforeAnswer:
				currentState = GameState.ShowingAnswer;
				ShowAnswer();
				break;
			case GameState.ShowingAnswer:
				currentState = GameState.End;
				break;

			case GameState.End:
			default:
				break;
		}
		GD.Print("New State: " + currentState.ToString());
	}

	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		GD.Print("QuestionAswerQuizzScene ready");
		questionLabel = this.GetNode<Label>("QuizzVBoxContainer/QuestionMarginContainer/QuestionLabel");
		answerLabel = this.GetNode<Label>("QuizzVBoxContainer/AnswerMarginContainer/AnswerLabel");
		mediaDisplay = this.GetNode<TextureRect>("QuizzVBoxContainer/MarginContainerVisualMedia/mediaDisplay");
		currentState = GameState.Beginning;
		if (questionLabel == null || answerLabel == null)
		{
			GD.PrintErr("Labels not found!");
			return;
		}
		// pour les besoinns de dev de QuestionAnswerQuizzScene
		/*----------------------------------------------------------------------------------------------------------*/
		GD.Print("TEST_SetNewQuizz ready");
		TEST_SetNewQuizz();
		/*----------------------------------------------------------------------------------------------------------*/
		StartGame();

	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}
}
