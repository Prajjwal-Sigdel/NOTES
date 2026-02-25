
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            CHAPTER 4 — GRAPHICS IN THREE DIMENSIONS                        ║
║                                                                            ║
║            CMP 234 · Pokhara University · BE Computer                      ║
║            Syllabus Hours: 8                                               ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝


This chapter extends 2D concepts into three dimensions. It covers 3D
coordinate systems, transformation matrices, surface representation methods
(polygons, Bezier curves, fractals), the 3D viewing pipeline, projection
types, and 3D clipping. Mastering this chapter is essential for understanding
how real-world objects are modeled, transformed, and projected onto a 2D
display.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.1  THREE DIMENSIONAL COORDINATE SYSTEMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Right-Hand vs. Left-Hand Coordinate Systems
  ──────────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  RIGHT-HAND SYSTEM (Standard in mathematics, OpenGL):            │
  │                                                                   │
  │       Y ↑                                                        │
  │         │    Z comes OUT of the screen (toward you)              │
  │         │   ╱                                                     │
  │         │  ╱                                                      │
  │         │╱                                                        │
  │         └──────────► X                                           │
  │        ╱                                                          │
  │       ╱ Z                                                        │
  │                                                                   │
  │  Rule: Curl right-hand fingers from X to Y → thumb points +Z    │
  │                                                                   │
  │  ─────────────────────────────────────────────────────────────── │
  │                                                                   │
  │  LEFT-HAND SYSTEM (DirectX, some game engines):                  │
  │                                                                   │
  │       Y ↑                                                        │
  │         │    Z goes INTO the screen (away from you)              │
  │         │                                                         │
  │         │                                                         │
  │         └──────────► X                                           │
  │               Z ↗ (into screen)                                  │
  │                                                                   │
  │  Rule: Curl left-hand fingers from X to Y → thumb points +Z     │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Key Differences
  ──────────────────

  ┌────────────────────────┬──────────────────────┬──────────────────────┐
  │  PROPERTY              │  RIGHT-HAND          │  LEFT-HAND           │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  +Z Direction          │  Out of screen       │  Into screen         │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Used by               │  OpenGL, Blender,    │  DirectX, Unity,     │
  │                        │  mathematics         │  Unreal Engine       │
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Cross product         │  X × Y = +Z          │  X × Y = -Z (or     │
  │                        │                      │  defined differently)│
  ├────────────────────────┼──────────────────────┼──────────────────────┤
  │  Positive rotation     │  Counterclockwise    │  Clockwise (when     │
  │                        │  (looking at origin  │  looking at origin   │
  │                        │  from +axis)         │  from +axis)         │
  └────────────────────────┴──────────────────────┴──────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.2  THREE DIMENSIONAL TRANSFORMATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


