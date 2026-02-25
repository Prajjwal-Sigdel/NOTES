
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║            CHAPTER 2 — SCAN CONVERSION ALGORITHMS                            ║
║                                                                              ║
║            CMP 234 · Pokhara University · BE Computer                        ║
║            Syllabus Hours: 7                                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝


This chapter covers the fundamental algorithms that convert geometric
primitives (lines, circles, ellipses) into pixel representations on a raster
display. These algorithms determine which pixels to illuminate and how to fill
regions efficiently. They form the backbone of every graphics rendering system
— from simple 2D line drawing to complex 3D scene rasterization.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.1  SCAN CONVERSION — CONCEPT AND MOTIVATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  DEFINITION                                                                 │
│                                                                             │
│  Scan Conversion (also called rasterization) is the process of              │
│  converting a geometric primitive described in continuous mathematical      │
│  terms (e.g., a line from (x₁,y₁) to (x₂,y₂)) into a set of discrete        │
│  pixel positions on a raster display that best approximates that            │
│  primitive.                                                                 │
│                                                                             │
│  Since a raster display is a grid of discrete pixels, we cannot draw        │
│  a perfectly smooth line — we can only select pixels that lie closest       │
│  to the ideal mathematical line. The challenge is to do this quickly,       │
│  accurately, and using only integer arithmetic when possible.               │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Why Is Scan Conversion Important?
  ────────────────────────────────────

  • Every visible object on a raster display must pass through scan
    conversion — lines, circles, polygons, curves, text characters.

  • The scan conversion algorithm directly affects:
      ✓ Rendering speed     — called millions of times per frame
      ✓ Visual quality      — how closely pixels match the ideal shape
      ✓ Hardware cost       — integer-only algorithms enable cheap hardware

  • Modern GPUs implement highly optimized scan conversion in dedicated
    hardware (rasterizer stage of the graphics pipeline).


  ► The Scan Conversion Pipeline
  ──────────────────────────────

        Mathematical         Determine           Set Pixel
        Description    ───►  Pixel       ───►    in Frame
        (endpoints,          Positions            Buffer
         center, radius)     (algorithm)

        y = mx + b           (3, 2)               framebuffer[3][2] = color
        (x₁,y₁)→(x₂,y₂)      (4, 3)               framebuffer[4][3] = color
                             (5, 3)               framebuffer[5][3] = color
                             ...                  ...


  ► Requirements of a Good Scan Conversion Algorithm
  ───────────────────────────────────────────────────

  ┌────────────────────────┬──────────────────────────────────────────────────┐
  │  REQUIREMENT           │  EXPLANATION                                     │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Accuracy              │  Pixels should lie as close to the ideal         │
  │                        │  geometric shape as possible.                    │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Speed                 │  Must use fast operations (addition, bit         │
  │                        │  shifts) — avoid multiplication, division,       │
  │                        │  and floating-point whenever possible.           │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Uniform Brightness    │  Lines of the same length should appear          │
  │                        │  equally bright regardless of slope.             │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  No Gaps               │  The generated pixels should form a              │
  │                        │  continuous, connected path — no holes.          │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Endpoint Accuracy     │  The line must start and end at the correct      │
  │                        │  pixel positions.                                │
  └────────────────────────┴──────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.2  LINE DRAWING ALGORITHMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


Line drawing is the most fundamental graphics operation. Given two endpoints
(x₁, y₁) and (x₂, y₂), we need to find which pixels best represent the
straight line between them.

  The mathematical equation of a line:
      y = mx + b
  where:
      m = Δy / Δx = (y₂ - y₁) / (x₂ - x₁)        [slope]
      b = y₁ - m·x₁                              [y-intercept]

  The direct approach (calculate y = mx + b for each x) is slow because it
  requires a floating-point multiplication per pixel. The algorithms below
  are much faster.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.2.1  DIGITAL DIFFERENTIAL ANALYZER (DDA) ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  KEY IDEA                                                                  │
│                                                                            │
│  DDA is an incremental algorithm that uses the line equation               │
│  directly. Instead of computing y = mx + b from scratch for each x,       │
│  it steps along one axis (whichever has the larger range) by 1 pixel      │
│  at a time and increments the other axis by the slope (or inverse         │
│  slope). Pixels are obtained by rounding the incremented values.          │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Algorithm Steps
  ─────────────────

  Given endpoints (x₁, y₁) and (x₂, y₂):

  Step 1:  Compute  Δx = x₂ - x₁   and   Δy = y₂ - y₁

  Step 2:  Determine the number of steps:
           steps = max(|Δx|, |Δy|)

  Step 3:  Compute increments per step:
           x_increment = Δx / steps
           y_increment = Δy / steps

  Step 4:  Starting from (x₁, y₁), repeat 'steps' times:
           x = x + x_increment
           y = y + y_increment
           Plot pixel at (round(x), round(y))


  ► Why step along the axis with the larger range?
  ─────────────────────────────────────────────────

  If |Δx| > |Δy| (shallow slope), we step x by 1 and y by m.
  If |Δy| > |Δx| (steep slope), we step y by 1 and x by 1/m.
  This ensures we never skip a pixel — every column (or row) gets
  exactly one pixel, producing a connected line with no gaps.


  ► Pseudocode
  ─────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  procedure DDA_Line(x1, y1, x2, y2):                           │
  │      dx = x2 - x1                                              │
  │      dy = y2 - y1                                              │
  │      steps = max(abs(dx), abs(dy))                             │
  │                                                                 │
  │      x_inc = dx / steps                                        │
  │      y_inc = dy / steps                                        │
  │                                                                 │
  │      x = x1                                                    │
  │      y = y1                                                    │
  │                                                                 │
  │      for i = 0 to steps:                                       │
  │          plot(round(x), round(y))                              │
  │          x = x + x_inc                                         │
  │          y = y + y_inc                                         │
  └──────────────────────────────────────────────────────────────────┘


  ► Solved Example 1 — DDA: Line from (2, 3) to (12, 8)
  ──────────────────────────────────────────────────────

  Δx = 12 - 2 = 10        Δy = 8 - 3 = 5
  steps = max(10, 5) = 10
  x_inc = 10/10 = 1.0     y_inc = 5/10 = 0.5

  ┌──────┬────────┬────────┬──────────────────┐
  │ Step │   x    │   y    │  Pixel (round)   │
  ├──────┼────────┼────────┼──────────────────┤
  │   0  │  2.0   │  3.0   │    (2,  3)       │
  │   1  │  3.0   │  3.5   │    (3,  4)       │
  │   2  │  4.0   │  4.0   │    (4,  4)       │
  │   3  │  5.0   │  4.5   │    (5,  5)       │
  │   4  │  6.0   │  5.0   │    (6,  5)       │
  │   5  │  7.0   │  5.5   │    (7,  6)       │
  │   6  │  8.0   │  6.0   │    (8,  6)       │
  │   7  │  9.0   │  6.5   │    (9,  7)       │
  │   8  │ 10.0   │  7.0   │   (10,  7)       │
  │   9  │ 11.0   │  7.5   │   (11,  8)       │
  │  10  │ 12.0   │  8.0   │   (12,  8)       │
  └──────┴────────┴────────┴──────────────────┘


  ► Solved Example 2 — DDA: Line from (5, 5) to (15, 9)
  ──────────────────────────────────────────────────────

  Δx = 15 - 5 = 10        Δy = 9 - 5 = 4
  steps = max(10, 4) = 10
  x_inc = 10/10 = 1.0     y_inc = 4/10 = 0.4

  ┌──────┬────────┬────────┬──────────────────┐
  │ Step │   x    │   y    │  Pixel (round)   │
  ├──────┼────────┼────────┼──────────────────┤
  │   0  │  5.0   │  5.0   │    (5,  5)       │
  │   1  │  6.0   │  5.4   │    (6,  5)       │
  │   2  │  7.0   │  5.8   │    (7,  6)       │
  │   3  │  8.0   │  6.2   │    (8,  6)       │
  │   4  │  9.0   │  6.6   │    (9,  7)       │
  │   5  │ 10.0   │  7.0   │   (10,  7)       │
  │   6  │ 11.0   │  7.4   │   (11,  7)       │
  │   7  │ 12.0   │  7.8   │   (12,  8)       │
  │   8  │ 13.0   │  8.2   │   (13,  8)       │
  │   9  │ 14.0   │  8.6   │   (14,  9)       │
  │  10  │ 15.0   │  9.0   │   (15,  9)       │
  └──────┴────────┴────────┴──────────────────┘


  ► Solved Example 3 — DDA: Line from (0, 0) to (7, 3)
  ─────────────────────────────────────────────────────

  Δx = 7          Δy = 3
  steps = max(7, 3) = 7
  x_inc = 7/7 = 1.0     y_inc = 3/7 ≈ 0.4286

  ┌──────┬────────┬────────┬──────────────────┐
  │ Step │   x    │   y    │  Pixel (round)   │
  ├──────┼────────┼────────┼──────────────────┤
  │   0  │  0.0   │  0.000 │    (0,  0)       │
  │   1  │  1.0   │  0.429 │    (1,  0)       │
  │   2  │  2.0   │  0.857 │    (2,  1)       │
  │   3  │  3.0   │  1.286 │    (3,  1)       │
  │   4  │  4.0   │  1.714 │    (4,  2)       │
  │   5  │  5.0   │  2.143 │    (5,  2)       │
  │   6  │  6.0   │  2.571 │    (6,  3)       │
  │   7  │  7.0   │  3.000 │    (7,  3)       │
  └──────┴────────┴────────┴──────────────────┘


  ► Advantages and Disadvantages of DDA
  ──────────────────────────────────────

  ┌──────────────────────────────┬──────────────────────────────────────────┐
  │  ADVANTAGES ✓                │  DISADVANTAGES ✗                        │
  ├──────────────────────────────┼──────────────────────────────────────────┤
  │  Simple and easy to          │  Uses floating-point arithmetic         │
  │  understand and implement    │  (addition per step) — slow on          │
  │                              │  hardware without FPU                   │
  ├──────────────────────────────┼──────────────────────────────────────────┤
  │  Faster than direct y=mx+b  │  Accumulated round-off errors can       │
  │  computation (no multiply    │  cause pixel drift over long lines      │
  │  per step)                   │                                         │
  ├──────────────────────────────┼──────────────────────────────────────────┤
  │  Works for all slopes        │  Rounding operation (round()) is        │
  │  (handles |m|<1 and |m|>1)  │  needed each step — extra cost          │
  ├──────────────────────────────┼──────────────────────────────────────────┤
  │  No multiplication in the    │  Not suitable for hardware              │
  │  inner loop                  │  implementation (FP operations)         │
  └──────────────────────────────┴──────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.2.2  BRESENHAM'S LINE DRAWING ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  KEY IDEA                                                                  │
