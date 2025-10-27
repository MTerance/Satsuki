using Godot;
using System;
using System.Collections.Generic;

namespace Satsuki.Scenes
{
	/// <summary>
	/// Exemple de sc�ne de quiz qui impl�mente GetSceneState()
	/// </summary>
	public partial class QuizScene : Node
	{
		private string _quizTitle = "Quiz de Test";
		private int _currentQuestionIndex = 0;
		private int _totalQuestions = 10;
		private int _score = 0;
		private bool _isActive = false;
		private List<string> _players = new List<string>();
		
		public override void _Ready()
		{
			GD.Print("?? QuizScene initialis�e");
		}
		
		/// <summary>
		/// Retourne l'�tat actuel de la sc�ne de quiz
		/// </summary>
		public object GetSceneState()
		{
			return new
			{
				QuizInfo = new
				{
					Title = _quizTitle,
					IsActive = _isActive,
					CurrentQuestion = _currentQuestionIndex + 1,
					TotalQuestions = _totalQuestions,
					Progress = _totalQuestions > 0 ? (float)_currentQuestionIndex / _totalQuestions * 100 : 0
				},
				PlayerStats = new
				{
					PlayerCount = _players.Count,
					Players = _players,
					CurrentScore = _score
				},
				Timing = new
				{
					SceneLoadTime = Time.GetTicksMsec(),
					Timestamp = DateTime.UtcNow
				}
			};
		}
		
		// M�thodes exemple pour manipuler l'�tat
		public void StartQuiz(string title, int questionCount)
		{
			_quizTitle = title;
			_totalQuestions = questionCount;
			_currentQuestionIndex = 0;
			_score = 0;
			_isActive = true;
			GD.Print($"?? Quiz d�marr�: {title} ({questionCount} questions)");
		}
		
		public void AddPlayer(string playerName)
		{
			if (!_players.Contains(playerName))
			{
				_players.Add(playerName);
				GD.Print($"?? Joueur ajout�: {playerName}");
			}
		}
		
		public void NextQuestion()
		{
			if (_currentQuestionIndex < _totalQuestions - 1)
			{
				_currentQuestionIndex++;
				GD.Print($"?? Question suivante: {_currentQuestionIndex + 1}/{_totalQuestions}");
			}
			else
			{
				_isActive = false;
				GD.Print("? Quiz termin�!");
			}
		}
		
		public void AddScore(int points)
		{
			_score += points;
			GD.Print($"?? Score: {_score} (+{points})");
		}
	}
}
