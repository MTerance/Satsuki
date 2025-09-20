using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Godot;
using SQLitePCL;

namespace Satsuki.MiniGames
{
    public partial class BilliardGame : Node3D
    {
        [Export] public Node3D whiteBall;
        [Export] public Node3D[] balls;
        [Export] public Node3D cue;
        [Export] public Camera3D camera;
        [Export] public Node3D[] pockets;

        private bool _isAiming = false;
        private float _force = 0.0f;
        private const float MaxForce = 20.0f;


        private void CheckPocketCollisions()
        {
            foreach (var pocket in pockets)
            {
                foreach(Node child in GetTree().GetNodesInGroup("balls"))
                {
                    if (child is Node3D ball && ball.GlobalPosition.DistanceTo(
                        pocket.GlobalPosition) < 0.1f)
                    {
                        GD.Print($"Ball pocketed : {ball.Name}");
                        ball.QueueFree();
                    }
                }
            }
        }

        public override void _Process(double delta)
        {
            if (_isAiming)
            {
                if (Input.IsActionPressed("UI_accept"))
                {
                    _force += (float)(delta * 10f); // Increase force while aiming
                    _force = Mathf.Clamp(_force, 0.0f, MaxForce); // Cap the force to a maximum value
                    /*
                    if (_force > MaxForce)
                        _force = MaxForce; // Cap the force to a maximum value
                    GD.Print($"Aiming with force: {_force}");
                    */
                }
                else if (Input.IsActionJustReleased("UI_accept"))
                {
                    ShootBall();
                    _isAiming = false;
                    _force = 0.0f; // Reset force after shooting
                }
            }
            CheckPocketCollisions();
        }

        private void ShootBall()
        {
            if (whiteBall != null && cue != null)
            {
                // Calculate the direction from the cue to the white ball
                Vector3 direction = camera.GlobalTransform.Basis.Z.Normalized();

                RigidBody3D ballBody = whiteBall.GetNode<RigidBody3D>("RigidBody3D");
                ballBody.ApplyImpulse(Godot.Vector3.Zero, direction * _force); // Apply impulse to the white ball
                GD.Print($"Shooting with force: {_force}");
            }
            else
            {
                GD.Print("White ball or cue is not set.");
            }
        }

        public override void _Input(InputEvent @event)
        {
            if (@event is InputEventMouseButton mouseButtonEvent)
            {
                if (mouseButtonEvent.ButtonIndex == MouseButton.Left && mouseButtonEvent.Pressed)
                {
                    _isAiming = true;
                    GD.Print("Aiming started");
                }
                else if (mouseButtonEvent.ButtonIndex == MouseButton.Left && !mouseButtonEvent.Pressed)
                {
                    _isAiming = false;
                    GD.Print("Aiming ended");
                }
            }
        }

        private void ShootWhiteBall()
        {
            Vector3 direction = (camera.GlobalTransform.Basis.Z * -1).Normalized();
            RigidBody3D ballBody = whiteBall.GetNode<RigidBody3D>("RigidBody3D");
            ballBody.ApplyImpulse(Vector3.Zero, direction * _force); // Adjust the force as needed
        }

        public override void _Ready()
        {
            if (!whiteBall.HasNode("RigidBody3D"))
            {
                RigidBody3D ballBody = new RigidBody3D();
                whiteBall.AddChild(ballBody);
                ballBody.GlobalTransform = whiteBall.GlobalTransform; // Set the initial position and rotation
            }
            else
            {
                GD.PrintErr("White ball does not have a RigidBody3D node.");
            }
        }
    }
}
