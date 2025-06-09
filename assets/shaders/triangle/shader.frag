#version 330 core

in vec2 textureCoords;

uniform sampler2D texture0;
uniform vec3 lColor;

out vec4 FragColor;

void main()
{
    FragColor = texture(texture0, textureCoords) * vec4(lColor, 1.0);
}
