using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Utils
{
    public interface INetwork
    {
        bool Start();
        bool Stop();
    }

    /// <summary>
    /// Classe de base Singleton thread-safe utilisant le pattern Lazy<T>
    /// </summary>
    /// <typeparam name="T">Type qui hérite de SingletonBase</typeparam>
    public abstract class SingletonBase<T>
        where T : SingletonBase<T>, new()
    {
        // Utilisation de Lazy<T> pour garantir la thread-safety et l'initialisation paresseuse
        private static readonly Lazy<T> _lazyInstance = new Lazy<T>(() => new T());

        /// <summary>
        /// Obtient l'instance unique du singleton (thread-safe)
        /// </summary>
        public static T GetInstance => _lazyInstance.Value;

        /// <summary>
        /// Constructeur protégé pour empêcher l'instanciation externe
        /// </summary>
        protected SingletonBase()
        {
            // Vérification pour empêcher l'instanciation multiple via réflection
            if (_lazyInstance.IsValueCreated)
            {
                throw new InvalidOperationException($"Une instance de {typeof(T).Name} existe déjà. Utilisez GetInstance pour y accéder.");
            }
        }

        /// <summary>
        /// Méthode optionnelle pour réinitialiser le singleton (utile pour les tests)
        /// ATTENTION: Cette méthode n'est pas thread-safe et ne devrait être utilisée que dans des contextes contrôlés
        /// </summary>
        protected static void ResetInstance()
        {
            // Note: Lazy<T> ne peut pas être "reset" facilement
            // Cette méthode est principalement documentaire
            // Pour un vrai reset, il faudrait utiliser une approche différente
            System.Diagnostics.Debug.WriteLine($"ATTENTION: ResetInstance appelé pour {typeof(T).Name}. Lazy<T> ne peut pas être reset facilement.");
        }

        /// <summary>
        /// Vérifie si l'instance a été créée
        /// </summary>
        public static bool IsInstanceCreated => _lazyInstance.IsValueCreated;
    }
}
