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
    /// <typeparam name="T">Type qui herite de SingletonBase</typeparam>
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
        /// Constructeur protege pour empecher l'instanciation externe
        /// </summary>
        protected SingletonBase()
        {
            // Verification pour empecher l'instanciation multiple via reflection
            if (_lazyInstance.IsValueCreated)
            {
                throw new InvalidOperationException($"Une instance de {typeof(T).Name} existe deja. Utilisez GetInstance pour y acceder.");
            }
        }

        /// <summary>
        /// Methode optionnelle pour reinitialiser le singleton (utile pour les tests)
        /// ATTENTION: Cette methode n'est pas thread-safe et ne devrait etre utilisee que dans des contextes controles
        /// </summary>
        protected static void ResetInstance()
        {
            // Note: Lazy<T> ne peut pas etre "reset" facilement
            // Cette methode est principalement documentaire
            // Pour un vrai reset, il faudrait utiliser une approche differente
            System.Diagnostics.Debug.WriteLine($"ATTENTION: ResetInstance appele pour {typeof(T).Name}. Lazy<T> ne peut pas etre reset facilement.");
        }

        /// <summary>
        /// Verifie si l'instance a ete creee
        /// </summary>
        public static bool IsInstanceCreated => _lazyInstance.IsValueCreated;
    }
}
