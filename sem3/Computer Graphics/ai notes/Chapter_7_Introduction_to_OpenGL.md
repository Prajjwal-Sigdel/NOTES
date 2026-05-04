
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            CHAPTER 7 — INTRODUCTION TO OPENGL                              ║
║                                                                            ║
║            CMP 234 · Pokhara University · BE Computer                      ║
║            Syllabus Hours: 7                                               ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝


OpenGL (Open Graphics Library) is the most widely used cross-platform
API for rendering 2D and 3D graphics. This chapter covers its architecture,
primitive types, window management with GLUT, transformation functions,
projection setup, lighting, and modern OpenGL concepts (shaders, VBOs, VAOs).


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.1  OPENGL OVERVIEW AND ARCHITECTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  WHAT IS OPENGL?                                                           │
│                                                                            │
│  ◆ A specification (not a software library) maintained by the Khronos    │
│    Group (originally Silicon Graphics, Inc.).                              │
│  ◆ Cross-platform: Windows, Linux, macOS, Android, iOS.                  │
│  ◆ Language-independent: C bindings are standard; wrappers exist for     │
│    C++, Python (PyOpenGL), Java (JOGL), JavaScript (WebGL), etc.         │
│  ◆ Hardware-accelerated: GPU drivers implement the OpenGL specification. │
│  ◆ State machine: OpenGL maintains a set of states (current color,      │
│    active texture, enabled features) that persist until changed.          │
└─────────────────────────────────────────────────────────────────────────────┘


  ► OpenGL Architecture — Graphics Pipeline
  ───────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  APPLICATION                                                     │
  │      │                                                            │
  │      ▼                                                            │
  │  ┌──────────────────┐                                            │
  │  │  Vertex Data      │  ← vertices, normals, colors, UVs        │
  │  └────────┬─────────┘                                            │
  │           ▼                                                       │
  │  ┌──────────────────┐                                            │
  │  │  Vertex Shader    │  ← transform vertices (MVP matrix)       │
  │  └────────┬─────────┘                                            │
  │           ▼                                                       │
  │  ┌──────────────────┐                                            │
  │  │  Primitive        │  ← assemble triangles from vertices       │
  │  │  Assembly         │                                            │
  │  └────────┬─────────┘                                            │
  │           ▼                                                       │
  │  ┌──────────────────┐                                            │
  │  │  Rasterization    │  ← convert primitives to fragments        │
  │  └────────┬─────────┘    (potential pixels)                      │
  │           ▼                                                       │
  │  ┌──────────────────┐                                            │
  │  │  Fragment Shader  │  ← compute color/lighting per fragment   │
  │  └────────┬─────────┘                                            │
  │           ▼                                                       │
  │  ┌──────────────────┐                                            │
  │  │  Per-Fragment     │  ← depth test, stencil test, blending    │
  │  │  Operations       │                                            │
  │  └────────┬─────────┘                                            │
  │           ▼                                                       │
  │  ┌──────────────────┐                                            │
  │  │  Frame Buffer     │  ← final pixel colors on screen          │
  │  └──────────────────┘                                            │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Fixed-Function vs. Programmable Pipeline
  ────────────────────────────────────────────

  ┌─────────────────────────┬──────────────────────┬──────────────────────┐
  │  PROPERTY               │  FIXED-FUNCTION      │  PROGRAMMABLE        │
  │                         │  (OpenGL ≤ 2.x)      │  (OpenGL 3.x+)      │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Pipeline               │  Built-in, rigid     │  Custom shaders      │
  │                         │  (glBegin/glEnd)     │  (GLSL programs)     │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Flexibility            │  Limited to what     │  Full control over   │
  │                         │  OpenGL provides     │  vertex & fragment   │
  │                         │                      │  processing          │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Lighting               │  glEnable(GL_LIGHT)  │  Custom illumination │
  │                         │  (Phong built-in)    │  in shaders          │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Learning curve         │  Easier to start     │  More complex but    │
  │                         │                      │  much more powerful  │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Performance            │  Lower (CPU-bound)   │  Higher (GPU-driven) │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Status                 │  Deprecated          │  Current standard    │
  └─────────────────────────┴──────────────────────┴──────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.2  OPENGL NAMING CONVENTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  PREFIX                │  MEANING                                    │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  gl                    │  Core OpenGL function (e.g., glClear)      │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  glu                   │  OpenGL Utility Library (e.g., gluLookAt)  │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  glut                  │  GLUT — GL Utility Toolkit for window      │
  │                        │  management (e.g., glutCreateWindow)        │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  GL_                   │  OpenGL constant (e.g., GL_TRIANGLES)      │
  └────────────────────────┴──────────────────────────────────────────────┘


  ► Data Type Suffixes
  ─────────────────────

  ┌───────────┬─────────────────┬───────────────────────────────────────────┐
  │  SUFFIX   │  C TYPE         │  EXAMPLE                                 │
  ├───────────┼─────────────────┼───────────────────────────────────────────┤
  │  f        │  GLfloat        │  glColor3f(1.0, 0.0, 0.0)               │
  │  d        │  GLdouble       │  glVertex3d(1.0, 2.0, 3.0)              │
  │  i        │  GLint          │  glColor3i(255, 0, 0)                    │
  │  s        │  GLshort        │  rarely used                             │
  │  ub       │  GLubyte        │  glColor3ub(255, 128, 0)                 │
  │  v        │  pointer/array  │  glVertex3fv(vertex_array)               │
  └───────────┴─────────────────┴───────────────────────────────────────────┘

  The number (2, 3, 4) indicates the number of parameters:
  • glVertex2f(x, y)        — 2D vertex
  • glVertex3f(x, y, z)     — 3D vertex
  • glColor4f(r, g, b, a)   — RGBA color



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.3  GLUT — GL UTILITY TOOLKIT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  GLUT handles window creation, input events, and menus — things OpenGL
  itself does NOT handle (OpenGL only draws; it has no concept of windows).

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  KEY GLUT FUNCTIONS:                                                   │
  │                                                                         │
  │  INITIALIZATION:                                                       │
  │  ► glutInit(&argc, argv)          — Initialize GLUT                   │
  │  ► glutInitDisplayMode(mode)      — Set display mode (color, depth)   │
  │  ► glutInitWindowSize(w, h)       — Set window dimensions             │
  │  ► glutInitWindowPosition(x, y)   — Set window position               │
  │  ► glutCreateWindow("title")      — Create the window                 │
  │                                                                         │
  │  CALLBACK REGISTRATION:                                                │
  │  ► glutDisplayFunc(display)       — Called when window needs redraw   │
  │  ► glutReshapeFunc(reshape)       — Called when window is resized     │
  │  ► glutKeyboardFunc(keyboard)     — Called on key press               │
  │  ► glutMouseFunc(mouse)           — Called on mouse click             │
  │  ► glutMotionFunc(motion)         — Called on mouse drag              │
  │  ► glutIdleFunc(idle)             — Called when system is idle        │
  │  ► glutTimerFunc(ms, timer, val)  — Called after ms milliseconds     │
  │                                                                         │
  │  EVENT LOOP:                                                           │
  │  ► glutMainLoop()                 — Start the event loop (never       │
  │                                     returns)                           │
  │                                                                         │
  │  BUILT-IN 3D OBJECTS:                                                  │
  │  ► glutWireCube(size)             ► glutSolidCube(size)               │
  │  ► glutWireSphere(r, sl, st)      ► glutSolidSphere(r, sl, st)       │
  │  ► glutWireTeapot(size)           ► glutSolidTeapot(size)             │
  │  ► glutWireTorus(i,o, sl, st)     ► glutSolidTorus(i,o, sl, st)      │
  │  ► glutWireCone(r, h, sl, st)     ► glutSolidCone(r, h, sl, st)      │
  └─────────────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.4  WINDOW SETUP AND DOUBLE BUFFERING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Display Modes
  ────────────────

  ┌──────────────────────┬─────────────────────────────────────────────────┐
  │  MODE FLAG           │  PURPOSE                                       │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  GLUT_SINGLE         │  Single buffer — draw directly to screen.    │
  │                      │  May cause flicker.                            │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  GLUT_DOUBLE         │  Double buffer — draw to back buffer, then   │
  │                      │  swap. Eliminates flicker. PREFERRED.         │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  GLUT_RGB            │  Use RGB color mode.                          │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  GLUT_RGBA           │  RGB + Alpha channel (transparency).          │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  GLUT_DEPTH          │  Enable depth buffer (for z-buffer HSR).     │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  GLUT_STENCIL        │  Enable stencil buffer.                       │
  └──────────────────────┴─────────────────────────────────────────────────┘

  Combined: glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);


  ► Double Buffering — How It Works
  ──────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  Without double buffering:                                       │
  │    Screen is drawn to directly → user sees partial drawing       │
  │    → visible flicker/tearing                                     │
  │                                                                   │
  │  With double buffering:                                          │
  │    ┌────────────┐    ┌────────────┐                              │
  │    │ BACK       │    │ FRONT      │                              │
  │    │ BUFFER     │    │ BUFFER     │ ← displayed on screen       │
  │    │            │    │            │                              │
  │    │ (drawing   │───►│ (displayed │   glutSwapBuffers()          │
  │    │  happens   │swap│  to user)  │   swaps back and front      │
  │    │  here)     │    │            │                              │
  │    └────────────┘    └────────────┘                              │
  │                                                                   │
  │  The user only sees completed frames. Drawing happens off-screen.│
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.5  OPENGL PRIMITIVE TYPES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  All geometry in OpenGL is specified as a combination of basic primitives:

  ┌─────────────────────────┬────────────────────────────────────────────────┐
  │  PRIMITIVE              │  DESCRIPTION AND VERTICES                     │
  ├─────────────────────────┼────────────────────────────────────────────────┤
  │  GL_POINTS              │  Individual points. Each vertex = one dot.   │
  ├─────────────────────────┼────────────────────────────────────────────────┤
  │  GL_LINES               │  Separate line segments. Vertices in pairs:  │
  │                         │  (v0-v1), (v2-v3), (v4-v5), ...              │
  ├─────────────────────────┼────────────────────────────────────────────────┤
  │  GL_LINE_STRIP          │  Connected line segments. v0→v1→v2→v3→...   │
  │                         │  Each vertex connects to the next.            │
  ├─────────────────────────┼────────────────────────────────────────────────┤
  │  GL_LINE_LOOP           │  Like LINE_STRIP but last vertex connects   │
  │                         │  back to first (closed loop).                │
  ├─────────────────────────┼────────────────────────────────────────────────┤
  │  GL_TRIANGLES           │  Separate triangles. Groups of 3:            │
  │                         │  (v0,v1,v2), (v3,v4,v5), ...                │
  ├─────────────────────────┼────────────────────────────────────────────────┤
  │  GL_TRIANGLE_STRIP      │  Connected triangles sharing edges:          │
  │                         │  (v0,v1,v2), (v2,v1,v3), (v2,v3,v4), ...   │
  │                         │  Efficient — each new vertex = 1 triangle.  │
  ├─────────────────────────┼────────────────────────────────────────────────┤
  │  GL_TRIANGLE_FAN        │  Fan of triangles from a central vertex:     │
  │                         │  (v0,v1,v2), (v0,v2,v3), (v0,v3,v4), ...   │
  ├─────────────────────────┼────────────────────────────────────────────────┤
  │  GL_QUADS               │  Quadrilaterals. Groups of 4 vertices.      │
  │  (deprecated in 3.x+)  │  (v0,v1,v2,v3), (v4,v5,v6,v7), ...         │
  ├─────────────────────────┼────────────────────────────────────────────────┤
  │  GL_POLYGON             │  Convex polygon from all listed vertices.   │
  │  (deprecated in 3.x+)  │  Must be convex and planar.                  │
  └─────────────────────────┴────────────────────────────────────────────────┘


  ► Usage Syntax (Fixed-Function)
  ────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  glBegin(GL_TRIANGLES);                                        │
  │      glColor3f(1, 0, 0);   glVertex3f(0, 1, 0);  // red       │
  │      glColor3f(0, 1, 0);   glVertex3f(-1, -1, 0); // green    │
  │      glColor3f(0, 0, 1);   glVertex3f(1, -1, 0);  // blue     │
  │  glEnd();                                                       │
  │                                                                 │
  │  Between glBegin and glEnd:                                    │
  │  • glVertex — specify vertex position (REQUIRED)              │
  │  • glColor  — set vertex color                                │
  │  • glNormal — set vertex normal (for lighting)                │
  │  • glTexCoord — set texture coordinate                         │
  │                                                                 │
  │  NOTE: Most other gl* calls are NOT allowed between            │
  │  glBegin/glEnd (e.g., no glEnable, no glTranslate).           │
  └──────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.6  CALLBACK FUNCTIONS — EVENT-DRIVEN PROGRAMMING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  OpenGL/GLUT programs are event-driven: you register callback functions
  that GLUT calls when specific events occur.


  ► Display Callback
  ───────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  void display() {                                              │
  │      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);      │
  │      // ... draw geometry ...                                  │
  │      glutSwapBuffers();  // if double-buffered                 │
  │  }                                                              │
  │  // Register: glutDisplayFunc(display);                        │
  │  // Trigger redraw: glutPostRedisplay();                       │
  └──────────────────────────────────────────────────────────────────┘


  ► Keyboard Callback
  ────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  void keyboard(unsigned char key, int x, int y) {              │
  │      switch (key) {                                            │
  │          case 27:  exit(0);  break;  // ESC key                │
  │          case 'r': angle += 5; break;                          │
  │      }                                                          │
  │      glutPostRedisplay();                                      │
  │  }                                                              │
  │  // Register: glutKeyboardFunc(keyboard);                      │
  └──────────────────────────────────────────────────────────────────┘


  ► Mouse Callback
  ─────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  void mouse(int button, int state, int x, int y) {            │
  │      if (button == GLUT_LEFT_BUTTON && state == GLUT_DOWN) {   │
  │          // left click at (x, y)                               │
  │      }                                                          │
  │  }                                                              │
  │  // Register: glutMouseFunc(mouse);                            │
  └──────────────────────────────────────────────────────────────────┘


  ► Reshape Callback
  ───────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  void reshape(int w, int h) {                                  │
  │      glViewport(0, 0, w, h);                                   │
  │      glMatrixMode(GL_PROJECTION);                              │
  │      glLoadIdentity();                                         │
  │      gluPerspective(60, (float)w/h, 0.1, 100);               │
  │      glMatrixMode(GL_MODELVIEW);                               │
  │  }                                                              │
  │  // Register: glutReshapeFunc(reshape);                        │
  └──────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.7  TRANSFORMATION FUNCTIONS IN OPENGL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  OpenGL maintains a matrix stack. Transformations are applied by
  MULTIPLYING the current matrix on the stack.

  ┌──────────────────────────────────┬────────────────────────────────────────┐
  │  FUNCTION                        │  EFFECT                               │
  ├──────────────────────────────────┼────────────────────────────────────────┤
  │  glMatrixMode(GL_MODELVIEW)      │  Switch to model-view matrix         │
  │  glMatrixMode(GL_PROJECTION)     │  Switch to projection matrix         │
  ├──────────────────────────────────┼────────────────────────────────────────┤
  │  glLoadIdentity()                │  Reset current matrix to identity    │
  ├──────────────────────────────────┼────────────────────────────────────────┤
  │  glTranslatef(tx, ty, tz)        │  Multiply by translation matrix     │
  ├──────────────────────────────────┼────────────────────────────────────────┤
  │  glRotatef(angle, x, y, z)       │  Rotate by angle° about axis (x,y,z)│
  ├──────────────────────────────────┼────────────────────────────────────────┤
  │  glScalef(sx, sy, sz)            │  Multiply by scaling matrix         │
  ├──────────────────────────────────┼────────────────────────────────────────┤
  │  glPushMatrix()                  │  Push copy of current matrix         │
  │  glPopMatrix()                   │  Restore previous matrix             │
  ├──────────────────────────────────┼────────────────────────────────────────┤
  │  gluLookAt(ex,ey,ez,             │  Set up camera (view matrix)        │
  │            cx,cy,cz,             │  eye, center, up                     │
  │            ux,uy,uz)             │                                      │
  └──────────────────────────────────┴────────────────────────────────────────┘


  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  IMPORTANT — REVERSE ORDER:                                            ║
  ║                                                                        ║
  ║  OpenGL applies transforms in REVERSE order of how they appear in     ║
  ║  code. The LAST transform written is applied FIRST to the object.     ║
  ║                                                                        ║
  ║  Example — Rotate then Translate:                                      ║
  ║    glTranslatef(5, 0, 0);  // applied SECOND                         ║
  ║    glRotatef(45, 0, 0, 1); // applied FIRST                          ║
  ║    drawObject();                                                       ║
  ║                                                                        ║
  ║  Object is rotated 45° FIRST, then translated by (5,0,0).            ║
  ║                                                                        ║
  ║  This is because OpenGL post-multiplies:                              ║
  ║    M = M_current × M_new                                              ║
  ║  So the vertex sees: v' = T × R × v                                  ║
  ╚══════════════════════════════════════════════════════════════════════════╝



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.8  PROJECTION SETUP IN OPENGL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Perspective Projection
  ─────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  glMatrixMode(GL_PROJECTION);                                  │
  │  glLoadIdentity();                                             │
  │                                                                 │
  │  // Method 1: gluPerspective                                   │
  │  gluPerspective(fovy, aspect, zNear, zFar);                    │
  │    // fovy   = field of view in Y direction (degrees)          │
  │    // aspect = width / height                                  │
  │    // zNear  = near clipping plane (must be > 0)               │
  │    // zFar   = far clipping plane                              │
  │                                                                 │
  │  // Method 2: glFrustum                                        │
  │  glFrustum(left, right, bottom, top, near, far);               │
  │    // defines the 6 planes of the view frustum                 │
  └──────────────────────────────────────────────────────────────────┘


  ► Orthographic Projection
  ──────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  glMatrixMode(GL_PROJECTION);                                  │
  │  glLoadIdentity();                                             │
  │                                                                 │
  │  // 3D orthographic                                            │
  │  glOrtho(left, right, bottom, top, near, far);                 │
  │                                                                 │
  │  // 2D orthographic (simpler — for 2D programs)                │
  │  gluOrtho2D(left, right, bottom, top);                         │
  │    // near = -1, far = 1 (default)                             │
  └──────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.9  LIGHTING IN OPENGL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  OpenGL's fixed-function pipeline implements the Phong illumination model
  (ambient + diffuse + specular) directly.

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  SETUP STEPS:                                                          │
  │                                                                         │
  │  1. Enable lighting:    glEnable(GL_LIGHTING);                        │
  │  2. Enable a light:     glEnable(GL_LIGHT0);  // up to GL_LIGHT7     │
  │  3. Set light properties:                                              │
  │     glLightfv(GL_LIGHT0, GL_AMBIENT,  ambient_array);                 │
  │     glLightfv(GL_LIGHT0, GL_DIFFUSE,  diffuse_array);                 │
  │     glLightfv(GL_LIGHT0, GL_SPECULAR, specular_array);                │
  │     glLightfv(GL_LIGHT0, GL_POSITION, position_array);                │
  │                                                                         │
  │  4. Set material properties:                                           │
  │     glMaterialfv(GL_FRONT, GL_AMBIENT,   mat_ambient);                │
  │     glMaterialfv(GL_FRONT, GL_DIFFUSE,   mat_diffuse);                │
  │     glMaterialfv(GL_FRONT, GL_SPECULAR,  mat_specular);               │
  │     glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);              │
  │                                                                         │
  │  LIGHT POSITION:                                                       │
  │  • position[3] = 1.0  →  Positional light (point source)             │
  │  • position[3] = 0.0  →  Directional light (like the sun)            │
  └─────────────────────────────────────────────────────────────────────────┘


  ► Shading Model Selection
  ──────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  glShadeModel(GL_SMOOTH);  // Gouraud shading (default)        │
  │  glShadeModel(GL_FLAT);    // Flat shading                     │
  │                                                                 │
  │  NOTE: OpenGL's fixed-function pipeline does NOT support       │
  │  true Phong shading (per-pixel normal interpolation). For      │
  │  that, you need a fragment shader in GLSL (modern OpenGL).     │
  └──────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.10  GLUT MENUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ┌──────────────────────────────────────────────────────────────────┐
  │  void menuCallback(int value) {                                │
  │      switch(value) {                                           │
  │          case 1: glClearColor(1, 0, 0, 1); break;  // Red      │
  │          case 2: glClearColor(0, 1, 0, 1); break;  // Green    │
  │          case 3: exit(0); break;                                │
  │      }                                                          │
  │      glutPostRedisplay();                                      │
  │  }                                                              │
  │                                                                 │
  │  // In main():                                                 │
  │  int menu = glutCreateMenu(menuCallback);                      │
  │  glutAddMenuEntry("Red Background", 1);                        │
  │  glutAddMenuEntry("Green Background", 2);                      │
  │  glutAddMenuEntry("Exit", 3);                                  │
  │  glutAttachMenu(GLUT_RIGHT_BUTTON);                            │
  │                                                                 │
  │  // Sub-menus:                                                 │
  │  int subMenu = glutCreateMenu(subMenuCallback);                │
  │  glutAddMenuEntry("Option A", 10);                             │
  │  glutAddMenuEntry("Option B", 11);                             │
  │  glutCreateMenu(mainMenuCallback);                             │
  │  glutAddSubMenu("Sub Menu →", subMenu);                       │
  │  glutAttachMenu(GLUT_RIGHT_BUTTON);                            │
  └──────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.11  MODERN OPENGL — SHADERS, VBOs, VAOs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► 7.11.1  GLSL — OpenGL Shading Language
  ──────────────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────────┐
