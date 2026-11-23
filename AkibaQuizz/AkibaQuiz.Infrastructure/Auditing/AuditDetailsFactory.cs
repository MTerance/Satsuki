using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json;

namespace AkibaQuiz.Infrastructure.Auditing
{
    internal static class AuditDetailsFactory
    {
        public static string ForQuestion(
            long? oldCategoryId,
            long? newCategoryId,
            IEnumerable<long> oldTagIds,
            IEnumerable<long> newTagIds)
        {
            ArgumentNullException.ThrowIfNull(oldTagIds);
            ArgumentNullException.ThrowIfNull(newTagIds);

            var previous = oldTagIds
                .Where(id => id > 0)
                .ToHashSet();

            var current = newTagIds
                .Where(id => id > 0)
                .ToHashSet();

            return JsonSerializer.Serialize(new
            {
                oldCategoryId,
                newCategoryId,

                tagsAdded = current
                    .Except(previous)
                    .OrderBy(id => id)
                    .ToArray(),

                tagsRemoved = previous
                    .Except(current)
                    .OrderBy(id => id)
                    .ToArray()
            });
        }

        public static string ForCategory(
            string? oldName,
            string? newName)
        {
            return JsonSerializer.Serialize(new
            {
                oldName,
                newName
            });
        }

        public static string ForTag(
            string? oldName,
            string? oldColor,
            string? newName,
            string? newColor)
        {
            return JsonSerializer.Serialize(new
            {
                oldName,
                oldColor,
                newName,
                newColor
            });
        }
    }
}
