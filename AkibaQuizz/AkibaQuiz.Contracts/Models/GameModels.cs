namespace AkibaQuiz.Contracts.Models;

// Modèles métier. Aucun de ces modèles ne dépend de MVC, Dapper ni de DTO HTTP.
public sealed class GameModel
{
    public long Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Author { get; set; } = string.Empty;
    public string? CreationDate { get; set; }
    public List<GameRoundModel> Rounds { get; set; } = [];
}

public sealed class GameRoundModel
{
    public long Id { get; set; }
    public long IdGame { get; set; }
    public int Position { get; set; }
    public List<RoundQuestionModel> Questions { get; set; } = [];
}

public sealed class RoundQuestionModel
{
    public long Id { get; set; }
    public long IdGameRound { get; set; }
    public long? IdQuestionAnswer { get; set; }
    public long? IdQCMQuestion { get; set; }
    public long? IdListQuestionsAnswers { get; set; }
    public long Position { get; set; }
}

public sealed class GameSummaryModel
{
    public long Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public int RoundCount { get; set; }
    public int QuestionCount { get; set; }
}
