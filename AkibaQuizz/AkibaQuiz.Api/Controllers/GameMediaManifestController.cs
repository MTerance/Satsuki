using AkibaQuiz.Api.Security;
using AkibaQuiz.Contracts.Models;
using AkibaQuiz.Application.Interfaces;
using OrchardCore.Media;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Controllers
{
    [ApiController]
    [Route("api/catalog/games/{id:long:min(1)}/media")]
    [TypeFilter(typeof(CielCatalogApiKeyFilter))]
    [TypeFilter(typeof(ApiExceptionFilter))]
    public sealed class GameMediaManifestController : ControllerBase
    {
        private readonly IGameService _gameService;
        private readonly IMediaFileStore _mediaFileStore;
        private readonly ILogger<GameMediaManifestController> _logger;

        public GameMediaManifestController(IGameService gameService, IMediaFileStore mediaFileStore, ILogger<GameMediaManifestController> logger)
        {
            _gameService = gameService;
            _mediaFileStore = mediaFileStore;
            _logger = logger;
        }

        [HttpGet]
        public async Task<IActionResult> Get(long id, CancellationToken cancellationToken)
        {
            var game = await _gameService.GetFullAsync(id, cancellationToken);
            if (game is null)
                return NotFound();
            var mediaItems = new List<QuizMediaModel>();

            foreach (var round in game.Rounds)
            {
                foreach (var question in round.Questions)
                {
                    if (question.QuestionAnswer is not null)
                    {
                        mediaItems.AddRange(question.QuestionAnswer.Medias);
                    }
                    else if (question.Qcm is not null)
                    {
                        mediaItems.AddRange(question.Qcm.Medias);

                    }
                }
            }

            var groups = mediaItems.GroupBy(m => m.IdMedia).OrderBy(g => g.Key).ToList();

            var result = new List<GameMediaItemDto>();

            var configureBaseUrl = Environment.GetEnvironmentVariable("AKIBA_PUBLIC_BASE_URL") ?? "";

            var baseUrl = string.IsNullOrWhiteSpace(configureBaseUrl) ?
                $"{Request.Scheme}://{Request.Host}" : configureBaseUrl.TrimEnd('/');
            if (!Uri.TryCreate(
                       baseUrl,
                       UriKind.Absolute,
                       out var baseUri) ||
                       baseUri.Scheme is not ("http" or "https"))
            {
                return Problem(
                    "AKIBA_PUBLIC_BASE_URL est invalide.",
                    statusCode: 500);
            }

            foreach (var group in groups)
            {
                var media = group.First();
                var path = media.Filename;

                // Un même IdMedia ne doit pas désigner
                // plusieurs fichiers différents.
                if (group.Any(m =>
                    !string.Equals(
                        m.Filename,
                        path,
                        StringComparison.Ordinal)))
                {
                    return Conflict(new
                    {
                        error =
                            $"Références incohérentes pour " +
                            $"IdMedia #{group.Key}."
                    });
                }

                // 4. Rejeter les chemins non conformes
                //    au stockage logique Orchard.
                if (!IsValidMediaPath(path))
                {
                    _logger.LogWarning(
                        "Le chemin de fichier {Path} pour IdMedia #{IdMedia} " +
                        "n'est pas conforme au stockage logique Orchard.",
                        path,
                        media.IdMedia);

                    result.Add(new GameMediaItemDto(
                        media.IdMedia,
                        path,
                        media.TypeMediaName,
                        null,
                        false));

                    continue;
                }

                // 5. Vérifier que le fichier existe.
                var file = await _mediaFileStore
                    .GetFileInfoAsync(path);
                _logger.LogWarning(
                    "MEDIA DIAGNOSTIC Id={Id}, Path={Path}, Exists={Exists}, IsDirectory={IsDirectory}",
                    media.IdMedia,
                    path,
                    file != null,
                    file?.IsDirectory
                );
                if (file is null || file.IsDirectory)
                {
                    result.Add(new GameMediaItemDto(
                        media.IdMedia,
                        path,
                        media.TypeMediaName,
                        null,
                        false));

                    continue;
                }

                // 6. Résoudre l'URL avec Orchard Core.
                var publicPath =
                    _mediaFileStore.MapPathToPublicUrl(path);

                var url = BuildAbsoluteUrl(
                    baseUri,
                    publicPath);

                _logger.LogWarning(
                    "MEDIA URL Id={Id}, PublicPath={PublicPath}, FinalUrl={Url}",
                    media.IdMedia,
                    publicPath,
                    url
                );

                result.Add(new GameMediaItemDto(
                    media.IdMedia,
                    path,
                    media.TypeMediaName,
                    url,
                    url is not null));
            }

            return Ok(new GameMediaManifestDto(
                id,
                result));
        }
        private static bool IsValidMediaPath(string? path)
        {
            if (string.IsNullOrWhiteSpace(path) ||
                path.Length > 1024 ||
                path.StartsWith('/') ||
                path.Contains('\\') ||
                path.Contains(':') ||
                path.Contains('?') ||
                path.Contains('#'))
            {
                return false;
            }

            return !path.Split('/').Any(segment =>
                string.IsNullOrWhiteSpace(segment) ||
                segment is "." or "..");
        }


        private static string? BuildAbsoluteUrl(
            Uri baseUri,
            string? publicPath)
        {
            if (string.IsNullOrWhiteSpace(publicPath))
                return null;

            publicPath = publicPath.Trim();

            // Refuser les URL relatives au protocole.
            if (publicPath.StartsWith("//",
                StringComparison.Ordinal))
            {
                return null;
            }

            // 1. Chemin public Orchard Core :
            //    /media/akibaquizz/questions/images/test.webp
            if (publicPath.StartsWith('/'))
            {
                return new Uri(
                    baseUri,
                    publicPath
                ).AbsoluteUri;
            }

            // 2. URL absolue (CDN, Azure, etc.).
            if (Uri.TryCreate(
                publicPath,
                UriKind.Absolute,
                out var absolute))
            {
                return absolute.Scheme is "http" or "https"
                    ? absolute.AbsoluteUri
                    : null;
            }

            // 3. Chemin relatif sans slash initial.
            return new Uri(
                baseUri,
                "/" + publicPath
            ).AbsoluteUri;
        }
    }
}
