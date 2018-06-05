#version 410
layout (location = 1) in vec3 center;
//uniform vec4 bg_color;
uniform mat4 u_projection;
uniform mat4 u_modelview;
uniform float u_size;
uniform float u_linewidth;


//out vec4 v_color;

void main()
{
    //v_color = bg_color;
    gl_Position =  u_modelview * vec4(center, 1.0);

    //gl_PointSize = size * u_projection[1][1] / gl_Position.w;
}