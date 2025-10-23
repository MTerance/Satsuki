using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Interfaces.Quizz
{
    public interface IQuizz
    {
        /// <summary>
        ///  return content of the quizz in a serializable format (JSON)
        /// </summary>
        /// <returns></returns>
        string GetQuizzState();
    }
}
