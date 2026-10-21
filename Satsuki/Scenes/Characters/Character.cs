using Godot;
using System;


public enum CharacterAnimation
{
	Idle,
	Walk,
	Sit
}


public partial class Character : Node3D
{
	// Called when the node enters the scene tree for the first time.
	public override void _Ready()
	{
	}

	public void SetAnimation(CharacterAnimation animation)
	{
		var animationPlayer = GetNodeOrNull<AnimationPlayer>("Y Bot/Animation");
		if (animationPlayer == null)
		{
			GD.PrintErr("AnimationPlayer not found!");
			return;
		}
		switch (animation)
		{
			case CharacterAnimation.Idle:
				animationPlayer.Play("Idle/mixamo_com");
				break;
			case CharacterAnimation.Walk:
				animationPlayer.Play("Walking/mixamo_com");
				break;
			case CharacterAnimation.Sit:
				animationPlayer.Play("Sitting Idle/mixamo_com");
				break;
			default:
				throw new ArgumentOutOfRangeException(nameof(animation), animation, null);
		}
	}

	// Called every frame. 'delta' is the elapsed time since the previous frame.
	public override void _Process(double delta)
	{
	}
}
