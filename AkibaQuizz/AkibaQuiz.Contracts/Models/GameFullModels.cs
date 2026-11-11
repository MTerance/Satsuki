namespace AkibaQuiz.Contracts.Models;

// Agrégat métier entièrement résolu pour les besoins de la régie Ciel.
public sealed class GameFullModel
{
    public GameModel Game { get; init; } = new();
    public List<GameFullRoundModel> Rounds { get; init; } = [];
}

public sealed class GameFullRoundModel
{
    public long Id { get; init; }
    public long Position { get; init; }
    public List<GameFullQuestionModel> Questions { get; init; } = [];
}

public sealed class GameFullQuestionModel
{
    public long Id { get; init; }
    public long Position { get; init; }
    public long? IdQuestionAnswer { get; init; }
    public long? IdQCMQuestion { get; init; }
    public QuestionAnswerModel? QuestionAnswer { get; init; }
    public QcmModel? Qcm { get; init; }
}
