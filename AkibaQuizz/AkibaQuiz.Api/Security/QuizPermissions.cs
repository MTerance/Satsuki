using OrchardCore.Security.Permissions;
using System;
using System.Collections.Generic;
using System.Text;

namespace AkibaQuiz.Api.Security
{
    public static class QuizPermissions
    {

        public static readonly Permission ViewQuizCatalog = new Permission("ViewQuizCatalog", "Consulter le Catalogue");
        public static readonly Permission ManageQuizQuestions = new Permission("ManageQuizQuestions", "Gérer les questions AkibaQuiz");
        public static readonly Permission ManageQuizGames = new Permission("ManageQuizGames", "Gérer les parties AkibaQuiz");
        public static readonly Permission ManageQuizReferences = new Permission("ManageQuizReferences", "Gérer les références AkibaQuiz (catégories et tags)");
        public static readonly Permission DeleteQuizContent = new Permission("DeleteQuizContent", "Supprimer le contenu AkibaQuiz (questions, QCM, parties)");
        public static readonly Permission ViewQuizAudit = new Permission("ViewQuizAudit", "Consulter le journal d'audit AkibaQuiz");
    }
}
