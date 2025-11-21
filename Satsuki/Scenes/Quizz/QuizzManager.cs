using Godot;
using Satsuki.Interfaces.Quizz;
using System;
using System.Collections.Generic;

public partial class QuizzManager : Node
{
	private List<IQuizz> listQuizz {get;set;}

	private List<IQuizz>.Enumerator currentQuizz {get;set;}
	
	
	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
		// 
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}
}
