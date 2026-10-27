
shader_type spatial;
render_mode unshaded, cull_disabled;

uniform sampler2D cinema_frame : source_color, filter_linear, repeat_disable;

varying vec2 screen_uv;

void vertex() {
    // Coordonnées mesurées sur Object_5
    float min_x = -8.890924;
    float max_x =  8.890924;
    float min_y =  1.805107;
    float max_y =  9.237907;

    // Projection horizontale complète de 0 à 1
    screen_uv.x = (VERTEX.x - min_x) / (max_x - min_x);

    // Origine verticale en haut de l'écran
    screen_uv.y = (max_y - VERTEX.y) / (max_y - min_y);

    screen_uv = clamp(screen_uv, vec2(0.0), vec2(1.0));
}

void fragment() {
    vec3 screen_color = texture(cinema_frame, screen_uv).rgb;

    ALBEDO = screen_color;
}