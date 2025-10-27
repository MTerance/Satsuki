namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface pour les syst�mes de cryptage
	/// </summary>
	public interface ICryptoSystem
	{
		/// <summary>
		/// Crypte un message
		/// </summary>
		/// <param name="plainText">Texte en clair</param>
		/// <returns>Texte crypt�</returns>
		string Encrypt(string plainText);
		
		/// <summary>
		/// D�crypte un message
		/// </summary>
		/// <param name="cipherText">Texte crypt�</param>
		/// <returns>Texte en clair</returns>
		string Decrypt(string cipherText);
		
		/// <summary>
		/// Teste le syst�me de cryptage
		/// </summary>
		/// <returns>True si le test r�ussit</returns>
		bool Test();
		
		/// <summary>
		/// G�n�re une nouvelle cl� de cryptage
		/// </summary>
		void GenerateNewKey();
	}
}