In 3D, we use 4×4 homogeneous matrices (extending the 3×3 matrices from 2D).
A 3D point (x, y, z) is represented as (x, y, z, 1) in homogeneous coords.


  ► 4.2.1  Translation
  ─────────────────────

      [1  0  0  tₓ] [x]   [x + tₓ]
      [0  1  0  tᵧ]·[y] = [y + tᵧ]
      [0  0  1  t_z] [z]   [z + t_z]
      [0  0  0   1] [1]   [  1   ]


  ► 4.2.2  Scaling
  ─────────────────

      [Sₓ  0   0   0] [x]   [Sₓ·x]
      [ 0  Sᵧ  0   0]·[y] = [Sᵧ·y]
      [ 0   0  S_z  0] [z]   [S_z·z]
      [ 0   0   0   1] [1]   [  1  ]


  ► 4.2.3  Rotation
  ──────────────────

  In 3D, rotation is about an AXIS (not a point like in 2D). The three
  fundamental rotations:

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │  Rotation about X-axis (Rₓ(θ)):      Y and Z rotate; X stays           │
  │                                                                         │
  │  [1     0       0     0]                                                │
  │  [0   cos θ  -sin θ   0]                                               │
  │  [0   sin θ   cos θ   0]                                               │
  │  [0     0       0     1]                                                │
  │                                                                         │
  │  ─────────────────────────────────────────────────────────────────────  │
  │                                                                         │
  │  Rotation about Y-axis (Rᵧ(θ)):      X and Z rotate; Y stays           │
  │                                                                         │
  │  [ cos θ   0   sin θ   0]                                              │
  │  [   0     1     0     0]                                               │
  │  [-sin θ   0   cos θ   0]                                              │
  │  [   0     0     0     1]                                               │
  │                                                                         │
  │  NOTE: The sin θ signs are SWAPPED compared to Rₓ and R_z.             │
  │  This is because Y = Z × X (cyclic order Z→X for Rᵧ).                 │
  │                                                                         │
  │  ─────────────────────────────────────────────────────────────────────  │
  │                                                                         │
  │  Rotation about Z-axis (R_z(θ)):      X and Y rotate; Z stays          │
  │                                                                         │
  │  [cos θ  -sin θ   0   0]                                               │
  │  [sin θ   cos θ   0   0]                                               │
  │  [  0       0     1   0]                                                │
  │  [  0       0     0   1]                                                │
  │                                                                         │
  │  This is identical to the 2D rotation matrix (extended to 4×4).         │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘


  ► 4.2.4  Reflection (3D)
  ─────────────────────────

  ┌───────────────────────┬──────────────────────────────────────────────────┐
  │  REFLECTION PLANE     │  MATRIX (negate the axis perpendicular to it)  │
  ├───────────────────────┼──────────────────────────────────────────────────┤
  │  About XY plane       │  diag(1, 1, -1, 1)   →  z' = -z              │
  │  (mirror on the       │                                                │
  │   floor / table)      │                                                │
  ├───────────────────────┼──────────────────────────────────────────────────┤
  │  About XZ plane       │  diag(1, -1, 1, 1)   →  y' = -y              │
  │  (mirror on the wall) │                                                │
  ├───────────────────────┼──────────────────────────────────────────────────┤
  │  About YZ plane       │  diag(-1, 1, 1, 1)   →  x' = -x              │
  │  (mirror on the side) │                                                │
  └───────────────────────┴──────────────────────────────────────────────────┘


  ► Solved Example 1 — 3D Translation
  ────────────────────────────────────

  Translate point (3, 5, 7) by (2, -1, 4):
      x' = 3 + 2 = 5,   y' = 5 - 1 = 4,   z' = 7 + 4 = 11
      Result: (5, 4, 11)


  ► Solved Example 2 — Rotation About Z-axis
  ────────────────────────────────────────────

  Rotate point (3, 4, 5) by 90° about Z-axis:

  cos 90° = 0,  sin 90° = 1

      x' = 3(0) - 4(1) = -4
      y' = 3(1) + 4(0) = 3
      z' = 5              (unchanged)

      Result: (-4, 3, 5)


  ► Solved Example 3 — 3D Scaling
  ────────────────────────────────

  Scale point (2, 3, 4) by factors Sₓ=2, Sᵧ=3, S_z=0.5:
      x' = 2×2 = 4,   y' = 3×3 = 9,   z' = 4×0.5 = 2
      Result: (4, 9, 2)


  ► Solved Example 4 — Composite 3D Transform
  ─────────────────────────────────────────────

  Rotate point (1, 0, 0) by 90° about X-axis, then translate by (0, 5, 0):

  Step 1: Rₓ(90°): x'=1, y'=0·cos90-0·sin90=0, z'=0·sin90+0·cos90=0
      → (1, 0, 0) stays the same (point is on the X-axis!)

  Better example: Rotate (0, 1, 0) by 90° about X-axis:
      x' = 0
      y' = 1·cos90 - 0·sin90 = 0
      z' = 1·sin90 + 0·cos90 = 1
      After rotation: (0, 0, 1)
  
  Then translate by (0, 5, 0): (0, 0+5, 1) = (0, 5, 1)



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.3  THREE DIMENSIONAL REPRESENTATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.3.1  POLYGON SURFACES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  Polygon surfaces are the most common way to represent 3D objects in      │
│  computer graphics. Any 3D shape is approximated as a mesh of flat        │
│  polygons (usually triangles). The more polygons used, the smoother       │
│  the approximation appears.                                                │
│                                                                            │
│  Even curved surfaces (spheres, cylinders) are rendered as triangulated   │
│  meshes by GPUs. Modern games use millions of triangles per frame.        │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Polygon Mesh Data Structures
  ───────────────────────────────

  A polygon mesh is stored using three tables:

  ┌─────────────────────────┬──────────────────────────────────────────────┐
  │  TABLE                   │  CONTENTS                                   │
  ├─────────────────────────┼──────────────────────────────────────────────┤
  │  Vertex Table            │  List of all unique vertices with their     │
  │                          │  (x, y, z) coordinates.                     │
  │                          │  V1(x₁,y₁,z₁), V2(x₂,y₂,z₂), ...        │
  ├─────────────────────────┼──────────────────────────────────────────────┤
  │  Edge Table              │  List of edges, each referencing two        │
  │                          │  vertex indices.                            │
  │                          │  E1(V1,V2), E2(V2,V3), ...                │
  ├─────────────────────────┼──────────────────────────────────────────────┤
  │  Face (Polygon) Table    │  List of faces, each referencing edges      │
  │                          │  or vertices that form the polygon.         │
  │                          │  F1(E1,E2,E3), F2(E3,E4,E5), ...          │
  └─────────────────────────┴──────────────────────────────────────────────┘


  ► Surface Normal Computation
  ─────────────────────────────

  The surface normal is a vector perpendicular to the polygon surface.
  It is essential for lighting calculations and back-face detection.

  Given three vertices V₁, V₂, V₃ of a polygon:

  Step 1: Compute two edge vectors:
      A = V₂ - V₁ = (x₂-x₁, y₂-y₁, z₂-z₁)
      B = V₃ - V₁ = (x₃-x₁, y₃-y₁, z₃-z₁)

  Step 2: Cross product  N = A × B:

  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                                                                        ║
  ║  N = A × B = (Aᵧ·B_z - A_z·Bᵧ,  A_z·Bₓ - Aₓ·B_z,  Aₓ·Bᵧ - Aᵧ·Bₓ) ║
  ║                                                                        ║
  ║  Or using the determinant form:                                        ║
  ║           | i    j    k  |                                             ║
  ║  N = det  | Aₓ   Aᵧ   A_z|                                            ║
  ║           | Bₓ   Bᵧ   B_z|                                            ║
  ║                                                                        ║
  ╚══════════════════════════════════════════════════════════════════════════╝

  Step 3: Normalize: N̂ = N / |N|   where |N| = √(Nₓ² + Nᵧ² + N_z²)


  ► Solved Example — Surface Normal
  ──────────────────────────────────

  Polygon vertices: V₁(1, 0, 1), V₂(0, 1, 1), V₃(0, 0, 0)

  A = V₂ - V₁ = (-1, 1, 0)
  B = V₃ - V₁ = (-1, 0, -1)

  N = A × B:
      Nₓ = (1)(-1) - (0)(0) = -1
      Nᵧ = (0)(-1) - (-1)(-1) = 0 - 1 = -1
      N_z = (-1)(0) - (1)(-1) = 0 + 1 = 1

  N = (-1, -1, 1)
  |N| = √(1 + 1 + 1) = √3 ≈ 1.732
  N̂ = (-0.577, -0.577, 0.577)

  The Z-component is positive → surface faces toward the viewer
  (if viewing along -Z direction).



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.3.2  CUBIC SPLINES AND BEZIER CURVES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Spline Curves — Overview
  ───────────────────────────

  A spline is a smooth curve defined by a set of control points. Unlike
  polylines (straight segments between points), splines produce smooth,
  continuous curves.

  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  TYPE                  │  DESCRIPTION                                │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Interpolation Curve   │  The curve PASSES THROUGH all control      │
  │                        │  points. Example: cubic spline, Hermite.   │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Approximation Curve   │  The curve is INFLUENCED by control points │
  │                        │  but may not pass through them.             │
  │                        │  Example: Bezier curve, B-spline.          │
  └────────────────────────┴──────────────────────────────────────────────┘


  ► Cubic Spline
  ───────────────

  A cubic spline fits a piecewise cubic polynomial P(t) = at³ + bt² + ct + d
  through a set of control points, ensuring:
    • The curve passes through every control point (interpolation)
    • The curve is C² continuous (position, first derivative, and second
      derivative are continuous at every joint)

  This makes cubic splines very smooth — no sudden changes in curvature.


  ► Bezier Curves — Full Derivation
  ──────────────────────────────────

