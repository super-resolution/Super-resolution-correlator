#version 330 core
in vec3 vPosition;
layout(location = 0) out vec3 FragData[2];
//out vec4 color;

void main()
{
    vec3 pos = vPosition;
    if (gl_FrontFacing) {
        FragData[0] = 0.5 * (pos + 1.0);
        FragData[1] = vec3(0.0);
    } else {
        FragData[0] = vec3(0.0);
        FragData[1] = 0.5 * (pos + 1.0);
    }
}