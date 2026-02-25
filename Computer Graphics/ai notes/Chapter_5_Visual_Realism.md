
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            CHAPTER 5 — VISUAL REALISM                                      ║
║                                                                            ║
║            CMP 234 · Pokhara University · BE Computer                      ║
║            Syllabus Hours: 7                                               ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝


This chapter deals with making 3D scenes look realistic. It covers hidden
surface removal (eliminating occluded faces), illumination and shading
models (simulating light interaction), color models, ray tracing, and
shadow generation.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.1  HIDDEN SURFACE REMOVAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  WHY HIDDEN SURFACE REMOVAL?                                               │
│                                                                            │
│  When rendering a 3D scene, some surfaces are obscured by others from     │
│  the viewer's perspective. Without hidden surface removal, overlapping    │
│  objects render on top of each other incorrectly, destroying the illusion │
│  of depth and solidity. HSR determines which surfaces are visible and     │
│  which are hidden, ensuring correct visual output.                        │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Classification of HSR Algorithms
  ────────────────────────────────────

  ┌──────────────────────┬────────────────────┬──────────────────────────────┐
  │  CATEGORY            │  WORKS IN          │  EXAMPLES                    │
  ├──────────────────────┼────────────────────┼──────────────────────────────┤
  │  Object-Space        │  3D world coords;  │  Back-face detection,        │
  │  Methods             │  compares objects   │  Depth sorting (Painter's)  │
  │                      │  against each other │                             │
  ├──────────────────────┼────────────────────┼──────────────────────────────┤
  │  Image-Space         │  2D screen coords; │  Z-buffer, A-buffer,        │
  │  Methods             │  per-pixel testing  │  Scan-line method           │
  └──────────────────────┴────────────────────┴──────────────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.1.1  BACK-FACE DETECTION (CULLING)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  The simplest hidden surface method. Eliminates polygons facing AWAY from
  the viewer — these are the "back faces" of a closed solid object.

  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  ALGORITHM:                                                            ║
  ║                                                                        ║
  ║  1. Compute the surface normal N of each polygon.                      ║
  ║  2. Compute the view vector V from the polygon to the viewer.          ║
  ║  3. Calculate dot product: D = N · V                                   ║
  ║                                                                        ║
  ║  Decision:                                                             ║
  ║    If D > 0  →  Front face (VISIBLE)   — normal faces toward viewer   ║
  ║    If D < 0  →  Back face  (HIDDEN)    — normal faces away            ║
  ║    If D = 0  →  Edge-on   (usually hidden)                            ║
  ║                                                                        ║
  ║  Simplified test (if viewer is along -Z direction):                    ║
  ║    If N_z > 0  →  front face (visible)                                ║
  ║    If N_z ≤ 0  →  back face (hidden)                                  ║
  ╚══════════════════════════════════════════════════════════════════════════╝

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │        N ↗ (normal)         N ↙ (normal)                         │
  │       ╱                       ╲                                   │
  │      ╱  polygon                 ╲  polygon                       │
  │     ╱───────────              ───╲────────                       │
  │                                                                   │
  │    D = N·V > 0              D = N·V < 0                          │
  │    → FRONT FACE             → BACK FACE                          │
  │    → VISIBLE                → HIDDEN                             │
  │                                                                   │
  │              ◄──── V (viewer direction)                           │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘

  Limitations:
    ✗ Only works for convex closed objects — for concave objects, a front
      face might still be occluded by another front face.
    ✗ Does NOT handle occlusion between different objects.
    ✗ Typically used as a PRE-PROCESSING step to eliminate ~50% of
      polygons before applying a more thorough method.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.1.2  Z-BUFFER (DEPTH BUFFER) METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  The most widely used HSR algorithm. Implemented in ALL modern GPU hardware.

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  DATA STRUCTURES:                                                      │
  │                                                                         │
  │  1. Frame Buffer (FB):  Stores the COLOR at each pixel (x, y).        │
  │  2. Z-Buffer (ZB):     Stores the DEPTH (z-value) at each pixel.     │
  │                                                                         │
  │  Both are initialized at the start:                                    │
  │    FB(x, y) = background color                                        │
  │    ZB(x, y) = z_far (maximum depth — farthest possible value)         │
  └─────────────────────────────────────────────────────────────────────────┘


  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  ALGORITHM:                                                            ║
  ║                                                                        ║
  ║  Initialize:                                                           ║
  ║    For every pixel (x, y):                                             ║
  ║      ZB(x, y) = MAX_DEPTH  (e.g., infinity or 1.0 in normalized)     ║
  ║      FB(x, y) = background_color                                      ║
  ║                                                                        ║
  ║  For each polygon P in the scene:                                      ║
  ║    For each pixel (x, y) covered by P:                                ║
  ║      Calculate z_depth of P at (x, y)                                 ║
  ║      If z_depth < ZB(x, y):       // closer to viewer                ║
  ║        ZB(x, y) = z_depth         // update depth                     ║
  ║        FB(x, y) = color of P      // update color                     ║
  ║      // else: pixel is behind existing surface — ignore               ║
  ║                                                                        ║
  ║  Display frame buffer contents.                                        ║
  ╚══════════════════════════════════════════════════════════════════════════╝


  ┌────────────────────────┬───────────────────────────────────────────────┐
  │  ADVANTAGE             │  DETAILS                                     │
  ├────────────────────────┼───────────────────────────────────────────────┤
  │  Simple                │  Easy to implement, very parallelizable     │
  │  Hardware support      │  Built into all GPUs natively               │
  │  No sorting needed     │  Polygons can be processed in any order     │
  │  Handles any geometry  │  Works for any polygon, intersecting ones   │
  │  O(n) per polygon      │  Per-pixel comparison only                  │
  ├────────────────────────┼───────────────────────────────────────────────┤
  │  DISADVANTAGE          │  DETAILS                                     │
  ├────────────────────────┼───────────────────────────────────────────────┤
  │  Memory usage          │  Needs extra buffer (same size as screen)   │
  │  Z-fighting            │  Surfaces at similar depths cause flicker   │
  │  No transparency       │  Cannot handle semi-transparent objects     │
  │                        │  (handled by A-buffer instead)              │
  │  Precision issues      │  Limited depth precision (24/32-bit float)  │
  └────────────────────────┴───────────────────────────────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.1.3  A-BUFFER METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  An extension of the Z-buffer that handles TRANSPARENCY and ANTIALIASING.
  The "A" stands for "Anti-aliased, Area-averaged, Accumulation buffer."

  Each pixel stores a LINKED LIST of fragments instead of a single depth:

  ┌───────────────────────────────────────────────────────────────────┐
  │  PIXEL (x, y):                                                   │
  │                                                                   │
  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                   │
  │  │ z = 3.2  │───►│ z = 5.7  │───►│ z = 8.1  │───► NULL         │
  │  │ color    │    │ color    │    │ color    │                    │
  │  │ opacity  │    │ opacity  │    │ opacity  │                    │
  │  │ coverage │    │ coverage │    │ coverage │                    │
  │  └──────────┘    └──────────┘    └──────────┘                   │
  │                                                                   │
  │  Fragments sorted front to back. Final color is computed by      │
  │  compositing all fragments using their opacity values.           │
  └───────────────────────────────────────────────────────────────────┘

  Compositing (front-to-back alpha blending):
    C_out = C_front × α + C_behind × (1 - α)

  ┌────────────────────────┬──────────────────────┬──────────────────────┐
  │  PROPERTY              │  Z-BUFFER            │  A-BUFFER            │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Storage per pixel     │  Single z + color    │  Linked list of      │
  │                        │                      │  fragments           │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Transparency          │  Not supported       │  Fully supported    │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Anti-aliasing         │  No                  │  Yes (area coverage)│
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Memory                │  Fixed               │  Variable (dynamic)  │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Speed                 │  Faster              │  Slower              │
  └────────────────────────┴──────────────────────┴──────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.1.4  SCAN-LINE METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  Processes the image one scan line at a time (horizontally, top to bottom).
  For each scan line, it determines which surfaces are visible.

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ALGORITHM:                                                            │
  │                                                                         │
  │  1. Create an Edge Table (ET) sorted by minimum y-coordinate.          │
  │  2. For each scan line y:                                              │
  │     a. Move edges from ET to Active Edge List (AEL) when y = y_min.   │
  │     b. For overlapping polygon spans on this scan line:               │
  │        - If only ONE polygon: fill with its color.                    │
  │        - If MULTIPLE polygons overlap: compare depths at that x       │
  │          to determine which is visible.                                │
  │     c. Remove edges where y = y_max.                                  │
  │     d. Update x-intercepts.                                           │
  │                                                                         │
  │  Advantage: Processes one scan line at a time — needs only one line   │
  │  of depth values in memory (not a full z-buffer).                     │
  └─────────────────────────────────────────────────────────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.1.5  DEPTH SORTING (PAINTER'S ALGORITHM)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  Works like a painter: draw the farthest objects first, then closer objects
  on top of them ("back-to-front" rendering).

  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  ALGORITHM:                                                            ║
  ║                                                                        ║
  ║  1. Sort all polygons by their farthest z-value (back to front).      ║
  ║  2. Resolve any depth ambiguities (overlapping z-ranges):             ║
  ║     a. Check if x-extents overlap.                                    ║
  ║     b. Check if y-extents overlap.                                    ║
  ║     c. If both overlap, check if one is entirely in front of other.   ║
  ║     d. If ambiguous, split the polygon and re-sort.                   ║
  ║  3. Render polygons from farthest to nearest.                         ║
  ╚══════════════════════════════════════════════════════════════════════════╝

  ┌────────────────────────────────────────────────────────────────────┐
  │  Advantages:    ✓ Handles transparency (just blend as you paint) │
  │                 ✓ Conceptually simple                             │
  │  Disadvantages: ✗ O(n log n) sorting                             │
  │                 ✗ Fails for cyclic overlap (A in front of B,     │
  │                   B in front of C, C in front of A)              │
  │                 ✗ Requires polygon splitting for ambiguous cases  │
  └────────────────────────────────────────────────────────────────────┘


  ► Comprehensive Comparison of HSR Methods
  ──────────────────────────────────────────

  ┌──────────────────┬──────────────┬───────────┬──────────────┬──────────────┐
  │  METHOD          │  SPACE       │  SPEED    │  TRANSPARENCY│  HARDWARE    │
  ├──────────────────┼──────────────┼───────────┼──────────────┼──────────────┤
  │  Back-Face       │  Object      │  Very Fast│  N/A (pre-   │  Yes         │
  │  Detection       │              │  O(n)     │  processing) │              │
  ├──────────────────┼──────────────┼───────────┼──────────────┼──────────────┤
  │  Z-Buffer        │  Image       │  Fast     │  No          │  Yes (GPU)   │
  │                  │              │  O(n·k)   │              │              │
  ├──────────────────┼──────────────┼───────────┼──────────────┼──────────────┤
  │  A-Buffer        │  Image       │  Moderate │  Yes         │  Limited     │
  ├──────────────────┼──────────────┼───────────┼──────────────┼──────────────┤
  │  Scan-Line       │  Image       │  Fast     │  No          │  No          │
  ├──────────────────┼──────────────┼───────────┼──────────────┼──────────────┤
  │  Depth Sorting   │  Object+     │  Moderate │  Yes         │  No          │
  │  (Painter's)     │  Image       │  O(n lg n)│              │              │
  └──────────────────┴──────────────┴───────────┴──────────────┴──────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.2  ILLUMINATION MODEL (PHONG ILLUMINATION)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  The Phong Illumination Model calculates the intensity (color/brightness)
  of light at a surface point by combining three components:


  ► The Three Components
  ───────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  1. AMBIENT LIGHT (Iₐ)                                          │
  │     Background illumination present everywhere equally.          │
  │     Does not depend on light position, surface orientation,      │
  │     or viewer position.                                          │
  │                                                                   │
  │     Formula:  Iₐ = kₐ · Lₐ                                     │
  │                                                                   │
  │     kₐ = ambient reflection coefficient (material property)     │
  │     Lₐ = ambient light intensity                                 │
  │                                                                   │
  │  ─────────────────────────────────────────────────────────────── │
  │                                                                   │
  │  2. DIFFUSE REFLECTION (I_d) — Lambert's Law                    │
  │     Light scattered equally in all directions from rough         │
  │     surfaces. Depends on angle between light and surface normal. │
  │                                                                   │
  │     Formula:  I_d = k_d · L_d · max(0, N̂ · L̂)                 │
  │                                                                   │
  │     k_d = diffuse reflection coefficient                        │
  │     L_d = diffuse light intensity                               │
  │     N̂   = unit surface normal                                    │
  │     L̂   = unit vector from surface to light source               │
  │     cos θ = N̂ · L̂  (Lambert's cosine law)                       │
  │                                                                   │
  │  ─────────────────────────────────────────────────────────────── │
  │                                                                   │
  │  3. SPECULAR REFLECTION (Iₛ) — Shiny Highlights                 │
  │     Mirror-like reflection; depends on view direction.           │
  │     Creates bright spots (specular highlights).                  │
  │                                                                   │
  │     Formula:  Iₛ = kₛ · Lₛ · max(0, R̂ · V̂)ⁿ                    │
  │                                                                   │
  │     kₛ = specular reflection coefficient                        │
  │     Lₛ = specular light intensity                               │
  │     R̂   = reflection vector = 2(N̂ · L̂)N̂ - L̂                    │
  │     V̂   = unit vector from surface to viewer                    │
  │     n   = shininess exponent (higher = tighter highlight)       │
  │           ◆ n = 1-10:  dull/matte                               │
  │           ◆ n = 100+:  mirror-like                              │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                                                                        ║
  ║  COMPLETE PHONG ILLUMINATION EQUATION:                                 ║
  ║                                                                        ║
  ║  I = kₐ·Lₐ + k_d·L_d·(N̂ · L̂) + kₛ·Lₛ·(R̂ · V̂)ⁿ                     ║
  ║                                                                        ║
  ║    = AMBIENT + DIFFUSE + SPECULAR                                      ║
  ║                                                                        ║
  ║  For multiple light sources:                                           ║
  ║                                                                        ║
  ║  I = kₐ·Lₐ + Σᵢ [k_d·L_dᵢ·(N̂ · L̂ᵢ) + kₛ·Lₛᵢ·(R̂ᵢ · V̂)ⁿ]          ║
  ║                                                                        ║
  ╚══════════════════════════════════════════════════════════════════════════╝


  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  VECTOR DIAGRAM:                                                 │
  │                                                                   │
  │                    N (normal)                                     │
  │                    ↑                                              │
  │          L ↗       │       ↖ R (reflection)                      │
  │         ╱  θ       │    θ   ╲                                     │
  │        ╱           │         ╲                                    │
  │  ─────╱────────────┼──────────╲─────── surface                   │
  │                    │           ╲                                  │
  │               Light│            ╲                                 │
  │              direction          V̂ (to viewer)                    │
  │                                                                   │
  │  θ = angle of incidence = angle of reflection                    │
  │  α = angle between R̂ and V̂  (specular depends on this)          │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Solved Example 1 — Basic Illumination
  ─────────────────────────────────────────

  Given: kₐ=0.2, k_d=0.5, kₛ=0.3, n=10
         Lₐ=0.1, L_d=0.8, Lₛ=1.0
         N̂·L̂ = cos 30° = 0.866
         R̂·V̂ = cos 15° = 0.966

  I = (0.2)(0.1) + (0.5)(0.8)(0.866) + (0.3)(1.0)(0.966)¹⁰
    = 0.02 + 0.3464 + 0.3 × (0.966)¹⁰
    = 0.02 + 0.3464 + 0.3 × 0.708
    = 0.02 + 0.3464 + 0.2124
    = 0.5788

  Breakdown: Ambient=0.02, Diffuse=0.3464, Specular=0.2124


  ► Solved Example 2 — Two Light Sources
  ────────────────────────────────────────

  Light source 1: L_d1=0.6, N̂·L̂₁=0.5, Lₛ₁=0.8, R̂₁·V̂=0.8
  Light source 2: L_d2=0.4, N̂·L̂₂=0.7, Lₛ₂=0.6, R̂₂·V̂=0.3
  Material: kₐ=0.1, k_d=0.6, kₛ=0.4, n=5, Lₐ=0.2

  Ambient = 0.1 × 0.2 = 0.02

  Light 1:
    Diffuse1  = 0.6 × 0.6 × 0.5 = 0.18
    Specular1 = 0.4 × 0.8 × (0.8)⁵ = 0.32 × 0.3277 = 0.1049

  Light 2:
    Diffuse2  = 0.6 × 0.4 × 0.7 = 0.168
    Specular2 = 0.4 × 0.6 × (0.3)⁵ = 0.24 × 0.00243 = 0.0006

  Total = 0.02 + 0.18 + 0.1049 + 0.168 + 0.0006 = 0.4735


  ► Solved Example 3 — Effect of Shininess
  ──────────────────────────────────────────

  Same setup: kₛ=0.5, Lₛ=1.0, R̂·V̂=0.9

  ┌──────────────┬─────────────┬──────────────────────────────┐
  │  Shininess n │  (0.9)ⁿ     │  Specular = 0.5 × (0.9)ⁿ   │
  ├──────────────┼─────────────┼──────────────────────────────┤
  │  n = 1       │  0.900      │  0.450  (broad, dull)       │
  │  n = 5       │  0.590      │  0.295                      │
  │  n = 10      │  0.349      │  0.174                      │
  │  n = 50      │  0.005      │  0.003  (tight, sharp)     │
  │  n = 100     │  0.0000266  │  ≈ 0    (mirror-like)      │
  └──────────────┴─────────────┴──────────────────────────────┘

  Higher n = smaller, more focused specular highlight.


  ► Solved Example 4 — Finding the Reflection Vector
  ────────────────────────────────────────────────────

  Given: N̂ = (0, 1, 0)  (surface pointing up)
         L̂ = (0.577, 0.577, 0.577)  (light from upper-right-front)

  N̂ · L̂ = 0 × 0.577 + 1 × 0.577 + 0 × 0.577 = 0.577

  R̂ = 2(N̂ · L̂)N̂ - L̂
     = 2(0.577)(0, 1, 0) - (0.577, 0.577, 0.577)
     = (0, 1.154, 0) - (0.577, 0.577, 0.577)
     = (-0.577, 0.577, -0.577)

  The reflection vector mirrors L̂ about the normal.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.3  SHADING METHODS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


Shading determines HOW the illumination model is applied across polygon
surfaces. There are three main methods, trading off speed vs. quality.


  ► 5.3.1  Flat (Constant) Shading
  ─────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  • Calculate illumination ONCE per polygon (using polygon normal).    │
  │  • Entire polygon gets the same color.                                 │
  │  • Individual polygon facets are visible (faceted appearance).        │
  │  • Very fast — one illumination calculation per polygon.              │
  │                                                                         │
  │  Best for: Quick previews, flat surfaces (walls, floors),             │
  │            situations where speed > quality.                           │
  └─────────────────────────────────────────────────────────────────────────┘


  ► 5.3.2  Gouraud Shading (Smooth / Intensity Interpolation)
  ────────────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ALGORITHM:                                                            │
  │                                                                         │
  │  1. Compute vertex normals by AVERAGING the normals of all            │
  │     polygons sharing that vertex:                                      │
  │                                                                         │
  │     N_v = (N₁ + N₂ + N₃ + ... + Nₖ) / |N₁ + N₂ + ... + Nₖ|         │
  │                                                                         │
  │     where N₁...Nₖ are normals of the k polygons meeting at vertex.   │
  │                                                                         │
  │  2. Apply illumination model at EACH VERTEX to get vertex colors      │
  │     (I₁, I₂, I₃ for a triangle).                                     │
  │                                                                         │
  │  3. INTERPOLATE colors across the polygon interior:                   │
  │     a. Along edges (scanline-edge intersections)                      │
  │     b. Along scanlines (between edge intersections)                   │
  │                                                                         │
  │     Edge interpolation: Iₐ = I₁ + (y - y₁)/(y₂ - y₁) × (I₂ - I₁)  │
  │     Scanline interp.:   Iₚ = Iₐ + (x - xₐ)/(x_b - xₐ) × (I_b-Iₐ) │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  GOURAUD INTERPOLATION DIAGRAM:                                  │
  │                                                                   │
  │            I₁ (vertex 1)                                         │
  │           ╱╲                                                      │
  │          ╱  ╲                                                     │
  │     Iₐ ◆────◆ I_b    ← scan line, intensities interpolated      │
  │        ╱ ·Iₚ· ╲         along edges then across scan line        │
  │       ╱        ╲                                                  │
  │      ╱──────────╲                                                 │
  │    I₂            I₃ (vertex intensities)                         │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Solved Example — Gouraud Interpolation
  ──────────────────────────────────────────

  Triangle vertices: V₁(10, 40, I=1.0), V₂(10, 10, I=0.2), V₃(30, 10, I=0.6)
  Find intensity at pixel (20, 25).

  At scan line y = 25:
    Edge V₁→V₂: x stays at 10, y goes 40→10
      Iₐ = 1.0 + (25-40)/(10-40) × (0.2-1.0)
         = 1.0 + (-15)/(-30) × (-0.8) = 1.0 + 0.5 × (-0.8) = 0.6

    Edge V₁→V₃: parametric approach
      t = (25-40)/(10-40) = 0.5
      x_b = 10 + 0.5(30-10) = 20
      I_b = 1.0 + 0.5(0.6-1.0) = 0.8

    At x = 20 (between xₐ=10 and x_b=20):
      Iₚ = 0.6 + (20-10)/(20-10) × (0.8-0.6) = 0.6 + 1.0 × 0.2 = 0.8

  Intensity at (20, 25) = 0.8


  ► 5.3.3  Phong Shading (Normal-Vector Interpolation)
  ─────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  ALGORITHM:                                                            │
  │                                                                         │
  │  1. Compute vertex normals (same as Gouraud step 1).                  │
  │  2. INTERPOLATE NORMALS across the polygon (not colors!).             │
  │     N_interp = (1-t)N₁ + t·N₂   (then normalize!)                    │
  │  3. Apply illumination model at EVERY PIXEL using the                 │
  │     interpolated normal at that pixel.                                 │
  │                                                                         │
  │  Key difference from Gouraud: Gouraud interpolates COLORS,           │
  │  Phong interpolates NORMALS and recomputes illumination per pixel.    │
  └─────────────────────────────────────────────────────────────────────────┘

  Result: Much better specular highlights (specular spot can appear in the
  middle of a polygon, which Gouraud cannot produce).


  ► Solved Example — Phong Normal Interpolation
  ───────────────────────────────────────────────

  Vertex normals: N₁ = (0, 0, 1), N₂ = (1, 0, 0)
  At t = 0.5:
      N_interp = 0.5(0,0,1) + 0.5(1,0,0) = (0.5, 0, 0.5)
      Normalize: |(0.5, 0, 0.5)| = √(0.25+0+0.25) = √0.5 = 0.707
      N̂ = (0.707, 0, 0.707)

  Now use this normal in the full Phong illumination equation at this pixel.


  ► Fast Phong Shading
  ─────────────────────

  Computing the full illumination equation at every pixel is expensive.
  Fast Phong approximates it using:
    ◆ Taylor series expansion of the illumination equation
    ◆ Pre-computed lookup tables for (R̂·V̂)ⁿ values
    ◆ Incremental computation across scan lines

  This reduces per-pixel cost while maintaining visual quality close
  to standard Phong shading.


  ► Comprehensive Shading Comparison
  ────────────────────────────────────

  ┌──────────────────┬──────────────────┬──────────────────┬──────────────────┐
  │  PROPERTY        │  FLAT            │  GOURAUD         │  PHONG           │
  ├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │  Computation     │  1 per polygon   │  1 per vertex    │  1 per pixel     │
  │  per             │                  │                  │                  │
  ├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │  What is         │  Nothing         │  Colors          │  Normals         │
  │  interpolated?   │  (uniform)       │  (intensities)   │  (vectors)       │
  ├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │  Specular        │  None (or per    │  Only at         │  At any pixel    │
  │  highlights      │  polygon)        │  vertices        │  (accurate)      │
  ├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │  Mach banding    │  Yes (visible    │  Reduced but     │  Eliminated      │
  │                  │  polygon edges)  │  still possible  │                  │
  ├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │  Quality         │  Lowest          │  Medium          │  Highest         │
  ├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │  Speed           │  Fastest         │  Medium          │  Slowest         │
  ├──────────────────┼──────────────────┼──────────────────┼──────────────────┤
  │  Use case        │  Real-time       │  Games, general  │  High-quality    │
  │                  │  previews        │  3D rendering    │  rendering       │
  └──────────────────┴──────────────────┴──────────────────┴──────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.4  COLOR MODELS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► 5.4.1  RGB Color Model (Additive)
  ────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │  Used by: Monitors, TV screens, projectors — any LIGHT EMITTING │
  │  device.                                                         │
  │                                                                   │
  │  Primary colors: Red, Green, Blue                                │
  │  Mixing model: ADDITIVE (adding more light = brighter)           │
  │                                                                   │
  │  R + G = Yellow       R + B = Magenta                            │
  │  G + B = Cyan         R + G + B = White                          │
  │  No light = Black                                                │
  │                                                                   │
  │  Each channel: 0–255 (8-bit) → 16.7 million colors total        │
  │                                                                   │
  │  RGB Cube:                                                       │
  │        Green (0,1,0)                                             │
  │           ╱│╲                                                     │
  │          ╱ │ ╲  → Yellow (1,1,0)                                 │
  │   Cyan ╱  │  ╲                                                   │
  │  (0,1,1)  │   Red (1,0,0)                                       │
  │           │  ╱                                                    │
  │           │ ╱  → Magenta (1,0,1)                                 │
  │    Blue ──┘╱                                                     │
  │   (0,0,1) ╱                                                      │
  │    Black (0,0,0) ─────── White (1,1,1) is diagonal corner       │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► 5.4.2  CMYK Color Model (Subtractive)
  ────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │  Used by: Printers, physical printing                            │
  │                                                                   │
  │  Primary colors: Cyan, Magenta, Yellow, Key (Black)              │
  │  Mixing model: SUBTRACTIVE (adding more ink = darker)            │
  │                                                                   │
  │  C + M = Blue        C + Y = Green                               │
  │  M + Y = Red         C + M + Y = muddy brown (theory: black)    │
  │  K (Key/Black) is added because CMY cannot produce true black.   │
  │  No ink = White (paper color)                                    │
  │                                                                   │
  │  Conversion from RGB to CMY:                                     │
  │    C = 1 - R,   M = 1 - G,   Y = 1 - B                         │
  └───────────────────────────────────────────────────────────────────┘


  ► Comparison
  ─────────────

  ┌────────────────────────┬──────────────────────┬──────────────────────┐
  │  PROPERTY              │  RGB                 │  CMYK                │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Type                  │  Additive            │  Subtractive         │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Base                  │  Light emission      │  Ink absorption      │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Default               │  Black (no light)    │  White (no ink)      │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  All colors mixed      │  White               │  Black (with K)      │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Used by               │  Screens, cameras    │  Printers, press     │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Channels              │  3 (R, G, B)         │  4 (C, M, Y, K)     │
  └────────────────────────┴──────────────────────┴──────────────────────┘


  ► Other Color Models
  ─────────────────────

  ┌────────────────────┬───────────────────────────────────────────────────┐
  │  MODEL             │  DESCRIPTION                                     │
  ├────────────────────┼───────────────────────────────────────────────────┤
  │  HSV / HSB         │  Hue (color), Saturation (purity), Value         │
  │                    │  (brightness). Intuitive for artists.            │
  ├────────────────────┼───────────────────────────────────────────────────┤
  │  HSL               │  Hue, Saturation, Lightness. Similar to HSV    │
  │                    │  but Lightness goes from black to white.        │
  ├────────────────────┼───────────────────────────────────────────────────┤
  │  CIE XYZ           │  Device-independent, standard reference model.  │
  │                    │  Encompasses all visible colors.                │
  ├────────────────────┼───────────────────────────────────────────────────┤
  │  CIE Lab           │  Perceptually uniform. Equal distances in the   │
  │                    │  color space = equal perceived differences.      │
  └────────────────────┴───────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.5  RAY TRACING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  DEFINITION                                                                │
│                                                                            │
│  Ray tracing is a rendering technique that traces the path of light       │
│  rays from the camera through each pixel into the scene. For each ray,   │
│  it computes intersections with objects, determines visibility, and       │
│  calculates illumination — including reflections, refractions, and       │
│  shadows.                                                                  │
└─────────────────────────────────────────────────────────────────────────────┘


  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  BASIC RAY TRACING ALGORITHM:                                          ║
  ║                                                                        ║
  ║  For each pixel (x, y) on the screen:                                  ║
  ║    1. Cast a ray from the eye through the pixel into the scene.       ║
  ║    2. Find the CLOSEST object intersection.                            ║
  ║    3. At the intersection point:                                       ║
  ║       a. Compute local illumination (ambient + diffuse + specular).   ║
  ║       b. If surface is REFLECTIVE: spawn a reflection ray and         ║
  ║          recursively trace it.                                         ║
  ║       c. If surface is TRANSPARENT: spawn a refraction ray and        ║
  ║          recursively trace it.                                         ║
  ║       d. Cast SHADOW RAYS toward each light source:                   ║
  ║          - If blocked by another object → point is in shadow          ║
  ║          - If not blocked → add light contribution                    ║
  ║    4. Combine all contributions for final pixel color.                 ║
  ║                                                                        ║
  ║  Recursion depth is limited to prevent infinite bouncing.              ║
  ╚══════════════════════════════════════════════════════════════════════════╝

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  RAY TRACING DIAGRAM:                                            │
  │                                                                   │
  │                    Light Source                                   │
  │                        ☼                                         │
  │                       ╱│                                          │
  │         Shadow ray → ╱ │                                         │
  │                     ╱  │  ← Shadow ray (blocked by Obj B)       │
  │              ╔═════╗   │                                         │
  │   Eye ──────►║Obj A║   │   ┌───────┐                            │
  │    ╲  primary║     ║   │   │ Obj B │                            │
  │     ╲  ray   ╚═════╝   │   └───────┘                            │
  │      ╲         │╲      │                                         │
  │       ╲        │ ╲ Reflection ray                                │
  │        ╲       │  ╲                                              │
  │         screen │   ╲→ more objects...                            │
  │                │ Refraction ray                                  │
  │                ↓                                                  │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Types of Rays
  ────────────────

  ┌──────────────────┬─────────────────────────────────────────────────────┐
  │  RAY TYPE        │  PURPOSE                                           │
  ├──────────────────┼─────────────────────────────────────────────────────┤
  │  Primary Ray     │  From eye through pixel to find first intersection │
  ├──────────────────┼─────────────────────────────────────────────────────┤
  │  Shadow Ray      │  From intersection to light — tests if in shadow  │
  ├──────────────────┼─────────────────────────────────────────────────────┤
  │  Reflection Ray  │  Bounced ray for mirror-like surfaces             │
  ├──────────────────┼─────────────────────────────────────────────────────┤
  │  Refraction Ray  │  Ray through transparent objects (Snell's Law)    │
  └──────────────────┴─────────────────────────────────────────────────────┘


  ► Advantages and Disadvantages
  ───────────────────────────────

  ┌────────────────────┬────────────────────────────────────────────────────┐
  │  ADVANTAGES        │  DISADVANTAGES                                    │
  ├────────────────────┼────────────────────────────────────────────────────┤
  │  ✓ Physically     │  ✗ Very computationally expensive                │
  │    accurate        │  ✗ Slow for real-time (improving with RTX GPUs) │
  │  ✓ Natural        │  ✗ Aliasing without supersampling               │
  │    reflections     │  ✗ Diffuse inter-reflection is costly           │
  │  ✓ Refractions    │    (path tracing/global illumination needed)     │
  │  ✓ Accurate       │                                                   │
  │    shadows         │                                                   │
  │  ✓ Easy to        │                                                   │
  │    implement       │                                                   │
  └────────────────────┴────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  5.6  SHADOW GENERATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  Shadows add significant realism to a scene. Two main techniques:


  ► Shadow Mapping (Image-Space)
  ───────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  TWO-PASS ALGORITHM:                                                   │
  │                                                                         │
  │  Pass 1: Render scene FROM THE LIGHT'S PERSPECTIVE.                   │
  │    → Store depth values in a "shadow map" (like a z-buffer from the  │
  │      light's viewpoint).                                               │
  │                                                                         │
  │  Pass 2: Render scene from the camera.                                │
  │    → For each visible pixel, transform to light's coordinate space.   │
  │    → Compare pixel's depth (from light) with shadow map value:       │
  │       - If pixel depth > shadow map depth → point is IN SHADOW       │
  │         (something is closer to the light, blocking it)               │
  │       - If pixel depth ≤ shadow map depth → point is LIT            │
  │                                                                         │
  │  Issues: Shadow acne (bias needed), aliasing (limited resolution),   │
  │          hard shadows only (no penumbra without extensions).          │
  └─────────────────────────────────────────────────────────────────────────┘


  ► Shadow Volumes (Object-Space)
  ────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  • For each occluding object, compute the volume of space that is     │
  │    in shadow (a "shadow volume").                                      │
  │  • Use the stencil buffer to track how many shadow volumes a pixel   │
  │    is inside.                                                          │
  │  • If inside ≥ 1 shadow volume → pixel is in shadow.                 │
  │  • Produces pixel-perfect shadows but expensive for complex scenes.  │
  └─────────────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OPENGL LAB — LIGHTING AND SHADING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► OpenGL Lighting Setup
  ────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  #include <GL/glut.h>                                          │
  │                                                                 │
  │  void initLighting() {                                         │
  │      glEnable(GL_LIGHTING);                                    │
  │      glEnable(GL_LIGHT0);                                      │
  │      glEnable(GL_DEPTH_TEST);                                  │
  │                                                                 │
  │      // Light properties                                       │
  │      GLfloat ambient[]  = {0.2, 0.2, 0.2, 1.0};              │
  │      GLfloat diffuse[]  = {0.8, 0.8, 0.8, 1.0};              │
  │      GLfloat specular[] = {1.0, 1.0, 1.0, 1.0};              │
  │      GLfloat position[] = {5.0, 5.0, 5.0, 1.0};              │
  │                                                                 │
  │      glLightfv(GL_LIGHT0, GL_AMBIENT,  ambient);              │
  │      glLightfv(GL_LIGHT0, GL_DIFFUSE,  diffuse);              │
  │      glLightfv(GL_LIGHT0, GL_SPECULAR, specular);             │
  │      glLightfv(GL_LIGHT0, GL_POSITION, position);             │
  │                                                                 │
  │      // Material properties                                    │
  │      GLfloat mat_ambient[]   = {0.2, 0.0, 0.0, 1.0};        │
  │      GLfloat mat_diffuse[]   = {0.8, 0.0, 0.0, 1.0};        │
  │      GLfloat mat_specular[]  = {1.0, 1.0, 1.0, 1.0};        │
  │      GLfloat mat_shininess[] = {50.0};                         │
  │                                                                 │
  │      glMaterialfv(GL_FRONT, GL_AMBIENT,   mat_ambient);       │
  │      glMaterialfv(GL_FRONT, GL_DIFFUSE,   mat_diffuse);       │
  │      glMaterialfv(GL_FRONT, GL_SPECULAR,  mat_specular);      │
  │      glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess);     │
  │  }                                                              │
  │                                                                 │
  │  void display() {                                              │
  │      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);      │
  │      glLoadIdentity();                                         │
  │      gluLookAt(3, 3, 5, 0, 0, 0, 0, 1, 0);                  │
  │                                                                 │
  │      // Smooth shading (Gouraud by default in OpenGL)          │
  │      glShadeModel(GL_SMOOTH);  // or GL_FLAT                   │
  │                                                                 │
  │      glutSolidSphere(1.0, 50, 50);  // lit sphere              │
  │      glutSwapBuffers();                                        │
  │  }                                                              │
  │                                                                 │
  │  int main(int argc, char** argv) {                             │
  │      glutInit(&argc, argv);                                    │
  │      glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH);           │
  │      glutInitWindowSize(600, 600);                             │
  │      glutCreateWindow("OpenGL Lighting");                      │
  │      initLighting();                                           │
  │      glutDisplayFunc(display);                                 │
  │      glutMainLoop();                                           │
  │      return 0;                                                 │
  │  }                                                              │
  │                                                                 │
  │  // GL_SMOOTH → Gouraud shading (default)                     │
  │  // GL_FLAT   → Flat shading                                   │
  │  // True Phong shading requires a fragment shader in           │
  │  // modern OpenGL (GLSL).                                      │
  └──────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHAPTER SUMMARY — QUICK REVISION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ┌────────────────────────────┬──────────────────────────────────────────────┐
  │  TOPIC                     │  KEY POINTS TO REMEMBER                     │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Back-Face Detection       │  N·V > 0 → visible; removes ~50%;         │
  │                            │  only for convex closed objects            │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Z-Buffer                  │  Per-pixel depth comparison; GPU native;   │
  │                            │  simple but no transparency                │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  A-Buffer                  │  Linked list per pixel; handles            │
  │                            │  transparency and anti-aliasing            │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Depth Sorting             │  Painter's: paint back-to-front;          │
  │                            │  handles transparency; O(n log n)          │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Phong Illumination        │  I = Ambient + Diffuse + Specular;        │
  │                            │  uses kₐ, k_d, kₛ, n coefficients        │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Flat Shading              │  1 color per polygon; fast; faceted       │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Gouraud Shading           │  Interpolate colors at vertices;          │
  │                            │  misses mid-polygon highlights            │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Phong Shading             │  Interpolate normals; per-pixel           │
  │                            │  illumination; best specular quality      │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  RGB / CMYK                │  Additive (screens) vs. Subtractive       │
  │                            │  (printers); C=1-R, M=1-G, Y=1-B        │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Ray Tracing               │  Trace rays: primary, shadow,             │
  │                            │  reflection, refraction; accurate but     │
  │                            │  expensive                                 │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Shadow Mapping            │  Two-pass: render from light, compare     │
  │                            │  depths; fast but aliasing issues         │
  └────────────────────────────┴──────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                         END OF CHAPTER 5                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝


---

## 📝 Exam Practice Questions

### From AI-Generated Sets (aiQuestions.txt)

**Set 1, Q5:**
a. Explain the A-Buffer method for hidden surface removal. How is it different from the Z-Buffer method?
b. Derive the Phong illumination model equation. Explain the role of ambient, diffuse, and specular components in visual realism.

**Set 1, Q6a** *(shading topic):*
What is Gouraud shading? Explain the intensity interpolation process with a triangular polygon example.

**Set 2, Q5:**
a. Explain the Depth Buffer (Z-Buffer) method for visible surface detection. What are its advantages and limitations?
b. Compare Flat shading, Gouraud shading, and Phong shading in terms of interpolation method, computation, and visual quality. Which produces the most realistic results and why?

**Set 3, Q5:**
a. Explain the Back-Face Detection method. For a polygon surface with vertices (1, 0, 1), (0, 1, 1), (0, 0, 0), determine whether the surface is visible from a viewpoint along the positive z-axis.
b. What is diffuse reflection? Derive Lambert's cosine law and explain its significance in the illumination model.

**Set 4, Q5:**
a. Explain the Scan Line method for visible surface detection with a detailed example. How does it use edge tables and active edge lists?
b. Explain specular reflection and the Phong reflection model. How does the shininess coefficient (n) affect the specular highlight on a surface?

**Set 5, Q5:**
a. What is the Depth Sorting (Painter's) algorithm? Describe the three overlap tests used to resolve ambiguity when surfaces overlap in depth.
b. Explain the concept of ambient light in the illumination model. How is the total intensity at a surface point calculated using the Phong model when multiple light sources are present?

**Set 6, Q5:**
a. Compare Back-Face Detection, Z-Buffer, and Depth Sorting methods for hidden surface removal in terms of accuracy, memory usage, and computational complexity.
b. What is Gouraud shading? Derive the intensity interpolation equations used in Gouraud shading along the edges and across scan lines for a triangular polygon.

**Set 7, Q5:**
a. Explain the A-Buffer method for hidden surface removal. How does it handle transparent surfaces differently from the Z-Buffer method?
b. What is the difference between an illumination model and a shading model? Explain constant (flat) shading and discuss its limitations.

**Set 8, Q5:**
a. Explain the Depth Sorting (Painter's) algorithm step by step. What are the limitations of this algorithm when surfaces cyclically overlap?
b. Derive the Phong illumination model. A surface has ambient reflectivity ka = 0.3, diffuse reflectivity kd = 0.5, specular reflectivity ks = 0.4, and shininess n = 32. If the ambient light intensity Ia = 0.2 and a point light source of intensity Ip = 0.8 makes an angle of 45 degrees with the normal, calculate the total reflected intensity (assume viewer direction coincides with the reflection direction).

**Set 9, Q5:**
a. Explain the Scan Line method for hidden surface removal. How are the active edge table and the polygon table used in this method?
b. What is Fast Phong shading? How does it approximate Phong shading to reduce computational cost while maintaining acceptable visual quality?

**Set 10, Q5:**
a. What is the Z-Buffer algorithm? Write the pseudocode and explain how the depth buffer is initialized and updated during rendering.
b. Explain the difference between Gouraud shading and Phong shading in terms of what is interpolated, computational cost, and visual quality. Illustrate the difference with a spherical object example.

---

### From Past Papers (Questions.txt)

**Set 1, Q5:**
a. Why is the Depth Sorting method called Painter's Algorithm? Explain the Scan Line method for visible surface detection with an example.
b. What is the difference between specular reflection versus diffuse reflection? Briefly explain polygon surface shading methods.

**Set 2, Q5:**
a. Why is the Depth Sorting method called Painter's Algorithm? Explain the Scan Line method for visible surface detection with an example.
b. Define specular reflection. Calculate the total intensity due to specular reflection caused by ambient light using the Phong model.

**Set 2, Q6a** *(shading topic):*
Compare Constant, Gouraud, and Phong shading. Also conclude the best model for shading and why.

**Set 3, Q5b** *(visible surface topic):*
Why is it required to detect visible surfaces in 3D viewing and not in 2D? How is the Back-Face Detection approach different from the Z-Buffer approach for detecting visible surfaces?

**Set 3, Q6b** *(illumination topic):*
What is an illumination model? Differentiate between Phong Shading and Gouraud Shading.

---

### Related Short Notes Topics (from Q7)
- Fast Phong shading — *aiQ Set 3*
- Depth cueing — *aiQ Set 5*
- Area subdivision method for visible surface detection — *aiQ Set 9*
- Specular Reflection — *Q Set 3*
- Area Subdivision Method — *Q Set 3*
