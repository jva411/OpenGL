#version 330 core

uniform vec3 lColor;

out vec4 FragColor;

void main() {
    FragColor = vec4(lColor, 1.0);
}
