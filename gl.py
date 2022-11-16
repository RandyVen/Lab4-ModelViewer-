import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from numpy import array, float32
from pygame import image

import obj

class Model(object):
    def __init__(self, objName, textureName, textureName2):

        self.model = obj.Obj(objName)

        self.createVertexBuffer()

        self.position = glm.vec3(0,0,0)
        self.rotation = glm.vec3(0,0,0)
        self.scale = glm.vec3(1,1,1)

        self.textureSurface = image.load(textureName)
        self.textureData = image.tostring(self.textureSurface, "RGB", True)
        self.texture = glGenTextures(1)

        self.textureSurface2 = image.load(textureName2)
        self.textureData2 = image.tostring(self.textureSurface2, "RGB", True)
        self.texture2 = glGenTextures(1)

    def getModelMatrix(self):
        identity = glm.mat4(1)
        translateMatrix = glm.translate(identity, self.position)
        Pitch = glm.rotate(identity, glm.radians(self.rotation.x), glm.vec3(1,0,0))
        Yaw   = glm.rotate(identity, glm.radians(self.rotation.y), glm.vec3(0,1,0))
        Roll  = glm.rotate(identity, glm.radians(self.rotation.z), glm.vec3(0,0,1))

        rotationMatrix = Pitch * Yaw * Roll
        scaleMatrix = glm.scale(identity, self.scale)
        return translateMatrix * rotationMatrix * scaleMatrix

    def createVertexBuffer(self ):
       
        buffer = []
        for face in self.model.faces:
            for i in range(3):
                # positions
                pos = self.model.vertices[face[i][0] - 1]
                buffer.append(pos[0])
                buffer.append(pos[1])
                buffer.append(pos[2])

                # normals
                norm = self.model.normals[face[i][2] - 1]
                buffer.append(norm[0])
                buffer.append(norm[1])
                buffer.append(norm[2])

                # texCoords
                uvs = self.model.texcoords[face[i][1] - 1]
                buffer.append(uvs[0])
                buffer.append(uvs[1])

        self.vertBuffer = array(buffer, dtype = float32)

        self.VBO = glGenBuffers(1) 
        self.VAO = glGenVertexArrays(1) 
        

    def renderInScene(self):
        
        glBindVertexArray(self.VAO)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        

        glBufferData(GL_ARRAY_BUFFER, #Buffer ID
                     self.vertBuffer.nbytes, 
                     self.vertBuffer, #Buffer data
                     GL_STATIC_DRAW)

        

        glVertexAttribPointer(0, #Attibute number
                              3, 
                              GL_FLOAT, #Type
                              GL_FALSE, 
                              4 * 8, 
                              ctypes.c_void_p(0)) 

        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, #Attibute number
                              3, 
                              GL_FLOAT, #Type
                              GL_FALSE, 
                              4 * 8, 
                              ctypes.c_void_p(4 * 3)) 

        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, #Attibute number
                              2, 
                              GL_FLOAT, #Type
                              GL_FALSE, 
                              4 * 8, 
                              ctypes.c_void_p(4 * 6)) 

        glEnableVertexAttribArray(2)

        # Dar textura
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexImage2D(GL_TEXTURE_2D, 
                     0, 
                     GL_RGB, 
                     self.textureSurface.get_width(),  
                     self.textureSurface.get_height(),  
                     0, 
                     GL_RGB, 
                     GL_UNSIGNED_BYTE, 
                     self.textureData) 

        glGenerateMipmap(GL_TEXTURE_2D)

        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_2D, self.texture2)
        glTexImage2D(GL_TEXTURE_2D, 
                     0, 
                     GL_RGB, 
                     self.textureSurface.get_width(), 
                     self.textureSurface.get_height(),  
                     0, 
                     GL_RGB, 
                     GL_UNSIGNED_BYTE, 
                     self.textureData2) 

        glGenerateMipmap(GL_TEXTURE_2D)

        glDrawArrays(GL_TRIANGLES, 0, len(self.model.faces) * 3) 

class Renderer(object):
    def __init__(self, screen):
        self.screen = screen
        _, _, self.width, self.height = screen.get_rect()

        glEnable(GL_DEPTH_TEST)
        glViewport(0,0, self.width, self.height)

        self.filledMode()

        self.scene = None
        self.tiempo = 0
        self.valor = 10
        self.pointLight = glm.vec3(0, 0, 2)
        self.fov = glm.radians(60)
        self.activeEffect = 0
        self.camPosition = glm.vec3(0,0,5)
        self.camRotation = glm.vec3(0,0,0) 

        self.viewMatix = self.getViewMatrix()

        #Projection Matrix
        self.projectionMatrix = glm.perspective(self.fov, 
                                                self.width / self.height, 
                                                0.1, 
                                                1000) 

    def horizontal_rotation(self, amount, position):
        center = position
        self.angle += amount
        self.camPosition.x = glm.sin(self.angle) * self.radius
        self.camPosition.z = glm.cos(self.angle) * self.radius
        self.view_matrix = glm.lookAt(center - self.camPosition, center, glm.vec3(0.0, 1.0, 0.0))

    def getViewMatrix(self):
        identity = glm.mat4(1)
        translateMatrix = glm.translate(identity, self.camPosition)
        Pitch = glm.rotate(identity, glm.radians(self.camRotation.x), glm.vec3(1,0,0))
        Yaw   = glm.rotate(identity, glm.radians(self.camRotation.y), glm.vec3(0,1,0))
        Roll  = glm.rotate(identity, glm.radians(self.camRotation.z), glm.vec3(0,0,1))

        rotationMatrix = Pitch * Yaw * Roll
        camMatrix = translateMatrix * rotationMatrix
        return glm.inverse(camMatrix)

    def wireframeMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def filledMode(self):
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def setShaders(self, vertexShader, fragShader):
        if vertexShader is not None and fragShader is not None:
            self.active_shader = compileProgram( compileShader(vertexShader, GL_VERTEX_SHADER),
                                                 compileShader(fragShader, GL_FRAGMENT_SHADER))
        else:
            self.active_shader = None

    def render(self):
        glClearColor(0.2,0.2,0.2,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUseProgram(self.active_shader)

        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "viewMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.viewMatix))
                                                                    
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "projectionMatrix"),
                               1, GL_FALSE, glm.value_ptr(self.projectionMatrix))

            glUniform1f(glGetUniformLocation(self.active_shader, "tiempo"), self.tiempo)
            glUniform1f(glGetUniformLocation(self.active_shader, "valor"), self.valor)
            glUniform1i(glGetUniformLocation(self.active_shader, "activeEffect"), self.activeEffect)

            glUniform3f(glGetUniformLocation(self.active_shader, "pointLight"),
                        self.pointLight.x, self.pointLight.y, self.pointLight.z)

        if self.active_shader:
            glUniformMatrix4fv(glGetUniformLocation(self.active_shader, "modelMatrix"),
                            1, GL_FALSE, glm.value_ptr(self.scene.getModelMatrix()))
            glUniform1i(glGetUniformLocation(self.active_shader, "tex1"), 0)
            glUniform1i(glGetUniformLocation(self.active_shader, "tex2"), 1)
            self.scene.renderInScene()