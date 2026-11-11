using System;
using System.Collections.Generic;
using System.Text;
using AkibaQuiz.Application.Catalog;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Infrastructure.Database;
using Dapper;

namespace AkibaQuiz.Infrastructure.Repositories
{
    public sealed class GameCatalogRepository : IGameCatalogRepository
    {
        private readonly SqliteConnectionFactory _connectionFactory;

        public GameCatalogRepository(SqliteConnectionFactory connectionFactory)
        {
            _connectionFactory = connectionFactory;
        }

        public async Task<IReadOnlyList<GameSummaryDto>> GetGamesAsync(CancellationToken cancellationToken)
        {
            const string sql = @"SELECT
                g.Id,
                g.Name,

                (
                    SELECT COUNT(*)
                    FROM GameRounds gr
                    WHERE gr.IdGame = g.Id
                ) AS RoundCount,

                (
                    SELECT COUNT(*)
                    FROM RoundQuestions rq
                    INNER JOIN GameRounds gr
                        ON gr.Id = rq.IdGameRound
                    WHERE gr.IdGame = g.Id
                ) AS QuestionCount

            FROM Games g
            ORDER BY g.Name COLLATE NOCASE, g.Id;";

            await using var connection = await _connectionFactory.OpenAsync(cancellationToken);
            var command = new CommandDefinition(sql, cancellationToken: cancellationToken);
            var games = await connection.QueryAsync<GameSummaryDto>(command);
            return games.ToList();
        }
    }
}
