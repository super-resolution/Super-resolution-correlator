#version 330
in vec3 TexCoord;
//in float v_sliceposition;
out vec4 color;

uniform sampler3D SIM0;
uniform sampler2D SIM1;
uniform sampler2D SIM2;
uniform sampler2D SIM3;
uniform vec4 SIMColor0;
uniform vec4 SIMColor1;
uniform vec4 SIMColor2;
uniform vec4 SIMColor3;



void main()
{
    vec4 tex1 = texture(SIM0, TexCoord).r * SIMColor0;
    //vec4 tex2 = texture(SIM0, vec3(TexCoord, v_sliceposition+1.0)).r * SIMColor0;

    color = vec4(tex1);
}

