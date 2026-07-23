using Godot;
using Satsuki.Interfaces.Quizz;
using Satsuki.Models.Resources;
using Satsuki.Scenes.Quizz.QCM.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;

namespace Satsuki.Scenes.Quizz.QCM
{

   

	public partial class QCMQuizzScene : Control, IQuizz
	{
		private Label questionLabel;
		private GameState currentState;
		private TextureRect mediaDisplay;
		private QCMQuizzModel currentQuizz;

		//

		private Label ProposalAlpha;
        private Label ProposalBeta;
        private Label ProposalGamma;
        private Label ProposalDelta;
        //

        public string GetQuizzState()
		{
			throw new NotImplementedException();
		}

		private enum GameState
		{
			Beginning,
			ShowMediaBeforeQuestion,
			ShowingQuestion,
			ShowingPropositions,
			BeginPlayersResponseTime,
			ShowMediaBeforeAnswer,
			ShowRightAnswer,
			End
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


		private void TEST_CreateQCMQuizz()
		{
			if (currentQuizz == null)
			{
				currentQuizz = JsonSerializer.Deserialize<QCMQuizzModel>(@"{""Id"":1,""Question"":""Quel est le nom du Gundam principalement piloté par Kira Yamato au début de Mobile Suit Gundam SEED ?"",""Answers"":[{""Id"":1,""Answer"":""Aegis Gundam"",""Color"":{""Item1"":255,""Item2"":80,""Item3"":80}},{""Id"":2,""Answer"":""Strike Gundam"",""Color"":{""Item1"":80,""Item2"":200,""Item3"":120}},{""Id"":3,""Answer"":""Blitz Gundam"",""Color"":{""Item1"":80,""Item2"":120,""Item3"":255}},{""Id"":4,""Answer"":""Buster Gundam"",""Color"":{""Item1"":255,""Item2"":190,""Item3"":60}}],""RightAnswerId"":2,""Medias"":{""DuringQuestion"":{""Path"":""res://Assets/Img/strike_gundam.png"",""Type"":""Image""}}}");
			}
		}


		private void SetProposal()
		{

		}

		private void ShowProposals()
		{
			/// TODO: Implement the logic to show the proposals to the players
			GD.Print("Show Proposals for Question: " + currentQuizz.Question);
			foreach (var answer in currentQuizz.Answers)
			{
				GD.Print($"Proposal: {answer.Answer} (Color: {answer.Color})");
			}
			ProposalAlpha.Text = currentQuizz.Answers[0].Answer;
			ProposalAlpha.Modulate = new Color(currentQuizz.Answers[0].Color.Item1 / 255f, currentQuizz.Answers[0].Color.Item2 / 255f, currentQuizz.Answers[0].Color.Item3 / 255f);
            ProposalAlpha.Visible = true;
			ProposalBeta.Visible = true;
            ProposalBeta.Text = currentQuizz.Answers[1].Answer;
            ProposalBeta.Modulate = new Color(currentQuizz.Answers[1].Color.Item1 / 255f, currentQuizz.Answers[1].Color.Item2 / 255f, currentQuizz.Answers[1].Color.Item3 / 255f);
            ProposalGamma.Text = currentQuizz.Answers[2].Answer;
            ProposalGamma.Visible = true;
            ProposalGamma.Modulate = new Color(currentQuizz.Answers[2].Color.Item1 / 255f, currentQuizz.Answers[2].Color.Item2 / 255f, currentQuizz.Answers[2].Color.Item3 / 255f);
            ProposalDelta.Text = currentQuizz.Answers[3].Answer;
            ProposalDelta.Visible = true;
            ProposalDelta.Modulate = new Color(currentQuizz.Answers[3].Color.Item1 / 255f, currentQuizz.Answers[3].Color.Item2 / 255f, currentQuizz.Answers[3].Color.Item3 / 255f);
        }

		private void ShowQuestion()
		{
			if ((bool)currentQuizz.Medias.ContainsKey(QCMQuizzModel.ShowStateMedia.DuringQuestion))
			{
				ShowMedia(currentQuizz.Medias[QCMQuizzModel.ShowStateMedia.DuringQuestion]);
			}
			questionLabel.Text = currentQuizz.Question;
			questionLabel.Visible = true;
		}

		private void ShowChrono()
		{
			/// TODO: Implement the logic to show a countdown timer for players to respond
			GD.Print("Show Chrono for Players Response Time");
		}

		private void WaitingWhilePlayersResponding()
		{
			GD.Print("Waiting for Players to Respond");
        }

		private void ShowRightAnswer()
		{
			/// TODO: Implement the logic to show the right answer to the players
			GD.Print("Show Right Answer for Question: " + currentQuizz.Answers.Where(x => 
				x.Id == currentQuizz.RightAnswerId));
			var rightAnswer = currentQuizz.Answers.FirstOrDefault(a => a.Id == currentQuizz.RightAnswerId);
		}

		private void EndGame()
		{
			questionLabel.Visible = false;
			GD.Print("Game Ended");
		}

		private bool CheckExistingMediaToShowInCurrentState()
		{
			return currentQuizz.Medias?.ContainsKey((QCMQuizzModel.ShowStateMedia)currentState) ?? false;
		}

		private void StartGame()
        {
            currentState = GameState.Beginning;
			questionLabel.Visible = false;
			ProposalAlpha.Visible = false;
			ProposalBeta.Visible = false;
			ProposalGamma.Visible = false;
			ProposalDelta.Visible = false;
            NextStateGame();
        }

        private void NextStateGame()
		{
			switch (currentState)
			{
				case GameState.Beginning:
					currentState = GameState.ShowMediaBeforeQuestion;
					if (!CheckExistingMediaToShowInCurrentState())
						NextStateGame(); // Skip to next state if no media to show
					else
						ShowMedia(currentQuizz.Medias[QCMQuizzModel.ShowStateMedia.BeforeQuestion]);
					break;
				case GameState.ShowMediaBeforeQuestion:
					currentState = GameState.ShowingQuestion;
					ShowQuestion();
					break;
				case GameState.ShowingQuestion:
					currentState = GameState.ShowingPropositions;
					ShowProposals();
					break;
				case GameState.ShowingPropositions:
					currentState = GameState.BeginPlayersResponseTime;
					ShowChrono();
					break;
				case GameState.BeginPlayersResponseTime:
					currentState = GameState.ShowMediaBeforeAnswer;
					break;
				case GameState.ShowMediaBeforeAnswer:
					currentState = GameState.ShowRightAnswer;
					ShowRightAnswer();
					break;
				case GameState.ShowRightAnswer:
					currentState = GameState.End;
					EndGame();
					break;
				case GameState.End:
				default:
					// End of the game, do nothing or reset
					break;
			}
		}

		public override void _Ready()
		{
			questionLabel = GetNode<Label>("QuizzVBoxContainer/QuestionMarginContainer/QuestionLabel");
            ProposalAlpha = GetNode<Label>("QuizzVBoxContainer/ProposalBoxContainerUp/ProposalAlpha");
            ProposalBeta = GetNode<Label>("QuizzVBoxContainer/ProposalBoxContainerUp/ProposalBeta");
            ProposalGamma = GetNode<Label>("QuizzVBoxContainer/ProposalBoxContainerDown/ProposalGamma");
            ProposalDelta = GetNode<Label>("QuizzVBoxContainer/ProposalBoxContainerDown/ProposalDelta");
            currentState = GameState.Beginning;
            TEST_CreateQCMQuizz();
            StartGame();
        }

		public override void _Process(double delta)
		{
		}

	}


}
