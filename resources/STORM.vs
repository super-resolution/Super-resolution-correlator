#version 330
layout (location = 1) in vec3 vPosition;
// Uniforms
// ------------------------------------
uniform float u_linewidth;
uniform float u_antialias;
uniform mat4 u_projection;
uniform mat4 u_modelview;
uniform vec4  fg_color;
uniform vec4  bg_color;
uniform float size;
// Varyings
// ------------------------------------
out vec4 v_fg_color;
out vec4 v_bg_color;
out float v_size;
out float v_linewidth;
out float v_antialias;

const float radius = 250.0;
void main (void) {
    v_size = size;
    v_linewidth = u_linewidth;
    v_antialias = u_antialias;
    v_fg_color  = fg_color;
    v_bg_color  = bg_color;
    gl_Position = u_projection*u_modelview*vec4(vPosition, 1.0);
    gl_PointSize = (size+ 2*(v_linewidth + 1.5*v_antialias))*u_projection[1][1] * radius / gl_Position.w;
}