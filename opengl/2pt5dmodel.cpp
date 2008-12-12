#if defined (__APPLE__)
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif

#include  <vector>
using namespace std;

struct vertex2 { 
    int x; 
    int y;
    int depth;
};

vertex2 shape[] = { {0, 0, 50}, {100, 0, 50}, {50, 50, 50}, {100, 100, 50}, {0, 100, 50} }; 

void drawFlatPoly(vertex2 poly[]) {
    glBegin(GL_LINE_LOOP);
    for(int i=0; i < 4; ++i) {
        glVertex2f(poly[i].x, poly[i].y);
    }
    glEnd();
}

void drawPolyWithFixedDepth(vertex2 poly[], int n, int depth) {

    // front of poly
    glBegin(GL_POLYGON);
    for(int i=0; i < n; ++i) {
        glVertex3f(poly[i].x, poly[i].y, 0);
    }
    glEnd();

    // back of poly
    glBegin(GL_POLYGON);
    for(int i=0; i < n; ++i) {
        glVertex3f(poly[i].x, poly[i].y, depth);
    }
    glEnd();
    
    // sides
    glBegin(GL_QUADS);
    for(int i=1; i < n; ++i) {
        glVertex3f(poly[i].x, poly[i].y, 0);
        glVertex3f(poly[i].x, poly[i].y, depth);
        glVertex3f(poly[i-1].x, poly[i-1].y, depth);
        glVertex3f(poly[i-1].x, poly[i-1].y, 0);
    }
    
    glVertex3f(poly[0].x, poly[0].y, 0);
    glVertex3f(poly[0].x, poly[0].y, depth);
    glVertex3f(poly[n-1].x, poly[n-1].y, depth);
    glVertex3f(poly[n-1].x, poly[n-1].y, 0);
    glEnd();
}

void drawPolyWithPerVertexDepth(vertex2 poly[], int n) {

    // front of poly
    glBegin(GL_TRIANGLE_FAN);
    for(int i=0; i < n; ++i) {
        glVertex3f(poly[i].x, poly[i].y, 0);
    }
    glEnd();

    // back of poly
    glBegin(GL_TRIANGLE_FAN);
    for(int i=0; i < n; ++i) {
        glVertex3f(poly[i].x, poly[i].y, poly[i].depth);
    }
    glEnd();
    
    // sides
    glBegin(GL_QUADS);
    for(int i=1; i < n; ++i) {
        if(poly[i].depth+poly[i-1].depth > 0.000001) {
            glVertex3f(poly[i].x, poly[i].y, 0);
            glVertex3f(poly[i].x, poly[i].y, poly[i].depth);
            glVertex3f(poly[i-1].x, poly[i-1].y, poly[i-1].depth);
            glVertex3f(poly[i-1].x, poly[i-1].y, 0);
        }
    }
    if(poly[0].depth+poly[n-1].depth > 0.000001) {
        glVertex3f(poly[0].x, poly[0].y, 0);
        glVertex3f(poly[0].x, poly[0].y, poly[0].depth);
        glVertex3f(poly[n-1].x, poly[n-1].y, poly[n-1].depth);
        glVertex3f(poly[n-1].x, poly[n-1].y, 0);
    }
    glEnd();
}

// display callback function, draw entire window
void display() {

    // window dimensions
    
    int width = glutGet(GLUT_WINDOW_WIDTH);
    int height = glutGet(GLUT_WINDOW_HEIGHT);

    // full window viewport
    
    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, width, 0, height, -100, 300);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT);

    static float theta=0;
    theta += 0.5f;

    glColor4f(0,0.75,0,0.9);
    glPushMatrix();
    glTranslatef(350, 350, 0);
    glRotatef(theta, 0.1, 1, 0);
    drawPolyWithFixedDepth(shape, 5, 20);
    glPopMatrix();

    // show back buffer
    glutSwapBuffers();
    
}

// keyboard callback - process keypresses
void keyboard(unsigned char key, int x, int y) {
    
    glutPostRedisplay();
}

// mouse button callback
void mouseButton(int button, int state, int x, int y) {

    glutPostRedisplay();

}

// mouse motion callback
void mouseMotion(int x, int y) {


    glutPostRedisplay();
}

// timer callback, called every 10ms or so to do animation updates
void update(int) {

    // call this again in ~10ms
    glutTimerFunc(10, update, 0);

    glutPostRedisplay(); 
}

int main(int argc, char **argv) {
   
    // initialize glut and window
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_RGBA|GLUT_DEPTH|GLUT_DOUBLE);
    glutInitWindowPosition(50, 50);
    glutInitWindowSize(800, 800);
    glutCreateWindow("2.5D Model Test");

    // add callbacks
    glutKeyboardFunc(keyboard);
    glutDisplayFunc(display);
    glutMouseFunc(mouseButton);
    glutMotionFunc(mouseMotion);
    glutTimerFunc(10, update, 10);

    //init();
    glEnable(GL_DEPTH_TEST);

    // start application
    glutMainLoop();

    return 0;
}
