#version 330
layout (location = 1) in vec4 vPosition;
layout (location = 2) in float cluster;

uniform mat4 u_projection;
uniform mat4 u_modelview;
uniform float size;
uniform float maxEmission;
uniform vec4 bg_color;


out vec4 v_color;
out float Emission;
out float u_maxEmission;
const float radius = 200.0;

void main()
{
        float x = mod(cluster, 6.0);
        if(cluster < 0.1){
            v_color = bg_color;
                }
        else if (cluster > 0.1){
            v_color = vec4(1.0);
        }
        //else if (x < 2.0){
        //    v_color = vec4(1.0,1.0,1.0,1.0);
        //    }
        //else if (x < 4.0){
        //    v_color = vec4(1.0,0.0,1.0,1.0);
        //    }
        //else{
        //    v_color = vec4(0.0,1.0,0.0,1.0);
        //    }

    gl_Position = u_projection * u_modelview * vec4(vPosition.xyz, 1.0);
    Emission = vPosition.w;
    u_maxEmission = maxEmission;
    gl_PointSize = size * u_projection[1][1] * radius / gl_Position.w;
}