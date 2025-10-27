namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les gestionnaires de base de données
	/// </summary>
	public interface IDatabase
	{
		/// <summary>
		/// Initialise la connexion à la base de données
		/// </summary>
		/// <param name="connectionString">Chaîne de connexion</param>
		/// <returns>True si la connexion réussit</returns>
		bool Initialize(string connectionString);
		
		/// <summary>
		/// Ferme la connexion à la base de données
		/// </summary>
		void Close();
		
		/// <summary>
		/// Vérifie si la base de données est connectée
		/// </summary>
		/// <returns>True si connecté</returns>
		bool IsConnected();
		
		/// <summary>
		/// Exécute une requête SQL
		/// </summary>
		/// <param name="query">Requête SQL</param>
		/// <returns>Nombre de lignes affectées</returns>
		int ExecuteQuery(string query);
	}
}
