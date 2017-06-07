# a Humanoid
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import math
import sys
from time import sleep

global dance,pos,v

##global ww,hh,theta,V,t
##global lookat

#theta = 0.0;
#V = 0.0;  
#t = 0.0;

class PartState:
    def __init__(self,tx,ty,tz,sx,sy,sz,rx,ry,rz,color):
        self.tx=tx
        self.ty=ty
        self.tz=tz
        self.sx=sx
        self.sy=sy
        self.sz=sz
        self.rx=rx
        self.ry=ry
        self.rz=rz
        self.color = color

class View:
    def __init__(self,eyeX,eyeY,eyeZ,centerX,centerY,centerZ,upX,upY,upZ):
        self.eyeX = eyeX
        self.eyeY = eyeY
        self.eyeZ = eyeZ
        self.centerX = centerX
        self.centerY = centerY
        self.centerZ = centerZ
        self.upX = upX
        self.upY = upY
        self.upZ = upZ

##        trunk,
##        head,
##            ,
##            larm,
##                lfarm,
##                
##            rarm,
##                rfarm,
##            ,
##            luleg,
##                llleg,
##            ruleg,
##                rlleg

global trunk,head
global larm,lfarm,rarm,rfarm
global luleg,llleg,ruleg,rlleg

def drawCube(wall_mat):
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, wall_mat)
    glBegin(GL_QUADS)
    #GL_AMBIENT_AND_DIFFUSE

    # left wall */
    glNormal3f(-1, 0, 0)
    glVertex3f(-1, -1,  1)
    glVertex3f(-1,  1,  1)
    glVertex3f(-1,  1, -1)
    glVertex3f(-1, -1, -1)

    # right wall */
    glNormal3f(1, 0, 0)
    glVertex3f( 1, -1,  1)
    glVertex3f( 1, -1, -1)
    glVertex3f( 1,  1, -1)
    glVertex3f( 1,  1,  1)

    # ceiling */
    glNormal3f(0, 1, 0)
    glVertex3f(-1,  1,  1)
    glVertex3f( 1,  1,  1)
    glVertex3f( 1,  1, -1)
    glVertex3f(-1,  1, -1)

    # back wall */
    glNormal3f(0, 0, -1)
    glVertex3f(-1, -1, -1)
    glVertex3f(-1,  1, -1)
    glVertex3f( 1,  1, -1)
    glVertex3f( 1, -1, -1)

    #floor
    glNormal3f(0, -1, 0)
    glVertex3f(-1, -1,  1)
    glVertex3f(-1, -1, -1)
    glVertex3f( 1, -1, -1)
    glVertex3f( 1, -1,  1)

    #front wall
    glNormal3f(0, 0, 1)
    glVertex3f(-1, -1,  1)
    glVertex3f( 1, -1,  1)
    glVertex3f( 1,  1,  1)
    glVertex3f(-1,  1,  1)
    
    glEnd();

