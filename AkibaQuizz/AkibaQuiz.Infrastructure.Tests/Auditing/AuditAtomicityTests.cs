using AkibaQuiz.Application.Auditing;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Infrastructure.Auditing;
using Dapper;
using Microsoft.Data.Sqlite;
using Xunit;

namespace AkibaQuiz.Infrastructure.Tests.Auditing
{
    public sealed class AuditAtomicityTests
    {
        private sealed class TestActorProvider(
            string actorId) : IAuditActorProvider
        {
            public AuditActor GetCurrent() =>
                new("System", actorId, null);
        }

        private static async Task<SqliteConnection>
            CreateDatabaseAsync()
        {
            var db = new SqliteConnection(
                "Data Source=:memory:");

            await db.OpenAsync();

            await db.ExecuteAsync("""
            CREATE TABLE QuestionsAnswers
            (
                Id INTEGER PRIMARY KEY,
                IdCategory INTEGER NOT NULL,
                Question TEXT NOT NULL
            );

            CREATE TABLE TagQuizz
            (
                IdQuestionAnswer INTEGER,
                IdTag INTEGER NOT NULL
            );

            CREATE TABLE AuditEvents
            (
                Id INTEGER PRIMARY KEY AUTOINCREMENT,
                OccurredAtUtc TEXT NOT NULL,
                EntityType TEXT NOT NULL,
                EntityId INTEGER NOT NULL,
                Action TEXT NOT NULL,

                ActorType TEXT NOT NULL
                    CHECK (ActorType IN (
                        'OrchardUser',
                        'AdminApi',
                        'System'
                    )),

                ActorId TEXT NOT NULL
                    CHECK (ActorId <> 'reject-insert'),

                CorrelationId TEXT,
                DetailsJson TEXT
            );
            """);

            return db;
        }

        [Fact]
        public async Task SuccessfulAudit_CommitsBoth()
        {
            await using var db =
                await CreateDatabaseAsync();

            var audit = new AuditTrail(
                new TestActorProvider("test-runner"));

            await using (var tx =
                await db.BeginTransactionAsync())
            {
                await db.ExecuteAsync(
                    """
                INSERT INTO QuestionsAnswers
                    (Id, IdCategory, Question)
                VALUES (1, 2, 'Test question');
                """,
                    transaction: tx);

                await audit.RecordChangeAsync(
                    db,
                    tx,
                    AuditEntityType.QuestionAnswer,
                    1,
                    AuditOperation.Create,
                    before: null,
                    CancellationToken.None);

                await tx.CommitAsync();
            }

            var questions = await db.ExecuteScalarAsync<long>(
                "SELECT COUNT(*) FROM QuestionsAnswers;");

            var events = await db.ExecuteScalarAsync<long>(
                "SELECT COUNT(*) FROM AuditEvents;");

            Assert.Equal(1, questions);
            Assert.Equal(1, events);
        }

        [Fact]
        public async Task AuditFailure_RollsBackBusinessOperation()
        {
            await using var db =
                await CreateDatabaseAsync();

            // L'identité est valide pour AuditSqlWriter,
            // mais refusée par la contrainte SQL de test.
            var audit = new AuditTrail(
                new TestActorProvider("reject-insert"));

            await using (var tx =
                await db.BeginTransactionAsync())
            {
                await db.ExecuteAsync(
                    """
                INSERT INTO QuestionsAnswers
                    (Id, IdCategory, Question)
                VALUES (1, 2, 'Test question');
                """,
                    transaction: tx);

                var error = await Assert.ThrowsAsync<
                    SqliteException>(
                    () => audit.RecordChangeAsync(
                        db,
                        tx,
                        AuditEntityType.QuestionAnswer,
                        1,
                        AuditOperation.Create,
                        before: null,
                        CancellationToken.None));

                Assert.Equal(19, error.SqliteErrorCode);

                // Aucun Commit : le DisposeAsync
                // annule la transaction.
            }

            var questions = await db.ExecuteScalarAsync<long>(
                "SELECT COUNT(*) FROM QuestionsAnswers;");

            var events = await db.ExecuteScalarAsync<long>(
                "SELECT COUNT(*) FROM AuditEvents;");

            Assert.Equal(0, questions);
            Assert.Equal(0, events);
        }
    }
}
