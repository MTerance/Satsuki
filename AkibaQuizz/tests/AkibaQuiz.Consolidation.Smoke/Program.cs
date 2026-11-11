using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Application.Services;
using AkibaQuiz.Contracts;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Contracts.Requests;

static void Check(bool condition, string name)
{
    if (!condition) throw new Exception("ECHEC: " + name);
    Console.WriteLine("OK: " + name);
}

var fakeGames = new GameRepo();
var fakeQuestions = new QuestionSvc();
var fakeQcms = new QcmSvc();
var service = new GameService(fakeGames, fakeQuestions, fakeQcms);

var summary = await service.GetSummariesAsync(CancellationToken.None);
Check(summary.Count == 1 && summary[0].RoundCount == 2, "Catalogue leger");

var full = await service.GetFullAsync(1, CancellationToken.None);
Check(full is not null && full.Game.Id == 1 && full.Rounds.Count == 2, "Game entier charge");
Check(full!.Rounds[0].Position == 1 && full.Rounds[1].Position == 2, "Manches ordonnees");
Check(full.Rounds[0].Questions[0].Qcm?.Answers[0].IsTrue == true, "QcmModel et bonne reponse");
Check(full.Rounds[1].Questions[0].QuestionAnswer?.Answer == "Sunrise", "QuestionAnswerModel");
Check(fakeQcms.GetCalls == 1, "Cache QCM pour references repetees");
Check(fakeQuestions.GetCalls == 1, "Charge une question libre une seule fois");
Check(await service.GetFullAsync(404, CancellationToken.None) is null, "Game absent retourne null");

fakeQcms.ReturnNull = true;
var didRejectMissing = false;
try { await service.GetFullAsync(1, CancellationToken.None); }
catch (ApiConflictException) { didRejectMissing = true; }
Check(didRejectMissing, "Reference QCM inexistante -> conflit");
fakeQcms.ReturnNull = false;

fakeGames.BadReference = true;
var didRejectBoth = false;
try { await service.GetFullAsync(1, CancellationToken.None); }
catch (ApiConflictException) { didRejectBoth = true; }
Check(didRejectBoth, "Deux references dans RoundQuestion -> conflit");
fakeGames.BadReference = false;

var didRejectWrite = false;
try
{
    await service.SaveAsync(null, new SaveGameRequest
    {
        Name = "Test",
        Rounds = [new SaveGameRoundRequest
        {
            Position = 1,
            Questions = [new SaveRoundQuestionRequest
            {
                Position = 1, IdQuestionAnswer = 1, IdQCMQuestion = 1
            }]
        }]
    }, "test", CancellationToken.None);
}
catch (ApiValidationException) { didRejectWrite = true; }
Check(didRejectWrite, "Ecriture Game invalide rejetee avant SQL");

Console.WriteLine("Tests applicatifs PASS. Exécuter aussi le build Web et les tests API sur Windows.");

sealed class GameRepo : IGameRepository
{
    public bool BadReference { get; set; }

    public Task<IReadOnlyList<GameSummaryModel>> GetSummariesAsync(CancellationToken ct)
        => Task.FromResult<IReadOnlyList<GameSummaryModel>>([
            new() { Id = 1, Name = "Test", RoundCount = 2, QuestionCount = 3 }
        ]);

    public Task<GameModel?> GetByIdAsync(long id, CancellationToken ct)
    {
        if (id != 1) return Task.FromResult<GameModel?>(null);
        var game = new GameModel
        {
            Id = 1, Name = "Test", Author = "Tests",
            Rounds =
            [
                new GameRoundModel
                {
                    Id = 21, IdGame = 1, Position = 2,
                    Questions = [new RoundQuestionModel { Id = 102, Position = 1, IdQuestionAnswer = 8 }]
                },
                new GameRoundModel
                {
                    Id = 20, IdGame = 1, Position = 1,
                    Questions =
                    [
                        new RoundQuestionModel { Id = 100, Position = 2, IdQCMQuestion = 7 },
                        new RoundQuestionModel { Id = 101, Position = 1,
                            IdQCMQuestion = 7, IdQuestionAnswer = BadReference ? 8 : null }
                    ]
                }
            ]
        };
        return Task.FromResult<GameModel?>(game);
    }

    public async Task<IReadOnlyList<GameModel>> GetAllAsync(CancellationToken ct)
        => [ (await GetByIdAsync(1, ct))! ];

    public Task<long> SaveAsync(long? id, SaveGameRequest request, string author, CancellationToken ct)
        => throw new NotImplementedException("Les ecritures SQLite sont testees par l'API et non par ce faux repository.");

    public Task<bool> DeleteAsync(long id, CancellationToken ct) => Task.FromResult(false);
}

sealed class QcmSvc : IQcmService
{
    public int GetCalls { get; private set; }
    public bool ReturnNull { get; set; }
    public Task<QcmModel?> GetByIdAsync(long id, CancellationToken ct)
    {
        GetCalls++;
        return Task.FromResult<QcmModel?>(ReturnNull ? null : new QcmModel
        {
            Id = id, Question = "Studios", Answers = [new QcmPropositionModel
            { Id = 1, IdQCMAnswer = 1, Answer = "Sunrise", IsTrue = true }]
        });
    }
    public Task<IReadOnlyList<QcmModel>> GetAllAsync(CancellationToken ct)
        => Task.FromResult<IReadOnlyList<QcmModel>>([]);
    public Task<QcmModel> SaveAsync(long? id, SaveQcmRequest req, string author, CancellationToken ct)
        => throw new NotImplementedException();
    public Task<bool> DeleteAsync(long id, CancellationToken ct) => Task.FromResult(false);
}

sealed class QuestionSvc : IQuestionService
{
    public int GetCalls { get; private set; }
    public Task<QuestionAnswerModel?> GetByIdAsync(long id, CancellationToken ct)
    {
        GetCalls++;
        return Task.FromResult<QuestionAnswerModel?>(new QuestionAnswerModel
        { Id = id, Question = "Studio ?", Answer = "Sunrise" });
    }
    public Task<IReadOnlyList<QuestionAnswerModel>> GetAllAsync(CancellationToken ct)
        => Task.FromResult<IReadOnlyList<QuestionAnswerModel>>([]);
    public Task<QuestionAnswerModel> SaveAsync(long? id, SaveQuestionAnswerRequest req, string author, CancellationToken ct)
        => throw new NotImplementedException();
    public Task<bool> DeleteAsync(long id, CancellationToken ct) => Task.FromResult(false);
}
