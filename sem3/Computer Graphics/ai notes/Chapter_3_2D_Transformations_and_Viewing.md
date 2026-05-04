
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║            CHAPTER 3 — TWO DIMENSIONAL GEOMETRIC                           ║
║                    TRANSFORMATIONS AND VIEWING                             ║
║                                                                            ║
║            CMP 234 · Pokhara University · BE Computer                      ║
║            Syllabus Hours: 8                                               ║
║                                                                            ║
╚══════════════════════════════════════════════════════════════════════════════╝


This chapter covers the mathematical operations that reposition, resize, and
reshape 2D objects — collectively called geometric transformations. It then
extends to the viewing pipeline: how a scene described in world coordinates
is mapped to a display window, and how portions outside the visible region
are clipped away. These concepts are fundamental to every graphics system
and are heavily tested in exams.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3.1  TWO DIMENSIONAL TRANSFORMATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  DEFINITION                                                                │
│                                                                            │
│  A geometric transformation is a function that maps every point (x, y)    │
│  of an object to a new point (x', y'), thereby changing the object's      │
│  position, orientation, size, or shape. In 2D graphics, there are five    │
│  basic transformations: Translation, Rotation, Scaling, Reflection,       │
│  and Shearing.                                                             │
└─────────────────────────────────────────────────────────────────────────────┘


  ► 3.1.1  Translation
  ─────────────────────

  Translation moves every point of an object by the same displacement
  (tₓ, tᵧ). It changes position without altering size, shape, or
  orientation.

  Equations:
      x' = x + tₓ
      y' = y + tᵧ

  Matrix form (2×1):
      [x']   [x]   [tₓ]
      [y'] = [y] + [tᵧ]

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  Example: Translate point (3, 5) by tₓ = 4, tᵧ = -2             │
  │  x' = 3 + 4 = 7                                                  │
  │  y' = 5 + (-2) = 3                                               │
  │  New point: (7, 3)                                                │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘

  Translation is NOT a linear transformation (it can't be expressed as
  a 2×2 matrix multiplication). This is why we need homogeneous
  coordinates (covered in section 3.3).


  ► 3.1.2  Rotation
  ──────────────────

  Rotation turns an object about a fixed point (pivot) by angle θ.
  By default, rotation is about the origin.

  Equations (counterclockwise, about origin):
      x' = x·cos θ - y·sin θ
      y' = x·sin θ + y·cos θ

  2×2 Matrix:
      [x']   [cos θ   -sin θ] [x]
      [y'] = [sin θ    cos θ] [y]

  ┌───────────────────────────────────────────────────────────────────┐
  │  Sign Convention:                                                 │
  │    ► Positive θ  →  counterclockwise (CCW) rotation              │
  │    ► Negative θ  →  clockwise (CW) rotation                     │
  │                                                                   │
  │  Special values:                                                  │
  │    θ = 90°:   cos 90° = 0, sin 90° = 1                          │
  │               x' = -y,  y' = x                                   │
  │    θ = 180°:  x' = -x,  y' = -y                                 │
  │    θ = 270°:  x' = y,   y' = -x                                 │
  └───────────────────────────────────────────────────────────────────┘


  ► 3.1.3  Scaling
  ─────────────────

  Scaling changes the size of an object by multiplying coordinates by
  scale factors Sₓ and Sᵧ.

  Equations:
      x' = x · Sₓ
      y' = y · Sᵧ

  2×2 Matrix:
      [x']   [Sₓ  0 ] [x]
      [y'] = [0   Sᵧ] [y]

  ┌───────────────────────────────────────────────────────────────────┐
  │  Scale Factor Behavior:                                           │
  │                                                                   │
  │  ┌─────────────────────┬──────────────────────────────────────┐  │
  │  │  CONDITION          │  EFFECT                              │  │
  │  ├─────────────────────┼──────────────────────────────────────┤  │
  │  │  S > 1              │  Enlargement (magnification)        │  │
  │  │  S = 1              │  No change (identity)               │  │
  │  │  0 < S < 1          │  Reduction (shrinking)              │  │
  │  │  S < 0              │  Reflection + scaling               │  │
  │  │  Sₓ = Sᵧ           │  Uniform scaling (shape preserved)  │  │
  │  │  Sₓ ≠ Sᵧ           │  Non-uniform (differential) scaling │  │
  │  └─────────────────────┴──────────────────────────────────────┘  │
  │                                                                   │
  │  ► Uniform scaling: Sₓ = Sᵧ → object maintains proportions     │
  │  ► Non-uniform: Sₓ ≠ Sᵧ → object distorts (stretched/squished) │
  └───────────────────────────────────────────────────────────────────┘

  Important: Scaling about the origin also moves the object (unless
  it's centered at the origin). To scale about a fixed point, use
  composite transformations (section 3.4).


  ► 3.1.4  Reflection
  ────────────────────

  Reflection produces a mirror image of an object about a line
  (reflection axis).

  ┌───────────────────────┬────────────────────────┬──────────────────┐
  │  REFLECTION AXIS      │  EQUATIONS             │  2×2 MATRIX      │
  ├───────────────────────┼────────────────────────┼──────────────────┤
  │  About X-axis         │  x' = x,  y' = -y     │  [ 1   0]       │
  │                       │                        │  [ 0  -1]       │
  ├───────────────────────┼────────────────────────┼──────────────────┤
  │  About Y-axis         │  x' = -x, y' = y      │  [-1   0]       │
  │                       │                        │  [ 0   1]       │
  ├───────────────────────┼────────────────────────┼──────────────────┤
  │  About Origin         │  x' = -x, y' = -y     │  [-1   0]       │
  │                       │                        │  [ 0  -1]       │
  ├───────────────────────┼────────────────────────┼──────────────────┤
  │  About line y = x     │  x' = y,  y' = x      │  [ 0   1]       │
  │                       │                        │  [ 1   0]       │
  ├───────────────────────┼────────────────────────┼──────────────────┤
  │  About line y = -x    │  x' = -y, y' = -x     │  [ 0  -1]       │
  │                       │                        │  [-1   0]       │
  └───────────────────────┴────────────────────────┴──────────────────┘


  ► 3.1.5  Shearing
  ──────────────────

  Shearing distorts the shape of an object by shifting one coordinate
  in proportion to the other. It "tilts" the object.

  ┌───────────────────────┬────────────────────────┬──────────────────┐
  │  TYPE                 │  EQUATIONS             │  2×2 MATRIX      │
  ├───────────────────────┼────────────────────────┼──────────────────┤
  │  X-Shear              │  x' = x + shₓ·y       │  [1   shₓ]      │
  │  (shear in x by y)    │  y' = y                │  [0    1 ]      │
  ├───────────────────────┼────────────────────────┼──────────────────┤
  │  Y-Shear              │  x' = x                │  [ 1    0]      │
  │  (shear in y by x)    │  y' = shᵧ·x + y       │  [shᵧ  1 ]      │
  └───────────────────────┴────────────────────────┴──────────────────┘

  ┌───────────────────────────────────────────────────────────────────┐
  │  Example: X-Shear with shₓ = 2 on triangle (0,0), (4,0), (2,3) │
  │                                                                   │
  │  (0,0): x' = 0 + 2(0) = 0,  y' = 0  →  (0, 0)                  │
  │  (4,0): x' = 4 + 2(0) = 4,  y' = 0  →  (4, 0)                  │
  │  (2,3): x' = 2 + 2(3) = 8,  y' = 3  →  (8, 3)                  │
  │                                                                   │
  │  The base stays fixed; the apex shifts right by 2×3 = 6 units.   │
  └───────────────────────────────────────────────────────────────────┘


  ► Summary of All Five Basic 2D Transformations
  ───────────────────────────────────────────────

  ┌───────────────────┬───────────────────────┬───────────────────────────────┐
  │  TRANSFORMATION   │  WHAT IT CHANGES      │  KEY PROPERTY                 │
  ├───────────────────┼───────────────────────┼───────────────────────────────┤
  │  Translation      │  Position             │  Additive, not multiplicative │
  │  Rotation         │  Orientation           │  Preserves shape and size    │
  │  Scaling          │  Size                  │  Can be uniform or non-uni.  │
  │  Reflection       │  Handedness (mirror)   │  Reverses orientation        │
  │  Shearing         │  Shape (distortion)    │  Preserves area              │
  └───────────────────┴───────────────────────┴───────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3.2  MATRIX REPRESENTATIONS OF TRANSFORMATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


In 2D, we can represent rotation, scaling, reflection, and shearing as
2×2 matrix multiplications:

    P' = M · P     where P = [x, y]ᵀ and M is a 2×2 matrix

However, translation CANNOT be expressed as a 2×2 multiplication — it's
an addition:  P' = P + T

This inconsistency is a problem because:
  • We can't combine translation with other transforms into a single matrix
  • Hardware would need different circuits for multiplication and addition
  • Multiple sequential transforms can't be pre-computed into one matrix

The solution: Homogeneous Coordinates (next section).



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3.3  HOMOGENEOUS COORDINATE SYSTEM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  THE PROBLEM                                                               │
│                                                                            │
│  Translation is P' = P + T (addition), while rotation/scaling are         │
│  P' = M·P (multiplication). We can't combine these into a single matrix  │
│  operation using 2×2 matrices. This makes it impossible to pre-compute   │
│  a sequence of mixed transforms into one matrix, which is essential for   │
│  performance in graphics hardware.                                         │
│                                                                            │
│  THE SOLUTION                                                              │
│                                                                            │
│  Add a third coordinate (called w or h). Represent 2D point (x, y) as    │
│  the 3D homogeneous point (x, y, 1). Now ALL transformations — including │
│  translation — can be expressed as 3×3 matrix multiplications.            │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Why Is This Called "Homogeneous"?
  ────────────────────────────────────

  In homogeneous coordinates, the point (x, y) is represented as
  (x·w, y·w, w) for any non-zero w. All of these represent the SAME
  Cartesian point:

      (2, 3, 1),  (4, 6, 2),  (6, 9, 3)  →  all represent (2, 3)

  To convert back: Cartesian = (X/w, Y/w)

  The "standard" form uses w = 1: point (x, y) → (x, y, 1).


  ► 3×3 Homogeneous Matrices for All Transformations
  ────────────────────────────────────────────────────

  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │  Translation T(tₓ, tᵧ):          Inverse T(-tₓ, -tᵧ):                │
  │                                                                         │
  │  [1   0   tₓ]                    [1   0  -tₓ]                          │
  │  [0   1   tᵧ]                    [0   1  -tᵧ]                          │
  │  [0   0    1]                    [0   0    1]                           │
  │                                                                         │
  │  ─────────────────────────────────────────────────────────────────────  │
  │                                                                         │
  │  Rotation R(θ):                   Inverse R(-θ):                        │
  │                                                                         │
  │  [cos θ  -sin θ   0]             [cos θ   sin θ   0]                   │
  │  [sin θ   cos θ   0]             [-sin θ  cos θ   0]                   │
  │  [  0       0     1]             [  0       0     1]                    │
  │                                                                         │
  │  ─────────────────────────────────────────────────────────────────────  │
  │                                                                         │
  │  Scaling S(Sₓ, Sᵧ):             Inverse S(1/Sₓ, 1/Sᵧ):               │
  │                                                                         │
  │  [Sₓ   0    0]                   [1/Sₓ   0     0]                      │
  │  [ 0   Sᵧ   0]                   [  0   1/Sᵧ   0]                      │
  │  [ 0    0    1]                   [  0    0      1]                      │
  │                                                                         │
  │  ─────────────────────────────────────────────────────────────────────  │
  │                                                                         │
  │  Reflection about X-axis:        Reflection about Y-axis:               │
  │                                                                         │
  │  [1    0    0]                   [-1    0    0]                          │
  │  [0   -1    0]                   [ 0    1    0]                          │
  │  [0    0    1]                   [ 0    0    1]                          │
  │                                                                         │
  │  ─────────────────────────────────────────────────────────────────────  │
  │                                                                         │
  │  Reflection about y = x:         Reflection about origin:               │
  │                                                                         │
  │  [0    1    0]                   [-1    0    0]                          │
  │  [1    0    0]                   [ 0   -1    0]                          │
  │  [0    0    1]                   [ 0    0    1]                          │
  │                                                                         │
  │  ─────────────────────────────────────────────────────────────────────  │
  │                                                                         │
  │  X-Shear Shₓ(a):                Y-Shear Shᵧ(b):                       │
  │                                                                         │
  │  [1    a    0]                   [1    0    0]                           │
  │  [0    1    0]                   [b    1    0]                           │
  │  [0    0    1]                   [0    0    1]                           │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘


  ► Why Homogeneous Coordinates Matter for Hardware
  ──────────────────────────────────────────────────

  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  GPU Advantage:                                                        ║
  ║                                                                        ║
  ║  • ALL transforms are now 3×3 matrix multiplications                  ║
  ║  • Multiple transforms can be PRE-MULTIPLIED into a single matrix     ║
  ║  • GPU has dedicated 4×4 matrix multiply hardware (4×4 for 3D)        ║
  ║  • One multiply unit handles ALL transform types                      ║
  ║  • No separate adder circuit needed for translation                   ║
  ║                                                                        ║
  ║  Example: Translate + Rotate + Scale = one matrix M_composite          ║
  ║           Apply to 1 million vertices: each just does M × [x,y,1]ᵀ   ║
  ╚══════════════════════════════════════════════════════════════════════════╝



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3.4  COMPOSITE TRANSFORMATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  DEFINITION                                                                │
│                                                                            │
│  A composite transformation combines multiple basic transformations into  │
│  a single equivalent transformation by multiplying their matrices.        │
│  This is essential for performing operations like rotating about an       │
│  arbitrary point, scaling about a fixed point, or reflecting about an    │
│  arbitrary line.                                                           │
│                                                                            │
│  KEY RULE: Matrix multiplication is applied RIGHT to LEFT:                │
│    M_composite = M_n · M_{n-1} · ... · M_2 · M_1                        │
│  The FIRST transformation applied is M_1 (rightmost).                    │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Rotation About an Arbitrary Pivot Point (pₓ, pᵧ)
  ────────────────────────────────────────────────────

  To rotate an object by angle θ about point (pₓ, pᵧ):

  Step 1: Translate pivot to origin        →  T(-pₓ, -pᵧ)
  Step 2: Rotate by θ about origin         →  R(θ)
  Step 3: Translate pivot back             →  T(pₓ, pᵧ)

  Composite matrix:

      M = T(pₓ, pᵧ) · R(θ) · T(-pₓ, -pᵧ)

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  [1  0  pₓ] [cos θ  -sin θ  0] [1  0  -pₓ]                     │
  │  [0  1  pᵧ]·[sin θ   cos θ  0]·[0  1  -pᵧ]                     │
  │  [0  0   1] [  0       0    1] [0  0    1]                       │
  │                                                                   │
  │  = [cos θ  -sin θ   pₓ(1-cos θ) + pᵧ·sin θ]                    │
  │    [sin θ   cos θ   pᵧ(1-cos θ) - pₓ·sin θ]                    │
  │    [  0       0                1             ]                    │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Scaling About a Fixed Point (h, k)
  ──────────────────────────────────────

  To scale about point (h, k) with factors (Sₓ, Sᵧ):

  Step 1: Translate (h, k) to origin       →  T(-h, -k)
  Step 2: Scale by (Sₓ, Sᵧ) at origin     →  S(Sₓ, Sᵧ)
  Step 3: Translate back                   →  T(h, k)

  Composite matrix:

      M = T(h, k) · S(Sₓ, Sᵧ) · T(-h, -k)

      = [Sₓ   0    h(1-Sₓ)]
        [ 0   Sᵧ   k(1-Sᵧ)]
        [ 0    0       1   ]


  ► Reflection About an Arbitrary Line y = mx + c
  ─────────────────────────────────────────────────

  To reflect about the line y = mx + c:

  Step 1: Translate line to pass through origin  →  T(0, -c)
  Step 2: Rotate line to coincide with X-axis    →  R(-α) where α = atan(m)
  Step 3: Reflect about X-axis                   →  Reflect_X
  Step 4: Rotate back                            →  R(α)
  Step 5: Translate back                         →  T(0, c)

  Composite: M = T(0,c) · R(α) · Reflect_X · R(-α) · T(0,-c)


  ► Reflection About the line y = x + c (Special Case: m = 1)
  ─────────────────────────────────────────────────────────────

  For y = x + c (slope = 1, angle = 45°):

  Step 1: Translate by T(0, -c)
  Step 2: Rotate by R(-45°)
  Step 3: Reflect about X-axis
  Step 4: Rotate by R(45°)
  Step 5: Translate by T(0, c)

  Simplified for y = x (c = 0): Just use the reflection matrix for y=x:

      [0   1   0]
      [1   0   0]
      [0   0   1]



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  SOLVED EXAMPLES — 2D TRANSFORMATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Example 1: Pivot Point Rotation
  ──────────────────────────────────

  Rotate triangle A(5, 8), B(15, 8), C(10, 16) about fixed point (10, 5)
  by some angle θ, then shift down by 2 units.

  For this problem, let's assume θ = 90° CCW (commonly asked).

  Step 1: Translate pivot (10, 5) to origin → T(-10, -5)
      A → (5-10, 8-5) = (-5, 3)
      B → (15-10, 8-5) = (5, 3)
      C → (10-10, 16-5) = (0, 11)

  Step 2: Rotate 90° CCW → R(90°):  x' = -y, y' = x
      A → (-3, -5)
      B → (-3, 5)
      C → (-11, 0)

  Step 3: Translate back → T(10, 5)
      A → (-3+10, -5+5) = (7, 0)
      B → (-3+10, 5+5) = (7, 10)
      C → (-11+10, 0+5) = (-1, 5)

  Step 4: Shift down by 2 → T(0, -2)
      A → (7, 0-2) = (7, -2)
      B → (7, 10-2) = (7, 8)
      C → (-1, 5-2) = (-1, 3)

  Final coordinates: A'(7, -2), B'(7, 8), C'(-1, 3)


  ► Example 2: Fixed-Point Scaling
  ─────────────────────────────────

  Scale triangle P(2, 2), Q(6, 2), R(4, 6) by Sₓ = 2, Sᵧ = 3 about
  fixed point (2, 2).

  Step 1: Translate fixed point to origin → T(-2, -2)
      P → (0, 0)    Q → (4, 0)    R → (2, 4)

  Step 2: Scale S(2, 3)
      P → (0×2, 0×3) = (0, 0)
      Q → (4×2, 0×3) = (8, 0)
      R → (2×2, 4×3) = (4, 12)

  Step 3: Translate back → T(2, 2)
      P → (2, 2)    Q → (10, 2)    R → (6, 14)

  Final: P'(2, 2), Q'(10, 2), R'(6, 14)

  Alternative using the direct formula M = T · S · T⁻¹:
      x' = Sₓ(x - h) + h = 2(x - 2) + 2 = 2x - 2
      y' = Sᵧ(y - k) + k = 3(y - 2) + 2 = 3y - 4


  ► Example 3: Reflection About y = x
  ─────────────────────────────────────

  Reflect triangle with vertices (1, 2), (4, 2), (3, 5) about y = x.

  Reflection about y = x swaps coordinates: (x, y) → (y, x)

      (1, 2) → (2, 1)
      (4, 2) → (2, 4)
      (3, 5) → (5, 3)

  Reflected triangle: (2, 1), (2, 4), (5, 3)


  ► Example 4: Reflection About y = x + 1 (Arbitrary Line)
  ──────────────────────────────────────────────────────────

  Reflect object with vertices (2, 3), (4, 3), (4, 5) about line y = x + 1.

  Step 1: Translate line to pass through origin → T(0, -1)
      Line y = x + 1 becomes y = x
      Vertices: (2, 2), (4, 2), (4, 4)

  Step 2: Reflect about y = x → swap (x, y)
      (2, 2) → (2, 2)
      (4, 2) → (2, 4)
      (4, 4) → (4, 4)

  Step 3: Translate back → T(0, 1)
      (2, 2) → (2, 3)
      (2, 4) → (2, 5)
      (4, 4) → (4, 5)

  Final: (2, 3), (2, 5), (4, 5)


  ► Example 5: Reflection About Arbitrary Line Through Two Points
  ────────────────────────────────────────────────────────────────

  Mirror placed vertically passing through (5, 0) and (0, 5).
  Find reflected view of triangle A(5, 30), B(30, 50), C(20, 60).

  Line through (5, 0) and (0, 5): slope m = (5-0)/(0-5) = -1
  Equation: y = -x + 5   →   y = -x + 5

  Step 1: Translate to origin → T(0, -5) (or T(-5, 0))
      Using T(0, -5): line becomes y = -x
      A → (5, 25),  B → (30, 45),  C → (20, 55)

  Step 2: Reflect about y = -x: (x, y) → (-y, -x)
      A → (-25, -5),   B → (-45, -30),   C → (-55, -20)

  Step 3: Translate back → T(0, 5)
      A → (-25, 0),    B → (-45, -25),   C → (-55, -15)

  Final reflected triangle: A'(-25, 0), B'(-45, -25), C'(-55, -15)


  ► Example 6: Composite Sequence (Scale, Rotate, Translate)
  ──────────────────────────────────────────────────────────

  Square A(0,0), B(2,0), C(2,2), D(0,2). Scale by 2 about origin, rotate
  45° about origin, translate by (5, 3). Find final coordinates.

  Step 1: Scale S(2, 2)
      A(0,0)→(0,0)  B(2,0)→(4,0)  C(2,2)→(4,4)  D(0,2)→(0,4)

  Step 2: Rotate 45° (cos 45° = sin 45° = √2/2 ≈ 0.707)
      A(0,0) → (0, 0)
      B(4,0) → (4×0.707, 4×0.707) = (2.83, 2.83)
      C(4,4) → (4×0.707-4×0.707, 4×0.707+4×0.707) = (0, 5.66)
      D(0,4) → (-4×0.707, 4×0.707) = (-2.83, 2.83)

  Step 3: Translate T(5, 3)
      A → (5, 3)
      B → (7.83, 5.83)
      C → (5, 8.66)
      D → (2.17, 5.83)



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3.5  WINDOWING CONCEPTS AND 2D VIEWING PIPELINE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Key Definitions
  ──────────────────

  ┌───────────────────┬──────────────────────────────────────────────────────┐
  │  TERM             │  DEFINITION                                         │
  ├───────────────────┼──────────────────────────────────────────────────────┤
  │  World            │  The coordinate system in which the scene/objects   │
  │  Coordinate       │  are defined. Can be infinite in extent. Uses       │
  │  System           │  real-number coordinates (e.g., meters).            │
  ├───────────────────┼──────────────────────────────────────────────────────┤
  │  Window           │  A rectangular region in WORLD coordinates that     │
  │                   │  specifies which part of the scene to display.      │
  │                   │  Also called the "clipping rectangle."              │
  │                   │  Defined by (xw_min, yw_min, xw_max, yw_max).      │
  ├───────────────────┼──────────────────────────────────────────────────────┤
  │  Viewport         │  A rectangular region on the OUTPUT DEVICE (screen) │
  │                   │  where the window contents are displayed.           │
  │                   │  Defined by (xv_min, yv_min, xv_max, yv_max).      │
  │                   │  Uses device coordinates (pixel positions).         │
  ├───────────────────┼──────────────────────────────────────────────────────┤
  │  Device           │  The coordinate system of the output device.        │
  │  Coordinate       │  Integer pixel positions on the screen.             │
  │  System           │                                                     │
  └───────────────────┴──────────────────────────────────────────────────────┘


  ► Difference Between Window and Viewport
  ─────────────────────────────────────────

  ┌────────────────────────┬──────────────────────────┬──────────────────────┐
  │  ASPECT                │  WINDOW                  │  VIEWPORT            │
  ├────────────────────────┼──────────────────────────┼──────────────────────┤
  │  Coordinate Space      │  World coordinates       │  Device coordinates  │
  ├────────────────────────┼──────────────────────────┼──────────────────────┤
  │  Purpose               │  Selects WHAT to show    │  Selects WHERE to    │
  │                        │  from the scene          │  show it on screen   │
  ├────────────────────────┼──────────────────────────┼──────────────────────┤
  │  Unit                  │  Real-world units        │  Pixels              │
  │                        │  (meters, etc.)          │                      │
  ├────────────────────────┼──────────────────────────┼──────────────────────┤
  │  Effect of Changing    │  Zooming in/out, panning │  Resizing, moving    │
  │                        │  (changes visible scene) │  the display area    │
  └────────────────────────┴──────────────────────────┴──────────────────────┘


  ► 2D Viewing Pipeline
  ──────────────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  World          Construct         Apply           Map to          │
  │  Coordinate  →  Window &      →   Clipping    →   Viewport   →  │
  │  Scene          View Params       (clip to         (device        │
  │  (objects)      (window           window           coordinates)   │
  │                 boundaries)       boundaries)                     │
  │                                                                   │
  │  ┌─────────┐   ┌─────────┐      ┌─────────┐    ┌─────────┐     │
  │  │ Define  │   │ Define  │      │ Remove  │    │ Scale & │     │
  │  │ objects │──►│ window  │─────►│ parts   │───►│ map to  │     │
  │  │ in WC   │   │ bounds  │      │ outside │    │ viewport│     │
  │  └─────────┘   └─────────┘      └─────────┘    └─────────┘     │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘

  The steps in detail:

  1. Model Transformation — position objects in world coordinates
  2. Viewing Transformation — define the window (what portion to view)
  3. Clipping — remove parts outside the window boundary
  4. Window-to-Viewport Mapping — transform from WC to device coords
  5. Device Output — render pixels on screen



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3.6  WINDOW TO VIEWPORT TRANSFORMATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Derivation
  ─────────────

  We need to map a point (xw, yw) in the window to (xv, yv) in the
  viewport such that proportional positions are preserved.

  The proportional position of xw in the window equals the proportional
  position of xv in the viewport:

      (xw - xw_min) / (xw_max - xw_min)  =  (xv - xv_min) / (xv_max - xv_min)

  Solving for xv:

  ╔══════════════════════════════════════════════════════════════════════════╗
  ║                                                                        ║
  ║  xv = xv_min + (xw - xw_min) × (xv_max - xv_min) / (xw_max - xw_min)║
  ║                                                                        ║
  ║  yv = yv_min + (yw - yw_min) × (yv_max - yv_min) / (yw_max - yw_min)║
  ║                                                                        ║
  ╚══════════════════════════════════════════════════════════════════════════╝

  Defining scale factors:
      Sₓ = (xv_max - xv_min) / (xw_max - xw_min)
      Sᵧ = (yv_max - yv_min) / (yw_max - yw_min)

  Simplified:
      xv = xv_min + (xw - xw_min) × Sₓ
      yv = yv_min + (yw - yw_min) × Sᵧ


  ► Matrix Form
  ──────────────

  The transformation can be decomposed as:
  1. Translate window to origin:  T(-xw_min, -yw_min)
  2. Scale to viewport size:      S(Sₓ, Sᵧ)
  3. Translate to viewport position: T(xv_min, yv_min)

  M = T(xv_min, yv_min) · S(Sₓ, Sᵧ) · T(-xw_min, -yw_min)


  ► Solved Example — Window to Viewport Mapping
  ──────────────────────────────────────────────

  Window: xw_min=0, yw_min=0, xw_max=20, yw_max=20
  Viewport: xv_min=100, yv_min=100, xv_max=400, yv_max=400
  Map point (10, 15).

  Sₓ = (400 - 100) / (20 - 0) = 300/20 = 15
  Sᵧ = (400 - 100) / (20 - 0) = 300/20 = 15

  xv = 100 + (10 - 0) × 15 = 100 + 150 = 250
  yv = 100 + (15 - 0) × 15 = 100 + 225 = 325

  Viewport coordinates: (250, 325)



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3.7  LINE CLIPPING — COHEN-SUTHERLAND ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  WHY CLIPPING?                                                             │
│                                                                            │
│  Not all parts of the scene fall within the window. Clipping removes      │
│  portions of primitives that lie outside the clipping boundary. Without   │
│  clipping, lines and polygons would extend beyond the display area,       │
│  causing artifacts, incorrect rendering, and wasted computation.          │
│                                                                            │
│  Cohen-Sutherland is the most widely studied and efficient line clipping  │
│  algorithm. It uses region codes to quickly classify and clip lines.      │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Region Codes (Outcodes)
  ──────────────────────────

  The clipping window divides the plane into 9 regions. Each region is
  assigned a 4-bit code (TBRL):

      Bit 4 (T): Above top    →  y > yw_max
      Bit 3 (B): Below bottom →  y < yw_min
      Bit 2 (R): Right of     →  x > xw_max
      Bit 1 (L): Left of      →  x < xw_min

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │       1001    │    1000    │    1010                              │
  │    (Above,    │  (Above)  │  (Above,                             │
  │     Left)     │           │   Right)                              │
  │  ─────────────┼───────────┼─────────────                         │
  │       0001    │    0000   │    0010                               │
  │    (Left)     │  (Inside) │  (Right)                              │
  │  ─────────────┼───────────┼─────────────                         │
  │       0101    │    0100   │    0110                               │
  │    (Below,    │  (Below)  │  (Below,                              │
  │     Left)     │           │   Right)                              │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Algorithm Steps
  ──────────────────

  1. Compute region codes for both endpoints P₁ and P₂.

  2. Check for trivial acceptance or rejection:
     • If code₁ OR code₂ = 0000 → BOTH inside → ACCEPT entire line
     • If code₁ AND code₂ ≠ 0000 → BOTH on same outside → REJECT

  3. If neither trivial case applies, the line partially crosses the
     window. Find the intersection with the window boundary where
     a non-zero bit indicates, clip, and repeat.


  ► Intersection Formulas
  ────────────────────────

  When clipping against a boundary, use the line parametric equation:

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  Left boundary   (x = xw_min):                                  │
  │    y = y₁ + (y₂-y₁)(xw_min - x₁)/(x₂-x₁)                     │
  │                                                                  │
  │  Right boundary  (x = xw_max):                                  │
  │    y = y₁ + (y₂-y₁)(xw_max - x₁)/(x₂-x₁)                     │
  │                                                                  │
  │  Bottom boundary (y = yw_min):                                   │
  │    x = x₁ + (x₂-x₁)(yw_min - y₁)/(y₂-y₁)                     │
  │                                                                  │
  │  Top boundary    (y = yw_max):                                   │
  │    x = x₁ + (x₂-x₁)(yw_max - y₁)/(y₂-y₁)                     │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘


  ► Solved Example — Cohen-Sutherland
  ────────────────────────────────────

  Clip window: A(20, 20), B(90, 20), C(90, 70), D(20, 70)
      xw_min = 20, xw_max = 90, yw_min = 20, yw_max = 70

  Line: P₁(10, 30) to P₂(80, 90)

  Step 1: Region codes
      P₁(10, 30): x=10 < 20 → Left bit set.  y=30 in [20,70].
                  Code = 0001

      P₂(80, 90): x=80 in [20,90].  y=90 > 70 → Top bit set.
                  Code = 1000

  Step 2: Trivial tests
      OR  = 0001 | 1000 = 1001 ≠ 0000 → not trivial accept
      AND = 0001 & 1000 = 0000         → not trivial reject
      → Must clip

  Step 3: P₁ has code 0001 (Left). Clip against left boundary (x=20):
      y = 30 + (90-30)(20-10)/(80-10) = 30 + 60(10/70) = 30 + 8.57 = 38.57

      New P₁' = (20, 38.57)
      Code of P₁' = 0000 (inside)

  Step 4: P₂ has code 1000 (Top). Clip against top boundary (y=70):
      x = 10 + (80-10)(70-30)/(90-30) = 10 + 70(40/60) = 10 + 46.67 = 56.67

      New P₂' = (56.67, 70)
      Code of P₂' = 0000 (inside)

  Step 5: Both codes = 0000 → ACCEPT
      Clipped line: (20, 38.57) to (56.67, 70)



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  3.8  POLYGON CLIPPING — SUTHERLAND-HODGMAN ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  KEY IDEA                                                                  │
│                                                                            │
│  Clip the polygon against each boundary of the clipping rectangle one     │
│  at a time (left, right, bottom, top). After clipping against one         │
│  boundary, the output vertex list becomes the input for the next          │
│  boundary. This "pipeline" approach simplifies the algorithm greatly.     │
└─────────────────────────────────────────────────────────────────────────────┘


  ► The Four Cases (for each edge of the clip boundary)
  ──────────────────────────────────────────────────────

  For each edge from vertex S to vertex P:

  ┌──────────────────────┬────────────────────────────────────────────┐
  │  CASE                │  ACTION                                    │
  ├──────────────────────┼────────────────────────────────────────────┤
  │  S inside, P inside  │  Output P                                 │
  │                      │  (both inside, keep the endpoint)          │
  ├──────────────────────┼────────────────────────────────────────────┤
  │  S inside, P outside │  Output intersection I                    │
  │                      │  (leaving the boundary)                   │
  ├──────────────────────┼────────────────────────────────────────────┤
  │  S outside, P outside│  Output nothing                           │
  │                      │  (entirely outside)                       │
  ├──────────────────────┼────────────────────────────────────────────┤
  │  S outside, P inside │  Output intersection I, then P            │
  │                      │  (entering the boundary)                  │
  └──────────────────────┴────────────────────────────────────────────┘


  ► Algorithm Steps
  ──────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  Input: Polygon vertex list, clip boundary                      │
  │  Output: Clipped polygon vertex list                            │
  │                                                                  │
  │  For each clip boundary (Left, Right, Bottom, Top):             │
  │      new_vertices = empty list                                  │
  │      S = last vertex in current list                            │
  │      For each vertex P in current list:                         │
  │          if S inside AND P inside:                              │
  │              add P to new_vertices                              │
  │          else if S inside AND P outside:                        │
  │              add intersection(S,P,boundary) to new_vertices     │
  │          else if S outside AND P outside:                       │
  │              add nothing                                        │
  │          else if S outside AND P inside:                        │
  │              add intersection(S,P,boundary) to new_vertices     │
  │              add P to new_vertices                              │
  │          S = P                                                  │
  │      current list = new_vertices                                │
  └──────────────────────────────────────────────────────────────────┘


  ► Solved Example — Sutherland-Hodgman
  ──────────────────────────────────────

  Clip triangle (50, 150), (150, 150), (100, 50) against clip window
  with left boundary x = 60.

  Vertices: A(50, 150), B(150, 150), C(100, 50)

  Clip against LEFT (x = 60):

  Edge A→B: A(50) is outside (50 < 60), B(150) is inside
      → Output intersection I₁ and B
      I₁: y = 150 + (150-150)(60-50)/(150-50) = 150
      I₁ = (60, 150)
      Output: (60, 150), (150, 150)

  Edge B→C: B(150) inside, C(100) inside
      → Output C
      Output: (100, 50)

  Edge C→A: C(100) inside, A(50) outside
      → Output intersection I₂
      I₂: y = 50 + (150-50)(60-100)/(50-100) = 50 + 100(−40/−50) = 50+80 = 130
      I₂ = (60, 130)
      Output: (60, 130)

  After clipping against LEFT: (60,150), (150,150), (100,50), (60,130)
  Then continue with RIGHT, BOTTOM, TOP boundaries similarly.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ADDITIONAL CONCEPTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Affine vs. Projective Transformations
  ────────────────────────────────────────

  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  AFFINE                │  PROJECTIVE                                 │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Preserves parallelism │  Parallel lines can converge                │
  │  (parallel lines stay  │  (vanishing points, perspective)           │
  │  parallel)             │                                             │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Preserves ratios of   │  Distances and ratios are NOT preserved    │
  │  distances along a     │                                             │
  │  line                  │                                             │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Includes: translation,│  Includes: perspective projection          │
  │  rotation, scaling,    │                                             │
  │  shearing, reflection  │                                             │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  3rd row of matrix is  │  3rd row has non-trivial values            │
  │  always [0, 0, 1]      │  (causes w ≠ 1 after transform)           │
  └────────────────────────┴──────────────────────────────────────────────┘


  ► Active vs. Passive Transformations
  ─────────────────────────────────────

  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  ACTIVE                │  PASSIVE                                    │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  The OBJECT moves      │  The COORDINATE SYSTEM moves                │
  │  relative to a fixed   │  relative to a fixed object                │
  │  coordinate system     │                                             │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Result: object at     │  Result: same object, different            │
  │  new position          │  coordinate description                    │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Used in: modeling     │  Used in: viewing (camera) transforms      │
  └────────────────────────┴──────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OPENGL LAB — 2D TRANSFORMATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► OpenGL Transform Functions
  ─────────────────────────────

  ┌──────────────────────────────┬──────────────────────────────────────────┐
  │  FUNCTION                    │  EFFECT                                 │
  ├──────────────────────────────┼──────────────────────────────────────────┤
  │  glTranslatef(tx, ty, 0)     │  Translate by (tx, ty) in 2D           │
  │  glRotatef(angle, 0, 0, 1)   │  Rotate by angle° about Z-axis (2D)   │
  │  glScalef(sx, sy, 1)         │  Scale by (sx, sy) in 2D              │
  └──────────────────────────────┴──────────────────────────────────────────┘

  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  IMPORTANT: OpenGL applies transforms in REVERSE ORDER!               ║
  ║                                                                        ║
  ║  The LAST transform function call before drawing is the FIRST         ║
  ║  applied to the object. This is because each call post-multiplies     ║
  ║  the current matrix:  M = M_current × M_new                          ║
  ║                                                                        ║
  ║  To rotate about pivot (px, py):                                      ║
  ║    glTranslatef(px, py, 0);     // Step 3 (applied last)              ║
  ║    glRotatef(angle, 0, 0, 1);   // Step 2                            ║
  ║    glTranslatef(-px, -py, 0);   // Step 1 (applied first)            ║
  ║    drawObject();                                                       ║
  ╚══════════════════════════════════════════════════════════════════════════╝


  ► Example Program: 2D Transformations
  ──────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  #include <GL/glut.h>                                          │
  │                                                                 │
  │  void drawTriangle() {                                         │
  │      glBegin(GL_TRIANGLES);                                    │
  │          glVertex2f(0, 0);                                     │
  │          glVertex2f(100, 0);                                   │
  │          glVertex2f(50, 80);                                   │
  │      glEnd();                                                  │
  │  }                                                              │
  │                                                                 │
  │  void display() {                                              │
  │      glClear(GL_COLOR_BUFFER_BIT);                             │
  │                                                                 │
  │      // Original (red)                                         │
  │      glColor3f(1, 0, 0);                                       │
  │      glPushMatrix();                                           │
  │      glTranslatef(100, 100, 0);                                │
  │      drawTriangle();                                           │
  │      glPopMatrix();                                            │
  │                                                                 │
  │      // Rotated 45° about center (green)                       │
  │      glColor3f(0, 1, 0);                                       │
  │      glPushMatrix();                                           │
  │      glTranslatef(150, 140, 0);   // pivot back                │
  │      glRotatef(45, 0, 0, 1);     // rotate                    │
  │      glTranslatef(-50, -40, 0);  // pivot to origin            │
  │      drawTriangle();                                           │
  │      glPopMatrix();                                            │
  │                                                                 │
  │      // Scaled 2x about (100,100) (blue)                       │
  │      glColor3f(0, 0, 1);                                       │
  │      glPushMatrix();                                           │
  │      glTranslatef(100, 100, 0);   // fixed point back          │
  │      glScalef(2, 2, 1);          // scale                     │
  │      glTranslatef(-100, -100, 0); // fixed point to origin     │
  │      drawTriangle();                                           │
  │      glPopMatrix();                                            │
  │                                                                 │
  │      glFlush();                                                │
  │  }                                                              │
  │                                                                 │
  │  int main(int argc, char** argv) {                             │
  │      glutInit(&argc, argv);                                    │
  │      glutInitWindowSize(600, 600);                             │
  │      glutCreateWindow("2D Transforms");                        │
  │      gluOrtho2D(0, 600, 0, 600);                              │
  │      glutDisplayFunc(display);                                 │
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
  │  Basic Transforms          │  5 types: T, R, S, Reflection, Shear       │
  │                            │  Translation is additive; others are ×     │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Homogeneous Coords        │  (x,y) → (x,y,1); all transforms become   │
  │                            │  3×3 matrix multiplications; w coordinate  │
  │                            │  enables translation as multiplication     │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Composite Transforms      │  Right-to-left matrix order; pivot         │
  │                            │  rotation = T · R · T⁻¹; fixed-point      │
  │                            │  scaling = T · S · T⁻¹                    │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Window                    │  Rectangle in world coords that selects    │
  │                            │  what to display                           │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Viewport                  │  Rectangle on screen where it's displayed  │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Window→Viewport           │  xv = xv_min + (xw-xw_min) × Sₓ          │
  │                            │  Sₓ = (xv_max-xv_min)/(xw_max-xw_min)    │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Cohen-Sutherland          │  4-bit region codes (TBRL), trivial        │
  │                            │  accept (OR=0), trivial reject (AND≠0),   │
  │                            │  clip at boundaries                       │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Sutherland-Hodgman        │  Clip polygon against one boundary at a   │
  │                            │  time; 4 cases (in-in, in-out, out-out,   │
  │                            │  out-in); pipeline approach                │
  └────────────────────────────┴──────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                         END OF CHAPTER 3                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝


---

## 📝 Exam Practice Questions

### From AI-Generated Sets (aiQuestions.txt)

**Set 1, Q3:**
a. Define the homogeneous coordinate system and explain why it is used in computer graphics transformations. Write the homogeneous matrix representations for translation, rotation, and scaling.
b. Perform fixed-point scaling of triangle P(2, 2), Q(6, 2), R(4, 6) with scaling factors Sx = 2 and Sy = 1.5 about the fixed point (4, 3). Show all steps.

**Set 2, Q3:**
a. What is 2D viewing pipeline? Explain each stage of the pipeline with a diagram.
b. Reflect the triangle with vertices A(3, 4), B(7, 4), C(5, 8) about the line y = −x. Show all transformation steps using composite matrices.

**Set 3, Q3:**
a. Perform rotation of a rectangle with vertices A(1, 1), B(4, 1), C(4, 3), D(1, 3) by 90 degrees counterclockwise about the pivot point (2, 2). Show all steps.
b. Explain the Cohen-Sutherland line clipping algorithm. Clip the line segment from P1(40, 15) to P2(75, 45) against the window defined by Xwmin = 20, Xwmax = 60, Ywmin = 10, Ywmax = 40.

**Set 4, Q3:**
a. What is shearing transformation? Derive the shearing matrix for both X-direction and Y-direction shearing. Apply X-shear with shearing parameter 2 to the triangle (0, 0), (4, 0), (2, 3).
b. Explain the Sutherland-Hodgman polygon clipping algorithm. Illustrate the four possible cases of edge-window boundary intersection with diagrams.

**Set 5, Q3:**
a. What is composite transformation? Derive the composite matrix for rotating an object about an arbitrary pivot point (px, py) by angle theta.
b. Derive the window-to-viewport coordinate transformation. If a window is defined by (0, 0) to (20, 20) and viewport by (100, 100) to (300, 300), map the point (5, 10).

**Set 6, Q3:**
a. Define 2D translation, rotation, and scaling transformations. Write their 3 × 3 homogeneous transformation matrices and explain the role of each element.
b. Using the Cohen-Sutherland algorithm, clip the line from P1(30, 60) to P2(60, 25) against the clipping window with boundaries Xmin = 10, Xmax = 50, Ymin = 10, Ymax = 50. Show all steps with region codes.

**Set 7, Q3:**
a. Perform reflection of the triangle with vertices (1, 2), (4, 2), (3, 5) about the Y-axis. Also perform reflection about the line y = x. Show both results separately.
b. Explain the Sutherland-Hodgman polygon clipping algorithm. Clip a triangle with vertices (10, 10), (60, 10), (35, 70) against the clipping window with Xmin = 20, Xmax = 50, Ymin = 15, Ymax = 55. Show processing for each window edge.

**Set 8, Q3:**
a. Derive the composite transformation matrix for scaling an object about a fixed point (h, k) with scaling factors Sx and Sy. Apply it to scale the triangle (1, 1), (3, 1), (2, 4) by Sx = 2, Sy = 3 about fixed point (2, 2).
b. What is the significance of clipping in computer graphics? Explain the four region codes in Cohen-Sutherland algorithm and the rules for trivial acceptance and trivial rejection.

**Set 9, Q3:**
a. What is composite transformation? A square with vertices A(0, 0), B(2, 0), C(2, 2), D(0, 2) is first scaled by factor 2 about the origin, then rotated 45 degrees about the origin, and finally translated by (5, 3). Find the final coordinates using composite transformation matrix.
b. Explain the 2D viewing pipeline. What are the mathematical steps to convert world coordinates to device coordinates?

**Set 10, Q3:**
a. What are the different types of 2D geometric transformations? Derive the transformation matrix for reflection about an arbitrary line y = mx + c.
   *OR:* Perform reflection of the object with vertices (1, 2), (5, 2), (5, 6), (1, 6) about the line y = x − 2. Show all composite transformation steps.
b. Using the Cohen-Sutherland algorithm, clip the line from P1(5, 25) to P2(50, 5) against the window with Xmin = 10, Xmax = 40, Ymin = 10, Ymax = 30. Show all steps with region codes and intersection calculations.

---

### From Past Papers (Questions.txt)

**Set 1, Q3:**
a. Differentiate between window and viewport. Discuss the 2-Dimensional Viewing Pipeline with the different steps involved. Further derivation is needed for the window-to-viewport coordinate transformation.
b. A mirror is placed vertically such that it passes through the points (5, 0) and (0, 5). Find the reflected view of triangle ABC with coordinates A(5, 30), B(30, 50), C(20, 60).
   *OR:* What is the significance of clipping in computer graphics? Let ABCD be the rectangular window A(20, 20), B(90, 20), C(90, 70), and D(20, 70). Find the region code for the end points and use the Cohen-Sutherland line clipping algorithm to clip the line P₁P₂ with P₁(10, 30) and P₂(80, 90).

**Set 2, Q3:**
a. What will be the final coordinates of a triangle with vertices A(5, 8), B(15, 8), C(10, 16) after rotating it about a fixed point (10, 5) and then shifting it down by two units?
b. Define window and viewport. Derive a matrix for window-to-viewport transformation along with the necessary steps.

**Set 3, Q3:**
a. What is uniform scaling? Reflect the object with vertices (2, 3), (4, 3), (4, 5) about the line y = x + 1.
b. How is the Scan Line algorithm different from the Flood Fill algorithm for filling polygons? Explain.

**Set 3, Q4a** *(clipping topic):*
What do you understand by the term clipping? Explain the Cohen-Sutherland Line Clipping Algorithm with a suitable example.

---

### Related Short Notes Topics (from Q7)
- Sutherland-Hodgman polygon clipping algorithm — *aiQ Set 2*
- Window-to-viewport transformation — *aiQ Set 4*
- Reflection transformation in 2D — *aiQ Set 5*
- Homogeneous coordinate system — *aiQ Set 8*
- Shearing transformation — *aiQ Set 9*