│  GLSL is a C-like programming language used to write shaders that run    │
│  directly on the GPU. Shaders are small programs that process vertices   │
│  (vertex shader) and fragments/pixels (fragment shader).                  │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Vertex Shader — Runs once per vertex
  ────────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  // Minimal Vertex Shader (GLSL 330)                           │
  │  #version 330 core                                              │
  │                                                                 │
  │  layout(location = 0) in vec3 aPos;      // vertex position   │
  │  layout(location = 1) in vec3 aColor;    // vertex color      │
  │                                                                 │
  │  out vec3 vertexColor;    // pass to fragment shader            │
  │                                                                 │
  │  uniform mat4 model;      // model transform                   │
  │  uniform mat4 view;       // view (camera) transform           │
  │  uniform mat4 projection; // projection matrix                 │
  │                                                                 │
  │  void main() {                                                 │
  │      gl_Position = projection * view * model * vec4(aPos, 1.0);│
  │      vertexColor = aColor;                                     │
  │  }                                                              │
  └──────────────────────────────────────────────────────────────────┘


  ► Fragment Shader — Runs once per fragment (potential pixel)
  ─────────────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  // Minimal Fragment Shader (GLSL 330)                         │
  │  #version 330 core                                              │
  │                                                                 │
  │  in vec3 vertexColor;     // received from vertex shader       │
  │  out vec4 FragColor;      // final pixel color                 │
  │                                                                 │
  │  void main() {                                                 │
  │      FragColor = vec4(vertexColor, 1.0);  // RGB + alpha       │
  │  }                                                              │
  └──────────────────────────────────────────────────────────────────┘


  ► GLSL Variable Types
  ──────────────────────

  ┌──────────────────────┬─────────────────────────────────────────────────┐
  │  QUALIFIER           │  PURPOSE                                       │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  in                  │  Input variable (from previous stage or VBO)   │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  out                 │  Output variable (to next stage)               │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  uniform             │  Global variable set by CPU. Same for all      │
  │                      │  vertices/fragments in a draw call.            │
  │                      │  Example: MVP matrices, light positions.       │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  vec2, vec3, vec4    │  Vector types (2, 3, 4 components)             │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  mat2, mat3, mat4    │  Matrix types (2×2, 3×3, 4×4)                 │
  ├──────────────────────┼─────────────────────────────────────────────────┤
  │  sampler2D           │  Texture sampler                               │
  └──────────────────────┴─────────────────────────────────────────────────┘


  ► 7.11.2  VBO — Vertex Buffer Object
  ──────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  A VBO stores vertex data (positions, colors, normals, UVs) in GPU   │
  │  memory instead of sending it from CPU every frame.                    │
  │                                                                         │
  │  Why: glBegin/glEnd sends data to GPU every frame (slow!).            │
  │  VBOs upload data ONCE, then the GPU uses it directly.                │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────┐
  │  // Create and fill a VBO                                      │
  │  float vertices[] = {                                          │
  │       0.0f,  0.5f, 0.0f,  // top vertex                       │
  │      -0.5f, -0.5f, 0.0f,  // bottom-left                      │
  │       0.5f, -0.5f, 0.0f   // bottom-right                     │
  │  };                                                             │
  │                                                                 │
  │  GLuint VBO;                                                   │
  │  glGenBuffers(1, &VBO);                  // generate buffer ID │
  │  glBindBuffer(GL_ARRAY_BUFFER, VBO);     // bind buffer        │
  │  glBufferData(GL_ARRAY_BUFFER,           // upload data        │
  │               sizeof(vertices),                                 │
  │               vertices,                                         │
  │               GL_STATIC_DRAW);           // data won't change  │
  └──────────────────────────────────────────────────────────────────┘


  ► 7.11.3  VAO — Vertex Array Object
  ─────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  A VAO stores the CONFIGURATION of vertex attributes — which VBOs    │
  │  to use, how the data is laid out, and which shader inputs they map   │
  │  to. Think of it as a "saved state" for vertex setup.                 │
  │                                                                         │
  │  Without VAO: You must re-bind VBOs and re-configure attributes      │
  │  every draw call.                                                      │
  │  With VAO: Just bind the VAO and draw — all config is recalled.      │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────────────────────────────────────────────────────┐
  │  GLuint VAO;                                                   │
  │  glGenVertexArrays(1, &VAO);                                   │
  │  glBindVertexArray(VAO);          // bind VAO                  │
  │                                                                 │
  │  // Set up VBO (see above)                                     │
  │  glBindBuffer(GL_ARRAY_BUFFER, VBO);                           │
  │                                                                 │
  │  // Configure vertex attribute 0 (position)                    │
  │  glVertexAttribPointer(                                        │
  │      0,               // attribute index (matches shader)      │
  │      3,               // 3 components (x, y, z)                │
  │      GL_FLOAT,        // data type                             │
  │      GL_FALSE,        // don't normalize                       │
  │      3*sizeof(float), // stride (bytes between vertices)       │
  │      (void*)0         // offset in buffer                      │
  │  );                                                             │
  │  glEnableVertexAttribArray(0);                                 │
  │                                                                 │
  │  glBindVertexArray(0);  // unbind VAO                          │
  │                                                                 │
  │  // DRAWING (in display callback):                             │
  │  glBindVertexArray(VAO);                                       │
  │  glDrawArrays(GL_TRIANGLES, 0, 3);  // draw 3 vertices        │
  │  glBindVertexArray(0);                                         │
  └──────────────────────────────────────────────────────────────────┘


  ► VBO vs. VAO — Quick Comparison
  ──────────────────────────────────

  ┌────────────────────────┬──────────────────────────┬──────────────────────┐
  │  PROPERTY              │  VBO                     │  VAO                 │
  ├────────────────────────┼──────────────────────────┼──────────────────────┤
  │  Stores                │  Actual vertex DATA      │  Attribute CONFIG    │
  │                        │  (positions, colors)     │  (how to interpret   │
  │                        │                          │  VBO data)           │
  ├────────────────────────┼──────────────────────────┼──────────────────────┤
  │  Lives on              │  GPU memory              │  GPU state object    │
  ├────────────────────────┼──────────────────────────┼──────────────────────┤
  │  Analogy               │  A data file on disk     │  A bookmark pointing │
  │                        │                          │  to the file + how   │
  │                        │                          │  to read it          │
  ├────────────────────────┼──────────────────────────┼──────────────────────┤
  │  Required in           │  Always                  │  Mandatory in        │
  │                        │                          │  OpenGL 3.x+         │
  └────────────────────────┴──────────────────────────┴──────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  7.12  COMPLETE OPENGL PROGRAM — ANNOTATED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ┌──────────────────────────────────────────────────────────────────┐
  │  #include <GL/glut.h>                                          │
  │                                                                 │
  │  float angle = 0.0f;                                           │
  │                                                                 │
  │  void display() {                                              │
  │      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);      │
  │      glLoadIdentity();                                         │
  │                                                                 │
  │      // Set up camera                                          │
  │      gluLookAt(0, 0, 5,  0, 0, 0,  0, 1, 0);                │
  │                                                                 │
  │      // Apply rotation (user-controlled)                       │
  │      glRotatef(angle, 0, 1, 0);                               │
  │                                                                 │
  │      // Draw a colored triangle                                │
  │      glBegin(GL_TRIANGLES);                                    │
  │          glColor3f(1, 0, 0);  glVertex3f( 0,  1, 0);         │
  │          glColor3f(0, 1, 0);  glVertex3f(-1, -1, 0);         │
  │          glColor3f(0, 0, 1);  glVertex3f( 1, -1, 0);         │
  │      glEnd();                                                   │
  │                                                                 │
  │      glutSwapBuffers();                                        │
  │  }                                                              │
  │                                                                 │
  │  void keyboard(unsigned char key, int x, int y) {             │
  │      if (key == 'r') angle += 5.0f;                           │
  │      if (key == 27) exit(0);  // ESC                           │
  │      glutPostRedisplay();                                      │
  │  }                                                              │
  │                                                                 │
  │  void reshape(int w, int h) {                                  │
  │      glViewport(0, 0, w, h);                                   │
  │      glMatrixMode(GL_PROJECTION);                              │
  │      glLoadIdentity();                                         │
  │      gluPerspective(60, (double)w/h, 0.1, 100);              │
  │      glMatrixMode(GL_MODELVIEW);                               │
  │  }                                                              │
  │                                                                 │
  │  int main(int argc, char** argv) {                             │
  │      glutInit(&argc, argv);                                    │
  │      glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH);│
  │      glutInitWindowSize(800, 600);                             │
  │      glutCreateWindow("OpenGL Demo");                          │
  │                                                                 │
  │      glEnable(GL_DEPTH_TEST);  // enable z-buffer              │
  │      glClearColor(0, 0, 0, 1); // black background            │
  │                                                                 │
  │      glutDisplayFunc(display);                                 │
  │      glutReshapeFunc(reshape);                                 │
  │      glutKeyboardFunc(keyboard);                               │
  │                                                                 │
  │      glutMainLoop();                                           │
  │      return 0;                                                 │
  │  }                                                              │
  └──────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHAPTER SUMMARY — QUICK REVISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ┌────────────────────────────┬──────────────────────────────────────────────┐
  │  TOPIC                     │  KEY POINTS TO REMEMBER                     │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  OpenGL Architecture       │  State machine; GPU-accelerated;           │
  │                            │  cross-platform; Khronos Group             │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Naming Convention         │  gl*, glu*, glut*, GL_*; suffix = type    │
  │                            │  (f=float, i=int); number = components    │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  GLUT                      │  Window creation, callbacks, menus,       │
  │                            │  built-in 3D shapes; glutMainLoop()       │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Double Buffering          │  GLUT_DOUBLE; draw to back buffer,        │
  │                            │  glutSwapBuffers(); no flicker             │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Primitives                │  GL_POINTS, GL_LINES, GL_TRIANGLES,       │
  │                            │  GL_TRIANGLE_STRIP, GL_TRIANGLE_FAN,      │
  │                            │  GL_QUADS, GL_POLYGON (last 2 deprecated) │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Transforms                │  glTranslatef, glRotatef, glScalef;       │
  │                            │  REVERSE ORDER; glPushMatrix/glPopMatrix  │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Projection                │  gluPerspective (perspective);            │
  │                            │  glOrtho (orthographic);                  │
  │                            │  set in GL_PROJECTION matrix mode        │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Lighting                  │  glEnable(GL_LIGHTING/GL_LIGHT0);         │
  │                            │  set light + material properties;         │
  │                            │  GL_SMOOTH = Gouraud, GL_FLAT = flat      │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  GLSL                      │  C-like shader language; vertex shader    │
  │                            │  + fragment shader; in/out/uniform vars   │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  VBO                       │  Vertex data stored on GPU; upload once,  │
  │                            │  draw many times; replaces glBegin/glEnd  │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  VAO                       │  Stores vertex attribute configuration;   │
  │                            │  bind VAO → all VBO config is recalled   │
  └────────────────────────────┴──────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                         END OF CHAPTER 7                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝


