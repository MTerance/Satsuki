
using OrchardCore.Security.Permissions;

namespace AkibaQuiz.Api.Security
{
    public class QuizPermissionProvider : IPermissionProvider
    {
        public Task<IEnumerable<Permission>> GetPermissionsAsync()
        {
            return Task.FromResult<IEnumerable<Permission>>(new[]
            {
                QuizPermissions.ViewQuizCatalog,
                QuizPermissions.ManageQuizQuestions,
                QuizPermissions.ManageQuizGames,
                QuizPermissions.ManageQuizReferences,
                QuizPermissions.DeleteQuizContent,
                QuizPermissions.ViewQuizAudit
            });
        }

        public IEnumerable<PermissionStereotype> GetDefaultStereotypes()
        {
            return [];
        }
    }
}