│                                                                            │
│  Bresenham's algorithm uses ONLY integer addition, subtraction, and       │
│  bit shifting — NO floating-point at all. It decides at each step         │
│  whether the next pixel should be to the right (E) or to the upper-      │
│  right (NE) by maintaining a "decision parameter" that tracks the        │
│  error between the ideal line and the chosen pixel.                       │
│                                                                            │
│  This makes it the fastest line drawing algorithm and ideal for           │
│  hardware implementation.                                                  │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Derivation for Slope |m| < 1 (First Octant)
  ──────────────────────────────────────────────

  We derive for the case where 0 < m < 1 (line goes more horizontal than
  vertical). The line moves from left to right, x always increments by 1,
  and we decide whether y stays the same or increments by 1.

  Consider the line equation:  y = (Δy/Δx) · x + b

  At each step, after plotting pixel (xₖ, yₖ), the next x is xₖ + 1.
  The actual (mathematical) y-value at xₖ + 1 is:

      y_actual = m(xₖ + 1) + b

  This y_actual falls between two candidate pixels:
      • Lower pixel:  yₖ        (choose E  — move East)
      • Upper pixel:  yₖ + 1    (choose NE — move NorthEast)

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │   yₖ + 1  ─── ●  (upper candidate — NE)                         │
  │                │                                                  │
  │              d₂│                                                  │
  │                │                                                  │
  │   y_actual ────┤─── ✕  (actual line position)                    │
  │                │                                                  │
  │              d₁│                                                  │
  │                │                                                  │
  │   yₖ      ─── ●  (lower candidate — E)                          │
  │                                                                   │
  │           at x = xₖ + 1                                          │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘

  Distance from actual to lower pixel:
      d₁ = y_actual - yₖ = m(xₖ + 1) + b - yₖ

  Distance from actual to upper pixel:
      d₂ = (yₖ + 1) - y_actual = yₖ + 1 - m(xₖ + 1) - b

  Decision: If d₁ - d₂ < 0, the actual line is closer to the lower
  pixel → choose E (y stays). Otherwise, choose NE (y increments).

      d₁ - d₂ = 2m(xₖ + 1) - 2yₖ + 2b - 1

  Substitute m = Δy/Δx and multiply both sides by Δx to eliminate
  the fraction (Δx > 0, so the sign doesn't change):

      pₖ = Δx(d₁ - d₂) = 2Δy · xₖ - 2Δx · yₖ + c

  where c = 2Δy + Δx(2b - 1) is a constant.


  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  DECISION PARAMETER FORMULA                                            ║
  ║                                                                        ║
  ║  pₖ = 2Δy · xₖ - 2Δx · yₖ + c                                       ║
  ║                                                                        ║
  ║  Decision Rule:                                                        ║
  ║    • If pₖ < 0  →  choose E   →  next pixel: (xₖ+1, yₖ)             ║
  ║    • If pₖ ≥ 0  →  choose NE  →  next pixel: (xₖ+1, yₖ+1)           ║
  ╚══════════════════════════════════════════════════════════════════════════╝


  ► Incremental Form (Avoiding Recomputation)
  ────────────────────────────────────────────

  Instead of computing pₖ from scratch each time, we derive the
  NEXT decision parameter from the current one:

      pₖ₊₁ = pₖ + 2Δy - 2Δx(yₖ₊₁ - yₖ)

  Since (yₖ₊₁ - yₖ) is either 0 or 1:

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  If pₖ < 0  (chose E, y stays):                                 │
  │      pₖ₊₁ = pₖ + 2Δy                                           │
  │                                                                  │
  │  If pₖ ≥ 0  (chose NE, y increments):                           │
  │      pₖ₊₁ = pₖ + 2Δy - 2Δx                                     │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘

  This is the beauty of Bresenham's algorithm — each step requires
  only ONE integer addition and ONE comparison!


  ► Initial Decision Parameter (p₀)
  ──────────────────────────────────

  At the starting point (x₁, y₁), substituting into the formula:

      p₀ = 2Δy - Δx


  ► Complete Algorithm (Slope 0 < m < 1)
  ───────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  procedure Bresenham_Line(x1, y1, x2, y2):                     │
  │      dx = x2 - x1                                              │
  │      dy = y2 - y1                                              │
  │      p = 2*dy - dx                 // initial decision param   │
  │                                                                 │
  │      x = x1,  y = y1                                           │
  │      plot(x, y)                                                │
  │                                                                 │
  │      for i = 1 to dx:                                          │
  │          if p < 0:                                             │
  │              p = p + 2*dy           // choose E                │
  │          else:                                                 │
  │              p = p + 2*dy - 2*dx    // choose NE               │
  │              y = y + 1                                         │
  │          x = x + 1                                             │
  │          plot(x, y)                                            │
  └──────────────────────────────────────────────────────────────────┘


  ► Extension for Slope > 1
  ─────────────────────────

  When |m| > 1, the line is steeper — y changes faster than x. In this
  case, we swap the roles of x and y:
    • y always increments by 1
    • We decide whether x stays or increments
    • p₀ = 2Δx - Δy
    • If pₖ < 0:  pₖ₊₁ = pₖ + 2Δx         (y++, x stays)
    • If pₖ ≥ 0:  pₖ₊₁ = pₖ + 2Δx - 2Δy   (y++, x++)


  ► Solved Example 1 — Bresenham: Line from (20, 10) to (30, 18)
  ───────────────────────────────────────────────────────────────

  Δx = 30 - 20 = 10       Δy = 18 - 10 = 8
  m = 8/10 = 0.8 < 1  →  use standard algorithm
  p₀ = 2(8) - 10 = 6

  2Δy = 16                2Δy - 2Δx = 16 - 20 = -4

  ┌──────┬────────┬────────┬────────┬──────────────────────────────┐
  │ Step │  pₖ    │ (x, y) │  Next  │  pₖ₊₁ calculation           │
  ├──────┼────────┼────────┼────────┼──────────────────────────────┤
  │   0  │   —    │(20,10) │  plot  │  p₀ = 6                     │
  │   1  │   6≥0  │(21,11) │  NE    │  6 + (-4) = 2               │
  │   2  │   2≥0  │(22,12) │  NE    │  2 + (-4) = -2              │
  │   3  │  -2<0  │(23,12) │  E     │ -2 + 16 = 14                │
  │   4  │  14≥0  │(24,13) │  NE    │ 14 + (-4) = 10              │
  │   5  │  10≥0  │(25,14) │  NE    │ 10 + (-4) = 6               │
  │   6  │   6≥0  │(26,15) │  NE    │  6 + (-4) = 2               │
  │   7  │   2≥0  │(27,16) │  NE    │  2 + (-4) = -2              │
  │   8  │  -2<0  │(28,16) │  E     │ -2 + 16 = 14                │
  │   9  │  14≥0  │(29,17) │  NE    │ 14 + (-4) = 10              │
  │  10  │  10≥0  │(30,18) │  NE    │  —                          │
  └──────┴────────┴────────┴────────┴──────────────────────────────┘

  Generated pixels: (20,10) (21,11) (22,12) (23,12) (24,13) (25,14)
                    (26,15) (27,16) (28,16) (29,17) (30,18)


  ► Solved Example 2 — Bresenham: Line from (1, 1) to (8, 5)
  ───────────────────────────────────────────────────────────

  Δx = 7           Δy = 4
  p₀ = 2(4) - 7 = 1
  2Δy = 8          2Δy - 2Δx = 8 - 14 = -6

  ┌──────┬────────┬────────┬────────┬──────────────────────────────┐
  │ Step │  pₖ    │ (x, y) │  Next  │  pₖ₊₁ calculation           │
  ├──────┼────────┼────────┼────────┼──────────────────────────────┤
  │   0  │   —    │ (1, 1) │  plot  │  p₀ = 1                     │
  │   1  │   1≥0  │ (2, 2) │  NE    │  1 + (-6) = -5              │
  │   2  │  -5<0  │ (3, 2) │  E     │ -5 + 8 = 3                  │
  │   3  │   3≥0  │ (4, 3) │  NE    │  3 + (-6) = -3              │
  │   4  │  -3<0  │ (5, 3) │  E     │ -3 + 8 = 5                  │
  │   5  │   5≥0  │ (6, 4) │  NE    │  5 + (-6) = -1              │
  │   6  │  -1<0  │ (7, 4) │  E     │ -1 + 8 = 7                  │
  │   7  │   7≥0  │ (8, 5) │  NE    │  —                          │
  └──────┴────────┴────────┴────────┴──────────────────────────────┘

  Generated pixels: (1,1) (2,2) (3,2) (4,3) (5,3) (6,4) (7,4) (8,5)


  ► Solved Example 3 — Bresenham: Line from (15, 5) to (25, 13)
  ──────────────────────────────────────────────────────────────

  Δx = 10          Δy = 8
  m = 0.8 < 1  →  standard algorithm
  p₀ = 2(8) - 10 = 6
  2Δy = 16         2Δy - 2Δx = 16 - 20 = -4

  ┌──────┬────────┬────────┬────────┬──────────────────────────────┐
  │ Step │  pₖ    │ (x, y) │  Next  │  pₖ₊₁ calculation           │
  ├──────┼────────┼────────┼────────┼──────────────────────────────┤
  │   0  │   —    │(15, 5) │  plot  │  p₀ = 6                     │
  │   1  │   6≥0  │(16, 6) │  NE    │  6 + (-4) = 2               │
  │   2  │   2≥0  │(17, 7) │  NE    │  2 + (-4) = -2              │
  │   3  │  -2<0  │(18, 7) │  E     │ -2 + 16 = 14                │
  │   4  │  14≥0  │(19, 8) │  NE    │ 14 + (-4) = 10              │
  │   5  │  10≥0  │(20, 9) │  NE    │ 10 + (-4) = 6               │
  │   6  │   6≥0  │(21,10) │  NE    │  6 + (-4) = 2               │
  │   7  │   2≥0  │(22,11) │  NE    │  2 + (-4) = -2              │
  │   8  │  -2<0  │(23,11) │  E     │ -2 + 16 = 14                │
  │   9  │  14≥0  │(24,12) │  NE    │ 14 + (-4) = 10              │
  │  10  │  10≥0  │(25,13) │  NE    │  —                          │
  └──────┴────────┴────────┴────────┴──────────────────────────────┘


  ► Solved Example 4 — Bresenham: Line from (2, 1) to (8, 13)  [Slope > 1]
  ──────────────────────────────────────────────────────────────────────────

  Δx = 6           Δy = 12
  m = 12/6 = 2 > 1  →  Swap roles: step y by 1, decide on x

  p₀ = 2Δx - Δy = 2(6) - 12 = 0
  2Δx = 12         2Δx - 2Δy = 12 - 24 = -12

  ┌──────┬────────┬────────┬────────┬──────────────────────────────┐
  │ Step │  pₖ    │ (x, y) │  Next  │  pₖ₊₁ calculation           │
  ├──────┼────────┼────────┼────────┼──────────────────────────────┤
  │   0  │   —    │ (2, 1) │  plot  │  p₀ = 0                     │
  │   1  │   0≥0  │ (3, 2) │  NE    │  0 + (-12) = -12            │
  │   2  │ -12<0  │ (3, 3) │  N     │ -12 + 12 = 0                │
  │   3  │   0≥0  │ (4, 4) │  NE    │  0 + (-12) = -12            │
  │   4  │ -12<0  │ (4, 5) │  N     │ -12 + 12 = 0                │
  │   5  │   0≥0  │ (5, 6) │  NE    │  0 + (-12) = -12            │
  │   6  │ -12<0  │ (5, 7) │  N     │ -12 + 12 = 0                │
  │   7  │   0≥0  │ (6, 8) │  NE    │  0 + (-12) = -12            │
  │   8  │ -12<0  │ (6, 9) │  N     │ -12 + 12 = 0                │
  │   9  │   0≥0  │ (7,10) │  NE    │  0 + (-12) = -12            │
  │  10  │ -12<0  │ (7,11) │  N     │ -12 + 12 = 0                │
  │  11  │   0≥0  │ (8,12) │  NE    │  0 + (-12) = -12            │
  │  12  │ -12<0  │ (8,13) │  N     │  —                          │
  └──────┴────────┴────────┴────────┴──────────────────────────────┘


  ► Comparison: DDA vs. Bresenham's Algorithm
  ────────────────────────────────────────────

  ┌─────────────────────────┬──────────────────────┬──────────────────────┐
  │  CRITERIA               │  DDA                 │  BRESENHAM'S         │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Arithmetic             │  Floating-point      │  Integer only        │
  │                         │  addition + rounding │  addition only       │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Speed                  │  Slower              │  Faster              │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Accuracy               │  Round-off errors    │  No round-off errors │
  │                         │  accumulate          │  (exact integers)    │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Hardware               │  Difficult (needs    │  Easy (only adders   │
  │  Implementation         │  FPU)                │  and comparators)    │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Complexity             │  Simpler to          │  Slightly more       │
  │                         │  understand          │  complex derivation  │
  ├─────────────────────────┼──────────────────────┼──────────────────────┤
  │  Operations per pixel   │  1 FP add + 1 round  │  1 integer add +    │
  │                         │                      │  1 comparison        │
  └─────────────────────────┴──────────────────────┴──────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.3  CIRCLE GENERATION — MIDPOINT CIRCLE ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  WHY NOT USE y = ±√(r² - x²)?                                            │
│                                                                            │
│  The direct equation requires a square root per pixel — extremely slow.   │
│  It also produces non-uniform spacing (pixels bunch up near the top       │
│  and bottom). The midpoint algorithm avoids ALL of this by using only     │
│  integer arithmetic and exploiting the circle's 8-way symmetry.           │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Eight-Way Symmetry of a Circle
  ─────────────────────────────────

  A circle is symmetric about both axes and both diagonals. If we compute
  one pixel (x, y) in the second octant (from 12 o'clock to 1:30), we
  automatically know SEVEN other pixels:

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │                    ( x,  y)     ( y,  x)                         │
  │                    (-x,  y)     (-y,  x)                         │
  │                    ( x, -y)     ( y, -x)                         │
  │                    (-x, -y)     (-y, -x)                         │
  │                                                                   │
  │   From ONE computed point, we plot EIGHT points.                  │
  │   This reduces computation by 8×.                                │
  │                                                                   │
  │               Octant 2 │ Octant 1                                │
  │             (-x,y)     │     (x,y)                               │
  │          ──────────────┼──────────────                            │
  │         (-y,x)         │         (y,x)    Octant 0               │
  │   Octant 3             │                                          │
  │         (-y,-x)        │        (y,-x)    Octant 7               │
  │   Octant 4             │                                          │
  │          ──────────────┼──────────────                            │
  │            (-x,-y)     │    (x,-y)                               │
  │               Octant 5 │ Octant 6                                │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Derivation of the Midpoint Circle Algorithm
  ──────────────────────────────────────────────

  The implicit equation of a circle centered at the origin with radius r:

      f(x, y) = x² + y² - r²

      • f(x, y) < 0  →  point is INSIDE the circle
      • f(x, y) = 0  →  point is ON the circle
      • f(x, y) > 0  →  point is OUTSIDE the circle

  We work in the second octant: starting at (0, r) and moving to where
  x = y (the 45° point). At each step, x increments by 1. We decide
  whether y stays or decrements by 1.

  The midpoint between the two candidates E(xₖ+1, yₖ) and SE(xₖ+1, yₖ-1)
  is:
      midpoint = (xₖ + 1, yₖ - ½)

  Decision parameter = f(midpoint):

      pₖ = f(xₖ + 1, yₖ - ½) = (xₖ + 1)² + (yₖ - ½)² - r²


  ╔══════════════════════════════════════════════════════════════════════════╗
  ║  DECISION RULES                                                        ║
  ║                                                                        ║
  ║  If pₖ < 0  →  midpoint is INSIDE  →  choose E   →  (xₖ+1, yₖ)      ║
  ║                 (circle boundary is beyond midpoint, y stays)          ║
  ║                                                                        ║
  ║  If pₖ ≥ 0  →  midpoint is OUTSIDE →  choose SE  →  (xₖ+1, yₖ-1)    ║
  ║                 (circle boundary is before midpoint, y decrements)     ║
  ╚══════════════════════════════════════════════════════════════════════════╝


  ► Incremental Update
  ─────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  If pₖ < 0  (chose E):                                          │
  │      pₖ₊₁ = pₖ + 2xₖ₊₁ + 1                                    │
  │                                                                  │
  │  If pₖ ≥ 0  (chose SE):                                         │
  │      pₖ₊₁ = pₖ + 2xₖ₊₁ + 1 - 2yₖ₊₁                           │
  │                                                                  │
  │  where xₖ₊₁ = xₖ + 1  and  yₖ₊₁ = yₖ or yₖ - 1               │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘


  ► Initial Decision Parameter (p₀)
  ──────────────────────────────────

  Starting at (0, r):
      p₀ = f(1, r - ½) = 1 + (r - ½)² - r²
         = 1 + r² - r + ¼ - r²
         = 5/4 - r

  For integer arithmetic, we use:  p₀ = 1 - r  (approximation valid
  because we only care about the sign, and the ¼ doesn't affect the
  sign for r ≥ 1).


  ► Algorithm
  ────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  procedure Midpoint_Circle(r):                                  │
  │      x = 0,  y = r                                             │
  │      p = 1 - r                                                 │
  │      plot_circle_points(x, y)                                  │
  │                                                                 │
  │      while x < y:                                              │
  │          x = x + 1                                             │
  │          if p < 0:                                             │
  │              p = p + 2*x + 1                                   │
  │          else:                                                 │
  │              y = y - 1                                         │
  │              p = p + 2*x + 1 - 2*y                             │
  │          plot_circle_points(x, y)                              │
  │                                                                 │
  │  procedure plot_circle_points(x, y):                           │
  │      // Plot all 8 symmetric points:                           │
  │      plot(x, y)   plot(-x, y)   plot(x, -y)   plot(-x, -y)   │
  │      plot(y, x)   plot(-y, x)   plot(y, -x)   plot(-y, -x)   │
  └──────────────────────────────────────────────────────────────────┘


  ► Solved Example 1 — Midpoint Circle: r = 10
  ──────────────────────────────────────────────

  p₀ = 1 - 10 = -9

  ┌──────┬────────┬────────┬────────┬──────────────────────────────┐
  │ Step │  pₖ    │ (x, y) │  Move  │  pₖ₊₁ calculation           │
  ├──────┼────────┼────────┼────────┼──────────────────────────────┤
  │   0  │   —    │(0, 10) │  start │  p₀ = -9                    │
  │   1  │  -9<0  │(1, 10) │  E     │ -9 + 2(1)+1 = -6            │
  │   2  │  -6<0  │(2, 10) │  E     │ -6 + 2(2)+1 = -1            │
  │   3  │  -1<0  │(3, 10) │  E     │ -1 + 2(3)+1 = 6             │
  │   4  │   6≥0  │(4,  9) │  SE    │  6 + 2(4)+1-2(9) = -1       │
  │   5  │  -1<0  │(5,  9) │  E     │ -1 + 2(5)+1 = 10            │
  │   6  │  10≥0  │(6,  8) │  SE    │ 10 + 2(6)+1-2(8) = 7        │
  │   7  │   7≥0  │(7,  7) │  SE    │  — (x = y, stop)            │
  └──────┴────────┴────────┴────────┴──────────────────────────────┘

  Second octant points: (0,10) (1,10) (2,10) (3,10) (4,9) (5,9) (6,8) (7,7)
  Each generates 8 symmetric points → total 8 × 8 = 64 plotted points.


  ► Solved Example 2 — Midpoint Circle: r = 8
  ─────────────────────────────────────────────

  p₀ = 1 - 8 = -7

  ┌──────┬────────┬────────┬────────┬──────────────────────────────┐
  │ Step │  pₖ    │ (x, y) │  Move  │  pₖ₊₁ calculation           │
  ├──────┼────────┼────────┼────────┼──────────────────────────────┤
  │   0  │   —    │(0,  8) │  start │  p₀ = -7                    │
  │   1  │  -7<0  │(1,  8) │  E     │ -7 + 2(1)+1 = -4            │
  │   2  │  -4<0  │(2,  8) │  E     │ -4 + 2(2)+1 = 1             │
  │   3  │   1≥0  │(3,  7) │  SE    │  1 + 2(3)+1-2(7) = -6       │
  │   4  │  -6<0  │(4,  7) │  E     │ -6 + 2(4)+1 = 3             │
  │   5  │   3≥0  │(5,  6) │  SE    │  3 + 2(5)+1-2(6) = 2        │
  │   6  │   2≥0  │(6,  5) │  SE    │  — (x > y, stop)            │
  └──────┴────────┴────────┴────────┴──────────────────────────────┘

  Second octant points: (0,8) (1,8) (2,8) (3,7) (4,7) (5,6) — stop at (6,5)
  since x > y.


  ► Solved Example 3 — Midpoint Circle: r = 5
  ─────────────────────────────────────────────

  p₀ = 1 - 5 = -4

  ┌──────┬────────┬────────┬────────┬──────────────────────────────┐
  │ Step │  pₖ    │ (x, y) │  Move  │  pₖ₊₁ calculation           │
  ├──────┼────────┼────────┼────────┼──────────────────────────────┤
  │   0  │   —    │(0,  5) │  start │  p₀ = -4                    │
  │   1  │  -4<0  │(1,  5) │  E     │ -4 + 2(1)+1 = -1            │
  │   2  │  -1<0  │(2,  5) │  E     │ -1 + 2(2)+1 = 4             │
  │   3  │   4≥0  │(3,  4) │  SE    │  4 + 2(3)+1-2(4) = 3        │
  │   4  │   3≥0  │(4,  3) │  SE    │  — (x > y, stop)            │
  └──────┴────────┴────────┴────────┴──────────────────────────────┘

  Second octant points: (0,5) (1,5) (2,5) (3,4) — stop at (4,3) since x > y.


  ► Solved Example 4 — Midpoint Circle: r = 12
  ──────────────────────────────────────────────

  p₀ = 1 - 12 = -11

  ┌──────┬────────┬────────┬────────┬──────────────────────────────┐
  │ Step │  pₖ    │ (x, y) │  Move  │  pₖ₊₁ calculation           │
  ├──────┼────────┼────────┼────────┼──────────────────────────────┤
  │   0  │   —    │(0, 12) │  start │  p₀ = -11                   │
  │   1  │ -11<0  │(1, 12) │  E     │ -11 + 2(1)+1 = -8           │
  │   2  │  -8<0  │(2, 12) │  E     │  -8 + 2(2)+1 = -3           │
  │   3  │  -3<0  │(3, 12) │  E     │  -3 + 2(3)+1 = 4            │
  │   4  │   4≥0  │(4, 11) │  SE    │   4 + 2(4)+1-2(11) = -9     │
  │   5  │  -9<0  │(5, 11) │  E     │  -9 + 2(5)+1 = 2            │
  │   6  │   2≥0  │(6, 10) │  SE    │   2 + 2(6)+1-2(10) = -5     │
  │   7  │  -5<0  │(7, 10) │  E     │  -5 + 2(7)+1 = 10           │
  │   8  │  10≥0  │(8,  9) │  SE    │  10 + 2(8)+1-2(9) = 9       │
  │   9  │   9≥0  │(9,  8) │  SE    │  — (x > y, stop)            │
  └──────┴────────┴────────┴────────┴──────────────────────────────┘

  Second octant points: (0,12) (1,12) (2,12) (3,12) (4,11) (5,11)
                        (6,10) (7,10) (8,9) — stop at (9,8) since x > y.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.4  ELLIPSE GENERATION — MIDPOINT ELLIPSE ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► Why Different Symmetry from Circle?
  ──────────────────────────────────────

  A circle has 8-way symmetry because rₓ = rᵧ (same radius in all
  directions). An ellipse has TWO different radii (rₓ and rᵧ), so it only
  has 4-way symmetry:

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  From one computed point (x, y), we get FOUR points:             │
  │      (x, y)    (-x, y)    (x, -y)    (-x, -y)                   │
  │                                                                   │
  │  Why not 8-way?  Swapping x and y (as in a circle) doesn't       │
  │  produce valid ellipse points because the radii are different.    │
  │                                                                   │
  │          Quadrant 2  │  Quadrant 1                                │
  │         (-x, y)      │     (x, y)                                │
  │       ───────────────┼───────────────                             │
  │         (-x,-y)      │     (x,-y)                                │
  │          Quadrant 3  │  Quadrant 4                                │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Ellipse Equation and Two Regions
  ───────────────────────────────────

  The implicit equation of an ellipse centered at the origin:

      f(x, y) = rᵧ²·x² + rₓ²·y² - rₓ²·rᵧ²

  Unlike a circle, the ellipse must be processed in TWO REGIONS because
  the slope changes from |slope| < 1 to |slope| > 1 as we trace the
  first quadrant:

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  Region 1:  Start at (0, rᵧ), step x by 1.                     │
  │             Continue while  2·rᵧ²·x  <  2·rₓ²·y                │
  │             (slope magnitude < 1 — x changes faster)             │
  │                                                                   │
  │  Region 2:  Continue from Region 1's endpoint, step y by -1.    │
  │             Continue until y = 0.                                 │
  │             (slope magnitude > 1 — y changes faster)             │
  │                                                                   │
  │   (0,rᵧ)●━━━━━━━━━━━━━━━━━━━━━━━━━━━━╮                         │
  │          ┃   Region 1                  │                          │
  │          ┃   (step x by 1)             │                          │
  │          ┃           Boundary where    │                          │
  │          ┃           2rᵧ²x = 2rₓ²y ───┤                         │
  │          ┃                    Region 2 │                          │
  │          ┃                  (step y)   │                          │
  │          ┃                             ●(rₓ,0)                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Region 1 Decision Parameters
  ───────────────────────────────

  Starting at (0, rᵧ), the midpoint is at (xₖ+1, yₖ - ½):

      p1ₖ = rᵧ²(xₖ+1)² + rₓ²(yₖ - ½)² - rₓ²rᵧ²

  Initial:
      p1₀ = rᵧ² - rₓ²rᵧ + ¼rₓ²

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  If p1ₖ < 0  (midpoint inside → choose E):                      │
  │      p1ₖ₊₁ = p1ₖ + 2rᵧ²xₖ₊₁ + rᵧ²                            │
  │                                                                  │
  │  If p1ₖ ≥ 0  (midpoint outside → choose SE):                    │
  │      p1ₖ₊₁ = p1ₖ + 2rᵧ²xₖ₊₁ - 2rₓ²yₖ₊₁ + rᵧ²                │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘


  ► Region 2 Decision Parameters
  ───────────────────────────────

  Transition to Region 2 when 2rᵧ²x ≥ 2rₓ²y. Now step y by -1 and
  decide on x:

      p2₀ = rᵧ²(x₀ + ½)² + rₓ²(y₀ - 1)² - rₓ²rᵧ²
      (where (x₀, y₀) is the last point from Region 1)

  ┌──────────────────────────────────────────────────────────────────┐
  │                                                                  │
  │  If p2ₖ > 0  (midpoint outside → choose S):                     │
  │      p2ₖ₊₁ = p2ₖ - 2rₓ²yₖ₊₁ + rₓ²                             │
  │                                                                  │
  │  If p2ₖ ≤ 0  (midpoint inside → choose SE):                     │
  │      p2ₖ₊₁ = p2ₖ + 2rᵧ²xₖ₊₁ - 2rₓ²yₖ₊₁ + rₓ²                │
  │                                                                  │
  └──────────────────────────────────────────────────────────────────┘


  ► Solved Example 1 — Midpoint Ellipse: rₓ = 8, rᵧ = 6
  ───────────────────────────────────────────────────────

  rₓ = 8, rᵧ = 6    rₓ² = 64    rᵧ² = 36

  Region 1:  p1₀ = rᵧ² - rₓ²rᵧ + ¼rₓ² = 36 - 64(6) + ¼(64) = 36 - 384 + 16 = -332

  ┌──────┬────────┬────────┬────────┬──────────────────────────────────────┐
  │ Step │  p1ₖ   │ (x, y) │  Move  │  p1ₖ₊₁ calculation                  │
  ├──────┼────────┼────────┼────────┼──────────────────────────────────────┤
  │   0  │   —    │(0,  6) │  start │  p1₀ = -332                         │
  │   1  │-332<0  │(1,  6) │  E     │ -332 + 2(36)(1)+36 = -332+72+36=-224│
  │   2  │-224<0  │(2,  6) │  E     │ -224 + 2(36)(2)+36 = -224+144+36=-44│
  │   3  │ -44<0  │(3,  6) │  E     │  -44 + 2(36)(3)+36 = -44+216+36=208 │
  │   4  │ 208≥0  │(4,  5) │  SE    │ 208+2(36)(4)-2(64)(5)+36            │
  │      │        │        │        │ = 208+288-640+36 = -108              │
  │   5  │-108<0  │(5,  5) │  E     │-108 + 2(36)(5)+36 = -108+360+36=288 │
  │   6  │ 288≥0  │(6,  4) │  SE    │ 288+2(36)(6)-2(64)(4)+36            │
  │      │        │        │        │ = 288+432-512+36 = 244               │
  │   7  │ 244≥0  │(7,  3) │  SE    │ Check: 2rᵧ²x = 2(36)(7) = 504     │
  │      │        │        │        │        2rₓ²y = 2(64)(3) = 384       │
  │      │        │        │        │ 504 > 384 → switch to Region 2      │
  └──────┴────────┴────────┴────────┴──────────────────────────────────────┘

  Region 1 points: (0,6) (1,6) (2,6) (3,6) (4,5) (5,5) (6,4) (7,3)

  Region 2:  Last point = (7, 3)
  p2₀ = rᵧ²(7+½)² + rₓ²(3-1)² - rₓ²rᵧ²
      = 36(56.25) + 64(4) - 64(36)
      = 2025 + 256 - 2304 = -23

  ┌──────┬────────┬────────┬────────┬──────────────────────────────────────┐
  │ Step │  p2ₖ   │ (x, y) │  Move  │  p2ₖ₊₁ calculation                  │
  ├──────┼────────┼────────┼────────┼──────────────────────────────────────┤
  │   1  │ -23≤0  │(8,  2) │  SE    │ -23+2(36)(8)-2(64)(2)+64            │
  │      │        │        │        │ = -23+576-256+64 = 361               │
  │   2  │ 361>0  │(8,  1) │  S     │ 361-2(64)(1)+64 = 361-128+64 = 297  │
  │   3  │ 297>0  │(8,  0) │  S     │  — (y = 0, stop)                    │
  └──────┴────────┴────────┴────────┴──────────────────────────────────────┘

  Region 2 points: (8,2) (8,1) (8,0)
  All first-quadrant points: (0,6)(1,6)(2,6)(3,6)(4,5)(5,5)(6,4)(7,3)(8,2)(8,1)(8,0)
  Each generates 4 symmetric points.


  ► Solved Example 2 — Midpoint Ellipse: rₓ = 6, rᵧ = 4
  ───────────────────────────────────────────────────────

  rₓ = 6, rᵧ = 4    rₓ² = 36    rᵧ² = 16

  Region 1:  p1₀ = 16 - 36(4) + ¼(36) = 16 - 144 + 9 = -119

  ┌──────┬────────┬────────┬────────┬──────────────────────────────────────┐
  │ Step │  p1ₖ   │ (x, y) │  Move  │  p1ₖ₊₁ calculation                  │
  ├──────┼────────┼────────┼────────┼──────────────────────────────────────┤
  │   0  │   —    │(0,  4) │  start │  p1₀ = -119                         │
  │   1  │-119<0  │(1,  4) │  E     │ -119 + 2(16)(1)+16 = -119+32+16=-71 │
  │   2  │ -71<0  │(2,  4) │  E     │  -71 + 2(16)(2)+16 = -71+64+16=9    │
  │   3  │   9≥0  │(3,  3) │  SE    │ 9+2(16)(3)-2(36)(3)+16              │
  │      │        │        │        │ = 9+96-216+16 = -95                  │
  │   4  │ -95<0  │(4,  3) │  E     │ -95+2(16)(4)+16 = -95+128+16=49     │
  │   5  │  49≥0  │(5,  2) │  SE    │ Check: 2rᵧ²x = 2(16)(5) = 160     │
  │      │        │        │        │        2rₓ²y = 2(36)(2) = 144       │
  │      │        │        │        │ 160 > 144 → switch to Region 2      │
  └──────┴────────┴────────┴────────┴──────────────────────────────────────┘

  Region 1 points: (0,4) (1,4) (2,4) (3,3) (4,3) (5,2)

  Region 2:  Last point = (5, 2)
  p2₀ = 16(5.5)² + 36(1)² - 36(16) = 16(30.25) + 36 - 576
      = 484 + 36 - 576 = -56

  ┌──────┬────────┬────────┬────────┬──────────────────────────────────────┐
  │ Step │  p2ₖ   │ (x, y) │  Move  │  p2ₖ₊₁ calculation                  │
  ├──────┼────────┼────────┼────────┼──────────────────────────────────────┤
  │   1  │ -56≤0  │(6,  1) │  SE    │ -56+2(16)(6)-2(36)(1)+36            │
  │      │        │        │        │ = -56+192-72+36 = 100                │
  │   2  │ 100>0  │(6,  0) │  S     │  — (y = 0, stop)                    │
  └──────┴────────┴────────┴────────┴──────────────────────────────────────┘

  Complete first-quadrant: (0,4)(1,4)(2,4)(3,3)(4,3)(5,2)(6,1)(6,0)



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.5  FILLED AREA PRIMITIVES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


Filling a polygon means coloring all the pixels that lie inside its boundary.
There are three main approaches, each with different use cases.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.5.1  SCAN LINE POLYGON FILL ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  KEY IDEA                                                                  │
│                                                                            │
│  Process the polygon one horizontal scan line at a time. For each scan    │
│  line, find all intersection points with polygon edges, sort them in      │
│  x-order, then fill pixels between consecutive PAIRS of intersections.    │
│  This is the standard method used in production renderers.                │
└─────────────────────────────────────────────────────────────────────────────┘


  ► How It Works — Step by Step
  ─────────────────────────────

  1. For each scan line y:
       a. Find all intersections of the scan line with polygon edges.
       b. Sort intersection x-coordinates in ascending order.
       c. Fill pixels between pairs: (x₁→x₂), (x₃→x₄), (x₅→x₆), ...
          This "odd-even" pairing ensures we fill inside regions only.

  2. To handle this efficiently, two data structures are used:

  ┌─────────────────────────┬──────────────────────────────────────────────┐
  │  DATA STRUCTURE          │  PURPOSE                                    │
  ├─────────────────────────┼──────────────────────────────────────────────┤
  │  Edge Table (ET)         │  Stores all polygon edges sorted by their  │
  │                          │  minimum y-coordinate. Each entry contains │
  │                          │  y_max, x_at_y_min, and 1/slope.           │
  ├─────────────────────────┼──────────────────────────────────────────────┤
  │  Active Edge List (AEL)  │  Contains only the edges that intersect    │
  │                          │  the current scan line. Updated as we move │
  │                          │  from one scan line to the next.           │
  └─────────────────────────┴──────────────────────────────────────────────┘

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  Example visualization:                                           │
  │                                                                   │
  │        ╱╲                                                         │
  │       ╱  ╲                                                        │
  │  ────╱────╲────   scan line y = 5                                │
  │     ╱      ╲      intersections at x = 3 and x = 9              │
  │    ╱        ╲     → fill pixels from x = 3 to x = 9             │
  │   ╱──────────╲                                                    │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Algorithm Pseudocode
  ──────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  1. Build the Edge Table (ET) from polygon vertices.            │
  │  2. Set y to the smallest y in ET.                              │
  │  3. Initialize Active Edge List (AEL) to empty.                 │
  │  4. Repeat until both AEL and ET are empty:                     │
  │     a. Move edges from ET to AEL whose y_min = y.               │
  │     b. Sort AEL by x-coordinate.                                │
  │     c. Fill between pairs: (x₁,x₂), (x₃,x₄), ...             │
  │     d. Remove edges from AEL whose y_max = y.                   │
  │     e. Increment y by 1.                                        │
  │     f. Update x in AEL:  x = x + 1/slope                      │
  └──────────────────────────────────────────────────────────────────┘


  ► Special Cases
  ────────────────

  • Horizontal edges: Excluded from ET (they don't create proper
    intersection points).

  • Shared vertices: If a scan line passes through a vertex shared by
    two edges, we count the intersection as:
      – TWO intersections if edges are on the same side (local min/max)
      – ONE intersection if edges are on opposite sides



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.5.2  BOUNDARY FILL ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  KEY IDEA                                                                  │
│                                                                            │
│  Start from an interior seed point and spread outward, coloring each      │
│  pixel with the fill color. Stop when you hit a pixel that already has    │
│  the BOUNDARY COLOR. The boundary color must be distinct and consistent   │
│  around the entire region.                                                 │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Connectivity
  ───────────────

  ┌───────────────────────────────────────────────────────────────────┐
  │                                                                   │
  │  4-Connected:  Only check UP, DOWN, LEFT, RIGHT neighbors        │
  │                                                                   │
  │                    ┌───┐                                          │
  │                    │ U │                                          │
  │                ┌───┼───┼───┐                                      │
  │                │ L │ P │ R │                                      │
  │                └───┼───┼───┘                                      │
  │                    │ D │                                          │
  │                    └───┘                                          │
  │                                                                   │
  │  8-Connected:  Also check all 4 diagonal neighbors               │
  │                                                                   │
  │                ┌───┬───┬───┐                                      │
  │                │UL │ U │UR │                                      │
  │                ├───┼───┼───┤                                      │
  │                │ L │ P │ R │                                      │
  │                ├───┼───┼───┤                                      │
  │                │DL │ D │DR │                                      │
  │                └───┴───┴───┘                                      │
  │                                                                   │
  │  4-connected may leave corners unfilled in diagonal boundaries.   │
  │  8-connected fills more thoroughly but may "leak" through         │
  │  diagonal gaps in thin boundaries.                                │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘


  ► Recursive Algorithm (4-Connected)
  ────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  procedure Boundary_Fill(x, y, fill_color, boundary_color):     │
  │      current = getpixel(x, y)                                  │
  │      if current ≠ boundary_color AND current ≠ fill_color:     │
  │          setpixel(x, y, fill_color)                            │
  │          Boundary_Fill(x+1, y, fill_color, boundary_color)     │
  │          Boundary_Fill(x-1, y, fill_color, boundary_color)     │
  │          Boundary_Fill(x, y+1, fill_color, boundary_color)     │
  │          Boundary_Fill(x, y-1, fill_color, boundary_color)     │
  └──────────────────────────────────────────────────────────────────┘


  ► Limitations
  ──────────────

  • Requires a consistent boundary color — if the boundary has gaps,
    the fill "leaks" outside.
  • Recursive implementation can cause stack overflow for large regions
    (each pixel call pushes a new stack frame).
  • Stack-based (iterative) implementations solve the overflow issue.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  2.5.3  FLOOD FILL ALGORITHM
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  KEY IDEA                                                                  │
│                                                                            │
│  Similar to Boundary Fill, but instead of stopping at a boundary color,   │
│  it replaces all connected pixels that have the SAME OLD COLOR with a     │
│  new fill color. It doesn't care about boundaries — it fills based on     │
│  matching the original (interior) color.                                   │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Recursive Algorithm (4-Connected)
  ────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  procedure Flood_Fill(x, y, new_color, old_color):             │
  │      if getpixel(x, y) == old_color:                           │
  │          setpixel(x, y, new_color)                             │
  │          Flood_Fill(x+1, y, new_color, old_color)              │
  │          Flood_Fill(x-1, y, new_color, old_color)              │
  │          Flood_Fill(x, y+1, new_color, old_color)              │
  │          Flood_Fill(x, y-1, new_color, old_color)              │
  └──────────────────────────────────────────────────────────────────┘


  ► Comparison: Boundary Fill vs. Flood Fill
  ──────────────────────────────────────────

  ┌────────────────────────┬──────────────────────────┬──────────────────────────┐
  │  CRITERIA              │  BOUNDARY FILL           │  FLOOD FILL              │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Stopping Condition    │  Stops at boundary       │  Stops when pixel color  │
  │                        │  color                   │  ≠ old_color             │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Boundary Requirement  │  Needs a consistent      │  No boundary needed;     │
  │                        │  boundary color           │  fills connected region  │
  │                        │                          │  of same color           │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Interior Assumption   │  Interior can be any     │  Interior must be        │
  │                        │  color except boundary   │  uniform old_color       │
  │                        │  and fill colors         │                          │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Use Case              │  Filling regions with    │  Replacing one color     │
  │                        │  drawn boundaries        │  with another (paint     │
  │                        │  (drawing programs)      │  bucket tool)            │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Parameters            │  (x, y, fill_color,      │  (x, y, new_color,       │
  │                        │   boundary_color)        │   old_color)             │
  └────────────────────────┴──────────────────────────┴──────────────────────────┘


  ► How is Scan Line different from Boundary Fill / Flood Fill?
  ────────────────────────────────────────────────────────────

  ┌────────────────────────┬──────────────────────────┬──────────────────────────┐
  │  CRITERIA              │  SCAN LINE               │  BOUNDARY/FLOOD FILL     │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Approach              │  Geometric — uses edge   │  Pixel-based — tests     │
  │                        │  intersections with scan │  each pixel's color      │
  │                        │  lines                   │  recursively             │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Input                 │  Polygon vertex list     │  Seed point + colors     │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Speed                 │  Much faster for large   │  Slower — tests pixels   │
  │                        │  polygons                │  one by one              │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Memory                │  Low (edge tables)       │  High (recursion stack)  │
  ├────────────────────────┼──────────────────────────┼──────────────────────────┤
  │  Usage                 │  Standard renderers,     │  Interactive paint tools │
  │                        │  GPU rasterizers         │  with seed picking       │
  └────────────────────────┴──────────────────────────┴──────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ANTIALIASING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  WHAT IS ALIASING?                                                         │
│                                                                            │
│  Aliasing is the visual artifact that occurs when continuous geometric     │
│  shapes are represented on a discrete pixel grid. Lines and edges appear  │
│  "jagged" or "stairstepped" — this staircase effect is called "jaggies." │
│  Aliasing is most noticeable on diagonal lines and curved edges.          │
│                                                                            │
│  Cause: The pixel grid has finite resolution. A mathematical line has     │
│  zero width, but a pixel has finite area. When we force a continuous      │
│  shape onto discrete pixels, information is lost → aliasing.              │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Antialiasing Techniques
  ──────────────────────────

  ┌─ 1. PRE-FILTERING (Area Sampling) ────────────────────────────────────────
  │
  │  Instead of treating each pixel as a point, treat it as a square area.
  │  The pixel's intensity is proportional to how much of the pixel area
  │  is covered by the geometric primitive.
  │
  │  ┌───────┐  If the ideal line covers 70% of this pixel's area,
  │  │░░░░███│  set its intensity to 70% (not full white or black).
  │  │░░░████│
  │  │░░█████│  This produces smooth gradual transitions at edges
  │  └───────┘  instead of harsh binary on/off.
  │
  │  Also called "area averaging" or "weighted area sampling."
  │  Computationally expensive but produces excellent results.
  │
  └────────────────────────────────────────────────────────────────────────────

  ┌─ 2. SUPER SAMPLING ANTIALIASING (SSAA) ───────────────────────────────────
  │
  │  Render the image at a higher resolution (e.g., 4× or 8× the display
  │  resolution), then downsample by averaging groups of sub-pixels into
  │  each display pixel.
  │
  │  Example: 4× SSAA renders at 3840×2160 for a 1920×1080 display,
  │  then each 2×2 block of rendered pixels is averaged into one
  │  display pixel.
  │
  │  ┌───────────────┐         ┌───────┐
  │  │ ○ ● │ ○ ○ │   │         │       │
  │  │ ○ ○ │ ● ○ │   │  ───►   │  avg  │   (average of 4 sub-pixels)
  │  └───────────────┘         └───────┘
  │
  │  ✓ Simple concept, excellent quality
  │  ✗ Very expensive — 4× pixels to render means 4× the work
  │
  └────────────────────────────────────────────────────────────────────────────

  ┌─ 3. MULTI-SAMPLE ANTIALIASING (MSAA) ─────────────────────────────────────
  │
  │  Like SSAA but more efficient. Multiple sample points per pixel test
  │  for coverage (is the sample inside the primitive?), but the fragment
  │  shader runs only ONCE per pixel, not once per sample.
  │
  │  Each pixel has N sample points (e.g., 4× MSAA = 4 samples per pixel).
  │  The color is computed once and shared among covered samples, but the
  │  final pixel color is weighted by how many samples were covered.
  │
  │  ✓ Much cheaper than SSAA (shader runs once, not N times)
  │  ✗ Doesn't antialias textures or shader effects — only edges
  │
  │  This is the standard antialiasing method in most games.
  │
  └────────────────────────────────────────────────────────────────────────────

  ┌─ 4. TEMPORAL ANTIALIASING (TAA) ──────────────────────────────────────────
  │
  │  Accumulates and blends samples from MULTIPLE FRAMES over time.
  │  Each frame uses a slightly jittered (offset) sample position.
  │  Over several frames, the jittered samples cover the pixel area
  │  and are blended together.
  │
  │  ✓ Very cheap per frame (only 1 sample per pixel per frame)
  │  ✓ Also antialiases shader effects and textures
  │  ✗ Can cause ghosting artifacts on fast-moving objects
  │  ✗ Requires motion vectors to compensate for movement
  │
  │  Used extensively in modern games (Unreal Engine, Unity HDRP).
  │
  └────────────────────────────────────────────────────────────────────────────


  ► Comparison of Antialiasing Methods
  ─────────────────────────────────────

  ┌─────────────┬───────────┬──────────────┬───────────────┬──────────────┐
  │  METHOD     │  QUALITY  │  PERFORMANCE │  EDGE AA      │  SHADER AA   │
  ├─────────────┼───────────┼──────────────┼───────────────┼──────────────┤
  │  None       │  Poor     │  Fastest     │  No           │  No          │
  │  SSAA       │  Best     │  Slowest     │  Yes          │  Yes         │
  │  MSAA       │  Good     │  Moderate    │  Yes          │  No          │
  │  TAA        │  Good     │  Fast        │  Yes          │  Yes         │
  └─────────────┴───────────┴──────────────┴───────────────┴──────────────┘


  ► Sub-Pixel Precision
  ──────────────────────

  Modern rasterizers don't work at whole-pixel resolution. They track
  geometry at sub-pixel precision — typically 1/16th or 1/256th of a pixel.
  This means the rasterizer knows where edge boundaries fall within a pixel,
  enabling proper antialiasing coverage calculations.

  Key benefit: Even without explicit antialiasing, sub-pixel precision
  ensures that triangles and lines that are thinner than a pixel are still
  rendered (with reduced intensity), preventing complete disappearance of
  thin features.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OPENGL LAB — SCAN CONVERSION IN PRACTICE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  The following OpenGL/GLUT programs demonstrate scan conversion concepts.


  ► Program 1: Drawing Lines Using OpenGL
  ────────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  #include <GL/glut.h>                                          │
  │                                                                 │
  │  void display() {                                              │
  │      glClear(GL_COLOR_BUFFER_BIT);                             │
  │      glColor3f(1.0, 0.0, 0.0);  // Red color                  │
  │                                                                 │
  │      // Draw a line from (100,100) to (400,300)                │
  │      glBegin(GL_LINES);                                        │
  │          glVertex2i(100, 100);                                 │
  │          glVertex2i(400, 300);                                 │
  │      glEnd();                                                  │
  │                                                                 │
  │      // Enable antialiasing                                    │
  │      glEnable(GL_LINE_SMOOTH);                                 │
  │      glEnable(GL_BLEND);                                       │
  │      glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);       │
  │                                                                 │
  │      glColor3f(0.0, 1.0, 0.0);  // Green color                │
  │      glBegin(GL_LINES);                                        │
  │          glVertex2i(100, 200);                                 │
  │          glVertex2i(400, 400);                                 │
  │      glEnd();                                                  │
  │                                                                 │
  │      glFlush();                                                │
  │  }                                                              │
  │                                                                 │
  │  int main(int argc, char** argv) {                             │
  │      glutInit(&argc, argv);                                    │
  │      glutInitWindowSize(500, 500);                             │
  │      glutCreateWindow("Line Drawing");                         │
  │      gluOrtho2D(0, 500, 0, 500);                              │
  │      glutDisplayFunc(display);                                 │
  │      glutMainLoop();                                           │
  │      return 0;                                                 │
  │  }                                                              │
  └──────────────────────────────────────────────────────────────────┘

  Compile:  g++ line.cpp -o line -lGL -lGLU -lglut
  Run:      ./line


  ► Program 2: Drawing a Filled Polygon
  ──────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  #include <GL/glut.h>                                          │
  │                                                                 │
  │  void display() {                                              │
  │      glClear(GL_COLOR_BUFFER_BIT);                             │
  │      glColor3f(0.0, 0.0, 1.0);  // Blue                       │
  │                                                                 │
  │      glBegin(GL_POLYGON);                                      │
  │          glVertex2i(150, 100);                                 │
  │          glVertex2i(350, 100);                                 │
  │          glVertex2i(400, 250);                                 │
  │          glVertex2i(250, 400);                                 │
  │          glVertex2i(100, 250);                                 │
  │      glEnd();                                                  │
  │                                                                 │
  │      glFlush();                                                │
  │  }                                                              │
  │                                                                 │
  │  int main(int argc, char** argv) {                             │
  │      glutInit(&argc, argv);                                    │
  │      glutInitWindowSize(500, 500);                             │
  │      glutCreateWindow("Filled Polygon");                       │
  │      gluOrtho2D(0, 500, 0, 500);                              │
  │      glutDisplayFunc(display);                                 │
  │      glutMainLoop();                                           │
  │      return 0;                                                 │
  │  }                                                              │
  └──────────────────────────────────────────────────────────────────┘


  ► Program 3: Bresenham's Line (Manual Implementation)
  ─────────────────────────────────────────────────────

  ┌──────────────────────────────────────────────────────────────────┐
  │  #include <GL/glut.h>                                          │
  │  #include <cmath>                                              │
  │                                                                 │
  │  void plotPixel(int x, int y) {                                │
  │      glBegin(GL_POINTS);                                       │
  │          glVertex2i(x, y);                                     │
  │      glEnd();                                                  │
  │  }                                                              │
  │                                                                 │
  │  void bresenham(int x1, int y1, int x2, int y2) {             │
  │      int dx = abs(x2 - x1), dy = abs(y2 - y1);                │
  │      int sx = (x1 < x2) ? 1 : -1;                             │
  │      int sy = (y1 < y2) ? 1 : -1;                             │
  │      int p = 2*dy - dx;                                        │
  │      int x = x1, y = y1;                                      │
  │                                                                 │
  │      for (int i = 0; i <= dx; i++) {                           │
  │          plotPixel(x, y);                                      │
  │          if (p < 0) {                                          │
  │              p += 2*dy;                                        │
  │          } else {                                              │
  │              p += 2*dy - 2*dx;                                 │
  │              y += sy;                                          │
  │          }                                                      │
  │          x += sx;                                              │
  │      }                                                          │
  │  }                                                              │
  │                                                                 │
  │  void display() {                                              │
  │      glClear(GL_COLOR_BUFFER_BIT);                             │
  │      glColor3f(1.0, 1.0, 0.0);                                │
  │      bresenham(50, 50, 400, 300);                              │
  │      glFlush();                                                │
  │  }                                                              │
  │                                                                 │
  │  int main(int argc, char** argv) {                             │
  │      glutInit(&argc, argv);                                    │
  │      glutInitWindowSize(500, 500);                             │
  │      glutCreateWindow("Bresenham Line");                       │
  │      gluOrtho2D(0, 500, 0, 500);                              │
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
  │  Scan Conversion           │  Converting mathematical shapes to pixels  │
  │                            │  on a raster grid                           │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  DDA                       │  Incremental, FP arithmetic, simple,       │
  │                            │  x_inc/y_inc based, prone to drift         │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Bresenham's Line          │  Integer only, decision parameter pₖ,      │
  │                            │  p₀=2Δy-Δx, hardware-friendly             │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Midpoint Circle           │  8-way symmetry, p₀=1-r, integer ops,     │
  │                            │  works from (0,r) to x=y                   │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Midpoint Ellipse          │  4-way symmetry, TWO regions,              │
  │                            │  boundary at 2rᵧ²x = 2rₓ²y               │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Scan Line Fill            │  Edge table + active edge list, geometric  │
  │                            │  approach, fills between intersection      │
  │                            │  pairs, fastest for large polygons         │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Boundary Fill             │  Seed-based, stops at boundary color,      │
  │                            │  recursive, 4-connected or 8-connected     │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Flood Fill                │  Seed-based, replaces old_color,           │
  │                            │  no boundary needed, paint-bucket tool     │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Antialiasing              │  Area sampling, SSAA, MSAA, TAA — reduce  │
  │                            │  jaggies by smoothing pixel transitions    │
  └────────────────────────────┴──────────────────────────────────────────────┘


╔══════════════════════════════════════════════════════════════════════════════╗
║                         END OF CHAPTER 2                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝


---

## 📝 Exam Practice Questions

### From AI-Generated Sets (aiQuestions.txt)

**Set 1, Q2:**
a. Derive Bresenham's Line Drawing Algorithm for slope |m| < 1. Using this algorithm, digitize the line from (20, 10) to (30, 18).
b. Differentiate between Boundary Fill and Flood Fill algorithms. Write the algorithm for 4-connected Boundary Fill.

**Set 2, Q2:**
a. Explain the DDA line drawing algorithm. Use DDA to rasterize the line from (2, 3) to (12, 8). Tabulate the computed pixel positions at each step.
b. Derive the midpoint ellipse generation algorithm. Explain why separate calculations are needed for Region 1 and Region 2.

**Set 3, Q2:**
a. Compare DDA and Bresenham's line drawing algorithms in terms of efficiency, accuracy, and computation type. Derive the initial decision parameter for Bresenham's algorithm for slope < 1.
b. Derive the midpoint circle generation algorithm. Use it to plot circle points for the first octant with radius 8. Tabulate all values of the decision parameter and the plotted coordinates.

**Set 4, Q2:**
a. Explain the midpoint circle drawing algorithm. Digitize a circle with center at origin and radius 12 for the first octant. Tabulate all decision parameters and the generated points.
b. Write and explain the Scan Line Polygon Fill algorithm with a diagram. How does it handle edges that share vertices?

**Set 5, Q2:**
a. Derive Bresenham's line drawing algorithm for a line with slope greater than 1. Use it to digitize the line from (2, 1) to (8, 13).
b. Compare the midpoint circle and midpoint ellipse generation algorithms. Why cannot the 8-way symmetry of the circle be applied to the ellipse?

**Set 6, Q2:**
a. Using the DDA algorithm, rasterize the line from (5, 5) to (15, 9). Tabulate the pixel coordinates at each step. What are the limitations of the DDA algorithm?
b. Derive the decision parameters for the midpoint ellipse generation algorithm in both Region 1 and Region 2. Explain the transition condition between the two regions.

**Set 7, Q2:**
a. Derive Bresenham's line drawing algorithm for the first octant. Digitize the line from (1, 1) to (8, 5). Show all intermediate calculations in tabular form.
b. Explain the Flood Fill algorithm using both 4-connected and 8-connected approaches. When would 8-connected be preferred over 4-connected? Discuss with an example.

**Set 8, Q2:**
a. What is scan conversion? Explain the DDA algorithm with its advantages and disadvantages. Rasterize the line from (0, 0) to (7, 3) using DDA.
b. Derive the midpoint circle algorithm. Why is it computationally efficient compared to directly using the circle equation x² + y² = r²?

**Set 9, Q2:**
a. Compare the DDA and Bresenham's line drawing algorithms. Why is Bresenham's algorithm preferred for hardware implementation?
b. Explain the midpoint circle generation algorithm. Using the algorithm, digitize the first octant of a circle with radius 15 (first five decision parameter iterations).

**Set 10, Q2:**
a. Digitize the line from (15, 5) to (25, 13) using Bresenham's Line Drawing Algorithm. Show all intermediate calculations in tabular form including the decision parameter at each step.
b. Explain the Scan Line Polygon Fill algorithm with a diagram. How are the edge table and active edge list initialized and updated during the fill process?

---

### From Past Papers (Questions.txt)

**Set 1, Q2:**
a. What is the difference between DDA and Bresenham's Line Algorithm? Discuss the "Midpoint Circle Drawing Algorithm" for 8 octants. Derive an expression for the decision parameter for: (i) Initial decision parameter P₀, (ii) Decision parameter when Pₖ < 0, (iii) Decision parameter when Pₖ > 0.
b. Explain the Boundary Fill algorithm in detail. How does this approach differ from Flood Fill?

**Set 2, Q2:**
a. Write the algorithm for both conditions of Bresenham's Line Drawing Algorithm and derive the initial decision parameter for slope less than 1.
b. Why do circle and ellipse use different point symmetry? Digitize the circle with radius 10.

**Set 3, Q2:**
a. How much time is spent scanning across each row of pixels during screen refresh on a raster system with a resolution of 1280 × 1024 and a refresh rate of 60 frames per second?
b. Why do circle and ellipse use different point symmetry? Explain the Midpoint Circle Generation Algorithm by calculating its initial decision parameter.

---

### Related Short Notes Topics (from Q7)
- Scan line polygon fill algorithm — *aiQ Set 3*
- Midpoint ellipse generation algorithm — *aiQ Set 6*
- Boundary Fill vs. Flood Fill Algorithm — *Q Set 2*
