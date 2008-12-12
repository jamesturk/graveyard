#include <GL/glfw.h>
#include <GL/gl.h>
#include <ft2build.h>
#include FT_FREETYPE_H

int main()
{
    glfwInit();
    glfwOpenWindow(800, 600, 8, 8, 8, 8, 0, 0, GLFW_WINDOW);
    
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, 800, 600, 0, -1.0, 1.0);
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
    
    do
    {
        glClear(GL_COLOR_BUFFER_BIT);

        // write code
        
        glfwSwapBuffers();
    } while(glfwGetWindowParam(GLFW_OPENED) && glfwGetKey(GLFW_KEY_ESC) != GLFW_PRESS);


    glfwCloseWindow();
    glfwTerminate();
}
