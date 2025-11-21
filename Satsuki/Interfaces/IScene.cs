namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface de base pour toutes les scènes du jeu
	/// </summary>
	public interface IScene
	{
		/// <summary>
		/// Retourne l'état actuel de la scène
		/// </summary>
		/// <returns>Un objet contenant l'état de la scène</returns>
		object GetSceneState();
	}
}
