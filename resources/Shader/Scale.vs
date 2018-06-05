#version 330
layout (location = 1) in vec3 vPosition;

uniform mat4 u_projection;
uniform mat4 u_modelview;
uniform vec4 color;


out vec4 v_color;

void main()
{
    v_color = color;
    gl_Position = u_projection * u_modelview * vec4(vPosition, 1.0);
    gl_PointSize = 10000;
}