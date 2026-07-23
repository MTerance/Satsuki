using Satsuki.Interfaces.Quizz;
using Satsuki.Models.Resources;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes.Quizz.QCM.Models
{
    public class QCMQuizzModel : IQuizzModel
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
        public List<AnswerQCMQuizzModel> Answers { get; set; }
        public int RightAnswerId { get; set; } // Id of the right answer
        public Dictionary<ShowStateMedia, MediaModel> Medias { get; set; } // Path to media file (image, audio, video)

        public QCMQuizzModel(string question, List<AnswerQCMQuizzModel> answers, int rightAnswerId, Dictionary<ShowStateMedia, MediaModel> medias = null)
        {
            Question = question;
            Answers = answers;
            RightAnswerId = rightAnswerId;
            Medias = medias ?? new Dictionary<ShowStateMedia, MediaModel>();
        }
    }
}
