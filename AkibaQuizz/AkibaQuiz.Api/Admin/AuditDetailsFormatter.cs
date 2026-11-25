using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json;

namespace AkibaQuiz.Api.Admin
{
    public static class AuditDetailsFormatter
    {
        public static IReadOnlyList<string> Describe(
            string? json)
        {
            if (string.IsNullOrWhiteSpace(json))
                return ["Aucun détail enregistré."];

            try
            {
                using var document = JsonDocument.Parse(json);
                var root = document.RootElement;

                if (root.ValueKind != JsonValueKind.Object)
                    return ["Format non reconnu."];

                var lines = new List<string>();

                string GetValue(string property)
                {
                    if (!root.TryGetProperty(
                            property, out var value) ||
                        value.ValueKind == JsonValueKind.Null)
                    {
                        return "—";
                    }

                    return value.ValueKind == JsonValueKind.String
                        ? value.GetString() ?? "—"
                        : value.ToString();
                }

                void AddDifference(
                    string oldProperty,
                    string newProperty,
                    string label)
                {
                    if (!root.TryGetProperty(
                            oldProperty, out _) &&
                        !root.TryGetProperty(
                            newProperty, out _))
                    {
                        return;
                    }

                    var oldValue = GetValue(oldProperty);
                    var newValue = GetValue(newProperty);

                    if (oldValue != newValue)
                    {
                        lines.Add(
                            $"{label} : {oldValue} → {newValue}");
                    }
                }

                void AddTags(
                    string property,
                    string label)
                {
                    if (!root.TryGetProperty(
                            property, out var values) ||
                        values.ValueKind != JsonValueKind.Array)
                    {
                        return;
                    }

                    var ids = values.EnumerateArray()
                        .Select(x => $"#{x}")
                        .ToArray();

                    if (ids.Length > 0)
                    {
                        lines.Add(
                            $"{label} : {string.Join(", ", ids)}");
                    }
                }

                AddDifference(
                    "oldName", "newName", "Nom");

                AddDifference(
                    "oldColor", "newColor", "Couleur");

                AddDifference(
                    "oldCategoryId",
                    "newCategoryId",
                    "Catégorie");

                AddTags("tagsAdded", "Tags ajoutés");
                AddTags("tagsRemoved", "Tags retirés");

                return lines.Count > 0
                    ? lines
                    : ["Aucune différence dans les champs suivis."];
            }
            catch (JsonException)
            {
                return ["JSON non interprétable."];
            }
        }
    }
}
