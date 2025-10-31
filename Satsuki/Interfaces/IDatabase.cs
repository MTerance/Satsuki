namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les gestionnaires de base de donn�es
	/// </summary>
	public interface IDatabase
	{
		/// <summary>
		/// Initialise la connexion � la base de donn�es
		/// </summary>
		/// <param name="connectionString">Cha�ne de connexion</param>
		/// <returns>True si la connexion r�ussit</returns>
		bool Initialize(string connectionString);
		
		/// <summary>
		/// Ferme la connexion � la base de donn�es
		/// </summary>
		void Close();
		
		/// <summary>
		/// V�rifie si la base de donn�es est connect�e
		/// </summary>
		/// <returns>True si connect�</returns>
		bool IsConnected();
		
		/// <summary>
		/// Ex�cute une requ�te SQL
		/// </summary>
		/// <param name="query">Requ�te SQL</param>
		/// <returns>Nombre de lignes affect�es</returns>
		int ExecuteQuery(string query);
	}
}
