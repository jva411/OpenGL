#version 330 core

uniform vec3 codeColor;

out vec4 FragColor;

void main() {
    FragColor = vec4(codeColor, 1.0);
}
