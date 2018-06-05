#version 330

in vec2 vPosition;
layout(location = 0) out vec4 color;

uniform sampler2D u_RayStart;
uniform sampler2D u_RayStop;
uniform sampler3D u_Volume0;
uniform sampler3D u_Volume1;
uniform sampler3D u_Volume2;
uniform sampler3D u_Volume3;
uniform vec4 u_Color0;
uniform vec4 u_Color1;
uniform vec4 u_Color2;
uniform vec4 u_Color3;



uniform float StepLength = 0.01;

void main()
{
    vec2 coord = vPosition;
    //vec2 coord = 0.5 * (vPosition + 1.0);
    vec3 rayStart = texture(u_RayStart, coord).xyz;
    vec3 rayStop = texture(u_RayStop, coord).xyz;

    if (rayStart == rayStop) {
        discard;
        return;
    }

    vec3 ray = rayStop - rayStart;
    float rayLength= length(ray);
    vec3 stepVector = StepLength * ray / rayLength;
    vec4 dst[4];
    vec3 pos;
    for (int i=0;i<3;++i){

        rayLength = length(ray);
        pos = rayStart;
        dst[i] = vec4(0.0);

        while (dst[i].a < 1 && rayLength > 0) {
            vec3 V = vec3(0.0);
            if (i==0) {
                V = texture(u_Volume0, pos).xyz;
              }
            if (i==1) {
                V = texture(u_Volume1, pos).xyz;
            }
            if (i==2) {
                V = texture(u_Volume2, pos).xyz;
            }
            if (i==3) {
                V = texture(u_Volume3, pos).xyz;
            }
            //vec3 V = texture(Volume0, pos).xyz;
            vec4 src = vec4(0.5 * (V + 1.0), dot(V, V));
            src.rgb *= src.a;
            dst[i] = (1.0 - dst[i].a) * src + dst[i];
            if (dst[i].r <0.05){
               dst[i] = vec4(0.0);
            }
            pos += stepVector;
            rayLength -= StepLength;
        }
    }

    color = vec4(u_Color0.rgb*dst[0].r, dst[0].a)+vec4(u_Color1.rgb*dst[1].r, dst[1].a)+vec4(u_Color2.rgb*dst[2].r, dst[2].a)+vec4(u_Color3.rgb*dst[3].r, dst[3].a) ;
    if (color.a>1.0){
        color.a = 1.0;
    }
}