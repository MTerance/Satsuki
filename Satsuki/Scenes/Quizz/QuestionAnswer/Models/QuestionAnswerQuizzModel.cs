using Satsuki.Interfaces.Quizz;
using Satsuki.Models.Resources;

namespace Satsuki.Scenes.Quizz.QuestionAnswer.Models
{
    public class QuestionAnswerQuizzModel : IQuizzModel
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

}
