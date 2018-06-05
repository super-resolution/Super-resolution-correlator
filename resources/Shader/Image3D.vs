#version 330
layout (location = 1) in vec3 position;
layout (location = 2) in vec3 texCoord;

//uniform float u_sliceposition;
uniform mat4 u_projection;
uniform mat4 u_modelview;
uniform bool u_UD;
uniform bool u_LR;

out vec3 TexCoord;
//out float v_sliceposition;

void main()
{


    vec3 pos = vec3(position.xy, position.z);

    gl_Position = u_projection * u_modelview *  vec4(pos, 1.0);
    //float v_sliceposition = position.z/12.0;
    vec3 tex = texCoord;

    TexCoord = tex;
}