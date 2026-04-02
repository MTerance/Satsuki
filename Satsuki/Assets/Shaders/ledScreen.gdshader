shader_type canvas_item;

// Résolution de la texture / viewport (en pixels)
uniform vec2 screen_resolution : hint_range(1.0, 8192.0) = vec2(1920.0,1080.0);

// Espacement entre centres de LEDs (en px)
uniform float led_pitch : hint_range(1.0,256.0) = 12.0;

// Rayon du point LED (en px)
uniform float led_radius : hint_range(0.5,128.0) = 4.0;

// Halo / glow autour de chaque LED
uniform float glow = 1.2;
uniform float glow_size : hint_range(0.0,128.0) = 10.0;

// Contraste / luminosité / gamma
uniform float brightness : hint_range(0.0,4.0) = 1.0;
uniform float contrast : hint_range(0.0,4.0) = 1.0;
uniform float gamma_correction : hint_range(0.1,3.0) = 1.0;

// Sous‑pixel RGB (optionnel)
uniform bool use_subpixel = false;
uniform float subpixel_offset_factor : hint_range(0.0,1.0) = 0.25;

// Scanlines et bruit
uniform float scanline_intensity : hint_range(0.0,1.0) = 0.06;
uniform float noise_strength : hint_range(0.0,0.2) = 0.02;

// Vignette subtile
uniform float vignette : hint_range(0.0,1.0) = 0.25;

// utilitaire simple pour bruit
float rand(vec2 co) {
	return fract(sin(dot(co, vec2(12.9898,78.233))) * 43758.5453);
}

vec3 apply_contrast_brightness(vec3 c, float cont, float bright) {
	c = (c - 0.5) * cont + 0.5;
	c *= bright;
	return clamp(c, 0.0, 1.0);
}

void fragment() {
	vec2 uv = UV;
	// coordonnées en pixels sur la texture
	vec2 fragPx = uv * max(screen_resolution, vec2(1.0));

	// centre de la cellule LED courante
	vec2 grid = fragPx / led_pitch;
	vec2 cell = floor(grid);
	vec2 centerPx = (cell + vec2(0.5)) * led_pitch;
	vec2 centerUV = centerPx / screen_resolution;

	// échantillonnage couleur (option sous-pixel)
	vec3 texColor;
	if (use_subpixel) {
		float off = (led_pitch * subpixel_offset_factor) / screen_resolution.x;
		float r = texture(TEXTURE, centerUV - vec2(off, 0.0)).r;
		float g = texture(TEXTURE, centerUV).g;
		float b = texture(TEXTURE, centerUV + vec2(off, 0.0)).b;
		texColor = vec3(r, g, b);
	} else {
		texColor = texture(TEXTURE, centerUV).rgb;
	}

	// distance (en px) du fragment au centre LED
	float dist = length(fragPx - centerPx);

	// coeur LED (disk)
	float core = 1.0 - smoothstep(led_radius * 0.85, led_radius, dist);

	// halo / glow (gaussian-like)
	float sigma = max(1.0, glow_size);
	float glowFactor = glow * exp(- (dist * dist) / (2.0 * sigma * sigma));

	// combinaison couleur
	vec3 color = texColor * (core + glowFactor);

	// scanlines subtiles
	float yFactor = fragPx.y / (led_pitch);
	float scan = 1.0 - scanline_intensity * (0.5 + 0.5 * sin(yFactor * 3.14159));
	color *= scan;

	// bruit par cellule
	float n = rand(cell + floor(TIME * 2.0));
	color += (n - 0.5) * noise_strength;

	// vignette
	vec2 center = vec2(0.5, 0.5);
	float d = distance(uv, center);
	color *= mix(1.0, 1.0 - vignette, smoothstep(0.0, 0.8, d));

	// contraste / luminosité / gamma
	color = apply_contrast_brightness(color, contrast, brightness);
	color = pow(max(color, vec3(0.0)), vec3(1.0 / max(0.0001, gamma_correction)));

	COLOR = vec4(color, 1.0);
}