┌─────────────────────────────────────────────────────────────────────────────┐
│  DEFINITION                                                                │
│                                                                            │
│  A Bezier curve of degree n is defined by (n+1) control points             │
│  P₀, P₁, ..., Pₙ and is parameterized by t ∈ [0, 1]:                     │
│                                                                            │
│           n                                                                │
│  P(t) =  Σ  Bᵢ,ₙ(t) · Pᵢ                                               │
│          i=0                                                               │
│                                                                            │
│  where Bᵢ,ₙ(t) are the Bernstein basis polynomials:                      │
│                                                                            │
│  Bᵢ,ₙ(t) = C(n,i) · tⁱ · (1-t)ⁿ⁻ⁱ                                     │
│                                                                            │
│  C(n,i) = n! / (i! · (n-i)!)                                             │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Cubic Bezier Curve (n = 3, most commonly used)
  ──────────────────────────────────────────────────

  Four control points: P₀, P₁, P₂, P₃

  Bernstein polynomials for n = 3:
      B₀,₃(t) = (1-t)³
      B₁,₃(t) = 3t(1-t)²
      B₂,₃(t) = 3t²(1-t)
      B₃,₃(t) = t³

  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  CUBIC BEZIER EQUATION:                                                ║
  ║                                                                        ║
  ║  P(t) = (1-t)³·P₀ + 3t(1-t)²·P₁ + 3t²(1-t)·P₂ + t³·P₃             ║
  ║                                                                        ║
  ║  where t ranges from 0 to 1                                            ║
  ╚══════════════════════════════════════════════════════════════════════════╝


  ► Properties of Bezier Curves
  ──────────────────────────────

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  1. Endpoint Interpolation: P(0) = P₀ and P(1) = P₃                   │
  │     The curve always starts at the first and ends at the last point.   │
  │                                                                         │
  │  2. Convex Hull Property: The curve lies entirely within the convex    │
  │     hull of the control points. This is useful for clipping.           │
  │                                                                         │
  │  3. Tangent at endpoints:                                               │
  │     P'(0) = 3(P₁ - P₀)  →  tangent direction at start                │
  │     P'(1) = 3(P₃ - P₂)  →  tangent direction at end                  │
  │                                                                         │
  │  4. Affine Invariance: Transforming control points transforms the      │
  │     curve equivalently (no need to recalculate).                       │
  │                                                                         │
  │  5. Variation Diminishing: The curve doesn't oscillate more than       │
  │     the control polygon.                                                │
  │                                                                         │
  │  6. Partition of Unity: All Bernstein polynomials sum to 1 at every t. │
  └──────────────────────────────────────────────────────────────────────────┘


  ► Solved Example 1 — Bezier Curve at t = 0.2
  ──────────────────────────────────────────────

  Control points: P₀(1,1), P₁(4,6), P₂(8,-3), P₃(12,2)

  At t = 0.2:
      B₀ = (0.8)³ = 0.512
      B₁ = 3(0.2)(0.8)² = 3(0.2)(0.64) = 0.384
      B₂ = 3(0.2)²(0.8) = 3(0.04)(0.8) = 0.096
      B₃ = (0.2)³ = 0.008

  Verify: 0.512 + 0.384 + 0.096 + 0.008 = 1.000 ✓

  x(0.2) = 0.512(1) + 0.384(4) + 0.096(8) + 0.008(12)
         = 0.512 + 1.536 + 0.768 + 0.096 = 2.912

  y(0.2) = 0.512(1) + 0.384(6) + 0.096(-3) + 0.008(2)
         = 0.512 + 2.304 - 0.288 + 0.016 = 2.544

  Point at t = 0.2: (2.912, 2.544)


  ► Solved Example 2 — Bezier Curve at t = 0.5
  ──────────────────────────────────────────────

  Control points: P₀(0,0), P₁(2,8), P₂(6,8), P₃(8,0)

  At t = 0.5:
      B₀ = (0.5)³ = 0.125
      B₁ = 3(0.5)(0.5)² = 0.375
      B₂ = 3(0.5)²(0.5) = 0.375
      B₃ = (0.5)³ = 0.125

  x(0.5) = 0.125(0) + 0.375(2) + 0.375(6) + 0.125(8)
         = 0 + 0.75 + 2.25 + 1.0 = 4.0

  y(0.5) = 0.125(0) + 0.375(8) + 0.375(8) + 0.125(0)
         = 0 + 3.0 + 3.0 + 0 = 6.0

  Point at t = 0.5: (4.0, 6.0)


  ► Solved Example 3 — Bezier Table for Multiple t Values
  ────────────────────────────────────────────────────────

  Control points: P₀(1,1), P₁(4,6), P₂(8,-3), P₃(12,2)

  ┌───────┬─────────┬─────────┬─────────┬─────────┬──────────────────┐
  │   t   │   B₀    │   B₁    │   B₂    │   B₃    │  Point (x, y)    │
  ├───────┼─────────┼─────────┼─────────┼─────────┼──────────────────┤
  │  0.0  │  1.000  │  0.000  │  0.000  │  0.000  │  (1.00,  1.00)   │
  │  0.2  │  0.512  │  0.384  │  0.096  │  0.008  │  (2.91,  2.54)   │
  │  0.4  │  0.216  │  0.432  │  0.288  │  0.064  │  (4.93,  2.38)   │
  │  0.5  │  0.125  │  0.375  │  0.375  │  0.125  │  (6.13,  1.63)   │
  │  0.6  │  0.064  │  0.288  │  0.432  │  0.216  │  (7.33,  0.57)   │
  │  0.8  │  0.008  │  0.096  │  0.384  │  0.512  │  (9.86,  0.22)   │
  │  1.0  │  0.000  │  0.000  │  0.000  │  1.000  │  (12.00, 2.00)   │
  └───────┴─────────┴─────────┴─────────┴─────────┴──────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.3.3  NON-PLANAR SURFACES — BEZIER SURFACES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  A Bezier surface is a 2D extension of Bezier curves. Instead of a 1D
  parameter t, it uses two parameters (u, v), both in [0, 1].

  A bicubic Bezier surface patch uses a 4×4 grid of 16 control points:

  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                                                                        ║
  ║              3   3                                                     ║
  ║  P(u,v) =   Σ   Σ  Bᵢ,₃(u) · Bⱼ,₃(v) · Pᵢⱼ                       ║
  ║             i=0 j=0                                                    ║
  ║                                                                        ║
  ║  where Pᵢⱼ are the 4×4 = 16 control points                           ║
  ║  and Bᵢ,₃ are cubic Bernstein polynomials                             ║
  ║                                                                        ║
  ╚══════════════════════════════════════════════════════════════════════════╝

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  16 Control Points (4×4 grid):                                   │
  │                                                                   │
  │  P₀₃ ─── P₁₃ ─── P₂₃ ─── P₃₃     (u direction →)              │
  │   │       │       │       │                                       │
  │  P₀₂ ─── P₁₂ ─── P₂₂ ─── P₃₂     (v direction ↓)              │
  │   │       │       │       │                                       │
  │  P₀₁ ─── P₁₁ ─── P₂₁ ─── P₃₁                                  │
  │   │       │       │       │                                       │
  │  P₀₀ ─── P₁₀ ─── P₂₀ ─── P₃₀                                  │
  │                                                                   │
  │  The surface interpolates the 4 corner control points.            │
  │  Interior points shape the surface but are not touched by it.    │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘

  Properties:
  • Corner interpolation: P(0,0)=P₀₀, P(1,0)=P₃₀, P(0,1)=P₀₃, P(1,1)=P₃₃
  • Boundary curves are Bezier curves
  • Convex hull property extends to 3D
  • Used in CAD (car body panels, aircraft fuselage)



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.3.4  FRACTAL GEOMETRY METHOD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  DEFINITION                                                                │
│                                                                            │
│  Fractals are geometric shapes that exhibit SELF-SIMILARITY — parts of   │
│  the shape resemble the whole at different scales. They are used to       │
│  model natural phenomena (mountains, coastlines, clouds, trees) that      │
│  cannot be described by smooth Euclidean geometry.                         │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Fractal Dimension
  ────────────────────

  Unlike Euclidean shapes (line=1D, surface=2D, solid=3D), fractals have
  FRACTIONAL dimensions, measured by:

      D = log(N) / log(S)

  where N = number of self-similar copies, S = scaling factor.


  ► Koch Snowflake — Classic Fractal Example
  ────────────────────────────────────────────

  Construction:
  1. Start with an equilateral triangle
  2. For each line segment:
     a. Divide into 3 equal parts
     b. Replace the middle third with two sides of an equilateral triangle
  3. Repeat infinitely

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  Iteration 0:    ╱╲                                              │
  │                 ╱  ╲                                              │
  │                ╱────╲                                             │
  │                                                                   │
  │  Iteration 1:    ╱╲                                              │
  │                 ╱  ╲                                              │
  │                ╱╲  ╱╲                                             │
  │               ╱  ╲╱  ╲                                            │
  │              ╱────╲╱──╲                                           │
  │                                                                   │
  │  Each iteration: N = 4 copies, each 1/3 the size → S = 3         │
  │  D = log(4) / log(3) ≈ 1.2619                                   │
  │                                                                   │
  │  The Koch curve has dimension ~1.26 — more than a line (1D)      │
  │  but less than a surface (2D). It has infinite length but         │
  │  encloses finite area.                                            │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Midpoint Displacement (Fractal Terrain)
  ──────────────────────────────────────────

  Used to generate realistic terrain:
  1. Start with a flat line segment (or grid for 2D terrain)
  2. Find the midpoint
  3. Displace the midpoint vertically by a random amount
  4. Reduce the random range by a roughness factor (e.g., ×0.5)
  5. Recursively subdivide and displace each half

  After many iterations, this produces natural-looking mountain ranges
  and coastlines. The roughness factor controls how jagged the terrain
  appears — high roughness = jagged mountains, low = gentle hills.


  ► Blobby Objects
  ──────────────────

  Blobby objects (also called metaballs or soft objects) are surfaces
  defined by an implicit field function rather than explicit polygons.

  Each blob source has a center point and a field function that decreases
  with distance. The surface is the isosurface where the combined field
  equals a threshold.

  Field function:  f(r) = e^(-a·r²)  (Gaussian falloff)

  When multiple blob sources are combined, their fields add together,
  creating smooth, organic merging effects — like water droplets merging
  or organic tissue modeling.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.4  THREE DIMENSIONAL VIEWING TRANSFORMATION AND PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  The 3D viewing pipeline maps 3D world objects onto a 2D display, similar
  to how a camera captures a 3D scene onto a 2D photograph.


  ► Pipeline Stages
  ──────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  World      Model       Viewing      Projection   Viewport       │
  │  Coords  →  Transform → Transform →  Transform → Transform      │
  │  (WC)       (position   (camera      (3D→2D      (NDC→          │
  │             objects)    setup)       mapping)    screen)          │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘

  ► Coordinate Systems in the Pipeline
  ──────────────────────────────────────

  ┌─────────────────────────────┬──────────────────────────────────────────┐
  │  COORDINATE SYSTEM          │  DESCRIPTION                             │
  ├─────────────────────────────┼──────────────────────────────────────────┤
  │  World Coordinate System    │  Global reference frame. Objects are     │
  │  (WC)                       │  positioned here using model transforms. │
  ├─────────────────────────────┼──────────────────────────────────────────┤
  │  Viewing Coordinate System  │  Camera-centered coordinates. The       │
  │  (VC) / Eye Space           │  camera is at origin, looking along -Z. │
  │                             │  Created by the View Matrix.            │
  ├─────────────────────────────┼──────────────────────────────────────────┤
  │  Normalized Viewing         │  Coordinates normalized to [-1,1] in    │
  │  Coordinate System (NVC)    │  all axes. Created by the Projection    │
  │  / Clip Space               │  Matrix. Clipping happens here.         │
  ├─────────────────────────────┼──────────────────────────────────────────┤
  │  Device Coordinate System   │  Final pixel coordinates on screen.     │
  │  (DC)                       │  Created by the Viewport Transform.     │
  └─────────────────────────────┴──────────────────────────────────────────┘


  ► View Matrix Construction
  ───────────────────────────

  The view matrix transforms from world space to camera (eye) space.
  Given:
    • Camera position: eye = (eₓ, eᵧ, e_z)
    • Look-at target:  center = (cₓ, cᵧ, c_z)
    • Up vector:       up = (uₓ, uᵧ, u_z)

  Step 1: Forward vector (camera looks along -forward):
      f = normalize(center - eye)

  Step 2: Right vector:
      r = normalize(f × up)

  Step 3: True up vector:
      u = r × f

  Step 4: View matrix:
      [rₓ   rᵧ   r_z   -r·eye ]
      [uₓ   uᵧ   u_z   -u·eye ]
      [-fₓ  -fᵧ  -f_z   f·eye ]
      [ 0    0     0       1    ]



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.5  PROJECTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


