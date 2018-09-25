#!/bin/python3
import sys
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from scipy.misc import ascent
from matplotlib import cm

# A small module to create something interactive with numpy
class simulator():
    def __init__(self, rgb_image=np.zeros([256,256,3],dtype=np.uint8)):
        self.__colormap=np.rint(np.array(cm.viridis.colors)*255).astype(np.uint8)
        self.__colormap[254:256]=np.array([[255,0,0],[255,0,0]])
        self.__background=rgb_image
        self.__pixels=np.copy(self.__background)
        self.__data=np.zeros([*rgb_image.shape[:-1]],dtype=np.uint8)
        self.__xy_max=rgb_image.shape[:-1]
        self.__xy=np.array([self.__xy_max[0]/2,self.__xy_max[1]/2],dtype=np.uint)
        self.__vxy=np.array([0,1],dtype=np.uint)

    def simstep(self):
        mask=np.where(self.__data!=0)
        resetmask=np.where(self.__data==1)
        self.__data[mask]-=1
        self.__xy=((self.__xy+self.__vxy)%self.__xy_max).astype(int)
        self.__data[self.__xy[0],self.__xy[1]]=255
        self.__pixels[mask]=self.__colormap[self.__data[mask]]
        self.__pixels[resetmask]=self.__background[resetmask]

    def get_state(self):
        return self.__pixels

    def inputhandler(self,key, x, y):
        if key==b"r":
            self.__reset()
        elif key in [100,101,102,103]:
            self.__directionchange(key)

    def __reset(self):
        self.__xy=np.array([self.__xy_max[0]/2,self.__xy_max[1]/2],dtype=np.uint)
        self.__vxy=np.array([0,1],dtype=np.uint)
        self.__pixels=np.copy(self.__background)
        self.__data=np.zeros([*self.__background.shape[:-1]],dtype=np.uint8)

    def __directionchange(self,key):
        if key==102:
            self.__vxy=np.array([0,1],dtype=np.uint)
        elif key==101:
            self.__vxy=np.array([1,0],dtype=np.uint)
        elif key==100:
            self.__vxy=np.array([0,self.__xy_max[1]-1],dtype=np.uint)
        elif key==103:
            self.__vxy=np.array([self.__xy_max[0]-1,0],dtype=np.uint)

class glwindow():
    # A square (to be used with GL_QUADS)
    vertices=((0,0),(1,0),(1,1),(0,1))

    def __init__(self, model=simulator, image=np.uint8(np.flipud(ascent()))):
        self.sim=model(image)
        self.data = image
        self.dim_xy_r=(self.data.shape[0],self.data.shape[1],self.data.shape[0]/self.data.shape[1])
        self.__paused = False
        glutInit(sys.argv)
        # Create a double-buffer RGBA window
        glutInitDisplayMode(GLUT_DOUBLE)
        glutInitWindowPosition(0, 0) #position upper left corner on screen
        # Scale up the window (will increase visibility of pixels)
        glutInitWindowSize(self.dim_xy_r[0]*4,self.dim_xy_r[1]*4)
        # Create a window, setting its title
        glutCreateWindow('interactive')
        # Set the display callback.
        glutDisplayFunc(self.__DrawGLScene)
        # Setup the 'logic control'
        glutIdleFunc(self.__IdleFunction)
        # Handle window rescaling
        glutReshapeFunc(self.__ReSizeGLScene)
        # Control user input
        glutKeyboardFunc(self.__keyPressed)
        glutSpecialFunc(self.__keyPressed)
        glutMouseFunc(self.__mousePressed)
        glutPassiveMotionFunc(self.__mousePassPos)
        glutMotionFunc(self.__mousePos)

        # Prepare texture (we only use one in total here)
        texture=glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        #GL_NEAREST or GL_LINEAR (GL_NEAREST, because we like pixel-graphics in this example)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        # Run the GLUT main loop until the user closes the window.
        glutMainLoop()

    # control the logic of the simulation and inform GLUT to schedule a display redraw
    def __IdleFunction(self):
        if not self.__paused:
            self.sim.simstep()
            glutPostRedisplay()
        else:
            pass

    # Every framedraw originates here:
    def __DrawGLScene(self):
        # Most important step (map the current state from the simulation to our texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, *self.dim_xy_r[:-1], 0, GL_RGB, GL_UNSIGNED_BYTE, self.sim.get_state())

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, 1, 0, 1, 0, 1)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glEnable(GL_TEXTURE_2D)
        glColor3f(1, 1, 1) #RGB luminosity of the texture
        glBegin(GL_QUADS) #Draw a shape with four vertices
        for vertex in self.vertices:
            glTexCoord2f(*vertex)
            glVertex2f(*vertex)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        # It will go to an off-screen frame buffer.

        # Copy the off-screen buffer to the screen.
        glutSwapBuffers()

    def __ReSizeGLScene(self,Width, Height):
        if Height == 0:
            Height = 1

        if (float(Width)/float(Height) > self.dim_xy_r[-1]):
            glViewport(int((Width-int(Height*self.dim_xy_r[-1]))/2), 0, int(Height*self.dim_xy_r[-1]), Height)
        else:
            glViewport(0, int((Height-int(Width*self.dim_xy_r[-1]))/2), Width, int(Width*self.dim_xy_r[-1]))

    def __keyPressed(self,key, x, y):
        # x, y - the curser position
        # pass arguments to simulator to decide on actions
        self.sim.inputhandler(key, x, y)
        # treat keys relevant for GLUT
        if key==b"r":
            glutPostRedisplay()
        elif key==b"p":
            self.__paused = not self.__paused
        elif key==b"\x1b" or key==b"q":
            exit()

    def __mousePressed(self,button,state,x,y):
        pass

    def __mousePassPos(self,x,y):
        pass

    def __mousePos(self,x,y):
        pass

def main():
    # Downsample the testimage by a factor of 2
    bw_image=np.uint8(np.flipud(ascent()))[::2,::2] 
    rgb_image=np.zeros([*bw_image.shape,3],dtype=np.uint8)
    rgb_image[:,:,:]=bw_image[:,:,np.newaxis]
    glwindow(image=rgb_image)

if __name__ == "__main__":
    main()
