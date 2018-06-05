#version 330 core
in vec2 TexCoord;

layout(location = 0) out vec4 color;

uniform sampler2D SIM0;
uniform sampler2D SIM1;
uniform sampler2D SIM2;
uniform sampler2D SIM3;
uniform vec4 SIMColor0;
uniform vec4 SIMColor1;
uniform vec4 SIMColor2;
uniform vec4 SIMColor3;

void main()
{   vec4 tex1 = texture(SIM0, TexCoord).r * SIMColor0;
    vec4 tex2 = texture(SIM1, TexCoord).r * SIMColor1;
    vec4 tex3 = texture(SIM2, TexCoord).r * SIMColor2;
    vec4 tex4 = texture(SIM3, TexCoord).r * SIMColor3;
    color = tex1 + tex2 + tex3 + tex4;
}