Projection is the fundamental operation that converts 3D coordinates into
2D coordinates for display. There are two main types.


  ► Comparison: Parallel vs. Perspective Projection
  ──────────────────────────────────────────────────

  ┌────────────────────────┬──────────────────────────┬──────────────────────────┐
  │  PROPERTY              │  PARALLEL                │  PERSPECTIVE             │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Projection Lines      │  All parallel to each    │  Converge to a center   │
  │                        │  other                   │  of projection (COP)    │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Distance Effect       │  No foreshortening —     │  Objects farther away   │
  │                        │  same size regardless    │  appear smaller         │
  │                        │  of distance             │  (foreshortening)       │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Parallel Lines        │  Remain parallel after   │  May converge to        │
  │                        │  projection              │  vanishing points       │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Realism               │  Less realistic          │  More realistic          │
  │                        │  (technical drawings)    │  (mimics human vision)  │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Use Cases             │  Engineering drawings,   │  Games, movies, VR,     │
  │                        │  CAD, architecture,      │  any realistic 3D       │
  │                        │  isometric games         │  rendering              │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Sub-types             │  Orthographic,           │  1-point, 2-point,      │
  │                        │  Axonometric (isometric, │  3-point perspective    │
  │                        │  dimetric, trimetric),   │                         │
  │                        │  Oblique (cavalier,      │                         │
  │                        │  cabinet)                │                         │
  └────────────────────────┴──────────────────────────┴──────────────────────────┘


  ► 4.5.1  Parallel (Orthographic) Projection
  ─────────────────────────────────────────────

  Simply drops the Z coordinate:
      xp = x
      yp = y

  Matrix:
      [1  0  0  0]
      [0  1  0  0]
      [0  0  0  0]
      [0  0  0  1]


  ► 4.5.2  Perspective Projection — Full Derivation
  ───────────────────────────────────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  Setup: Center of projection (eye) at origin.                    │
  │         Projection plane at z = d (distance d from the eye).     │
  │         A 3D point P(x, y, z) is projected to P'(xp, yp, d).    │
  │                                                                   │
  │               P(x,y,z)                                           │
  │              ╱                                                    │
  │            ╱                                                      │
  │          ╱                                                        │
  │   Eye──╱────────────────── Projection plane at z = d             │
  │  (0,0,0)     P'(xp,yp,d)                                        │
  │                                                                   │
  │  By similar triangles:                                            │
  │                                                                   │
  │    xp / d  =  x / z    →    xp = x · d / z                      │
  │    yp / d  =  y / z    →    yp = y · d / z                      │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘

  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  PERSPECTIVE PROJECTION EQUATIONS:                                     ║
  ║                                                                        ║
  ║    xp = x · d / z                                                      ║
  ║    yp = y · d / z                                                      ║
  ║                                                                        ║
  ║  In homogeneous coordinates:                                           ║
  ║                                                                        ║
  ║  [1  0  0  0] [x]   [ x ]                                             ║
  ║  [0  1  0  0]·[y] = [ y ]   →  divide by w: (x/z·d, y/z·d, 1)       ║
  ║  [0  0  1  0] [z]   [ z ]       which gives  (xd/z, yd/z)             ║
  ║  [0  0  1/d 0] [1]   [z/d]                                             ║
  ║                                                                        ║
  ║  The w-component becomes z/d. After perspective divide (÷w):          ║
  ║    xp = x/(z/d) = xd/z    yp = y/(z/d) = yd/z                        ║
  ╚══════════════════════════════════════════════════════════════════════════╝


  ► Types of Perspective Projection
  ──────────────────────────────────

  ┌─────────────────┬──────────────────────────────────────────────────────┐
  │  TYPE           │  DESCRIPTION                                        │
  ├─────────────────┼──────────────────────────────────────────────────────┤
  │  1-Point        │  One vanishing point. Projection plane parallel     │
  │  Perspective    │  to one principal face. Lines perpendicular to      │
  │                 │  the face converge. Example: looking down a road.   │
  ├─────────────────┼──────────────────────────────────────────────────────┤
  │  2-Point        │  Two vanishing points. Projection plane cuts two    │
  │  Perspective    │  principal axes. Most common in architecture.       │
  ├─────────────────┼──────────────────────────────────────────────────────┤
  │  3-Point        │  Three vanishing points. Projection plane tilted    │
  │  Perspective    │  against all three axes. Used for dramatic views    │
  │                 │  (looking up at a skyscraper).                      │
  └─────────────────┴──────────────────────────────────────────────────────┘


  ► Solved Example 1 — Perspective Projection
  ────────────────────────────────────────────

  Project point (6, 8, 12) onto plane at d = 4:
      xp = 6 × 4 / 12 = 2
      yp = 8 × 4 / 12 = 2.67

      Projected point: (2, 2.67)


  ► Solved Example 2 — Cube Projection
  ──────────────────────────────────────

  A unit cube has corners at (0,0,5), (1,0,5), (1,1,5), (0,1,5),
  (0,0,6), (1,0,6), (1,1,6), (0,1,6). Project onto z = 3 (d = 3).

  Front face (z = 5):
      (0,0,5) → (0×3/5, 0×3/5) = (0, 0)
      (1,0,5) → (1×3/5, 0) = (0.6, 0)
      (1,1,5) → (0.6, 0.6)
      (0,1,5) → (0, 0.6)

  Back face (z = 6):
      (0,0,6) → (0, 0)
      (1,0,6) → (3/6, 0) = (0.5, 0)
      (1,1,6) → (0.5, 0.5)
      (0,1,6) → (0, 0.5)

  Notice: Back face projects SMALLER than front face → foreshortening!


  ► Solved Example 3 — Orthographic Projection
  ──────────────────────────────────────────────

  Project the same cube orthographically:

  Front face: (0,0,5) → (0, 0),  (1,0,5) → (1, 0),  etc.
  Back face:  (0,0,6) → (0, 0),  (1,0,6) → (1, 0),  etc.

  Front and back project to the SAME positions → no depth information.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  4.6  CLIPPING IN THREE DIMENSIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  3D clipping removes objects outside the viewing volume (frustum or box).
  The Cohen-Sutherland algorithm extends to 3D using 6-bit region codes:

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  6-BIT OUTCODE:  [Far | Near | Top | Bottom | Right | Left]     │
  │                                                                   │
  │  Bit 1 (Left):    x < x_min                                     │
  │  Bit 2 (Right):   x > x_max                                     │
  │  Bit 3 (Bottom):  y < y_min                                     │
  │  Bit 4 (Top):     y > y_max                                     │
  │  Bit 5 (Near):    z < z_near                                    │
  │  Bit 6 (Far):     z > z_far                                     │
  │                                                                   │
  │  Trivial accept: OR of both codes = 000000                      │
  │  Trivial reject: AND of both codes ≠ 000000                     │
  │                                                                   │
  │  Otherwise, clip against the appropriate plane and repeat.       │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Viewing Volume
  ─────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │  Parallel Projection:  Rectangular box (cuboid)                        │
  │    Defined by: x_min, x_max, y_min, y_max, z_near, z_far             │
  │                                                                         │
  │  Perspective Projection:  Frustum (truncated pyramid)                  │
  │    Defined by: field of view angle, aspect ratio, z_near, z_far       │
  │                                                                         │
  │         ╱────────────╲   ← far plane                                   │
  │        ╱              ╲                                                 │
  │       ╱   frustum      ╲                                                │
  │      ╱                  ╲                                               │
  │     ╱────────────────────╲  ← near plane                               │
  │          eye (COP)                                                      │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ADDITIONAL TOPICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Euler Angles and Gimbal Lock
  ───────────────────────────────

  Euler angles represent 3D rotation as three sequential rotations about
  the coordinate axes (e.g., first about X, then Y, then Z).

  Problem — Gimbal Lock: When two rotation axes align (e.g., pitch = 90°),
  one degree of freedom is lost. The object can no longer rotate
  independently about all three axes. This is a fundamental limitation
  of Euler angles.

  Solution: Quaternions (see below).


  ► Quaternions
  ──────────────

  A quaternion q = w + xi + yj + zk is a 4-component mathematical object
  that represents 3D rotations without gimbal lock.

  ┌──────────────────────────────────────────────────────────────────────────┐
  │  A rotation of angle θ about unit axis (aₓ, aᵧ, a_z):                │
  │                                                                         │
  │  q = cos(θ/2) + sin(θ/2)(aₓi + aᵧj + a_zk)                           │
  │                                                                         │
  │  Advantages over Euler angles:                                          │
  │    ✓ No gimbal lock                                                    │
  │    ✓ Smooth interpolation (SLERP) for animation                       │
  │    ✓ Compact (4 values vs. 3×3 = 9 matrix values)                     │
  │    ✓ Efficient composition (quaternion multiplication)                 │
  │                                                                         │
  │  Used by: game engines (Unity, Unreal), robotics, aerospace           │
  └──────────────────────────────────────────────────────────────────────────┘


  ► B-Splines and NURBS
  ───────────────────────

  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  TYPE                  │  DESCRIPTION                                │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  B-Spline              │  Like Bezier but with LOCAL control — moving│
  │                        │  one control point only affects nearby curve.│
  │                        │  Allows higher-order curves without high-   │
  │                        │  degree polynomials (uses knot vector).     │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  NURBS (Non-Uniform    │  B-Spline with weights on control points.  │
  │  Rational B-Spline)    │  Can exactly represent conic sections       │
  │                        │  (circles, ellipses) — Bezier/B-splines    │
  │                        │  cannot. Industry standard for CAD.         │
  └────────────────────────┴──────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OPENGL LAB — 3D GRAPHICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► OpenGL 3D Setup (Camera + Perspective)
  ─────────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  #include <GL/glut.h>                                          │
  │                                                                 │
  │  void display() {                                              │
  │      glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);      │
  │      glLoadIdentity();                                         │
  │                                                                 │
  │      // Set up camera                                          │
  │      gluLookAt(5, 5, 5,    // eye position                    │
  │                0, 0, 0,    // look-at target                   │
  │                0, 1, 0);   // up vector                        │
  │                                                                 │
  │      // Draw a wireframe cube                                  │
  │      glColor3f(1, 1, 0);                                       │
  │      glutWireCube(2.0);                                        │
  │                                                                 │
  │      // Draw a Bezier curve using line segments                │
  │      glColor3f(0, 1, 0);                                       │
  │      glBegin(GL_LINE_STRIP);                                   │
  │      for (float t = 0; t <= 1.0; t += 0.01) {                │
  │          float b0 = (1-t)*(1-t)*(1-t);                        │
  │          float b1 = 3*t*(1-t)*(1-t);                          │
  │          float b2 = 3*t*t*(1-t);                               │
  │          float b3 = t*t*t;                                     │
  │          float x = b0*0 + b1*2 + b2*6 + b3*8;                │
  │          float y = b0*0 + b1*8 + b2*8 + b3*0;                │
  │          glVertex3f(x, y, 0);                                  │
  │      }                                                          │
  │      glEnd();                                                  │
  │                                                                 │
  │      glutSwapBuffers();                                        │
  │  }                                                              │
  │                                                                 │
  │  void reshape(int w, int h) {                                  │
  │      glViewport(0, 0, w, h);                                   │
  │      glMatrixMode(GL_PROJECTION);                              │
  │      glLoadIdentity();                                         │
  │      gluPerspective(60, (float)w/h, 0.1, 100);               │
  │      glMatrixMode(GL_MODELVIEW);                               │
  │  }                                                              │
  │                                                                 │
  │  int main(int argc, char** argv) {                             │
  │      glutInit(&argc, argv);                                    │
  │      glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH);           │
  │      glutInitWindowSize(600, 600);                             │
  │      glutCreateWindow("3D Graphics");                          │
  │      glEnable(GL_DEPTH_TEST);                                  │
  │      glutDisplayFunc(display);                                 │
  │      glutReshapeFunc(reshape);                                 │
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
  │  3D Coordinate Systems     │  RH (OpenGL) vs LH (DirectX);             │
  │                            │  curl fingers X→Y, thumb = +Z             │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  3D Transforms             │  4×4 homogeneous matrices; T, S, R        │
  │                            │  about each axis; Rᵧ has swapped signs    │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Polygon Surfaces          │  Vertex/Edge/Face tables; surface normal   │
  │                            │  = cross product of edge vectors           │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Bezier Curves             │  P(t) = Σ Bᵢ,ₙ(t)·Pᵢ; cubic uses 4      │
  │                            │  control points; endpoint interpolation;   │
  │                            │  convex hull property                      │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Fractal Geometry          │  Self-similarity; D = log(N)/log(S);      │
  │                            │  Koch snowflake D ≈ 1.26; midpoint        │
  │                            │  displacement for terrain                  │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Parallel Projection       │  Drops Z; no foreshortening; parallel     │
  │                            │  lines stay parallel                       │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Perspective Projection    │  xp = xd/z; foreshortening; vanishing     │
  │                            │  points; more realistic                    │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  3D Clipping               │  6-bit outcode; 6 clipping planes         │
  │                            │  (L, R, B, T, Near, Far)                  │
  └────────────────────────────┴──────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                         END OF CHAPTER 4                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝


