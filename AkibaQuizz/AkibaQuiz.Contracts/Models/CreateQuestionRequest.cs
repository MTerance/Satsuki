using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Text;

namespace AkibaQuiz.Contracts.Models
{
    public sealed class CreateQuestionRequest
    {
        [Required]
        [MinLength(3)]
        public string Question { get; set; } = String.Empty;
        [Required]
        [MinLength(3)]
        public string Answer { get; set; } = String.Empty;
        [Range(1, 1000)]
        public int Points { get; set; } = 100;
        [Range(1, 300)]
        public int TimeLimitSeconds { get; set; } = 30;
    }
}
