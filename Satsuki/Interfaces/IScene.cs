namespace Satsuki.Interfaces
{
	/// <summary>
	/// Interface de base pour toutes les scenes du jeu
	/// </summary>
	public interface IScene
	{
		/// <summary>
		/// Retourne l'etat actuel de la scene
		/// </summary>
		/// <returns>Un objet contenant l'etat de la scene</returns>
		object GetSceneState();
	}
}