---

## 📝 Exam Practice Questions

### From AI-Generated Sets (aiQuestions.txt)

**Set 1, Q4:**
a. Derive the general equation for perspective projection with a neat diagram. What is the difference between one-point, two-point, and three-point perspective projections?
b. What are fractal geometry methods? Explain the concept of self-similarity and fractal dimension with the Koch snowflake as an example.

**Set 2, Q4:**
a. What are polygon surfaces in 3D representation? Explain how surface normals are computed for a polygon defined by its vertices.
b. Differentiate between parallel and perspective projection with real-life application examples. Derive the projection matrix for one-point perspective projection.

**Set 3, Q4:**
a. What is a Bezier curve? Derive the parametric equation for a cubic Bezier curve using Bernstein polynomials.
b. Explain the 3D viewing transformation pipeline. How does it differ from the 2D viewing pipeline?

**Set 4, Q4:**
a. Explain 3D translation, rotation, and scaling transformations with their 4 × 4 homogeneous matrix representations.
b. What are cubic spline curves? How do they differ from Bezier curves in terms of continuity and control point influence?

**Set 5, Q4:**
a. Explain polygon surface representation in 3D graphics. How are polygon meshes stored using vertex lists and edge lists?
b. Given four control points P0(0, 0), P1(2, 8), P2(6, 8), P3(8, 0), calculate five points on the cubic Bezier curve at t = 0, 0.25, 0.5, 0.75, 1.0. Tabulate the results.

