using System.ComponentModel.DataAnnotations;
namespace AkibaQuiz.Contracts;

// DTO métier; les entités SQL restent conformes au schéma de Quizz.db.
public sealed record CategoryDto(long Id, string Name);
public sealed record TagDto(long Id, string Name, string? Color);
public sealed record MediaDto(long Id, long IdMedia, string Filename, long IdTypeMedia, string TypeMediaName, string TypeDisplay);
public sealed record PropositionDto(long Id, long IdQCMAnswer, string Answer, bool IsTrue);
public sealed record QcmDto(long Id, string Question, long IdCategory, string? CategoryName, string Author, string CreationDate, string LastUpdatedTDate, List<PropositionDto> Answers, List<TagDto> Tags, List<MediaDto> Medias);
public sealed record QuestionDto(long Id, string Question, string Answer, long IdCategory, string? CategoryName, string Author, string CreationDate, string LastUpdateDate, List<TagDto> Tags, List<MediaDto> Medias);
public sealed record RoundQuestionDto(long Id, long Position, long? IdQuestionAnswer, long? IdQCMQuestion, long? IdListQuestionsAnswers);
public sealed record RoundDto(long Id, long Position, List<RoundQuestionDto> Questions);
public sealed record GameDto(long Id, string Name, string Author, string? CreationDate, List<RoundDto> Rounds);
public sealed class MediaRef { [Range(1, long.MaxValue)] public long IdMedia { get; set; } [Required] public string TypeDisplay { get; set; } = ""; }
public sealed class QuestionWrite
{
    [Required]
    public string Question { get; set; } = "";
    [Required]
    public string Answer { get; set; } = "";
    [Range(1, long.MaxValue)] 
    public long IdCategory { get; set; }
    public List<long> TagIds { get; set; } = [];
    public List<MediaRef> Medias { get; set; } = [];
}
public sealed class PropositionWrite { [Required] public string Answer { get; set; } = ""; public bool IsTrue { get; set; } }
public sealed class QcmWrite { [Required] public string Question { get; set; } = ""; [Range(1, long.MaxValue)] public long IdCategory { get; set; } public List<PropositionWrite> Answers { get; set; } = []; public List<long> TagIds { get; set; } = []; public List<MediaRef> Medias { get; set; } = []; }
public sealed class RoundQuestionWrite { public long Position { get; set; } public long? IdQuestionAnswer { get; set; } public long? IdQCMQuestion { get; set; } public long? IdListQuestionsAnswers { get; set; } }
public sealed class RoundWrite { public long Position { get; set; } public List<RoundQuestionWrite> Questions { get; set; } = []; }
public sealed class GameWrite { [Required] public string Name { get; set; } = ""; public List<RoundWrite> Rounds { get; set; } = []; }
public sealed class ApiValidationException(string message) : Exception(message);
public sealed class ApiConflictException(string message) : Exception(message);
