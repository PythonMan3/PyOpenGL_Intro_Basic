from OpenGL.GL import *
from OpenGL.GLU import *
import glfw
import numpy as np
import gl_util

vert_pos = np.array([[0.0, 0.5, 0.0], [-0.5, -0.5, 0.0], [0.5, -0.5, 0.0]], dtype=np.float32)
vert_color = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], dtype=np.float32)
program = None
pos_vbo = None
color_vbo = None
pos_loc = -1
color_loc = -1

vertex_shader_src="""
#version 400 core

in vec3 position;
in vec3 color;
out vec3 outColor;

void main(void) {
    outColor = color;
    gl_Position = vec4(position, 1.0);
}
""".strip()

fragment_shader_src="""
#version 400 core

in vec3 outColor;
out vec4 outFragmentColor;

void main(void) {
    outFragmentColor = vec4(outColor, 1.0);
}
""".strip()

def init(window, width, height):
    global program, pos_vbo, color_vbo, pos_loc, color_loc
    program = gl_util.create_program(vertex_shader_src, fragment_shader_src)
    pos_loc = glGetAttribLocation(program, "position")
    color_loc = glGetAttribLocation(program, "color")
    pos_vbo = gl_util.create_vbo(vert_pos)
    color_vbo = gl_util.create_vbo(vert_color)

def update(window, width, height):
    pass

def draw():
    glUseProgram(program)
    glEnableVertexAttribArray(pos_loc)
    glBindBuffer(GL_ARRAY_BUFFER, pos_vbo)
    glVertexAttribPointer(pos_loc, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(color_loc)
    glBindBuffer(GL_ARRAY_BUFFER, color_vbo)
    glVertexAttribPointer(color_loc, 3, GL_FLOAT, GL_FALSE, 0, None)
    num_vertex = vert_pos.size // 3
    glDrawArrays(GL_TRIANGLES, 0, num_vertex)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glUseProgram(0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

def main():
    if not glfw.init():
        return

    window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "PyOpenGL Sample", None, None)
    if not window:
        glfw.terminate()
        print('Failed to create window')
        return

    glfw.make_context_current(window)

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 0)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    init(window, SCREEN_WIDTH, SCREEN_HEIGHT)

    while not glfw.window_should_close(window):
        glClearColor(0, 0, 0, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        update(window, SCREEN_WIDTH, SCREEN_HEIGHT)
        draw()

        glfw.swap_buffers(window)

        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()

if __name__ == "__main__":
    main()