**Set 6, Q4:**
a. Explain clipping in three dimensions. How is the Cohen-Sutherland algorithm extended to 3D using 6-bit region codes?
b. What is a Bezier surface? How is it constructed as a Cartesian product of two Bezier curves? Write the mathematical equation for a bi-cubic Bezier surface patch.

**Set 7, Q4:**
a. Derive the matrices for 3D rotation about the X-axis, Y-axis, and Z-axis. Rotate the point (3, 4, 5) by 90 degrees about the Z-axis.
b. Find the coordinate on the cubic Bezier curve at t = 0.5 with control points (0, 0), (1, 3), (5, 3), (6, 0). Show the detailed calculation using the Bernstein polynomial form.

**Set 8, Q4:**
a. Compare parallel and perspective projections with examples and diagrams. Derive the projection matrix for orthographic parallel projection.
b. Explain the 3D viewing pipeline from world coordinates to screen coordinates. What is the significance of View Reference Point (VRP) and View Plane Normal (VPN)?

**Set 9, Q4:**
a. What are 3D geometric transformations? Derive the 4 × 4 matrix for 3D reflection about the XY plane, XZ plane, and YZ plane.
b. Derive the cubic Bezier curve equation. Find the coordinate at t = 0.4 for control points (2, 0), (4, 6), (7, 6), (9, 0). Show complete calculation.

