#version 330
layout (location = 0) in vec4 pos;
uniform mat4 u_projection;
uniform mat4 u_modelview;
out vec3 vPosition;

void main()
{
    gl_Position = pos;
    vPosition = pos.xyz;
}
