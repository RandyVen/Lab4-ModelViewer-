vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;
uniform vec3 pointLight; 
uniform int activeEffect;

out vec3 outColor;
out vec2 outTexCoords;
out float glowAmount;
out float effect;

void main()
{
    if (activeEffect == 1){
        effect = 1.0;
    }else {
        effect = 0.0;
    }
    vec4 norm = vec4(normal, 0.0);
    vec4 pos = modelMatrix * vec4 (position, 1.0);
    vec4 light = vec4(pointLight, 1.0);

    float intensity = dot(modelMatrix * norm, normalize(light - pos));
    //float intensityGlowAmount = dot(norm, modelMatrix);
    glowAmount = 1 - intensity;

    gl_Position = projectionMatrix * viewMatrix * pos;
    outColor = vec3(1.0, 1.0, 1.0);
    outTexCoords = texCoords;
}

"""

toon_vertex_shaders = """
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
    //intensity = intensity > 0.95 ? 1 : (intensity > 0.7 ? 0.8 : (intensity > 0.4 ? 0.6 : (intensity > 0.2 ? 0.4 : 0.3)));
    //intensity = intensity > 0.85 ? 1 : (intensity > 0.6 ? 0.8 : (intensity > 0.45 ? 0.55 : (intensity > 0.3 ? 0.4 : 0.25)));
    //intensity = intensity > 0.95 ? 1 : (intensity > 0.75 ? 0.8 : (intensity > 0.5 ? 0.6 : (intensity > 0.25 ? 0.4 : 0.2)));
    intensity = intensity > 0.95 ? 1 : (intensity > 0.5 ? 0.6 : (intensity > 0.25 ? 0.4 : 0.2));
    //intensity = intensity > 0.95 ? 1 : (intensity > 0.7 ? 0.7 : (intensity > 0.4 ? 0.4 : (intensity > 0.1 ? 0.1 : 0.05)));
    //intensity = intensity > 0.95 ? 0.05 : (intensity > 0.7 ? 0.4 : (intensity > 0.4 ? 0.7 : (intensity > 0.1 ? 1 : 0.05)));

    gl_Position = projectionMatrix * viewMatrix * pos;
    outColor = vec3(1.0, 1.0, 1.0) * intensity;
    outTexCoords = texCoords;
}
"""
dizziness_vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 normal;
layout (location = 2) in vec2 texCoords;

uniform mat4 modelMatrix;
uniform mat4 viewMatrix;
uniform mat4 projectionMatrix;

uniform float tiempo;
uniform vec3 pointLight; 
uniform float valor;
uniform int activeEffect;

out vec3 outColor;
out vec2 outTexCoords;

void main()
{
    vec4 pos = vec4(position, 1.0);
    vec4 norm = vec4(normal, 0.0);
    if(activeEffect == 1){
        pos = pos + norm * sin(tiempo) / valor;
        outColor = vec3(1.0-tiempo, 1.0, 1.0-tiempo);
    }else if(activeEffect == 2){
        pos = pos + norm * log(tiempo) / 5;
        outColor = vec3(1.0, 1.0-tiempo, 1.0-tiempo);
    }else{
        pos = modelMatrix * pos;
        outColor = vec3(1.0);
    }
    vec4 light = vec4(pointLight, 1.0);

    float intensity = dot(modelMatrix * norm, normalize(light - pos));

    gl_Position = projectionMatrix * viewMatrix * pos;
    outTexCoords = texCoords;
}
"""

fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

in vec3 outColor; 
in vec2 outTexCoords;

uniform sampler2D tex;

void main()
{
    fragColor = vec4(outColor,1) * texture(tex, outTexCoords);
}
"""

toon_fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

in vec3 outColor; 
in vec2 outTexCoords;

uniform sampler2D tex;

void main()
{
    fragColor = vec4(1-outColor.x, 1-outColor.y, 1-outColor.z,1) * texture(tex, outTexCoords);
}
"""

neg_fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

in vec3 outColor; 
in vec2 outTexCoords;
in float effect;

uniform sampler2D tex;

void main()
{
    vec4 neg = vec4(1.0, 1.0, 1.0, 1.0);
    fragColor = texture(tex, outTexCoords);
    if(effect == 1){
        fragColor = neg - texture(tex, outTexCoords);
    }
}
"""

wft_fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

in vec3 outColor; 
in vec2 outTexCoords;

uniform int activeEffect;
uniform sampler2D tex;

void main()
{
    vec4 neg = vec4(1.0, 1.0, 1.0, 1.0);
    if(activeEffect == 1){
        fragColor = neg - texture(tex, outTexCoords);
    }else{
        texture(tex, outTexCoords);
    }
}
"""

glow_fragment_shader = """
#version 460
layout (location = 0) out vec4 fragColor;

in vec3 outColor; 
in vec2 outTexCoords;
in float glowAmount;

uniform sampler2D tex;

void main()
{
    
    vec4 glowColor = vec4(0.0 * glowAmount, 1.0 * glowAmount, 0.0 * glowAmount, 1.0);
    fragColor = glowColor + texture(tex, outTexCoords);
}
"""