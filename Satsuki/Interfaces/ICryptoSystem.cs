namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les systèmes de cryptage
	/// </summary>
	public interface ICryptoSystem
	{
		/// <summary>
		/// Crypte un message
		/// </summary>
		/// <param name="plainText">Texte en clair</param>
		/// <returns>Texte crypté</returns>
		string Encrypt(string plainText);
		
		/// <summary>
		/// Décrypte un message
		/// </summary>
		/// <param name="cipherText">Texte crypté</param>
		/// <returns>Texte en clair</returns>
		string Decrypt(string cipherText);
		
		/// <summary>
		/// Teste le système de cryptage
		/// </summary>
		/// <returns>True si le test réussit</returns>
		bool Test();
		
		/// <summary>
		/// Génère une nouvelle clé de cryptage
		/// </summary>
		void GenerateNewKey();
	}
}
