#version 330
layout (location = 0) in vec4 pos;
uniform mat4 u_projection;
uniform mat4 u_modelview;
uniform bool u_UD;
uniform bool u_LR;


out vec2 vPosition;

void main()
{
    gl_Position = pos;
    vec2 tex = 0.5 * (pos.xy + 1.0);
    if (u_UD){
        tex = vec2(tex.s, 1.0 - tex.t);
        }
    if (u_LR){
        tex = vec2(1 - tex.s, tex.t);
        }
    vPosition = tex;
}
