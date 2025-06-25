#version 330 core

#define MAX_LIGHTS 16
#define SPECULAR_FUNCTION CalcBlinnPhongSpecular

struct Material {
    sampler2D diffuse;
    sampler2D specular;
    float shininess;
};

struct PointLight {
    vec3 position;

    vec3 ambient;
    vec3 diffuse;
    vec3 specular;
};

in vec2 textureCoords;
in vec3 normal;
in vec3 fragmentPosition;

uniform Material material;
uniform PointLight[MAX_LIGHTS] lights;
uniform int n_lights;
uniform vec3 cameraPosition;

out vec4 FragColor;

vec3 CalcPointLight(PointLight light, vec3 cameraDirection);
float CalcPhongSpecular(vec3 lightDirection, vec3 cameraDirection);
float CalcBlinnPhongSpecular(vec3 lightDirection, vec3 cameraDirection);

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
    vec3 diffuseMapped = vec3(texture(material.diffuse, textureCoords));

    vec3 ambientLight = light.ambient * diffuseMapped;

    vec3 lightDirection = normalize(light.position - fragmentPosition);
    float diffuse = max(dot(normal, lightDirection), 0.0);
    vec3 diffuseLight = light.diffuse * diffuse * diffuseMapped;

    vec3 specularLight = vec3(0.0, 0.0, 0.0);
    if (diffuse > 0.0) {
        float specular = SPECULAR_FUNCTION(lightDirection, cameraDirection);
        specularLight = light.specular * specular * vec3(texture(material.specular, textureCoords));
    }

    return (ambientLight + diffuseLight + specularLight);
}


float CalcPhongSpecular(vec3 lightDirection, vec3 cameraDirection) {
    vec3 reflectedLightDirection = reflect(-lightDirection, normal);
    float specular = pow(max(dot(cameraDirection, reflectedLightDirection), 0.0), material.shininess);
    return specular;
}

float CalcBlinnPhongSpecular(vec3 lightDirection, vec3 cameraDirection) {
    vec3 halfwayDirection = normalize(lightDirection + cameraDirection);
    float specular = pow(max(dot(normal, halfwayDirection), 0.0), material.shininess * 4.0);
    return specular;
}
