
using System;
using System.Threading;
using System.Threading.Tasks;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Infrastructure.Database;
using Dapper;

namespace AkibaQuiz.Infrastructure.Repositories
{
    public sealed class MediaCatalogRepository
        : IMediaCatalogRepository
    {
        private readonly SqliteConnectionFactory _connectionFactory;

        public MediaCatalogRepository(
            SqliteConnectionFactory connectionFactory)
        {
            _connectionFactory = connectionFactory;
        }

        public async Task<long> ResolveOrCreateAsync(
            string orchardPath,
            string mediaType,
            CancellationToken cancellationToken)
        {
            if (string.IsNullOrWhiteSpace(orchardPath))
                throw new ArgumentException(
                    "Le chemin Orchard est obligatoire.",
                    nameof(orchardPath));

            if (string.IsNullOrWhiteSpace(mediaType))
                throw new ArgumentException(
                    "Le type du média est obligatoire.",
                    nameof(mediaType));

            orchardPath = orchardPath.Trim();
            mediaType = mediaType.Trim();

            await using var db =
                await _connectionFactory.OpenAsync(cancellationToken);

            await using var tx =
                await db.BeginTransactionAsync(cancellationToken);

            // ==========================================
            // 1. RECHERCHER LE TYPE DE MEDIA
            // ==========================================

            var typeId = await db.ExecuteScalarAsync<long?>(
                new CommandDefinition(
                    """
                    SELECT Id
                    FROM TypeMedia
                    WHERE Name = @Name COLLATE NOCASE
                    LIMIT 1;
                    """,
                    new
                    {
                        Name = mediaType
                    },
                    transaction: tx,
                    cancellationToken: cancellationToken
                )
            );

            // ==========================================
            // 2. CREER LE TYPE S'IL N'EXISTE PAS
            // ==========================================

            if (!typeId.HasValue)
            {
                typeId = await db.ExecuteScalarAsync<long>(
                    new CommandDefinition(
                        """
                        INSERT INTO TypeMedia (Name)
                        VALUES (@Name);

                        SELECT last_insert_rowid();
                        """,
                        new
                        {
                            Name = mediaType
                        },
                        transaction: tx,
                        cancellationToken: cancellationToken
                    )
                );
            }

            // ==========================================
            // 3. RECHERCHER LE MEDIA EXISTANT
            // ==========================================

            var mediaId = await db.ExecuteScalarAsync<long?>(
                new CommandDefinition(
                    """
                    SELECT Id
                    FROM Medias
                    WHERE Filename = @Filename
                      AND IdTypeMedia = @IdTypeMedia
                    LIMIT 1;
                    """,
                    new
                    {
                        Filename = orchardPath,
                        IdTypeMedia = typeId.Value
                    },
                    transaction: tx,
                    cancellationToken: cancellationToken
                )
            );

            // ==========================================
            // 4. CREER LE MEDIA S'IL N'EXISTE PAS
            // ==========================================

            if (!mediaId.HasValue)
            {
                mediaId = await db.ExecuteScalarAsync<long>(
                    new CommandDefinition(
                        """
                        INSERT INTO Medias
                            (Filename, IdTypeMedia)
                        VALUES
                            (@Filename, @IdTypeMedia);

                        SELECT last_insert_rowid();
                        """,
                        new
                        {
                            Filename = orchardPath,
                            IdTypeMedia = typeId.Value
                        },
                        transaction: tx,
                        cancellationToken: cancellationToken
                    )
                );
            }

            // ==========================================
            // 5. VALIDER LA TRANSACTION
            // ==========================================

            await tx.CommitAsync(cancellationToken);

            return mediaId.Value;
        }
    }
}
