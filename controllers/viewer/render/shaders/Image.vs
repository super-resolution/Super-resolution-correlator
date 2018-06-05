#version 330 core
layout (location = 1) in vec3 position;
layout (location = 2) in vec2 texCoord;
uniform mat4 u_projection;
uniform mat4 u_modelview;
uniform bool u_UD;
uniform bool u_LR;

out vec2 TexCoord;

void main()
{
    gl_Position = u_projection * u_modelview *  vec4(position, 1.0);
    vec2 tex = texCoord;
    if (u_UD){
    tex = vec2(tex.s, 1.0 - tex.t);
       }
    if (u_LR){
    tex = vec2(1 - tex.s, tex.t);
    }
    TexCoord = tex;
}