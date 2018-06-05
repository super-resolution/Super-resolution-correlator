#version 330
layout (location = 1) in vec2 vPosition;
layout (location = 2) in vec3 simplex;

uniform mat4 u_projection;
uniform mat4 u_modelview;
uniform float size;
uniform float alpha;
//uniform vec4 color;


out vec4 v_color;
const float radius = 200.0;

void main()
{
        v_color = vec4(0.0,0.0,0.0,0.0);
        //if(simplex.x < alpha){//interior
        //    v_color = vec4(1.0,1.0,1.0,0.5);
            if (simplex.y < alpha){
                    v_color = vec4(0.0,1.0,0.0,1.0);
                if (simplex.z > alpha){
                    v_color = vec4(1.0,1.0,1.0,1.0);


                }
            }
        //}


    gl_Position = u_projection * u_modelview * vec4(vPosition.xy, vec2(1.0));
    //gl_PointSize = size * u_projection[1][1] * radius / gl_Position.w;
}