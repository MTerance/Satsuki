using Godot;
using Satsuki.Interfaces.Quizz;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes.Quizz.QCM
{
    public class  AnswerQcmQuizzModel
    {
        public int Id { get; set; }
        public string Answer { get; set; }
        public Tuple<int,int,int> Color { get; set; }
    }

    public class QCMQuizzModel
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
        public List<AnswerQcmQuizzModel> Answers { get; set; }
        public Dictionary<ShowStateMedia, MediaModel> Medias { get; set; } // Path to media file (image, audio, video)

        public QCMQuizzModel(string question, List<AnswerQcmQuizzModel> answers, Dictionary<ShowStateMedia, MediaModel> medias = null)
        {
            Question = question;
            Answers = answers;
            Medias = medias ?? new Dictionary<ShowStateMedia, MediaModel>();
        }
    }

    public partial class QCMQuizzScene : Control, IQuizz
    {
        private Label questionLabel;
        private GameState currentState;
        private TextureRect mediaDisplay;
        private QCMQuizzModel currentQuizz;

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
            // todo : write the rest of the states

        }
    }
}
