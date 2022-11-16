vertex_shader_tiempo_ejemplo = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;
uniform vec3 pointLight; 

out vec3 outColor;
out vec2 outTexCoords;

void main()
{

    vec4 norm = vec4(normal, 0.0);
    vec4 pos = modelMatrix * vec4 (position.x, position.y, position.z + sin(tiempo * position.x), 1.0);
    vec4 light = vec4(pointLight, 1.0);

    float intensity = dot(modelMatrix * norm, normalize(light - pos));

    gl_Position = projectionMatrix * viewMatrix * pos;
    outColor = vec3(1.0, 1.0, 1.0);
    outTexCoords = texCoords;
}

"""

vertex_shader_luz_ejemplo = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;
uniform vec3 pointLight; 

out vec3 outColor;
out vec2 outTexCoords;

void main()
{

    vec4 norm = vec4(normal, 0.0);
    vec4 pos = modelMatrix * vec4 (position, 1.0);
    vec4 light = vec4(pointLight, 1.0);

    float intensity = dot(modelMatrix * norm, normalize(light - pos));

    gl_Position = projectionMatrix * viewMatrix * pos;
    outColor = vec3(1.0, 1.0, 1.0) * intensity;
    outTexCoords = texCoords;
}

"""

vertex_shader_ejemplo_desimflar = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;
uniform vec3 pointLight; 

out vec3 outColor;
out vec2 outTexCoords;

void main()
{

    vec4 norm = vec4(normal, 0.0);

    vec4 pos = vec4(position, 1.0) + norm * sin(tiempo) / 10;
    pos = modelMatrix * pos;

    vec4 light = vec4(pointLight, 1.0);

    float intensity = dot(modelMatrix * norm, normalize(light - pos));

    gl_Position = projectionMatrix * viewMatrix * pos;
    outColor = vec3(1.0, 1.0, 1.0);
    outTexCoords = texCoords;
}

"""

vertex_shader_ejemplo_desimflar_input = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;
uniform float valor;
uniform vec3 pointLight; 

out vec3 outColor;
out vec2 outTexCoords;

void main()
{

    vec4 norm = vec4(normal, 0.0);

    vec4 pos = vec4(position, 1.0) + norm * valor;
    pos = modelMatrix * pos;

    vec4 light = vec4(pointLight, 1.0);

    float intensity = dot(modelMatrix * norm, normalize(light - pos));

    gl_Position = projectionMatrix * viewMatrix * pos;
    outColor = vec3(1.0, 1.0 - valor, 1.0 - valor);
    outTexCoords = texCoords;
}

"""

test_vertex_shader_ejemplo_desimflar_input = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

out vec2 outTexCoords;

void main()
{

    vec4 norm = vec4(normal, 0.0);

    vec4 pos = vec4(position, 1.0);
    pos = modelMatrix * pos;

    gl_Position = projectionMatrix * viewMatrix * pos;
    outTexCoords = texCoords;
}

"""

test_fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

in vec2 outTexCoords;

uniform sampler2D tex1;
uniform sampler2D tex2;

void main()
{
    fragColor = texture(tex1, outTexCoords) - texture(tex2, outTexCoords);
}
"""