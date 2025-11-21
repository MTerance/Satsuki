using Godot;
using Satsuki.Interfaces;
using System;
using System.Text.Json;

namespace Satsuki.Scenes.Examples
{
	/// <summary>
	/// Exemple de scène de quiz implémentant INetworkScene
	/// </summary>
	public partial class NetworkQuizScene : Node, INetworkScene
	{
		private DateTime _sceneStartTime;
		private string _quizTitle = "Quiz Réseau";
		private int _currentQuestionIndex = 0;
		private int _totalQuestions = 10;
		private bool _isPaused = false;
		private bool _isActive = false;
		
		public override void _Ready()
		{
			_sceneStartTime = DateTime.UtcNow;
			GD.Print("?? NetworkQuizScene initialisée");
		}
		
		/// <summary>
		/// Retourne l'état actuel de la scène (IScene)
		/// </summary>
		public object GetSceneState()
		{
			return new
			{
				SceneInfo = new
				{
					SceneName = "NetworkQuizScene",
					SceneType = "Quiz",
					StartTime = _sceneStartTime,
					ElapsedTime = (DateTime.UtcNow - _sceneStartTime).TotalSeconds
				},
				QuizInfo = new
				{
					Title = _quizTitle,
					IsActive = _isActive,
					IsPaused = _isPaused,
					CurrentQuestion = _currentQuestionIndex + 1,
					TotalQuestions = _totalQuestions,
					Progress = _totalQuestions > 0 ? (float)_currentQuestionIndex / _totalQuestions * 100 : 0
				},
				Status = new
				{
					Timestamp = DateTime.UtcNow
				}
			};
		}
		
		/// <summary>
		/// Traite les orders BACKEND (INetworkScene)
		/// </summary>
		public void HandleSceneOrder(string clientId, string order, string jsonData)
		{
			GD.Print($"?? [NetworkQuizScene] Order de {clientId}: {order}");
			
			try
			{
				using JsonDocument doc = JsonDocument.Parse(jsonData);
				JsonElement root = doc.RootElement;
				
				switch (order)
				{
					case "StartQuiz":
						StartQuiz();
						SendOrderResponse(clientId, order, "Quiz démarré", true);
						break;
						
					case "PauseQuiz":
						PauseQuiz();
						SendOrderResponse(clientId, order, "Quiz mis en pause", true);
						break;
						
					case "ResumeQuiz":
						ResumeQuiz();
						SendOrderResponse(clientId, order, "Quiz repris", true);
						break;
						
					case "StopQuiz":
						StopQuiz();
						SendOrderResponse(clientId, order, "Quiz arrêté", true);
						break;
						
					case "SkipQuestion":
						SkipQuestion();
						SendOrderResponse(clientId, order, "Question sautée", true);
						break;
						
					case "GetQuizState":
						var state = GetSceneState();
						SendOrderResponse(clientId, order, JsonSerializer.Serialize(state), true);
						break;
						
					default:
						GD.PrintErr($"?? Order inconnu: {order}");
						SendOrderResponse(clientId, order, $"Order inconnu: {order}", false);
						break;
				}
			}
			catch (Exception ex)
			{
				GD.PrintErr($"? Erreur HandleSceneOrder: {ex.Message}");
				SendOrderResponse(clientId, order, $"Erreur: {ex.Message}", false);
			}
		}
		
		/// <summary>
		/// Traite les requests clients (INetworkScene)
		/// </summary>
		public void HandleSceneRequest(string clientId, string request, string jsonData)
		{
			GD.Print($"?? [NetworkQuizScene] Request de {clientId}: {request}");
			
			try
			{
				using JsonDocument doc = JsonDocument.Parse(jsonData);
				JsonElement root = doc.RootElement;
				
				switch (request)
				{
					case "SubmitAnswer":
						if (root.TryGetProperty("questionId", out JsonElement qIdElement) &&
							root.TryGetProperty("answer", out JsonElement answerElement))
						{
							int questionId = qIdElement.GetInt32();
							string answer = answerElement.GetString();
							float timeTaken = root.TryGetProperty("timeTaken", out JsonElement timeElement) 
								? timeElement.GetSingle() : 0;
							
							HandleAnswerSubmission(clientId, questionId, answer, timeTaken);
						}
						break;
						
					case "RequestHint":
						SendHint(clientId);
						break;
						
					case "GetCurrentQuestion":
						SendCurrentQuestion(clientId);
						break;
						
					case "JoinQuiz":
						if (root.TryGetProperty("playerName", out JsonElement nameElement))
						{
							string playerName = nameElement.GetString();
							JoinQuiz(clientId, playerName);
						}
						break;
						
					default:
						GD.PrintErr($"?? Request inconnue: {request}");
						SendRequestResponse(clientId, request, null, false, $"Request inconnue: {request}");
						break;
				}
			}
			catch (Exception ex)
			{
				GD.PrintErr($"? Erreur HandleSceneRequest: {ex.Message}");
				SendRequestResponse(clientId, request, null, false, $"Erreur: {ex.Message}");
			}
		}
		
