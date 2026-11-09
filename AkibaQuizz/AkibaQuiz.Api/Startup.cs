using AkibaQuiz.Application.Interfaces;
using AkibaQuiz.Application.Services;
using AkibaQuiz.Infrastructure.Repositories;
using AkibaQuiz.Infrastructure.Database;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Routing;
using Microsoft.Data.Sqlite;
using Microsoft.Extensions.DependencyInjection;
using OrchardCore.Modules;

namespace AkibaQuiz.Api;

public sealed class Startup : StartupBase
{
    public override void ConfigureServices(IServiceCollection services)
    {
        var connectionString = Environment.GetEnvironmentVariable("AkibaQuiz") ??
            "Data Source=AkibaQuiz.db;Cache=Shared;Mode=ReadWriteCreate;Pooling=True;Max Pool Size=100;";

        services.AddSingleton(
            new SqliteConnectionFactory(connectionString));
        services.AddScoped<IQcmRepository, QcmRepository>();
        services.AddScoped<IQcmService, QcmService>();
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

