#version 330 core

struct Material {
    sampler2D diffuse;
    sampler2D specular;
    float shininess;
};

struct Light {
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

in vec2 textureCoords;
in vec3 normal;
in vec3 fragmentPosition;
in vec3 lightInViewPosition;

uniform Material material;
uniform Light light;

out vec4 FragColor;

void main()
{
    vec3 diffuseMapped = vec3(texture(material.diffuse, textureCoords));

    vec3 ambientLight = light.ambient * diffuseMapped;

    vec3 lightDirection = normalize(lightInViewPosition - fragmentPosition);
    float diffuse = max(dot(normal, lightDirection), 0.0);
    vec3 diffuseLight = light.diffuse * diffuse * diffuseMapped;

    vec3 viewDirection = normalize(-fragmentPosition);
    vec3 reflectedLightDirection = reflect(-lightDirection, normal);
    float specular = pow(max(dot(viewDirection, reflectedLightDirection), 0.0), material.shininess);
    vec3 specularLight = light.specular * specular * vec3(texture(material.specular, textureCoords));

    vec3 finalLightColor = ambientLight + diffuseLight + specularLight;
    FragColor = vec4(finalLightColor, 1.0);
}
