namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface de base pour toutes les sc�nes du jeu
	/// </summary>
	public interface IScene
	{
		/// <summary>
		/// Retourne l'�tat actuel de la sc�ne
		/// </summary>
		/// <returns>Un objet contenant l'�tat de la sc�ne</returns>
		object GetSceneState();
	}
}
