import pygame
import numpy as np
import glm
from pygame import key
from pygame.locals import *
import shaders
from gl import Renderer, Model

width = 940
height = 540

deltaTime = 0.0

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)

clock = pygame.time.Clock()

rend = Renderer(screen)
rend.setShaders(shaders.vertex_shader, shaders.fragment_shader)
activeShader = 1

index = 0

face = [Model('Ivy.obj', 'Grama.bmp', 'model_normal.bmp'),
        Model('Mew.obj', 'metalGOD.bmp', 'model_normal.bmp'),
        Model('Groudon.obj', 'lava.bmp', 'model_normal.bmp'),
        ]

radius =  ((rend.camPosition.x - face[index].position.x) ** 2 + (rend.camPosition.y - face[index].position.y) ** 2 + (rend.camPosition.z - face[index].position.z) ** 2)**0.5
angle = 0
xtemp = rend.camPosition.x
ytemp = rend.camPosition.y
ztemp = rend.camPosition.z
angleTemp = 0
def circularMov(angle):
    if angle == 0:
        angle = angleTemp
    x = glm.sin(angle) * radius
    z = glm.cos(angle) * radius
    rend.viewMatix = glm.lookAt(glm.vec3(x, ytemp, z), face[index].position, glm.vec3(0.0, 1.0, 0.0))
    return x, z, angle

rend.scene = face[index]
sickTime = 0
angryTime = 0
isRunning = True
while isRunning:

    keys = pygame.key.get_pressed()
    isPressed = False

    # Traslacion de camara

    if keys[K_g]:
        radius += 10 * deltaTime
        xtemp, ztemp, angleTemp = circularMov(0)
    if keys[K_s]:
        ytemp -= 1 * deltaTime
        xtemp = glm.sin(angleTemp) * radius
        ztemp = glm.cos(angleTemp) * radius
        rend.viewMatix = glm.lookAt(glm.vec3(xtemp, ytemp, ztemp), face[index].position, glm.vec3(0.0, 1.0, 0.0))
    if keys[K_w]:
        ytemp += 1 * deltaTime 
        xtemp = glm.sin(angleTemp) * radius
        ztemp = glm.cos(angleTemp) * radius
        rend.viewMatix = glm.lookAt(glm.vec3(xtemp, ytemp, ztemp), face[index].position, glm.vec3(0.0, 1.0, 0.0))

    # Rotacion de camara
    if keys[K_d]:
        angle += deltaTime
        xtemp, ztemp, angleTemp = circularMov(angle)
        if activeShader == 5:
            if angryTime > 0:
                angryTime -= 1 * deltaTime
            if sickTime < 5.5:
                sickTime += deltaTime
            isPressed = True
            if rend.valor > 2:
                rend.valor -= 0.5 * deltaTime
    if keys[K_a]:
        angle -= deltaTime
        xtemp, ztemp, angleTemp = circularMov(angle)
        if activeShader == 5:
            if angryTime > 0:
                angryTime -= 1 * deltaTime
            if sickTime < 5.5:
                sickTime += deltaTime
            isPressed = True
            if rend.valor > 2:
                rend.valor -= 0.5 * deltaTime

    #Zoom de camara
    if keys[K_q]:
        if rend.fov > glm.radians(5):
            rend.fov -= glm.radians(5)
            rend.projectionMatrix = glm.perspective(rend.fov, 
                                                    rend.width / rend.height, 
                                                    0.1, 
                                                    1000) 
    if keys[K_e]:
        if rend.fov <= glm.radians(60):
            rend.fov += glm.radians(5)
            rend.projectionMatrix = glm.perspective(rend.fov, 
                                                    rend.width / rend.height, 
                                                    0.1, 
                                                    1000) 
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            isRunning = False

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                isRunning = False
            if ev.key == K_LEFT:
                index = (index - 1) % len(face)
                rend.scene = face[index] 
            if ev.key == K_RIGHT:
                index = (index + 1)  % len(face)
                rend.scene = face[index]
            if ev.key == K_1:
                rend.filledMode()
            if ev.key == K_2:
                rend.wireframeMode()
            if ev.key == K_3:
                activeShader = 1
                rend.activeEffect = 0
                rend.setShaders(shaders.vertex_shader, shaders.fragment_shader)
            if ev.key == K_4:
                activeShader = 2
                rend.activeEffect = 0
                rend.setShaders(shaders.toon_vertex_shaders, shaders.fragment_shader)
            if ev.key == K_5:
                activeShader = 3
                rend.activeEffect = 0
                rend.setShaders(shaders.vertex_shader, shaders.neg_fragment_shader)
            if ev.key == K_6:
                rend.activeEffect = 0
                activeShader = 4
                rend.setShaders(shaders.vertex_shader, shaders.glow_fragment_shader)
            if ev.key == K_7:
                rend.activeEffect = 0
                activeShader = 5
                rend.setShaders(shaders.dizziness_vertex_shader, shaders.fragment_shader)
            if ev.key == K_8:
                rend.activeEffect = 0
                activeShader = 6
                rend.setShaders(shaders.vertex_shader, shaders.wft_fragment_shader)

    if activeShader ==3:
        if ztemp < 0:
            rend.activeEffect = 1
        elif ztemp >= 0:
            rend.activeEffect = 0
    
    if activeShader == 5:
        if not isPressed:
            if sickTime > 0:
                sickTime -= deltaTime
            rend.activeEffect = 0
            if angryTime < 5.5:
                angryTime += deltaTime
        rend.tiempo += deltaTime 
    
        if angryTime > 4:
            rend.activeEffect = 2
        
        if angryTime < 4:
            if sickTime > 4:
                rend.activeEffect = 1
            else:
                rend.activeEffect = 0
                rend.tiempo = 2
    
    deltaTime = clock.tick(60) / 1000
    rend.render()
    pygame.display.flip()

pygame.quit()