		// ===== Méthodes du Quiz =====
		
		private void StartQuiz()
		{
			_isActive = true;
			_isPaused = false;
			_currentQuestionIndex = 0;
			GD.Print("?? Quiz démarré");
		}
		
		private void PauseQuiz()
		{
			_isPaused = true;
			GD.Print("?? Quiz mis en pause");
		}
		
		private void ResumeQuiz()
		{
			_isPaused = false;
			GD.Print("?? Quiz repris");
		}
		
		private void StopQuiz()
		{
			_isActive = false;
			_isPaused = false;
			GD.Print("?? Quiz arrêté");
		}
		
		private void SkipQuestion()
		{
			if (_currentQuestionIndex < _totalQuestions - 1)
			{
				_currentQuestionIndex++;
				GD.Print($"?? Question sautée, maintenant à {_currentQuestionIndex + 1}/{_totalQuestions}");
			}
		}
		
		private void HandleAnswerSubmission(string clientId, int questionId, string answer, float timeTaken)
		{
			// Vérifier la réponse (logique simplifiée)
			bool isCorrect = answer?.ToLower() == "paris"; // Exemple
			int points = isCorrect ? 100 : 0;
			
			GD.Print($"? Réponse de {clientId}: {answer} ({(isCorrect ? "Correct" : "Incorrect")})");
			
			// Envoyer le résultat
			var response = new
			{
				target = "Scene",
				response = "AnswerResult",
				questionId = questionId,
				isCorrect = isCorrect,
				points = points,
				timeTaken = timeTaken,
				timestamp = DateTime.UtcNow
			};
			
			SendToClient(clientId, response);
		}
		
		private void SendHint(string clientId)
		{
			var hint = new
			{
				target = "Scene",
				response = "Hint",
				hint = "C'est la capitale de la France",
				timestamp = DateTime.UtcNow
			};
			
			SendToClient(clientId, hint);
			GD.Print($"?? Indice envoyé à {clientId}");
		}
		
		private void SendCurrentQuestion(string clientId)
		{
			var question = new
			{
				target = "Scene",
				response = "CurrentQuestion",
				questionId = _currentQuestionIndex,
				question = "Quelle est la capitale de la France ?",
				answers = new[] { "Paris", "Londres", "Berlin", "Madrid" },
				timestamp = DateTime.UtcNow
			};
			
			SendToClient(clientId, question);
			GD.Print($"? Question envoyée à {clientId}");
		}
		
		private void JoinQuiz(string clientId, string playerName)
		{
			var response = new
			{
				target = "Scene",
				response = "QuizJoined",
				playerName = playerName,
				quizTitle = _quizTitle,
				totalQuestions = _totalQuestions,
				timestamp = DateTime.UtcNow
			};
			
			SendToClient(clientId, response);
			GD.Print($"?? {playerName} a rejoint le quiz");
		}
		
		// ===== Méthodes d'Envoi =====
		
		private void SendOrderResponse(string clientId, string order, string message, bool success)
		{
			var response = new
			{
				target = "Scene",
				orderResponse = order,
				success = success,
				message = message,
				timestamp = DateTime.UtcNow
			};
			
			SendToClient(clientId, response);
		}
		
		private void SendRequestResponse(string clientId, string request, object data, bool success, string message)
		{
			var response = new
			{
				target = "Scene",
				requestResponse = request,
				success = success,
				data = data,
				message = message,
				timestamp = DateTime.UtcNow
			};
			
			SendToClient(clientId, response);
		}
		
		private void SendToClient(string clientId, object data)
		{
			// Note: Dans une vraie implémentation, on utiliserait MainGameScene.SendMessageToClient
			// Ici c'est un exemple simplifié
			string json = JsonSerializer.Serialize(data);
			GD.Print($"?? Envoi à {clientId}: {json}");
		}
	}
}