def resize(w, h):
    glViewport(0, 0, w , h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60.0, float(w)/float(h), 10.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    #ww = w
    #hh = h
                 
def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLightfv(GL_LIGHT0,GL_POSITION,(30,30,30))
    global dance
    global pos
    global v
    global trunk,head
    global larm,lfarm,rarm,rfarm
    global luleg,llleg,ruleg,rlleg
    pos = 0
    dance = 'rrrararaRRRARARAttxcccxTTttfvvfsffvcdaxzxcRRRRsrcccrrsrssraarrdrxcr'
    v = View(15,15,15,0,0,0,0,1,0)



    trunk = PartState(0,0,0, 5  ,7  ,2.5,0,0,0,(0,0,1,0.0))
    head = PartState (0,0,0, 1.6,2  ,2  ,0,0,0,(0,1,0,0.2))
    larm = PartState (0,0,0, 1.2,3.5,1.5,0,0,0,(1,0,0,0.2))
    lfarm = PartState(0,0,0, 1.0,3.0,1.0,0,0,0,(1,0.5,0,0.2))
    rarm = PartState (0,0,0, 1.2,3.5,1.5,0,0,0,(1,0,0,0.2))
    rfarm = PartState(0,0,0, 1.0,3.0,1.0,0,0,0,(1,0.5,0,0.2))
    luleg = PartState(0,0,0, 1.1,3.0,2  ,0,0,0,(0,0,1,0.2))
    llleg = PartState(0,0,0, 0.9,4.5,1.8,0,0,0,(0,0,1,0.2))
    ruleg = PartState(0,0,0, 1.1,3.0,2  ,0,0,0,(0,0,1,0.2))
    rlleg = PartState(0,0,0, 0.9,4.5,1.8,0,0,0,(0,0,1,0.2))
    
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glColor4f(0,0,1,0)
    #v = View(0,0,35,0,0,0,0,1,0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glPushMatrix()
    gluLookAt(v.eyeX,v.eyeY,v.eyeZ,v.centerX,v.centerY,v.centerZ,v.upX,v.upY,v.upZ)
    #hierarchy modelling
    global trunk

    glTranslatef(trunk.tx,trunk.ty,trunk.tz)
    glRotatef(trunk.ry,0,1,0)
    drawTrunk()
    drawHead()
    drawArms() 
    drawLegs()
    glPopMatrix()
    glutSwapBuffers()

def drawTrunk():
    glPushMatrix()
    glScalef(trunk.sx,trunk.sy,trunk.sz)
    wall_mat = (trunk.color[0],trunk.color[1],trunk.color[2],0)
    drawCube(wall_mat)
    glPopMatrix()    

#   glNormal3f
#   glutSolidCube(10.0)
    
def drawHead():
    glPushMatrix()
    global head
    glRotatef(head.ry,0,1,0)
    glTranslatef(0,trunk.sy+head.sy,0)
    glScalef(head.sx,head.sy,head.sz)
    wall_mat = (head.color[0],head.color[1],head.color[2],0)
    drawCube(wall_mat)
    #glScalef(1/head.sx,1/head.sy,1/head.sz)
    #eyeL
    glPushMatrix()
    glTranslatef(-0.5,0.5,1.1)
    glColor4f(1,1,1,0)
    glutSolidSphere(0.2,16,16)
    glPopMatrix()

    #eyeR
    glPushMatrix()
    glTranslatef(0.5,0.5,1.1)
    glColor4f(1,1,1,0)
    glutSolidSphere(0.2,16,16)
    glPopMatrix()    

    glPopMatrix()
def drawArms():
    #left Arm
    global larm
    glPushMatrix() #start larm
    glTranslatef(-(trunk.sx+larm.sx),trunk.sy,0)
    glRotatef(larm.rx,1,0,0)
    glTranslatef(0,-larm.sy,0)
    glPushMatrix() #start Scaling
    glScalef(larm.sx,larm.sy,larm.sz)
    wall_mat = (larm.color[0],larm.color[1],larm.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling

    #lfarm
    global lfarm
    glPushMatrix() #start lfarm
    glTranslatef(0,-(larm.sy),0)
    glRotatef(lfarm.rx,1,0,0)
    glTranslatef(0,-lfarm.sy,0)
    glPushMatrix() #start Scaling
    glScalef(lfarm.sx,lfarm.sy,lfarm.sz) 
    wall_mat = (lfarm.color[0],lfarm.color[1],lfarm.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling
    glPopMatrix() #end lfarm
    
    glPopMatrix() #end left Arms

    #right arm
    global rarm
    glPushMatrix() #start right arm
    glTranslatef(trunk.sx+rarm.sx,trunk.sy,0)
    glRotatef(rarm.rx,1,0,0)
    glTranslatef(0,-rarm.sy,0)
    glPushMatrix() #start scaling
    glScalef(rarm.sx,rarm.sy,rarm.sz)
    wall_mat = (rarm.color[0],rarm.color[1],rarm.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling

    #right Fore Arm
    global rfarm
    glPushMatrix() #start rfarm
    glTranslatef(0,-rarm.sy,0)
    glRotatef(rfarm.rx,1,0,0)
    glTranslatef(0,-rfarm.sy,0)
    glPushMatrix() #start Scaling
    glScalef(rfarm.sx,rfarm.sy,rfarm.sz) 
    wall_mat = (rfarm.color[0],rfarm.color[1],rfarm.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling
    glPopMatrix() #end rfarm
    
    glPopMatrix() #end right arm
def drawLegs():
    #left legs
    global luleg
    glPushMatrix() #start luleg
    glTranslatef(-(0.4*trunk.sx),-trunk.sy,0)
    glRotatef(luleg.rx,1,0,0)
    glTranslatef(0,-luleg.sy,0)
    glPushMatrix() #start Scaling
    glScalef(luleg.sx,luleg.sy,luleg.sz)
    wall_mat = (luleg.color[0],luleg.color[1],luleg.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling

    #lfarm
    global llleg
    glPushMatrix() #start lfarm
    glTranslatef(0,-(luleg.sy),0)
    glRotatef(llleg.rx,1,0,0)
    glTranslatef(0,-llleg.sy,0)
    glPushMatrix() #start Scaling
    glScalef(llleg.sx,llleg.sy,llleg.sz) 
    wall_mat = (llleg.color[0],llleg.color[1],llleg.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling
    glPopMatrix() #end llleg
    
    glPopMatrix() #end Left Leg

    #right Leg
    global ruleg
    glPushMatrix() #start luleg
    glTranslatef(0.4*trunk.sx,-trunk.sy,0)
    glRotatef(ruleg.rx,1,0,0)
    glTranslatef(0,-ruleg.sy,0)
    glPushMatrix() #start Scaling
    glScalef(ruleg.sx,ruleg.sy,ruleg.sz)
    wall_mat = (ruleg.color[0],ruleg.color[1],ruleg.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling

    #lfarm
    global rlleg
    glPushMatrix() #start lfarm
    glTranslatef(0,-(ruleg.sy),0)
    glRotatef(rlleg.rx,1,0,0)
    glTranslatef(0,-rlleg.sy,0)
    glPushMatrix() #start Scaling
    glScalef(rlleg.sx,rlleg.sy,rlleg.sz) 
    wall_mat = (rlleg.color[0],rlleg.color[1],rlleg.color[2],0)
    drawCube(wall_mat)
    glPopMatrix() #end Scaling
    glPopMatrix() #end llleg
    
    glPopMatrix() #end Left Leg
    
def myKey1(k,x1,y1):
    global dance,pos
    if(k == 'm'):
        if(pos == len(dance)):
            pos-=len(dance)
        myKey(dance[pos],0,0)
        pos += 1
    else:
        myKey(k,x1,y1)

##    global danceEnable,dance
##    if(k == 'm'):
##        danceEnable ^= 1
##        
##    if(danceEnable == 1):
##        glutKeyboardFunc(None)
##        for i in range(0,len(dance)):
##            myKey(dance[i],0,0)
##            sleep(0.5)
##        glutKeyboardFunc(myKey1)
##            
##    myKey(k,x1,y1)


def zoom(a):
    x = v.centerX - v.eyeX
    y = v.centerY - v.eyeY
    z = v.centerZ - v.eyeZ

    x_ = a*x
    y_ = a*y
    z_ = a*z

    e_ = (v.centerX - x_ , v.centerY - y_ , v.centerZ - z_)
    return View(e_[0],e_[1],e_[2],v.centerX,v.centerY,v.centerZ,v.upX,v.upY,v.upZ)

    
    
    
def myKey(key,x,y):
    global v
    ch = key.decode("utf-8")
    #print(type(key), key, type(ch), ch)
    key = ch
    if(key == 'r'):
        trunk.ry += 5
        trunk.ry %= 360
        glutPostRedisplay()
    elif(key == 'R'):
        trunk.ry -= 5
        trunk.ry %= 360
        glutPostRedisplay()
    elif(key == 't'):
        trunk.tx += 0.25
        trunk.tx %= 360
        glutPostRedisplay()
    elif(key == 'T'):
        trunk.tx -= 0.25
        trunk.tx %= 360
        glutPostRedisplay()

        #zoom in zoom out 
    elif(key == 'y'):
        v1 = zoom(0.80)
        v = v1
        glutPostRedisplay()
    elif(key == 'Y'):
        v1 = zoom(1.2)
        v = v1
        glutPostRedisplay()
        
    #rotations
    #rotate left arm
    elif(key == 'a'):
        larm.rx += 5
        larm.rx %= 360
        glutPostRedisplay()

    elif(key == 'A'):
        larm.rx -= 5
        larm.rx %= 360
        glutPostRedisplay()

    elif(key == 'z'):
        lfarm.rx += 5
        lfarm.rx %= 360
        glutPostRedisplay()

    elif(key == 'Z'):
        lfarm.rx -= 5
        lfarm.rx %= 360
        glutPostRedisplay()
    #rotate right arm
    elif(key == 's'):
        rarm.rx += 5
        rarm.rx %= 360
        glutPostRedisplay()
        
    elif(key == 'S'):
        rarm.rx -= 5
        rarm.rx %= 360
        glutPostRedisplay()
    
    elif(key == 'x'):
        rfarm.rx += 5
        rarm.rx %= 360
        glutPostRedisplay()
        
    elif(key == 'X'):
        rfarm.rx -= 5
        rarm.rx %= 360
        glutPostRedisplay()
    #rotate left leg
    elif(key == 'd'):
        luleg.rx += 5
        luleg.rx %= 360
        glutPostRedisplay()

    elif(key == 'D'):
        luleg.rx -= 5
        luleg.rx %= 360
        glutPostRedisplay()

    elif(key == 'c'):
        llleg.rx += 5
        llleg.rx %= 360
        glutPostRedisplay()
        
    elif(key == 'C'):
        llleg.rx -= 5
        llleg.rx %= 360
        glutPostRedisplay()
    #rotate right leg
    elif(key == 'f'):
        ruleg.rx += 5
        ruleg.rx %= 360
        glutPostRedisplay()

    elif(key == 'F'):
        ruleg.rx -= 5
        ruleg.rx %= 360
        glutPostRedisplay()

    elif(key == 'v'):
        rlleg.rx += 5
        rlleg.rx %= 360
        glutPostRedisplay()

    elif(key == 'V'):
        rlleg.rx -= 5
        rlleg.rx %= 360
        glutPostRedisplay()
    #elif
           

glutInit(sys.argv)
glutInitWindowPosition(50,25)
glutInitWindowSize(500,500)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE| GLUT_DEPTH)
glutCreateWindow("Humanoid")
glutReshapeFunc(resize)
init()
glutDisplayFunc(display)
glutKeyboardFunc(myKey1)
glutMainLoop()

