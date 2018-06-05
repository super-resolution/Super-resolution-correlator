#version 330
in vec4 v_color;
//out vec4 Color;
layout(location = 0) out vec4 Color;



void main()
{
    if (v_color == vec4(0.0)){
        discard;
        }
    //vec2 coord = gl_PointCoord-vec2(0.5);
    //float l = length(coord)*2;
    //if (l > 1.0)
    //    discard;
    //float pos = sqrt(1.0-l*l);
    Color = v_color;//vec4(pos)*v_color;
}