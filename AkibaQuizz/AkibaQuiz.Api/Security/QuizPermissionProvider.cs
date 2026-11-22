using OrchardCore.Security.Permissions;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Security
{
    public class QuizPermissionProvider : IPermissionProvider
    {
        public Task<IEnumerable<Permission>> GetPermissionsAsync()
        {
            return Task.FromResult<IEnumerable<Permission>>(new[]
            {
                QuizPermissions.ManageQuizQuestions,
                QuizPermissions.ManageQuizGames,
                QuizPermissions.ManageQuizReferences,
                QuizPermissions.DeleteQuizContent,
                QuizPermissions.ViewQuizCatalog

            });
        }

        public IEnumerable<PermissionStereotype> GetDefaultStereotypes()
        {
            return [];
        }
    }
}
