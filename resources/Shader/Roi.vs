#version 330 core
layout (location = 1) in vec2 position;
uniform mat4 u_projection;
uniform mat4 u_modelview;
//uniform float u_size;
uniform vec4 u_color;

out vec4 v_color;

void main()
{
    gl_Position = u_projection * u_modelview *  vec4(position, 0.0, 1.0);
    v_color = u_color;
}