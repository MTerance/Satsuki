using AkibaQuiz.Api.Security;
using AkibaQuiz.Api.Navigation;
using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Application.Services;
using AkibaQuiz.Infrastructure.Repositories;
using AkibaQuiz.Infrastructure.Database;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Routing;
using Microsoft.Data.Sqlite;
using Microsoft.Extensions.DependencyInjection;
using OrchardCore.Modules;
using OrchardCore.Navigation;
using OrchardCore.Security.Permissions;
namespace AkibaQuiz.Api;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        var connectionString = Environment.GetEnvironmentVariable("AKIBA_DB_PATH");
        if (string.IsNullOrEmpty(connectionString))
        {
            throw new InvalidOperationException("The AKIBA_DB_PATH environment variable is not set.");
        }

        services.AddSingleton(
            new SqliteConnectionFactory(connectionString));
        services.AddScoped<CielCatalogApiKeyFilter>();
        services.AddHttpContextAccessor();
        services.AddScoped<IAuditActorProvider, HttpAuditActorProvider>();
        services.AddScoped<IPermissionProvider, QuizPermissionProvider>();
        services.AddScoped<IMediaCatalogRepository, MediaCatalogRepository>();
        services.AddScoped<IMediaCatalogService, MediaCatalogService>();
        services.AddScoped<IQuestionCatalogRepository, QuestionCatalogRepository>();
        services.AddScoped<IQuestionCatalogService, QuestionCatalogService>();
        services.AddScoped<IQcmRepository, QcmRepository>();
        services.AddScoped<IReferenceRepository, ReferenceRepository>();
        services.AddScoped<IQuestionRepository, QuestionRepository>();
        services.AddScoped<IGameRepository, GameRepository>();
        services.AddScoped<IQuestionService, QuestionService>();
        services.AddScoped<IQcmService, QcmService>();
        services.AddScoped<IGameService, GameService>();
        services.AddScoped<IReferenceService, ReferenceService>();
        services.AddNavigationProvider<QuizStudioAdminMenu>();
        services.AddScoped<AdminApiKeyFilter>();
        services.AddScoped<ApiExceptionFilter>();
    }

    public override void Configure(IApplicationBuilder builder, IEndpointRouteBuilder routes, IServiceProvider serviceProvider)
    {
        routes.MapAreaControllerRoute(
            name: "Home",
            areaName: "AkibaQuiz.Api",
            pattern: "Home/Index",
            defaults: new { controller = "Home", action = "Index" }
        );
    }
}

