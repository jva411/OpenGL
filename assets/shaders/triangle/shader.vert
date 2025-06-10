#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aNormal;
layout (location = 2) in vec2 aTextureCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform vec3 lightPosition;

out vec2 textureCoords;
out vec3 normal;
out vec3 fragmentPosition;
out vec3 lightInViewPosition;

void main()
{
    vec4 worldPos = model * vec4(aPos, 1.0);
    gl_Position = projection * view * worldPos;
    fragmentPosition = vec3(view * worldPos);
    textureCoords = aTextureCoords;
    normal = mat3(transpose(inverse(view * model))) * aNormal;
    lightInViewPosition = vec3(view * vec4(lightPosition, 1.0));
}
