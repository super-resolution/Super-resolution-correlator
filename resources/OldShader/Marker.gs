#version 410
layout (points) in;
layout (triangle_strip, max_vertices = 4) out;

uniform mat4 u_projection;
uniform mat4 u_modelview;
uniform float u_size;
uniform float u_linewidth;


void line(in vec4 pos, in float length, in float linewidth, in int orientation, in float offset)
{
    float x1;
    float x2;
    float y1;
    float y2;
    if(orientation == 0)
        {
        x1 = length;
        x2 = -length;
        y1 = linewidth + offset;
        y2 = -linewidth + offset;
        }
    else
        {
        y1 = length;
        y2 = -length;
        x1 = linewidth + offset;
        x2 = -linewidth + offset;
        }

    gl_Position = u_projection * (pos + vec4(x1, y1, 0.0, 0.0));
    EmitVertex();

    gl_Position = u_projection * (pos + vec4(x1, y2, 0.0, 0.0));
    EmitVertex();

    gl_Position = u_projection * (pos + vec4(x2, y1, 0.0, 0.0));
    EmitVertex();

    gl_Position = u_projection * (pos + vec4(x2, y2, 0.0, 0.0));
    EmitVertex();



    EndPrimitive();


}
void main ()
{
    vec4 pos = vec4(gl_in[0].gl_Position.xyz, 1.0);

    line(pos, u_size, u_linewidth, 0, 0.0);
    line(pos, u_size, u_linewidth, 1, 0.0);
}