**Set 10, Q4:**
a. What is fractal geometry? Explain the construction of the Koch snowflake curve. How is fractal dimension computed?
b. Explain the difference between one-point, two-point, and three-point perspective projections with diagrams and real-life examples. How do vanishing points affect the projected view?

---

### From Past Papers (Questions.txt)

**Set 1, Q4:**
a. Discuss the difference between spline approximation curve versus an interpolation curve. Derive an expression for perspective projection with the necessary diagram.
b. Derive the equation for the cubic Bezier curve and find the coordinate at t = 0.2 with respect to the control points (1, 1), (4, 6), (8, −3), and (12, 2).

**Set 2, Q4:**
a. Why is it required to map object descriptions from the world coordinates to the device coordinates? Explain the mapping process with the necessary equations.
b. Differentiate between parallel and perspective projection with real-life application examples.

**Set 3, Q5a** *(Bezier/3D topic):*
Define blobby objects with an example. What is a cubic Bezier curve? Derive the equation of a cubic Bezier curve.

**Set 3, Q6a** *(3D viewing topic):*
Explain the 3D Viewing Pipeline. Briefly explain the significance of World Coordinate System, Viewing Coordinate System, Normalized Viewing Coordinate System, and Device Coordinate System in the viewing pipeline.

---

### Related Short Notes Topics (from Q7)
- Three-dimensional coordinate systems — *aiQ Set 1*
- Bezier surfaces — *aiQ Set 2*
- Fractal geometry methods — *aiQ Set 6*
- 3D clipping — *aiQ Set 7*
- Non-planar Bezier surfaces — *aiQ Set 8*
- Cubic spline curves — *aiQ Set 10*
- 3D Representations — *Q Set 2*
- Parallel vs. Perspective Projection — *Q Set 3*
