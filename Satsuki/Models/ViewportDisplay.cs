using Godot;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Satsuki.Models
{
	public partial class ViewportDisplay : MeshInstance3D
	{
		// Assign this in the Inspector: the SubViewport node containing your 3D scene
		[Export]
		public SubViewport CameraViewport;

		public override void _Ready()
		{
			if (CameraViewport == null)
			{
				GD.PrintErr("No SubViewport assigned in Inspector.");
				return;
			}

			// Get the first surface material override or create one
			Material baseMaterial = GetSurfaceOverrideMaterial(0) ?? new StandardMaterial3D();

			// Ensure it is a ShaderMaterial to use uniforms
			if (baseMaterial is not ShaderMaterial shaderMat)
			{
				shaderMat = new ShaderMaterial();
				shaderMat.Shader = GD.Load<Shader>("res://Assets/Img/LobbyScreen/Shaders/ViewPortDisplay.gdshader"); // Path to your shader
			}

			// Pass the viewport texture to the shader
			// get_texture() retrieves the ViewportTexture directly
			shaderMat.SetShaderParameter("screen_texture", CameraViewport.GetTexture());

			// Apply the material to the mesh surface
			SetSurfaceOverrideMaterial(0, shaderMat);
		}
	}
}
