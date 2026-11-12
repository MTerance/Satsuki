using Microsoft.Extensions.Localization;
using OrchardCore.Navigation;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Navigation
{
    public sealed class QuizStudioAdminMenu : INavigationProvider
    {
        private readonly IStringLocalizer _localizer;

        public QuizStudioAdminMenu(IStringLocalizer<QuizStudioAdminMenu> localizer)
        {
            _localizer = localizer;
        }

        public ValueTask BuildNavigationAsync(string name, NavigationBuilder builder)
        {
            if (!string.Equals(name, "admin", StringComparison.OrdinalIgnoreCase))
            {
                return ValueTask.CompletedTask;
            }

            builder.Add(_localizer["Quiz Studio"], "5", menu =>
            {
                menu
                    .Add(_localizer["Banque de contenu"], "1", item => item
                        .Action("Index", "QuizStudio", new { area = "AkibaQuiz.Api" })
                        /*
                        .Permission(Permissions.ManageQuizStudio)
                        .LocalNav());
                        */
                        );
            });
            return ValueTask.CompletedTask;
        }




    }
}
