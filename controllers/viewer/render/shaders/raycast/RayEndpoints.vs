#version 330 core
layout (location = 0) in vec3 Position;
out vec3 vPosition;
uniform mat4 u_projection;
uniform mat4 u_modelview;

void main()
{
    gl_Position = u_projection * u_modelview * vec4(Position,1.0);
    vPosition = Position.xyz;
}