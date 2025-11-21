using Godot;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Satsuki.Scenes
{
	/// <summary>
	/// Exemple de scène de jeu qui implémente GetSceneState()
	/// </summary>
	public partial class GameplayScene : Node
	{
		private string _levelName = "Level 1";
		private int _playerHealth = 100;
		private int _playerMaxHealth = 100;
		private int _enemiesKilled = 0;
		private int _totalEnemies = 20;
		private float _playTime = 0.0f;
		private bool _isPaused = false;
		private Dictionary<string, int> _inventory = new Dictionary<string, int>();
		
		public override void _Ready()
		{
			GD.Print("?? GameplayScene initialisée");
			
			// Initialiser l'inventaire exemple
			_inventory["coins"] = 0;
			_inventory["health_potions"] = 3;
			_inventory["mana_potions"] = 2;
		}
		
		public override void _Process(double delta)
		{
			if (!_isPaused)
			{
				_playTime += (float)delta;
			}
		}
		
		/// <summary>
		/// Retourne l'état actuel de la scène de jeu
		/// </summary>
		public object GetSceneState()
		{
			return new
			{
				Level = new
				{
					Name = _levelName,
					Progress = _totalEnemies > 0 ? (float)_enemiesKilled / _totalEnemies * 100 : 0,
					EnemiesRemaining = _totalEnemies - _enemiesKilled,
					TotalEnemies = _totalEnemies
				},
				Player = new
				{
					Health = _playerHealth,
					MaxHealth = _playerMaxHealth,
					HealthPercentage = (float)_playerHealth / _playerMaxHealth * 100,
					IsAlive = _playerHealth > 0
				},
				Inventory = _inventory.Select(kvp => new
				{
					Item = kvp.Key,
					Quantity = kvp.Value
				}).ToList(),
				Session = new
				{
					PlayTime = Math.Round(_playTime, 2),
					PlayTimeFormatted = FormatTime(_playTime),
					IsPaused = _isPaused,
					StartTime = DateTime.UtcNow.AddSeconds(-_playTime)
				},
				Statistics = new
				{
					EnemiesKilled = _enemiesKilled,
					KillRate = _playTime > 0 ? Math.Round(_enemiesKilled / _playTime * 60, 2) : 0, // Kills per minute
					SurvivalTime = _playTime
				}
			};
		}
		
		/// <summary>
		/// Formate le temps de jeu
		/// </summary>
		private string FormatTime(float seconds)
		{
			int minutes = (int)(seconds / 60);
			int secs = (int)(seconds % 60);
			return $"{minutes:D2}:{secs:D2}";
		}
		
		// Méthodes exemple pour manipuler l'état
		public void SetLevel(string levelName, int totalEnemies)
		{
			_levelName = levelName;
			_totalEnemies = totalEnemies;
			_enemiesKilled = 0;
			GD.Print($"??? Niveau chargé: {levelName}");
		}
		
		public void TakeDamage(int damage)
		{
			_playerHealth = Math.Max(0, _playerHealth - damage);
			GD.Print($"?? Dégâts reçus: -{damage} HP (restant: {_playerHealth})");
			
			if (_playerHealth <= 0)
			{
				GD.Print("?? Game Over!");
			}
		}
		
		public void Heal(int amount)
		{
			_playerHealth = Math.Min(_playerMaxHealth, _playerHealth + amount);
			GD.Print($"?? Soins: +{amount} HP (actuel: {_playerHealth})");
		}
		
		public void KillEnemy()
		{
			if (_enemiesKilled < _totalEnemies)
			{
				_enemiesKilled++;
				GD.Print($"?? Ennemi éliminé! ({_enemiesKilled}/{_totalEnemies})");
			}
		}
		
		public void AddToInventory(string item, int quantity = 1)
		{
			if (_inventory.ContainsKey(item))
			{
				_inventory[item] += quantity;
			}
			else
			{
				_inventory[item] = quantity;
			}
			GD.Print($"?? Objet ajouté: {item} x{quantity}");
		}
		
		public void TogglePause()
		{
			_isPaused = !_isPaused;
			GD.Print(_isPaused ? "?? Jeu en pause" : "?? Jeu repris");
		}
	}
}