---

## 📝 Exam Practice Questions

### From AI-Generated Sets (aiQuestions.txt)

**Set 1, Q6b:**
Explain the basic architecture and rendering pipeline of OpenGL. What role do callback functions play in OpenGL programming?

**Set 2, Q6b:**
How are basic geometric transformations (translation, rotation, scaling) implemented in OpenGL? Explain the significance of glPushMatrix() and glPopMatrix().

**Set 3, Q6b:**
Explain how lighting and material properties are set up in OpenGL. What is the role of glLightfv() and glMaterialfv() functions?

**Set 4, Q6b:**
What are the different projection functions available in OpenGL? Explain gluPerspective() and glOrtho() with their parameters and typical use cases.

**Set 5, Q6b:**
Explain how double buffering and animation are achieved in OpenGL using GLUT. Describe the role of glutSwapBuffers() and glutIdleFunc() in smooth animation.

**Set 6, Q6b:**
Describe the different output primitives available in OpenGL (GL_POINTS, GL_LINES, GL_TRIANGLES, GL_QUADS, GL_POLYGON, etc.). Write sample code to draw a filled triangle with per-vertex coloring.

**Set 7, Q6b:**
How does OpenGL implement the Phong illumination model? Explain the functions used to set up lights (glLightfv) and materials (glMaterialfv) with their parameters.

**Set 8, Q6b:**
Explain the role of GLUT callback functions in OpenGL. Describe glutDisplayFunc(), glutReshapeFunc(), glutKeyboardFunc(), and glutMouseFunc() with their usage.

**Set 9, Q6b:**
Write the structure of an OpenGL program to draw a 3D cube with basic lighting. Explain the role of glEnable(GL_LIGHTING), glEnable(GL_DEPTH_TEST), and gluLookAt() in the program.

**Set 10, Q6b:**
How are perspective and orthographic projections set up in OpenGL? Explain gluPerspective(), glOrtho(), and gluLookAt() with their parameters and typical usage in a 3D scene.

---

### From Past Papers (Questions.txt)

**Set 1, Q6b:**
What is the significance of OpenGL in computer graphics? Discuss the Open Graphics Library in detail with the different features associated with it.

**Set 2, Q6b:**
Why do we need a machine-independent graphical language? Explain the rendering pipeline of OpenGL.

---

### Related Short Notes Topics (from Q7)
- OpenGL lighting and material setup — *aiQ Set 6*
