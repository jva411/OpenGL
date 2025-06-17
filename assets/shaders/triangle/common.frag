#version 330 core

#define MAX_LIGHTS 16

struct Material {
    vec3 diffuse;
    vec3 specular;
    float shininess;
};

struct PointLight {
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

in vec3 normal;
in vec3 fragmentPosition;

uniform Material material;
uniform PointLight[MAX_LIGHTS] lights;
uniform int n_lights;
uniform vec3 cameraPosition;

out vec4 FragColor;

vec3 CalcPointLight(PointLight light, vec3 cameraDirection);

void main()
{
    vec3 cameraDirection = normalize(cameraPosition - fragmentPosition);

    vec3 finalColor = vec3(0.0, 0.0, 0.0);
    for (int i=0; i<n_lights; i++) {
        finalColor += CalcPointLight(lights[i], cameraDirection);
    }

    FragColor = vec4(finalColor, 1.0);
}


vec3 CalcPointLight(PointLight light, vec3 cameraDirection) {
    vec3 ambientLight = light.ambient * material.diffuse;

    vec3 lightDirection = normalize(light.position - fragmentPosition);
    float diffuse = max(dot(normal, lightDirection), 0.0);
    vec3 diffuseLight = light.diffuse * diffuse * material.diffuse;

    vec3 reflectedLightDirection = reflect(-lightDirection, normal);
    float specular = pow(max(dot(cameraDirection, reflectedLightDirection), 0.0), material.shininess);
    vec3 specularLight = light.specular * specular * material.specular;

    return (ambientLight + diffuseLight + specularLight);
}
