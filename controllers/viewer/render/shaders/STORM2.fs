#version 330
in vec4 v_color;
in float Emission;
in float u_maxEmission;
//out vec4 Color;
layout(location = 0) out vec4 Color;



void main()
{
    if (v_color == vec4(0.0)){
        discard;
        }
    vec2 coord = gl_PointCoord-vec2(0.5);
    float l = length(coord)*2;
    if (l > 1.0)
        discard;
    float pos = sqrt(1.0-l*l);
    float strength = sqrt(Emission/u_maxEmission);
    if (strength>1.0)
        strength = 1.0;
    Color = vec4(pos)*v_color*vec4(vec3(strength), 1.0);
}