
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            CHAPTER 6 — GRAPHICAL STANDARDS                                 ║
║                                                                            ║
║            CMP 234 · Pokhara University · BE Computer                      ║
║            Syllabus Hours: 3                                               ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝


This chapter covers standardization in computer graphics — why standards
are needed, the major standards (GKS, PHIGS), language bindings, modern
standards, and graphics file formats.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6.1  NEED FOR MACHINE-INDEPENDENT GRAPHICAL STANDARDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  THE PROBLEM:                                                              │
│                                                                            │
│  In the early days of CG, every graphics hardware manufacturer had its    │
│  own proprietary API and command set. A program written for one device    │
│  would NOT work on another. Developers had to rewrite their graphics     │
│  code for each new system.                                                 │
│                                                                            │
│  THE SOLUTION: Machine-independent graphics standards that provide a     │
│  common interface between applications and hardware.                      │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Why Standards Are Needed
  ───────────────────────────

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  1. PORTABILITY:     Code runs on different hardware without changes.  │
  │  2. INTEROPERABILITY: Different software can exchange graphics data.   │
  │  3. REDUCED COST:    Write once, run anywhere; no vendor lock-in.     │
  │  4. DEVICE INDEPENDENCE: Application code separated from hardware.    │
  │  5. LONGEVITY:       Standard-based code remains usable for years.    │
  │  6. EDUCATION:       Common framework for teaching and learning.      │
  └──────────────────────────────────────────────────────────────────────────┘


  ► Graphics System Architecture
  ───────────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  ┌─────────────────────┐                                         │
  │  │  APPLICATION         │  ← user's graphics program             │
  │  │  PROGRAM             │                                         │
  │  └────────┬────────────┘                                         │
  │           │ function calls                                        │
  │  ┌────────▼────────────┐                                         │
  │  │  GRAPHICS            │  ← STANDARD INTERFACE (GKS/PHIGS/     │
  │  │  STANDARD API        │    OpenGL) provides device-independent │
  │  └────────┬────────────┘    functions                            │
  │           │ translated commands                                   │
  │  ┌────────▼────────────┐                                         │
  │  │  DEVICE DRIVER       │  ← hardware-specific translation       │
  │  └────────┬────────────┘                                         │
  │           │                                                       │
  │  ┌────────▼────────────┐                                         │
  │  │  OUTPUT DEVICE       │  ← screen, printer, plotter            │
  │  └─────────────────────┘                                         │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6.2  GKS — GRAPHICAL KERNEL SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  GKS (1977, ISO standard 1985) was the FIRST international standard      │
│  for computer graphics. It was developed by ISO (International            │
│  Organization for Standardization) as ISO 7942.                           │
│                                                                            │
│  It provides a set of FUNCTIONS for 2D graphics that are independent     │
│  of any particular hardware device.                                       │
└─────────────────────────────────────────────────────────────────────────────┘


  ► GKS Core Concepts
  ─────────────────────

  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  CONCEPT               │  DESCRIPTION                                │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Workstation           │  An abstract representation of a physical   │
  │                        │  device (screen, plotter, etc.). GKS can   │
  │                        │  output to multiple workstations.           │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Output Primitives     │  Polyline, Polymarker, Fill Area, Text     │
  │                        │  — the basic drawing elements.             │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Segments              │  Groups of output primitives that can be   │
  │                        │  stored, transformed, and manipulated.     │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Transformations       │  Normalization (world → NDC) and           │
  │                        │  Workstation (NDC → device coordinates).   │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Input Functions       │  6 logical input classes: Locator, Stroke, │
  │                        │  Valuator, Choice, Pick, String            │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Input Modes           │  Request (wait), Sample (poll), Event      │
  │                        │  (queue-based)                              │
  └────────────────────────┴──────────────────────────────────────────────┘


  ► GKS Coordinate Systems
  ──────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  World Coordinates (WC) ──► NDC ──► Device Coordinates (DC)     │
  │       (user-defined)   Normalization    Workstation              │
  │                        Transform       Transform                 │
  │                                                                   │
  │  NDC = Normalized Device Coordinates (0.0 to 1.0 range)         │
  │  This two-stage mapping allows device independence.              │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► GKS Levels
  ──────────────

  GKS defines implementation levels based on input and output capabilities:

  ┌──────────┬──────────────────────────────────────────────────────────────┐
  │  LEVEL   │  DESCRIPTION                                               │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  Level 0 │  Minimal output only (draw primitives)                     │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  Level 1 │  Level 0 + segment storage and manipulation                │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  Level 2 │  Level 1 + full segment operations (rename, transform)     │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  Input   │  a: no input, b: request input, c: request + sample +     │
  │  Levels  │  event input (appended to output level, e.g., "2c")       │
  └──────────┴──────────────────────────────────────────────────────────────┘


  ► GKS Limitations
  ──────────────────

    ✗ Only supports 2D graphics — no 3D capabilities.
    ✗ No support for hierarchical object modeling.
    ✗ Limited to flat, non-interactive rendering.
    ✗ Superseded by PHIGS for 3D applications.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6.3  PHIGS — PROGRAMMER'S HIERARCHICAL INTERACTIVE GRAPHICS SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  PHIGS (ISO 9592, 1989) extends GKS to support 3D graphics and           │
