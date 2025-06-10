#version 330 core

in vec2 textureCoords;
in vec3 normal;
in vec3 fragmentPosition;
in vec3 lightInViewPosition;

uniform sampler2D texture0;
uniform vec3 lightColor;
uniform vec3 cameraPosition;

out vec4 FragColor;

void main()
{
    float ambientLightstrength = 0.5;
    vec3 ambientLightColor = vec3(1.0);
    vec3 ambientLight = ambientLightColor * ambientLightstrength;

    vec3 lightDirection = normalize(lightInViewPosition - fragmentPosition);
    float angle = max(dot(normal, lightDirection), 0.0);
    vec3 diffuseLight = angle * lightColor;

    float specularStrength = 0.8;
    vec3 viewDirection = normalize(-fragmentPosition);
    vec3 reflectedLightDirection = reflect(-lightDirection, normal);
    float specular = pow(max(dot(viewDirection, reflectedLightDirection), 0.0), 32);
    vec3 specularLight = specularStrength * specular * lightColor;

    vec3 finalLightColor = ambientLight + diffuseLight + specularLight;

    FragColor = texture(texture0, textureCoords) * vec4(finalLightColor, 1.0);
}
