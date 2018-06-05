#version 330
in vec4 v_color;
in float Emission;
in float u_maxEmission;
in float z_Position;
//out vec4 Color;
layout(location = 0) out vec4 Color;



void main()
{


    if (v_color == vec4(0.0)){
        discard;
        }

    float z = z_Position/300 ;
    vec4 red = vec4(1.0,0.0,0.0,1.0);
    vec4 green = vec4(0.0,1.0,0.0,1.0);
    vec4 blue = vec4(0.0,0.0,1.0,1.0);
    vec4 col = vec4(0.0);
    if (z<0){
        col = mix(red,green,z+1.0);
    }
    else{
        col = mix(green,blue,z);
    }
    vec2 coord = gl_PointCoord-vec2(0.5);
    float l = length(coord)*2;
    if (l > 1.0)
        discard;
    float pos = sqrt(1.0-l*l);
    float strength = sqrt(Emission/u_maxEmission);
    if (strength>1.0)
        strength = 1.0;
    Color = vec4(pos)*col*vec4(vec3(strength), 1.0);
}