│  HIERARCHICAL modeling. An extended version, PHIGS+, adds lighting,      │
│  shading, and advanced rendering.                                         │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Key Features of PHIGS
  ─────────────────────────

  ┌────────────────────────────┬──────────────────────────────────────────────┐
  │  FEATURE                   │  DESCRIPTION                                │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  3D Graphics Support       │  All operations work in 3D space.          │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Hierarchical Modeling     │  Objects organized as a TREE (Structure    │
  │                            │  Network). Parent transforms cascade       │
  │                            │  to children — like a scene graph.        │
  │                            │  Example: car body → wheels → bolts       │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Centralized Structure     │  CSS stores all graphical data. Can be    │
  │  Store (CSS)               │  modified dynamically for animation.      │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Structure Elements        │  Primitives (polyline3, fill3), attributes,│
  │                            │  transforms, labels, pick IDs stored as   │
  │                            │  elements in structures.                   │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Dynamic Editing           │  Structures can be edited element-by-      │
  │                            │  element using an "element pointer."       │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  PHIGS+ Extensions         │  Lighting, shading, curved surfaces,      │
  │                            │  depth cueing, color mapping.              │
  └────────────────────────────┴──────────────────────────────────────────────┘


  ► PHIGS Hierarchical Modeling Example
  ──────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  Structure: ROBOT                                                │
  │  ├── Transform: position robot in world                          │
  │  ├── Structure: BODY                                             │
  │  │   ├── Fill3: torso polygon                                    │
  │  │   ├── Structure: LEFT_ARM                                     │
  │  │   │   ├── Transform: shoulder rotation                        │
  │  │   │   ├── Fill3: upper arm                                    │
  │  │   │   └── Structure: LEFT_HAND                                │
  │  │   │       ├── Transform: wrist rotation                       │
  │  │   │       └── Fill3: hand polygon                             │
  │  │   └── Structure: RIGHT_ARM                                    │
  │  │       └── ... (similar hierarchy)                             │
  │  └── Structure: HEAD                                             │
  │      └── Fill3: head polygon                                     │
  │                                                                   │
  │  Rotating the shoulder automatically rotates the entire arm      │
  │  and hand — transforms propagate DOWN the hierarchy.             │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6.4  GKS vs. PHIGS COMPARISON
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ┌────────────────────────┬──────────────────────┬──────────────────────┐
  │  PROPERTY              │  GKS                 │  PHIGS               │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Dimension             │  2D only             │  3D                  │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  ISO Standard          │  ISO 7942 (1985)     │  ISO 9592 (1989)     │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Object Model          │  Flat segments       │  Hierarchical        │
  │                        │  (no nesting)        │  structures          │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Data Storage          │  GKS Metafile        │  Centralized         │
  │                        │                      │  Structure Store     │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Dynamic Editing       │  Limited             │  Full element-level  │
  │                        │                      │  editing             │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Lighting/Shading      │  No                  │  Yes (PHIGS+)        │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Complexity            │  Simpler             │  More complex        │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Use Case              │  Simple 2D drawings  │  Complex 3D models,  │
  │                        │                      │  CAD, simulation     │
  └────────────────────────┴──────────────────────┴──────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6.5  LANGUAGE BINDINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  A language binding specifies how the abstract functions of a graphics    │
