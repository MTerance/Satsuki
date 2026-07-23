using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Scenes.Quizz.QCM.Models
{
    public class AnswerQCMQuizzModel
    {
        public int Id { get; set; }
        public string Answer { get; set; }
        public Tuple<int, int, int> Color { get; set; }
    }
}