│  standard (GKS, PHIGS) are mapped to a specific programming language.    │
│                                                                            │
│  The standard defines WHAT functions exist and WHAT they do; the          │
│  language binding defines HOW they are called in a particular language.   │
└─────────────────────────────────────────────────────────────────────────────┘


  ┌──────────────────────┬────────────────────────────────────────────────┐
  │  LANGUAGE            │  BINDING NOTES                                │
  ├──────────────────────┼────────────────────────────────────────────────┤
  │  Fortran             │  The first official binding for GKS.          │
  │                      │  ISO 8651-1.                                  │
  ├──────────────────────┼────────────────────────────────────────────────┤
  │  C                   │  ISO 8651-3. C binding for GKS. Functions    │
  │                      │  use prefix gks_ (e.g., gks_polyline).       │
  ├──────────────────────┼────────────────────────────────────────────────┤
  │  Pascal              │  ISO 8651-2.                                  │
  ├──────────────────────┼────────────────────────────────────────────────┤
  │  Ada                 │  ISO 8651-4.                                  │
  └──────────────────────┴────────────────────────────────────────────────┘

  Example of language binding difference:
  • Abstract function: "POLYLINE(n, x_array, y_array)"
  • C binding:         gks_polyline(n, x, y);
  • Fortran binding:   CALL GPL(N, PX, PY)



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6.6  MODERN GRAPHICS STANDARDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  GKS and PHIGS are largely historical. Modern graphics use:

  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  STANDARD              │  DESCRIPTION                                │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  OpenGL                │  Khronos Group. Cross-platform, open-source│
  │  (1992–present)        │  3D graphics API. Works on Windows, Linux, │
  │                        │  macOS. Industry standard for decades.     │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Vulkan (2016)         │  Khronos Group. Low-level successor to     │
  │                        │  OpenGL. More control, less overhead.       │
  │                        │  Better multi-threading support.           │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  DirectX / Direct3D    │  Microsoft. Windows/Xbox exclusive. Widely │
  │  (1995–present)        │  used in PC gaming. DirectX 12 is low-level│
  │                        │  like Vulkan. Includes Direct3D for 3D.    │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Metal (2014)          │  Apple. Low-level API for macOS/iOS. Apple │
  │                        │  deprecated OpenGL in favor of Metal.      │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  WebGL (2011)          │  Web-based 3D graphics using JavaScript.   │
  │                        │  Based on OpenGL ES. Runs in browsers.     │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  WebGPU (2023)         │  Modern web GPU API. Successor to WebGL.   │
  │                        │  Exposes modern GPU features in browsers.  │
  └────────────────────────┴──────────────────────────────────────────────┘


  ► Evolution Timeline
  ─────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  1977 ─── GKS developed (2D only)                               │
  │  1985 ─── GKS becomes ISO standard                              │
  │  1989 ─── PHIGS becomes ISO standard (3D, hierarchical)          │
  │  1992 ─── OpenGL 1.0 released (Silicon Graphics)                │
  │  1995 ─── DirectX 1.0 (Microsoft)                               │
  │  2004 ─── OpenGL 2.0 (programmable shaders — GLSL)              │
  │  2011 ─── WebGL 1.0 (3D in browsers)                            │
  │  2014 ─── Metal (Apple)                                          │
  │  2016 ─── Vulkan 1.0 (Khronos)                                  │
  │  2023 ─── WebGPU (modern web graphics)                          │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6.7  GRAPHICS FILE FORMATS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► 6.7.1  Raster (Bitmap) Formats
  ──────────────────────────────────

  Store images as a grid of pixels. Each pixel has a color value.

  ┌──────────┬──────────────────────────────────────────────────────────────┐
  │  FORMAT  │  DESCRIPTION                                               │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  BMP     │  Bitmap. Uncompressed, large files. Windows native format. │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  JPEG    │  Joint Photographic Experts Group. LOSSY compression.      │
  │          │  Great for photographs. Small file size. No transparency.  │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  PNG     │  Portable Network Graphics. LOSSLESS compression.          │
  │          │  Supports alpha transparency. Good for web graphics.       │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  GIF     │  Graphics Interchange Format. Lossless, but limited to    │
  │          │  256 colors. Supports animation frames.                    │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  TIFF    │  Tagged Image File Format. High quality, large files.     │
  │          │  Used in printing and publishing. Supports layers.         │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  WebP    │  Google format. Both lossy and lossless. Better           │
  │          │  compression than JPEG/PNG. Supports animation/alpha.     │
  └──────────┴──────────────────────────────────────────────────────────────┘


  ► 6.7.2  Vector Formats
  ─────────────────────────

  Store images as mathematical descriptions (points, lines, curves, shapes).
  Infinitely scalable without quality loss.

  ┌──────────┬──────────────────────────────────────────────────────────────┐
  │  FORMAT  │  DESCRIPTION                                               │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  SVG     │  Scalable Vector Graphics. XML-based, open standard.      │
  │          │  Used on the web. Editable with text editors.              │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  AI      │  Adobe Illustrator. Proprietary vector format.            │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  EPS     │  Encapsulated PostScript. Used in professional printing.  │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  PDF     │  Portable Document Format. Can contain both vector and    │
  │          │  raster elements. Universal document format.               │
  └──────────┴──────────────────────────────────────────────────────────────┘


  ► 6.7.3  3D Model Formats
  ───────────────────────────

  ┌──────────┬──────────────────────────────────────────────────────────────┐
  │  FORMAT  │  DESCRIPTION                                               │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  OBJ     │  Wavefront. Simple text-based format for 3D geometry.     │
  │          │  Stores vertices, normals, texture coords, faces.          │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  STL     │  Stereolithography. Used in 3D printing. Only stores     │
  │          │  triangle meshes (no color/texture).                       │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  FBX     │  Autodesk. Supports meshes, materials, animation, bones. │
  │          │  Widely used in games and film.                            │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  glTF    │  GL Transmission Format. "JPEG of 3D." Efficient, web-   │
  │          │  friendly, JSON-based. Khronos standard.                  │
  ├──────────┼──────────────────────────────────────────────────────────────┤
  │  COLLADA │  COLLAborative Design Activity. XML-based interchange     │
  │  (.dae)  │  format. Khronos standard. Used for data exchange.        │
  └──────────┴──────────────────────────────────────────────────────────────┘


  ► Raster vs. Vector Comparison
  ───────────────────────────────

  ┌────────────────────────┬──────────────────────┬──────────────────────┐
  │  PROPERTY              │  RASTER              │  VECTOR              │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Stored as             │  Pixel grid          │  Math descriptions  │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Scaling               │  Quality degrades    │  Infinite, lossless │
  │                        │  (pixelation)        │                      │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  File size             │  Large (more pixels  │  Small (geometric   │
  │                        │  = larger file)      │  descriptions only) │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Best for              │  Photos, complex     │  Logos, icons, text │
  │                        │  images, screenshots │  illustrations      │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Editing               │  Pixel by pixel      │  Object by object  │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Examples              │  JPEG, PNG, BMP      │  SVG, AI, EPS       │
  └────────────────────────┴──────────────────────┴──────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  6.8  DATA VISUALIZATION AND SCENE GRAPHS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Data Visualization
  ─────────────────────

  Converting abstract data into visual representations to make patterns,
  trends, and insights more understandable.

  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  TECHNIQUE             │  USE CASE                                   │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  2D Charts/Graphs      │  Bar, line, pie, scatter — statistical data│
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  3D Volume Rendering   │  Medical imaging (CT, MRI), fluid dynamics │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Isosurface Rendering  │  Surfaces of constant value in 3D data     │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Scientific Vis.       │  Weather maps, molecular structures,       │
  │                        │  terrain models, flow visualization        │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Information Vis.      │  Network graphs, treemaps, heatmaps        │
  └────────────────────────┴──────────────────────────────────────────────┘


  ► Scene Graphs
  ───────────────

  A scene graph is a hierarchical data structure (tree or DAG) that
  organizes the spatial and logical representation of a graphical scene.

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  Structure:                                                            │
  │                                                                         │
  │  ◆ Root Node: The scene or world.                                     │
  │  ◆ Group Nodes: Apply transforms, visibility, or effects              │
  │    to all children.                                                     │
  │  ◆ Leaf Nodes: Actual geometry (meshes, primitives),                  │
  │    lights, cameras.                                                     │
  │                                                                         │
  │  Key Properties:                                                       │
  │  • Transform inheritance: child inherits parent's transform           │
  │  • Efficient culling: entire branches can be skipped                  │
  │  • Reuse: same geometry node referenced by multiple parents (DAG)    │
  │  • Used by: game engines (Unity, Unreal), 3D tools (Blender),        │
  │    PHIGS, OpenSceneGraph, Three.js                                    │
  └─────────────────────────────────────────────────────────────────────────┘


  ► Color Spaces and Standards
  ─────────────────────────────

  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  COLOR SPACE           │  PURPOSE                                    │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  sRGB                  │  Standard for monitors and web. Default     │
  │                        │  color space for almost all displays.       │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Adobe RGB             │  Wider gamut than sRGB. Used in             │
  │                        │  professional photography and printing.     │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  DCI-P3               │  Cinema standard. Used in HDR displays.    │
  │                        │  Wider than sRGB.                           │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Rec. 709              │  HDTV standard. Matches sRGB primaries.    │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Rec. 2020             │  Ultra HD / 4K TV standard. Very wide      │
  │                        │  gamut covering most visible colors.        │
  └────────────────────────┴──────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHAPTER SUMMARY — QUICK REVISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ┌────────────────────────────┬──────────────────────────────────────────────┐
  │  TOPIC                     │  KEY POINTS TO REMEMBER                     │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Machine Independence      │  Standards separate application from       │
  │                            │  hardware; enable portability              │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  GKS                       │  First ISO standard (1985); 2D only;      │
  │                            │  workstations, segments, 6 input classes   │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  PHIGS                     │  3D + hierarchical modeling; CSS; PHIGS+   │
  │                            │  adds lighting/shading; ISO 9592           │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Language Binding          │  Maps abstract functions to specific        │
  │                            │  programming language (C, Fortran, etc.)   │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Modern Standards          │  OpenGL, Vulkan, DirectX, Metal, WebGL    │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Raster Formats            │  BMP, JPEG (lossy), PNG (lossless+alpha), │
  │                            │  GIF (256 colors), TIFF                    │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Vector Formats            │  SVG (web), AI (Adobe), EPS, PDF          │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  3D Formats                │  OBJ, STL, FBX, glTF, COLLADA             │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Scene Graphs              │  Tree/DAG of transforms + geometry;       │
  │                            │  used by game engines and PHIGS            │
  └────────────────────────────┴──────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                         END OF CHAPTER 6                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝


---

## 📝 Exam Practice Questions

### From AI-Generated Sets (aiQuestions.txt)

**Set 2, Q6a:**
What is GKS (Graphical Kernel System) and its features? What are the different levels of GKS implementation?

**Set 3, Q6a:**
What is PHIGS (Programmer's Hierarchical Interactive Graphics System)? How does it extend GKS with hierarchical modeling and 3D support?

**Set 4, Q6a:**
Discuss the need for graphics file format standards. Compare raster and vector graphics file formats with examples of each.

**Set 5, Q6a:**
What is data visualization? Explain different techniques used for visualizing scalar and vector datasets with examples.

**Set 6, Q6a:**
Explain the concept of language binding in graphical standards. What is the difference between GKS and PHIGS in terms of capabilities and features?

**Set 7, Q6a:**
Discuss the visualization of data sets. What role does computer graphics play in scientific visualization? Give real-world examples.

**Set 8, Q6a:**
Compare RGB and CMYK color models. Explain how colors are represented and converted between these two models.

**Set 9, Q6a:**
What are graphical software standards? Why is software portability important in graphics programming? Explain with reference to GKS and PHIGS.

**Set 10, Q6a:**
What is the need for machine-independent graphical languages? Discuss the features and architecture of OpenGL as a modern graphical standard.

---

### From Past Papers (Questions.txt)

**Set 1, Q6a:**
Discuss the need for machine-independent graphical languages. Explain two different graphical software standards.

**Set 3, Q4b** *(standards topic):*
Why do we need a machine-independent graphical language? Explain two different graphical software standards.

---

### Related Short Notes Topics (from Q7)
- Color models (RGB and CMYK) — *aiQ Set 1*
- Graphics file formats — *aiQ Set 1, Q Set 1*
- CMYK color model — *aiQ Set 4*
- PHIGS standard — *aiQ Set 7*
- RGB color model — *aiQ Set 10*
- Color Models — *Q Set 1*
