
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║            CHAPTER 1 — OVERVIEW OF COMPUTER GRAPHICS                         ║
║                    AND GRAPHICS SYSTEMS                                      ║
║                                                                              ║
║            CMP 234 · Pokhara University · BE Computer                        ║
║            Syllabus Hours: 7                                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝


This chapter provides a comprehensive introduction to the field of Computer
Graphics — its definition, history, applications, and the hardware and software
systems that make graphical output possible. By the end of this chapter, you
will understand how images are generated on screens, how the hardware pipeline
works from frame buffer to phosphor glow, and how modern GPUs have transformed
the entire discipline.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1.1  INTRODUCTION TO COMPUTER GRAPHICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


┌─────────────────────────────────────────────────────────────────────────────┐
│  DEFINITION                                                                 │
│                                                                             │
│  Computer Graphics (CG) is the branch of computer science concerned with    │
│  the creation, storage, manipulation, and display of pictures, images,      │
│  and visual representations of data using computers. It transforms          │
│  numerical and symbolic data into visual form, enabling humans to           │
│  interact with and interpret complex information intuitively.               │
│                                                                             │ 
│  In simple terms: CG is about using a computer to generate images from      │
│  data — whether that data is a 3D model of a building, a mathematical       │
│  equation, medical scan data, or game-world geometry.                       │
└─────────────────────────────────────────────────────────────────────────────┘


  ► Types of Computer Graphics
  ─────────────────────────────

  Computer graphics can be broadly classified into two types:

  ┌────────────────────────────┬────────────────────────────────────────────┐
  │  TYPE                      │  DESCRIPTION                               │
  ├────────────────────────────┼────────────────────────────────────────────┤
  │  Interactive Graphics      │  The user controls the content of the      │
  │                            │  image dynamically using input devices     │
  │                            │  (mouse, keyboard, joystick). The display  │
  │                            │  responds in real time to user actions.    │
  │                            │  Example: video games, CAD tools, virtual  │
  │                            │  reality environments.                     │
  ├────────────────────────────┼────────────────────────────────────────────┤
  │  Non-Interactive (Passive) │  The image is produced entirely by the     │
  │  Graphics                  │  computer without user control during      │
  │                            │  rendering. The user views a pre-computed  │
  │                            │  result.                                   │
  │                            │  Example: movie CGI, animated films,       │
  │                            │  rendered architectural walkthroughs.      │
  └────────────────────────────┴────────────────────────────────────────────┘


  ► Brief History and Evolution
  ─────────────────────────────

  • 1950s — Ivan Sutherland's "Sketchpad" (1963) is considered the birth
            of interactive computer graphics. It introduced concepts like
            object-oriented graphics, instancing, and light-pen interaction.

  • 1970s — Raster graphics began replacing vector graphics. The frame
            buffer concept emerged, enabling filled areas and color.

  • 1980s — Personal computers brought graphics to consumers. GUIs
            (Macintosh, Windows) made graphical interaction mainstream.

  • 1990s — Hardware-accelerated 3D graphics (GPUs) emerged. OpenGL (1992)
            standardized cross-platform 3D rendering. Real-time 3D gaming
            became commercially viable (Doom, Quake).

  • 2000s — Programmable shaders replaced fixed-function pipelines, giving
            artists and developers unprecedented control over rendering.

  • 2010s — Mobile GPUs reached console-level power. VR headsets (Oculus
            Rift, HTC Vive) revived virtual reality.

  • 2020s — Real-time ray tracing (NVIDIA RTX), AI-driven graphics (DLSS,
            neural rendering), and the metaverse push the frontier.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1.1.1  APPLICATIONS OF COMPUTER GRAPHICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


Computer graphics is not just about games and movies — it pervades nearly every
field of modern technology. Below is a detailed exploration of the major
application areas, as required by the syllabus and frequently asked in exams.


  ┌─ 1. COMPUTER AIDED DESIGN (CAD) ──────────────────────────────────────────
  │
  │  CAD is arguably the most commercially important application of CG.
  │  Engineers and architects use graphical software to design, modify,
  │  analyze, and optimize products before physical manufacturing.
  │
  │  How CAD uses CG:
  │    • Wireframe Modeling  — Objects represented as edges and vertices.
  │    • Surface Modeling    — Objects defined by their outer surfaces.
  │    • Solid Modeling      — Full volumetric representation (CSG, B-rep).
  │    • Parametric Design   — Dimensions as parameters; change one value
  │                           and the entire design updates automatically.
  │
  │  Impact on Engineering:
  │    ✓ Reduced design time from months to days
  │    ✓ Virtual prototyping eliminates expensive physical prototypes
  │    ✓ Simulation (FEA, CFD) runs directly on the CAD model
  │    ✓ Manufacturing instructions (G-code) generated from CAD data
  │    ✓ Collaborative design across global teams via shared 3D models
  │
  │  Examples: AutoCAD, SolidWorks, CATIA, Fusion 360, FreeCAD
  │
  └────────────────────────────────────────────────────────────────────────────


  ┌─ 2. COMPUTER SIMULATION ──────────────────────────────────────────────────
  │
  │  Computer simulations model real-world processes graphically, allowing
  │  scientists and engineers to visualize phenomena that are too expensive,
  │  dangerous, or impossible to observe directly.
  │
  │  Types of Simulation:
  │    • Flight Simulators    — Train pilots in realistic virtual cockpits
  │                            with weather, terrain, and failure scenarios.
  │    • Driving Simulators   — Test vehicle dynamics and driver behavior.
  │    • Physics Simulation   — Fluid dynamics, structural mechanics,
  │                            particle systems (explosions, smoke, fire).
  │    • Military Simulation  — Tactical training, war-gaming, equipment
  │                            operation without live ammunition.
  │    • Urban Planning       — Simulate traffic flow, pedestrian movement,
  │                            building shadow patterns over time.
  │
  │  Key Advantage: Simulations allow "what-if" analysis — change
  │  parameters and instantly see the visual consequences without
  │  building physical models or risking lives.
  │
  └────────────────────────────────────────────────────────────────────────────


  ┌─ 3. SCIENTIFIC VISUALIZATION ─────────────────────────────────────────────
  │
  │  Scientific visualization converts abstract numerical data into visual
  │  representations, making patterns, trends, and anomalies visible that
  │  would be impossible to detect by examining raw numbers alone.
  │
  │  Applications:
  │    • Medical Imaging    — CT scans, MRI data rendered as 3D volume
  │                          visualizations, enabling non-invasive surgery
  │                          planning and tumor detection.
  │    • Molecular Biology  — Protein structures, DNA helices rendered in
  │                          3D for drug design and genomic research.
  │    • Weather Prediction — Atmospheric data visualized as 3D cloud
  │                          formations, pressure maps, wind vectors.
  │    • Astronomy          — Galaxy formation simulations, black hole
  │                          visualizations, cosmological models.
  │    • Geoscience         — Seismic data, geological strata, ocean
  │                          current visualization.
  │
  └────────────────────────────────────────────────────────────────────────────


  ┌─ 4. ENTERTAINMENT AND GAMING ─────────────────────────────────────────────
  │
  │  The gaming and entertainment industry is the largest consumer-facing
  │  driver of CG technology advancement.
  │
  │    • Video Games      — Real-time 3D rendering with physics, AI,
  │                         lighting, shadows, and post-processing effects.
  │                         Modern AAA games render millions of triangles
  │                         at 60+ frames per second.
  │    • Movie VFX        — CGI characters (Gollum, Thanos), virtual
  │                         environments, digital doubles, motion capture.
  │    • Animation Films  — Pixar, DreamWorks, Disney use CG exclusively.
  │                         Tools: Maya, Blender, Houdini, RenderMan.
  │    • AR/VR            — Augmented Reality (Pokémon GO, AR navigation)
  │                         and Virtual Reality (gaming, training, therapy).
  │
  │  Impact on Realism and Player Immersion:
  │    ✓ Photorealistic rendering (PBR, ray tracing) blurs virtual/real
  │    ✓ Real-time global illumination creates lifelike lighting
  │    ✓ Motion capture and facial animation create believable characters
  │    ✓ Haptic feedback and 3D audio enhance sensory immersion
  │    ✓ Open-world procedural generation creates vast explorable spaces
  │
  └────────────────────────────────────────────────────────────────────────────


  ┌─ 5. EDUCATION AND TRAINING ───────────────────────────────────────────────
  │
  │    • Interactive Tutorials — 3D anatomy viewers, virtual chemistry labs
  │    • E-Learning            — Animated explanations of complex concepts
  │    • Surgical Training     — Virtual surgery simulators with haptic
  │                              feedback for medical students
  │    • Skill Development     — Equipment operation training (crane,
  │                              excavator, lathe) without physical risk
  │
  └────────────────────────────────────────────────────────────────────────────


  ┌─ 6. MEDICINE ─────────────────────────────────────────────────────────────
  │
  │    • CT/MRI Visualization  — 3D reconstruction of internal organs
  │    • Surgical Planning     — Virtual 3D models of patient anatomy
  │    • Prosthetics Design    — 3D scanning + CAD for custom prosthetics
  │    • Radiation Therapy     — Visual planning of radiation beam paths
  │    • Telemedicine          — Remote diagnosis using 3D medical imaging
  │
  └────────────────────────────────────────────────────────────────────────────


  ┌─ 7. OTHER APPLICATION AREAS ──────────────────────────────────────────────
  │
  │    • GUI Design      — Desktop environments, mobile interfaces, icons
  │    • Cartography     — Digital maps, GIS systems (Google Earth)
  │    • Art and Design  — Digital painting, graphic design, typography
  │    • Manufacturing   — CNC programming, robotic path visualization
  │    • Business        — Data dashboards, infographics, presentations
  │
  └────────────────────────────────────────────────────────────────────────────



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1.1.2  RECENT TRENDS IN COMPUTER GRAPHICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ┌────────────────────────┬──────────────────────────────────────────────────┐
  │  TREND                 │  DESCRIPTION                                     │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Real-Time Ray         │  NVIDIA RTX GPUs introduced hardware ray         │
  │  Tracing               │  tracing (RT cores) in 2018, enabling            │
  │                        │  physically accurate reflections, refractions,   │
  │                        │  and global illumination in real-time games.     │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Virtual Reality (VR)  │  Head-mounted displays (HMDs) with positional    │
  │                        │  tracking, rendering two stereoscopic views      │
  │                        │  at 90+ FPS for immersive 3D experiences.        │
  │                        │  Devices: Meta Quest, Valve Index, PSVR2.        │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Augmented Reality     │  Overlays virtual objects on the real world      │
  │  (AR)                  │  using camera + display. Uses spatial mapping,   │
  │                        │  object recognition, and real-time rendering.    │
  │                        │  Devices: Microsoft HoloLens, Apple Vision Pro.  │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  AI-Driven Graphics    │  Neural networks for super-resolution (DLSS),    │
  │                        │  denoising (OptiX AI Denoiser), procedural       │
  │                        │  content generation, and neural radiance         │
  │                        │  fields (NeRF) for 3D reconstruction.            │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  GPU Compute (GPGPU)   │  GPUs used for general-purpose parallel          │
  │                        │  computing (CUDA, OpenCL) — machine learning,    │
  │                        │  physics simulation, cryptocurrency mining.      │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Cloud Rendering       │  Complex rendering offloaded to cloud servers.   │
  │                        │  Cloud gaming (GeForce NOW, Xbox Cloud) streams  │
  │                        │  rendered frames to thin clients.                │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Metaverse             │  Persistent 3D virtual worlds for social         │
  │                        │  interaction, work, and commerce — requiring     │
  │                        │  real-time rendering of complex environments.    │
  └────────────────────────┴──────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1.2  INTERACTIVE INPUT DEVICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


Input devices allow users to communicate with the graphics system — providing
positions, selections, text, and commands. Understanding input devices is
essential for designing interactive graphics applications.


  ► Classification of Input Devices — Six Logical Classes
  ────────────────────────────────────────────────────────

  Graphics standards (GKS, PHIGS) classify input devices not by their
  physical form, but by the type of input they provide. This logical
  classification enables device-independent programming — the same program
  works with different physical devices that provide the same logical input.

  ┌─────────────────┬──────────────────────────┬──────────────────────────────┐
  │  LOGICAL CLASS  │  INPUT PROVIDED          │  PHYSICAL DEVICE EXAMPLES    │
  ├─────────────────┼──────────────────────────┼──────────────────────────────┤
  │  Locator        │  A position (x, y) in    │  Mouse, trackball, joystick, │
  │                 │  world coordinates       │  digitizing tablet, touch    │
  │                 │                          │  screen, light pen           │
  ├─────────────────┼──────────────────────────┼──────────────────────────────┤
  │  Stroke         │  A sequence of positions │  Mouse (click-drag), pen     │
  │                 │  (a drawn path)          │  tablet, finger on touch     │
  │                 │                          │  screen                      │
  ├─────────────────┼──────────────────────────┼──────────────────────────────┤
  │  Valuator       │  A single scalar value   │  Potentiometer dial, slider  │
  │                 │  (real number)           │  bar, scroll wheel, analog   │
  │                 │                          │  joystick axis               │ 
  ├─────────────────┼──────────────────────────┼──────────────────────────────┤
  │  Choice         │  A selection from a set  │  Function keys, menu items,  │
  │                 │  of alternatives         │  radio buttons, combo box,   │
  │                 │                          │  button panel                │
  ├─────────────────┼──────────────────────────┼──────────────────────────────┤
  │  String         │  A text string           │  Keyboard, on-screen         │
  │                 │                          │  keyboard, voice input       │
  ├─────────────────┼──────────────────────────┼──────────────────────────────┤
  │  Pick           │  Identification of a     │  Mouse click on an object,   │
  │                 │  displayed object        │  light pen touch on object   │
  └─────────────────┴──────────────────────────┴──────────────────────────────┘


  ► Three Modes of Input Handling
  ───────────────────────────────

  ┌──────────────────┬───────────────────────────────────────────────────────┐
  │  MODE            │  DESCRIPTION                                          │
  ├──────────────────┼───────────────────────────────────────────────────────┤
  │  Request Mode    │  The program pauses execution and waits until the     │
  │                  │  user provides input. Like scanf() in C — the         │
  │                  │  program blocks until input is received.              │
  │                  │  Example: "Click to place a point" — program waits.   │
  ├──────────────────┼───────────────────────────────────────────────────────┤
  │  Sample Mode     │  The program reads the current state of the device    │
  │                  │  immediately, without waiting. The device is          │
  │                  │  always "on" and the program grabs its current        │
  │                  │  value at any moment.                                 │
  │                  │  Example: Reading joystick position every frame in    │
  │                  │  a game — don't wait, just read the current tilt.     │
  ├──────────────────┼───────────────────────────────────────────────────────┤
  │  Event Mode      │  Input events are queued by the system. The program   │
  │                  │  processes events from the queue asynchronously.      │
  │                  │  This is the standard model for GUIs and OpenGL       │
  │                  │  (GLUT's callback architecture uses event mode).      │
  │                  │  Example: Mouse click → event added to queue →        │
  │                  │  callback function invoked when event is processed.   │
  └──────────────────┴───────────────────────────────────────────────────────┘


  ► Detailed Physical Input Devices
  ─────────────────────────────────

  ◆ Mouse
    The most common locator device. Tracks relative movement on a surface
    and translates it to cursor movement on screen. Optical mice use an
    LED/laser and image sensor to detect surface texture movement. Buttons
    provide pick/choice input.

  ◆ Trackball
    Essentially an inverted mouse — the user rotates a ball with fingers
    while the body stays stationary. Used in CAD workstations and embedded
    systems (laptops, military equipment) where desk space is limited.
    Provides fine control for precise positioning.

  ◆ Joystick
    A lever mounted on a base that tilts in two axes, providing continuous
    (x, y) position input. Can function as a locator (cursor control) or
    valuator (tilt angle maps to a scalar value). Spring-loaded joysticks
    return to center when released. Used extensively in gaming, flight
    simulation, and robotic control.

  ◆ Digitizing Tablet (Graphics Tablet)
    A flat surface with an embedded grid of wires that detect the position
    of a special stylus (pen). Provides absolute positioning (each point on
    the tablet maps to a fixed point on screen), pressure sensitivity, and
    tilt detection. Used by digital artists and CAD professionals.

  ◆ Light Pen
    A pen-shaped device that detects light emitted by the CRT phosphors.
    When pointed at the screen, it senses the moment its position is
    illuminated during the raster scan, allowing the system to determine
    the screen coordinates. Only works with CRT displays (not LCDs).

  ◆ Touch Screen
    Allows direct interaction by touching the display surface.

    ┌───────────────────┬──────────────────────────────────────────────────┐
    │  TYPE             │  WORKING PRINCIPLE                               │
    ├───────────────────┼──────────────────────────────────────────────────┤
    │  Resistive        │  Two flexible conductive layers separated by     │
    │                   │  a gap. Pressing the screen makes the layers     │
    │                   │  contact, and the touch position is determined   │
    │                   │  by measuring voltage at the contact point.      │
    │                   │  Works with any object (stylus, gloved finger).  │
    ├───────────────────┼──────────────────────────────────────────────────┤
    │  Capacitive       │  The screen has a conductive coating that        │
    │                   │  stores charge. When a finger (which is          │
    │                   │  electrically conductive) touches the surface,   │
    │                   │  it disturbs the electrostatic field. Sensors    │
    │                   │  at the corners measure the change in            │
    │                   │  capacitance to determine touch position.        │
    │                   │  Supports multi-touch (pinch, zoom, rotate).     │
    │                   │  Does NOT work with non-conductive objects.      │
    ├───────────────────┼──────────────────────────────────────────────────┤
    │  Infrared         │  Grid of IR emitters and detectors around the    │
    │                   │  screen edges. A touch breaks IR beams,          │
    │                   │  identifying position by which beams are         │
    │                   │  interrupted. Works with any object.             │
    ├───────────────────┼──────────────────────────────────────────────────┤
    │  SAW (Surface     │  Ultrasonic waves travel across the screen.      │
    │  Acoustic Wave)   │  A touch absorbs some wave energy; position is   │
    │                   │  determined by analyzing the absorbed signal.    │
    └───────────────────┴──────────────────────────────────────────────────┘

  ◆ Data Gloves
    A glove fitted with flex sensors (fiber optic or resistive) on each
    finger joint to measure finger bending, and position/orientation
    sensors (electromagnetic or inertial) on the back of the hand to track
    hand movement in 3D space.

    How They Work:
      1. Flex sensors measure the bend angle of each finger joint
         (typically 10-22 sensors per glove).
      2. Position tracker (e.g., magnetic tracker) provides 6-DOF
         (x, y, z, roll, pitch, yaw) hand position and orientation.
      3. The combined data allows the system to reconstruct a virtual
         hand that mirrors the user's real hand movements.

    Applications: Virtual reality interaction, sign language recognition,
    robotic teleoperation, rehabilitation therapy, 3D modeling gestures.

  ◆ Space Ball / 3D Mouse
    A 6-DOF input device that senses force and torque applied in all three
    translational and three rotational axes simultaneously. Used in CAD
    for navigating 3D models (pan, zoom, rotate without switching modes).

  ◆ Image Scanner
    Converts a physical image (document, photograph) into a digital raster
    image by illuminating the surface and measuring reflected light
    intensity with a CCD or CIS sensor array.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1.3  DISPLAY DEVICES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


Display devices are the output end of the graphics pipeline — they convert
electrical signals into visible images. Understanding display technology is
essential because the choice of display determines the color depth, resolution,
refresh rate, and type of graphics system architecture.


  ► 1.3.1  Cathode Ray Tube (CRT)
  ────────────────────────────────

  The CRT was the dominant display technology from the 1950s through the
  early 2000s. Though now largely replaced by flat panels, it remains
  foundational to understanding graphics systems because raster scan and
  random scan architectures were designed around it.

  ┌─────────────────── STRUCTURE OF A CRT ──────────────────────────┐
  │                                                                 │
  │   Electron   Focusing   Deflection     Phosphor                 │
  │    Gun        System     System         Screen                  │
  │                                                                 │
  │   ┌───┐     ┌─────┐    ┌───────┐                                │
  │   │ K ├────►│Grids├───►│Plates/├──────────►  ░░░░░░░░░░░░       │
  │   │   │     │     │    │ Coils │           Screen with          │
  │   └───┘     └─────┘    └───────┘           Phosphor Coating     │
  │                                                                 │
  │   Heated    Electrostatic  Electromagnetic    Light emitted     │
  │  cathode    or magnetic    or electrostatic   when electrons    │
  │  emits      lenses focus   fields steer the   strike phosphor   │
  │  electrons  beam to a      beam to desired    coating on the    │
  │             sharp point    screen position    inner surface     │
  │                                                                 │
  └─────────────────────────────────────────────────────────────────┘

  Working Principle — Step by Step:
    1. The cathode (heated filament) emits a stream of electrons
       through thermionic emission.
    2. The control grid regulates the intensity of the beam — higher
       voltage = more electrons = brighter spot.
    3. Focusing system (electrostatic or electromagnetic lenses)
       converges the electron beam to a sharp point.
    4. Deflection system steers the beam to the correct (x, y)
       position on the screen:
         • Electrostatic deflection — voltage applied to deflection
           plates (faster, used in oscilloscopes).
         • Electromagnetic deflection — current through deflection
           coils (used in TV/monitor CRTs).
    5. The focused beam strikes the phosphor coating on the inner
       surface of the screen, causing it to emit visible light
       (fluorescence).
    6. The phosphor glows briefly and then fades (persistence). To
       maintain the image, the beam must periodically redraw (refresh)
       the entire picture before the phosphor fades completely.


  ► 1.3.2  Color CRT Techniques
  ──────────────────────────────

  There are two primary methods for producing color on a CRT:

  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║  METHOD 1: BEAM PENETRATION                                               ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║                                                                           ║
  ║  The screen is coated with two layers of phosphor:                        ║
  ║    • Outer layer: RED phosphor                                            ║
  ║    • Inner layer: GREEN phosphor                                          ║
  ║                                                                           ║
  ║  Principle:                                                               ║
  ║    The speed (energy) of the electron beam determines which layer         ║
  ║    the electrons penetrate to:                                            ║
  ║      → Low-speed beam  → excites only outer RED layer → RED glow          ║
  ║      → High-speed beam → penetrates to inner GREEN layer → GREEN glow     ║
  ║      → Medium-speed    → excites both layers → ORANGE / YELLOW            ║
  ║                                                                           ║
  ║  Advantages:                                                              ║
  ║    ✓ Simple design — only one electron gun needed                         ║
  ║    ✓ Inexpensive compared to shadow mask                                  ║
  ║                                                                           ║
  ║  Disadvantages:                                                           ║
  ║    ✗ Very limited color range (only Red, Green, Orange, Yellow)           ║
  ║    ✗ Cannot produce blue, cyan, magenta, or white                         ║
  ║    ✗ Quality of intermediate colors is poor                               ║
  ║    ✗ Slow color switching (changing beam speed takes time)                ║
  ║                                                                           ║
  ║  Usage: Older random-scan (vector) displays, oscilloscopes                ║
  ║                                                                           ║
  ╚═══════════════════════════════════════════════════════════════════════════╝


  ╔═══════════════════════════════════════════════════════════════════════════╗
  ║  METHOD 2: SHADOW MASK                                                    ║
  ╠═══════════════════════════════════════════════════════════════════════════╣
  ║                                                                           ║
  ║  The screen has groups of three phosphor dots (a "triad" or "pixel"):     ║
  ║    • One RED phosphor dot                                                 ║
  ║    • One GREEN phosphor dot                                               ║
  ║    • One BLUE phosphor dot                                                ║
  ║                                                                           ║
  ║  Three separate electron guns — one for each color — fire                 ║
  ║  simultaneously. A perforated metal plate (the SHADOW MASK) is placed     ║
  ║  between the guns and the screen.                                         ║
  ║                                                                           ║
  ║  Principle:                                                               ║
  ║    The shadow mask has tiny holes aligned so that each electron gun       ║
  ║    can only hit its corresponding phosphor dot:                           ║
  ║      → Red gun's beam passes through hole → hits ONLY red dot             ║
  ║      → Green gun's beam → passes same hole at different angle →           ║
  ║        hits ONLY green dot                                                ║
  ║      → Blue gun's beam → hits ONLY blue dot                               ║
  ║                                                                           ║
  ║  The beams converge at the mask hole and diverge behind it to hit         ║
  ║  their respective phosphor dots.                                          ║
  ║                                                                           ║
  ║                 Three Electron Guns                                       ║
  ║                  R    G    B                                              ║
  ║                   \   |   /                                               ║
  ║                    \  |  /                                                ║
  ║                     \ | /                                                 ║
  ║                 ─────[●]───── ← Shadow Mask (hole)                        ║
  ║                     / | \                                                 ║
  ║                    /  |  \                                                ║
  ║                   /   |   \                                               ║
  ║                  R    G    B  ← Phosphor dots on screen                   ║
  ║                                                                           ║
  ║  Advantages:                                                              ║
  ║    ✓ Full color range — any color by mixing R, G, B intensities           ║
  ║    ✓ Millions of colors possible (256 levels × 3 = 16.7 million)          ║
  ║    ✓ High image quality                                                   ║
  ║                                                                           ║
  ║  Disadvantages:                                                           ║
  ║    ✗ Complex and expensive — three guns, precision mask alignment         ║
  ║    ✗ Shadow mask absorbs ~85% of electrons (low energy efficiency)        ║
  ║    ✗ Mask can warp from heat (causing color purity errors)                ║
  ║    ✗ Lower brightness than beam penetration (due to mask blocking)        ║
  ║                                                                           ║
  ║  Usage: All modern CRT monitors and televisions (until LCD takeover)      ║
  ║                                                                           ║
  ╚═══════════════════════════════════════════════════════════════════════════╝


  ┌──────────────────────────────────────────────────────────────────────────┐
  │           COMPARISON: BEAM PENETRATION vs. SHADOW MASK                   │
  ├────────────────────────┬─────────────────────┬───────────────────────────┤
  │  PARAMETER             │  BEAM PENETRATION   │  SHADOW MASK              │
  ├────────────────────────┼─────────────────────┼───────────────────────────┤
  │  Electron Guns         │  1 (single)         │  3 (one per color)        │
  │  Color Range           │  4 colors (R,G,O,Y) │  Millions (16.7M+)        │
  │  Color Method          │  Beam speed control │  Additive mixing R+G+B    │
  │  Cost                  │  Low                │  High                     │
  │  Image Quality         │  Low                │  High                     │
  │  Brightness            │  Higher             │  Lower (mask blocks ~85%) │
  │  Resolution            │  Lower              │  Higher                   │
  │  Typical Use           │  Vector displays    │  Raster displays, TVs     │
  │  Modern Relevance      │  Obsolete           │  Obsolete (replaced by    │
  │                        │                     │  LCD, but historically    │
  │                        │                     │  dominant)                │
  └────────────────────────┴─────────────────────┴───────────────────────────┘


  ► 1.3.3  Flat Panel Displays
  ────────────────────────────

  Flat panel displays have completely replaced CRTs for all consumer and
  professional applications. They are thinner, lighter, consume less power,
  and produce no geometric distortion.


  ◆ LCD (Liquid Crystal Display)

    Working Principle:
      1. A backlight (LED or fluorescent) provides uniform white light
         from behind the panel.
      2. Light passes through a rear polarizing filter (polarizes in
         one direction, say horizontal).
      3. The polarized light enters a layer of liquid crystal molecules
         arranged in a twisted alignment (Twisted Nematic or IPS).
      4. In the OFF state, the liquid crystals rotate the polarization
         by 90°, allowing light to pass through the front polarizer
         (which is oriented at 90° to the rear one). The pixel appears
         BRIGHT.
      5. When voltage is applied, the crystals untwist and stop rotating
         the light's polarization. The light is blocked by the front
         polarizer. The pixel appears DARK.
      6. By varying the voltage, intermediate brightness levels are
         achieved.
      7. Each pixel has three sub-pixels with Red, Green, and Blue color
         filters to produce color.

    ┌──────────────────────────────────────────────────────────────────┐
    │  Backlight → Rear Polarizer → Liquid Crystal → Front Polarizer │
    │                                   ↕                             │
    │                           Voltage Control                       │
    │                    (twists/untwists crystals)                   │
    └──────────────────────────────────────────────────────────────────┘


  ◆ LED Display

    Technically, most "LED displays" are LCD displays that use LEDs as the
    backlight source instead of fluorescent tubes (CCFL). However, true LED
    displays (like those in large outdoor billboards or MicroLED panels)
    use individual LEDs as the actual light-emitting elements.

    Types:
      • Edge-lit LED LCD  — LEDs placed around the edges of the panel.
      • Direct-lit LED LCD — LEDs behind the entire panel (better
                            uniformity, allows local dimming).
      • Mini-LED          — Thousands of tiny LEDs for precise local
                            dimming zones, improving contrast.
      • MicroLED          — Microscopic self-emitting LEDs for each
                            pixel (no backlight needed). Emerging
                            premium technology with perfect blacks.


  ◆ OLED (Organic Light Emitting Diode)

    Working Principle:
      Each pixel is a self-emitting organic compound that produces light
      when current flows through it. No backlight is needed.

      Structure (simplified):
        Cathode → Electron Transport Layer → Emissive Layer (organic) →
        Hole Transport Layer → Anode (transparent) → Substrate (glass)

    Advantages over LCD:
      ✓ Perfect blacks (pixel simply turns off — zero light emission)
      ✓ Infinite contrast ratio
      ✓ Wider viewing angles (no backlight to scatter)
      ✓ Thinner and lighter (no backlight assembly)
      ✓ Faster response time (<0.1ms vs LCD's 1-5ms)
      ✓ Flexible displays possible (foldable phones)

    Disadvantages:
      ✗ Organic compounds degrade over time (burn-in risk)
      ✗ Blue OLED has shorter lifespan than red/green
      ✗ More expensive to manufacture at large sizes
      ✗ Lower peak brightness than high-end LED LCDs


  ┌─────────────────────────────────────────────────────────────────────────┐
  │              COMPARISON: CRT vs. LCD vs. OLED                           │
  ├────────────────────┬──────────────┬──────────────┬──────────────────────┤
  │  PARAMETER         │  CRT         │  LCD         │  OLED                │
  ├────────────────────┼──────────────┼──────────────┼──────────────────────┤
  │  Display Type      │  Emissive    │  Transmissive│  Emissive            │
  │  Backlight Needed  │  No (beam)   │  Yes         │  No (self-emitting)  │
  │  Thickness         │  Very thick  │  Thin        │  Very thin           │
  │  Weight            │  Heavy       │  Light       │  Very light          │
  │  Power Consumption │  High        │  Medium      │  Low (varies)        │
  │  Contrast Ratio    │  Good        │  Moderate    │  Infinite            │
  │  Response Time     │  Fast (~1ms) │  Slow (1-5ms)│  Very fast (<0.1ms)  │
  │  Viewing Angle     │  Good        │  Limited     │  Excellent           │
  │  Burn-in Risk      │  Yes         │  No          │  Yes                 │
  │  Color Accuracy    │  Good        │  Good        │  Excellent           │
  │  Lifespan          │  Long        │  Long        │  Moderate            │
  │  Form Factor       │  Bulky       │  Flat        │  Flat / Flexible     │
  │  Cost              │  Obsolete    │  Low-Medium  │  High                │
  └────────────────────┴──────────────┴──────────────┴──────────────────────┘



  ► 1.3.4  Hard Copy Devices
  ──────────────────────────

  Hard copy devices produce permanent graphical output on physical media
  (paper, film, fabric). They convert the digital image from the frame
  buffer into tangible form.

  ┌────────────────────────┬──────────────────────────────────────────────────┐
  │  DEVICE                │  DESCRIPTION                                     │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Inkjet Printer        │  Sprays tiny droplets of liquid ink onto paper   │
  │                        │  through microscopic nozzles. Droplets are       │
  │                        │  placed with precision to form the image.        │
  │                        │  • Thermal inkjet: heats ink to create           │
  │                        │    bubbles that push droplets out.               │
  │                        │  • Piezoelectric: crystal deformation ejects     │
  │                        │    droplets.                                     │
  │                        │  Uses CMYK color model. Good for photographs.    │
  │                        │  Resolution: 300-4800+ DPI.                      │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Laser Printer         │  Uses a laser beam to draw the image on a        │
  │                        │  photosensitive drum. The charged areas attract  │
  │                        │  toner (fine powder), which is transferred to    │
  │                        │  paper and fused by heat.                        │
  │                        │  Steps: Charge → Expose → Develop → Transfer     │
  │                        │  → Fuse → Clean.                                 │
  │                        │  Fast, high quality, cost-effective for text.    │
  │                        │  Resolution: 600-2400 DPI.                       │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Plotter               │  Draws continuous lines using pens on paper.     │
  │                        │  • Pen plotter: moves a pen across the paper     │
  │                        │    (produces true vector output).                │
  │                        │  • Electrostatic plotter: charges paper and      │
  │                        │    applies toner (raster output).                │
  │                        │  Used for large-format engineering drawings,     │
  │                        │  architectural blueprints.                       │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  3D Printer            │  Builds physical objects layer by layer from     │
  │                        │  a 3D digital model (STL file). Technologies:    │
  │                        │  FDM, SLA, SLS. Bridges CG and manufacturing.    │
  ├────────────────────────┼──────────────────────────────────────────────────┤
  │  Film Recorder         │  Exposes photographic film using a CRT or        │
  │                        │  laser, producing high-resolution slides or      │
  │                        │  negatives for print publication.                │
  └────────────────────────┴──────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────────┐
  │          COMPARISON: INKJET vs. LASER PRINTER                           │
  ├─────────────────────┬──────────────────────┬────────────────────────────┤
  │  PARAMETER          │  INKJET              │  LASER                     │
  ├─────────────────────┼──────────────────────┼────────────────────────────┤
  │  Printing Method    │  Liquid ink droplets │  Toner powder + heat       │
  │  Speed              │  Slower              │  Faster                    │
  │  Cost per Page      │  Higher (ink is      │  Lower (toner lasts        │
  │                     │  expensive)          │  longer)                   │
  │  Initial Cost       │  Lower               │  Higher                    │
  │  Photo Quality      │  Excellent           │  Good                      │
  │  Text Quality       │  Good                │  Excellent (sharper edges) │
  │  Best For           │  Photos, low volume  │  Text, high volume         │
  └─────────────────────┴──────────────────────┴────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1.4  RASTER SCAN AND RANDOM SCAN SYSTEMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


The two fundamental architectures for driving a display are raster scan and
random scan (vector). These represent fundamentally different approaches to
converting image descriptions into visible output.


  ► 1.4.1  Raster Scan System
  ───────────────────────────

  In a raster scan system, the electron beam (or backlight in LCDs) sweeps
  across the entire screen in a fixed pattern — left to right, top to
  bottom — painting the image one horizontal scan line at a time, like
  reading a book.

  ┌────────────────────────────────────────────────────────────────────┐
  │                    RASTER SCAN PATTERN                             │
  │                                                                    │
  │   ────────────────────────────►  Scan Line 1                       │
  │   ◄───────────────────── (Horizontal Retrace)                      │
  │   ────────────────────────────►  Scan Line 2                       │
  │   ◄─────────────────────                                           │
  │   ────────────────────────────►  Scan Line 3                       │
  │       ...                                                          │
  │   ────────────────────────────►  Scan Line N (last)                │
  │   ◄═══════════════════════════ (Vertical Retrace: beam returns     │
  │                                  to top-left corner)               │
  │                                                                    │
  │   One complete sweep = ONE FRAME                                   │
  │   The process repeats at the REFRESH RATE (e.g., 60 Hz)            │
  └────────────────────────────────────────────────────────────────────┘

  Key Characteristics:
    • The image is stored as a 2D array of pixel values in a FRAME BUFFER
      (a dedicated block of memory).
    • Each pixel's intensity/color is read from the frame buffer as the
      beam reaches that pixel's position.
    • Produces FILLED AREAS — can display solid regions, gradients, and
      photographic images.
    • Refresh is content-independent — the entire screen is refreshed
      regardless of how complex the image is.
    • Supports millions of colors per pixel.

  Interlaced vs. Non-Interlaced (Progressive) Scanning:
    • Non-interlaced: Every scan line is painted in every frame. Smoother
      but requires double the bandwidth.
    • Interlaced: Odd lines painted in one pass (odd field), even lines in
      the next (even field). Two fields make one frame. Reduces bandwidth
      but can cause visible flicker on fine horizontal patterns.


  ► 1.4.2  Random Scan (Vector) System
  ─────────────────────────────────────

  In a random scan system, the electron beam is directed only to the parts
  of the screen where the image exists — drawing lines (vectors) directly
  from endpoint to endpoint in any order. The beam can move to any random
  position on the screen at any time.

  ┌────────────────────────────────────────────────────────────────────┐
  │                   RANDOM SCAN PATTERN                              │
  │                                                                    │
  │              ╱╲                                                    │
  │             ╱  ╲              The beam draws each                  │
  │            ╱    ╲             line/vector directly                 │
  │           ╱______╲            by moving from one                   │
  │                               endpoint to the next                 │
  │           ┌──────┐            in any order.                        │
  │           │      │                                                 │
  │           │      │            No scan lines.                       │
  │           └──────┘            No pixel grid.                       │
  │                                                                    │
  │   Image stored as a DISPLAY LIST (list of drawing commands):       │
  │     MOVE_TO(x1,y1) → LINE_TO(x2,y2) → LINE_TO(x3,y3) → ...         │
  │                                                                    │
  │   The beam retraces the entire display list at the refresh rate.   │
  └────────────────────────────────────────────────────────────────────┘

  Key Characteristics:
    • Image stored as a DISPLAY LIST (also called display file) — a
      sequence of line-drawing commands, not a pixel array.
    • The beam draws only where there are lines — blank areas are skipped.
    • Produces WIREFRAME IMAGES — lines and curves only, no filled areas.
    • Refresh time depends on image complexity — more lines = more time
      to redraw = potential flicker for complex images.
    • Very smooth, high-resolution lines (no staircase/aliasing effect).
    • Limited color capability (typically uses beam penetration for color).


  ┌──────────────────────────────────────────────────────────────────────────┐
  │            COMPARISON: RASTER SCAN vs. RANDOM SCAN                       │
  ├──────────────────────────┬────────────────────┬──────────────────────────┤
  │  PARAMETER               │  RASTER SCAN       │  RANDOM SCAN             │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Beam Movement           │  Fixed pattern     │  Arbitrary / random      │
  │                          │  (left→right,      │  (directly to drawing    │
  │                          │  top→bottom)       │  positions)              │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Image Storage           │  Frame buffer      │  Display list            │
  │                          │  (pixel array)     │  (drawing commands)      │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Image Type              │  Filled areas,     │  Lines/wireframes only   │
  │                          │  photos, gradients │                          │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Refresh Time            │  Constant (depends │  Variable (depends on    │
  │                          │  on resolution)    │  number of lines)        │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Line Quality            │  Aliased (jagged   │  Smooth, high            │
  │                          │  staircase effect) │  resolution              │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Color Capability        │  Millions of       │  Limited (4 colors via   │
  │                          │  colors (RGB)      │  beam penetration)       │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Memory Requirement      │  High (frame       │  Low (only stores        │
  │                          │  buffer: MBs)      │  drawing commands)       │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Filled Area Rendering   │  Yes               │  No                      │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Flicker                 │  None (if refresh  │  Possible for complex    │
  │                          │  rate ≥ 60 Hz)     │  images (many vectors)   │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Cost                    │  Lower             │  Higher                  │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Realistic Images        │  Yes (photos)      │  No (wireframe only)     │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Modern Usage            │  ALL modern        │  Obsolete (historical    │
  │                          │  displays          │  significance only)      │
  ├──────────────────────────┼────────────────────┼──────────────────────────┤
  │  Application Areas       │  General computing,│  Oscilloscopes, air      │
  │                          │  gaming, design    │  traffic control (old)   │
  └──────────────────────────┴────────────────────┴──────────────────────────┘

  Why Random Scan Was Largely Replaced:
    → Raster scan can display filled areas, photographs, and complex
      shading — essential for modern graphics.
    → Frame buffer memory became cheap, making raster systems affordable.
    → GPUs are designed around raster processing (scan conversion).
    → Modern applications demand photorealistic rendering, which requires
      per-pixel color control — only possible with raster systems.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1.5  VIDEO CONTROLLER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


The video controller (also called display controller or RAMDAC controller) is
the hardware component responsible for reading pixel data from the frame buffer
and converting it into the electrical signals that drive the display.


  ► Architecture and Refresh Operation
  ─────────────────────────────────────

  ┌─────────────────────── VIDEO CONTROLLER BLOCK DIAGRAM ─────────────────┐
  │                                                                        │
  │   ┌──────────────┐      ┌────────────────┐      ┌──────────────┐       │
  │   │              │      │                │      │              │       │
  │   │  CPU / GPU   ├─────►│  FRAME BUFFER  ├─────►│    VIDEO     │       │
  │   │  (writes     │      │  (Stores pixel │      │  CONTROLLER  │       │
  │   │   pixel      │      │   values as    │      │              │       │
  │   │   data)      │      │   a 2D array)  │      │  ┌─────────┐ │       │
  │   │              │      │                │      │  │X Counter│ │       │
  │   └──────────────┘      └────────┬───────┘      │  │Y Counter│ │       │
  │                                  │              │  └─────────┘ │       │
  │                                  │              │      │       │       │
  │                                  ▼              │      ▼       │       │
  │                           ┌──────────────┐      │  ┌──────┐    │       │
  │                           │ Pixel Value  ├─────►│  │ DAC  │    │       │
  │                           │ (from memory)│      │  └──┬───┘    │       │
  │                           └──────────────┘      │     │        │       │
  │                                                 │     ▼        │       │
  │                                                 │  Analog      │       │
  │                                                 │  Signal      ├──────►│
  │                                                 │  (to         │  To   │
  │                                                 │  display)    │ CRT/  │
  │                                                 └──────────────┘ LCD   │
  │                                                                        │
  └────────────────────────────────────────────────────────────────────────┘


  ► Step-by-Step Refresh Operation
  ────────────────────────────────

  The video controller performs the following cycle continuously at the
  refresh rate (e.g., 60 times per second):

    Step 1: The X (horizontal) and Y (vertical) counters are initialized
            to (0, 0) — the top-left pixel of the screen.

    Step 2: The controller uses the (X, Y) counters to compute the memory
            address of the corresponding pixel in the frame buffer:
              address = base_address + (Y × screen_width + X) × bytes_per_pixel

    Step 3: The pixel value (a binary number representing color/intensity)
            is read from the frame buffer memory.

    Step 4: The pixel value is sent to the DAC (Digital-to-Analog
            Converter), which converts it to analog voltage signals
            (one each for R, G, B in a color system).

    Step 5: The analog signals drive the display — controlling electron
            beam intensity (CRT) or pixel transistor voltage (LCD).

    Step 6: The X counter is incremented (move to next pixel on the
            same scan line).

    Step 7: When X reaches the end of a scan line (X = screen_width):
              • X is reset to 0.
              • Y is incremented (move to the next scan line).
              • Horizontal retrace occurs (beam returns to left edge).

    Step 8: When Y reaches the bottom of the screen (Y = screen_height):
              • Both X and Y are reset to 0.
              • Vertical retrace occurs (beam returns to top-left).
              • One complete FRAME has been displayed.

    Step 9: The entire process repeats for the next frame.


  ► Display Processor (Graphics Controller)
  ──────────────────────────────────────────

  A display processor is a specialized processing unit that offloads
  graphical computations from the main CPU. It sits between the CPU and
  the frame buffer, interpreting high-level drawing commands (stored in
  a display file / display list) and converting them into pixel data
  written to the frame buffer.

  In a random scan system:
    • The display processor reads the display file (list of vector
      commands) and directly drives the beam deflection circuitry to
      draw lines on the screen. No frame buffer is used.

  In a raster scan system:
    • The display processor (modern GPU) executes scan conversion
      algorithms — converting geometric primitives (lines, triangles)
      into pixel values stored in the frame buffer.

  The display processor concept evolved into the modern GPU, which is a
  massively parallel processor capable of executing millions of
  vertex/fragment operations per second.



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1.6  DIGITAL-TO-ANALOG CONVERTER (DAC) AND FRAME BUFFER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► 1.6.1  Digital-to-Analog Converter (DAC)
  ──────────────────────────────────────────

  The DAC is the bridge between the digital world (binary pixel values in
  memory) and the analog world (voltage signals that drive the display).

  ┌─────────────────────── DAC OPERATION ─────────────────────────────┐
  │                                                                   │
  │   Digital Pixel Value              Analog Voltage Signal          │
  │   (from frame buffer)             (to display)                    │
  │                                                                   │
  │   Binary: 10110100  ──────►  DAC  ──────►  0.703 V                │
  │   (= 180 out of 255)                       (= 180/255 × Vmax)     │
  │                                                                   │
  │   For a color system, THREE DACs work in parallel:                │
  │     R bits → DAC_R → Red voltage                                  │
  │     G bits → DAC_G → Green voltage                                │
  │     B bits → DAC_B → Blue voltage                                 │
  │                                                                   │
  │   The three analog voltages control the three electron guns       │
  │   (CRT) or three sub-pixel transistors (LCD) simultaneously.      │
  │                                                                   │
  └───────────────────────────────────────────────────────────────────┘

  For an n-bit DAC:
    • $2^n$ discrete voltage levels are possible.
    • An 8-bit DAC produces 256 levels per channel.
    • Three 8-bit DACs (one per R, G, B) produce
      $256 \times 256 \times 256 = 16,777,216$ colors (24-bit true color).

  Speed Requirement:
    The DAC must convert pixels fast enough to keep up with the display's
    pixel clock. For a 1920×1080 display at 60 Hz refresh with blanking
    intervals, the pixel clock is approximately 148.5 MHz — meaning the
    DAC must convert one pixel every ~6.7 nanoseconds.


  ► 1.6.2  Frame Buffer — Detailed Organization
  ──────────────────────────────────────────────

  The frame buffer is a dedicated block of memory that stores the complete
  image to be displayed. Each pixel on the screen has a corresponding
  memory location in the frame buffer that stores its color value.

  ┌─────────────────────── FRAME BUFFER ORGANIZATION ──────────────────┐
  │                                                                    │
  │   Screen Pixel (x, y)  ←→  Memory Address in Frame Buffer          │
  │                                                                    │
  │   Frame Buffer is organized as a 2D array:                         │
  │                                                                    │
  │   ┌─────┬─────┬─────┬─────┬─────┬─────┐                            │
  │   │(0,0)│(1,0)│(2,0)│(3,0)│ ... │(W,0)│  Row 0 (Scan Line 0)       │
  │   ├─────┼─────┼─────┼─────┼─────┼─────┤                            │
  │   │(0,1)│(1,1)│(2,1)│(3,1)│ ... │(W,1)│  Row 1                     │
  │   ├─────┼─────┼─────┼─────┼─────┼─────┤                            │
  │   │(0,2)│(1,2)│(2,2)│(3,2)│ ... │(W,2)│  Row 2                     │
  │   ├─────┼─────┼─────┼─────┼─────┼─────┤                            │
  │   │ ... │ ... │ ... │ ... │ ... │ ... │  ...                       │
  │   ├─────┼─────┼─────┼─────┼─────┼─────┤                            │
  │   │(0,H)│(1,H)│(2,H)│(3,H)│ ... │(W,H)│  Row H (last row)          │
  │   └─────┴─────┴─────┴─────┴─────┴─────┘                            │
  │                                                                    │
  │   W = screen width in pixels                                       │
  │   H = screen height in pixels                                      │
  │   Each cell stores B bits (the "bit depth" or "color depth")       │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────────────┐
  │  KEY TERMINOLOGY                                                   │
  │                                                                    │
  │  • Bit Depth (B)     — Number of bits stored per pixel.            │
  │                        Determines how many distinct colors/        │
  │                        intensities each pixel can represent.       │
  │                                                                    │
  │  • Color Depth       — Total number of colors =  $2^B$             │
  │                                                                    │
  │  • Resolution        — Total number of pixels = Width × Height     │
  │                        (e.g., 1920 × 1080 = 2,073,600 pixels)      │
  │                                                                    │
  │  • Aspect Ratio      — Ratio of width to height of the display     │
  │                        (e.g., 16:9 for widescreen, 4:3 for old)    │
  │                                                                    │
  │  • Refresh Rate      — Number of times the full frame is redrawn   │
  │                        per second (measured in Hz). Typically      │
  │                        60 Hz, 75 Hz, 120 Hz, 144 Hz, or 240 Hz.    │
  │                        Higher refresh rate = smoother motion.      │
  │                                                                    │
  │  • Frame Buffer Size — Total memory required:                      │
  │                                                                    │
  │         Size (bits)  = Width × Height × Bit_Depth                  │
  │         Size (bytes) = (Width × Height × Bit_Depth) / 8            │
  │         Size (MB)    = Size (bytes) / (1024 × 1024)                │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘


  ► Frame Buffer Size Calculation — Solved Examples
  ──────────────────────────────────────────────────

  ┌────────────────────────────────────────────────────────────────────┐
  │  EXAMPLE 1                                                         │
  │  Resolution: 640 × 480,  Colors: 256 (8-bit)                       │
  │                                                                    │
  │  Bit depth = log₂(256) = 8 bits/pixel                              │
  │  Frame buffer = 640 × 480 × 8 = 2,457,600 bits                     │
  │               = 2,457,600 / 8 = 307,200 bytes                      │
  │               = 307,200 / 1024 = 300 KB                            │
  │               ≈ 0.293 MB                                           │
  └────────────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────────────┐
  │  EXAMPLE 2                                                         │
  │  Resolution: 1280 × 800,  Colors: 16,777,216 (24-bit true color)   │
  │                                                                    │
  │  Total colors = 16,777,216 = 2²⁴ → Bit depth = 24 bits/pixel       │
  │  Frame buffer = 1280 × 800 × 24 = 24,576,000 bits                  │
  │               = 24,576,000 / 8 = 3,072,000 bytes                   │
  │               = 3,072,000 / (1024 × 1024) ≈ 2.93 MB                │
  │                                                                    │
  │  ★ This is a frequently asked exam question — see Set 2, Q1(b).    │
  └────────────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────────────┐
  │  EXAMPLE 3                                                         │
  │  Resolution: 1024 × 768,  Colors: 16 million (24-bit)              │
  │                                                                    │
  │  Frame buffer = 1024 × 768 × 24 = 18,874,368 bits                  │
  │               = 18,874,368 / 8 = 2,359,296 bytes                   │
  │               = 2,359,296 / (1024 × 1024) ≈ 2.25 MB                │
  └────────────────────────────────────────────────────────────────────┘

  ┌────────────────────────────────────────────────────────────────────┐
  │  EXAMPLE 4                                                         │
  │  Resolution: 1920 × 1080,  Color Depth: 32-bit (24-bit RGB + 8     │
  │  alpha)                                                            │
  │                                                                    │
  │  Frame buffer = 1920 × 1080 × 32 = 66,355,200 bits                 │
  │               = 66,355,200 / 8 = 8,294,400 bytes                   │
  │               = 8,294,400 / (1024 × 1024) ≈ 7.91 MB                │
  │                                                                    │
  │  ★ This is a common exam question — see AI Set 7, Q1(a).           │
  └────────────────────────────────────────────────────────────────────┘


  ► Flickering and Refresh Calculation — Solved Examples
  ──────────────────────────────────────────────────────

  Flickering occurs when the phosphor fades significantly between
  consecutive refreshes — i.e., when the refresh rate is too low. The
  human eye perceives flicker below approximately 50-60 Hz.

  ┌─────────────────────────────────────────────────────────────────────┐
  │  EXAMPLE 1: Will it flicker? (Set 1, Q1a)                           │
  │                                                                     │
  │  Given:                                                             │
  │    Resolution = 640 × 480                                           │
  │    Time per pixel = 20 ns = 20 × 10⁻⁹ s                             │
  │                                                                     │
  │  Total pixels = 640 × 480 = 307,200                                 │
  │  Total scan time = 307,200 × 20 × 10⁻⁹ = 6.144 × 10⁻³ s             │
  │                  = 6.144 ms per frame                               │
  │                                                                     │
  │  Refresh rate = 1 / 0.006144 = 162.76 Hz                            │
  │                                                                     │
  │  ✓ Since 162.76 Hz >> 60 Hz, there will be NO flickering.           │
  │    The display refreshes fast enough that the phosphor does not     │
  │    fade perceptibly between frames.                                 │
  └─────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────┐
  │  EXAMPLE 2: Refresh rate calculation (AI Set 9, Q1b)                │
  │                                                                     │
  │  Given:                                                             │
  │    Resolution = 800 × 600                                           │
  │    Time per pixel = 15 ns                                           │
  │                                                                     │
  │  Total pixels = 800 × 600 = 480,000                                 │
  │  Total scan time = 480,000 × 15 × 10⁻⁹ = 7.2 × 10⁻³ s               │
  │                  = 7.2 ms per frame                                 │
  │                                                                     │
  │  Achievable refresh rate = 1 / 0.0072 = 138.89 Hz                   │
  │                                                                     │
  │  ✓ Well above the 60 Hz threshold, no flickering.                   │
  └─────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────┐
  │  EXAMPLE 3: Time per scan line (AI Set 3, Q2a)                      │
  │                                                                     │
  │  Given:                                                             │
  │    Resolution = 1280 × 1024                                         │
  │    Refresh rate = 60 fps                                            │
  │                                                                     │
  │  Total pixels per frame = 1280 × 1024 = 1,310,720                   │
  │  Total time per frame = 1 / 60 = 0.01667 s = 16.67 ms               │
  │  Time per pixel = 16.67 ms / 1,310,720 ≈ 12.72 ns                   │
  │                                                                     │
  │  Pixels per scan line = 1280                                        │
  │  Time per scan line = 1280 × 12.72 ns = 16,281.6 ns                 │
  │                     ≈ 16.28 μs per scan line                        │
  └─────────────────────────────────────────────────────────────────────┘


  ► Resolution, Aspect Ratio, and Image Quality
  ──────────────────────────────────────────────

  ┌────────────────────────┬──────────────────────────────────────────────┐
  │  CONCEPT               │  DESCRIPTION & IMPACT ON QUALITY             │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Resolution            │  The total number of pixels in each          │
  │                        │  dimension (e.g., 1920 × 1080). Higher       │
  │                        │  resolution = more detail, sharper images,   │
  │                        │  but requires more memory and bandwidth.     │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Aspect Ratio          │  Ratio of width to height. Common ratios:    │
  │                        │  4:3 (old monitors), 16:9 (widescreen),      │
  │                        │  16:10 (some laptops), 21:9 (ultrawide).     │
  │                        │  Mismatched aspect ratios cause stretching   │
  │                        │  or black bars.                              │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Refresh Rate          │  Higher refresh rate reduces motion blur     │
  │                        │  and eliminates flicker. 60 Hz is baseline,  │ 
  │                        │  120+ Hz is preferred for gaming.            │
  ├────────────────────────┼──────────────────────────────────────────────┤
  │  Pixel Density (PPI)   │  Pixels per inch — depends on both           │
  │                        │  resolution and physical screen size.        │
  │                        │  Higher PPI = sharper image. Retina          │
  │                        │  displays have 220+ PPI.                     │
  └────────────────────────┴──────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1.7  GRAPHICS SOFTWARE AND MODERN GRAPHICS HARDWARE (GPU)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ► 1.7.1  Graphics Software
  ──────────────────────────

  Graphics software provides the interface between the programmer/user and
  the graphics hardware. It can be categorized into:

  ┌────────────────────────────┬──────────────────────────────────────────────┐
  │  CATEGORY                  │  EXAMPLES & DESCRIPTION                      │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Graphics APIs             │  OpenGL, Vulkan, DirectX, Metal, WebGL.      │
  │  (Application Programming  │  Provide functions for drawing primitives,   │
  │   Interfaces)              │  applying transformations, setting up        │
  │                            │  cameras, lighting, and texturing.           │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Utility Libraries         │  GLUT/freeglut (windowing for OpenGL),       │
  │                            │  GLU (OpenGL Utility), GLM (math library),   │
  │                            │  GLEW/GLAD (extension loading).              │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Shading Languages         │  GLSL (OpenGL), HLSL (DirectX), MSL          │
  │                            │  (Metal), WGSL (WebGPU). Programs that       │
  │                            │  run on the GPU to control vertex and        │
  │                            │  fragment processing.                        │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Modeling / DCC Software   │  Blender, Maya, 3ds Max, ZBrush,             │
  │                            │  SolidWorks. Used to create 3D models,       │
  │                            │  animations, and visual effects.             │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Game Engines              │  Unity, Unreal Engine, Godot. Provide        │
  │                            │  complete graphics + physics + audio +       │
  │                            │  scripting frameworks for interactive        │
  │                            │  applications.                               │
  ├────────────────────────────┼──────────────────────────────────────────────┤
  │  Image Editing Software    │  Photoshop, GIMP, Krita. Raster image        │
  │                            │  manipulation — filters, compositing,        │
  │                            │  color correction.                           │
  └────────────────────────────┴──────────────────────────────────────────────┘


  ► 1.7.2  Modern Graphics Hardware — The GPU
  ────────────────────────────────────────────

  The GPU (Graphics Processing Unit) is the most important piece of
  hardware in a modern graphics system. Originally designed solely for
  graphics rendering, GPUs have evolved into massively parallel processors
  capable of both graphics and general-purpose computation.


  ◆ Why GPUs Exist — The Need for Parallel Processing

    Graphics rendering is inherently parallel: each pixel can be computed
    independently of others. A single frame at 1920×1080 has over 2 million
    pixels, and modern games render 60+ frames per second. That's 120+
    million pixel calculations per second — far too many for a CPU, which
    excels at sequential tasks but has only a few cores.

    GPUs solve this with MASSIVE PARALLELISM:
      • A modern CPU has 8-16 cores.
      • A modern GPU has 5,000-16,000+ cores (smaller but numerous).
      • Each GPU core handles a few pixels or vertices simultaneously.


  ◆ GPU Architecture — Simplified Overview

  ┌─────────────────────── GPU BLOCK DIAGRAM ──────────────────────────┐
  │                                                                    │
  │   ┌──────────────────────────────────────────────────────────────┐ │
  │   │                    GPU CHIP                                  │ │
  │   │                                                              │ │
  │   │   ┌─────────────────────────────────────────────────────┐    │ │
  │   │   │  Streaming Multiprocessors (SMs)                    │    │ │
  │   │   │  ┌────┐ ┌────┐ ┌────┐ ┌────┐    ... (×N SMs)        │    │ │
  │   │   │  │Core│ │Core│ │Core│ │Core│                        │    │ │
  │   │   │  │Core│ │Core│ │Core│ │Core│   Each SM has 32-128   │    │ │
  │   │   │  │Core│ │Core│ │Core│ │Core│   CUDA/shader cores    │    │ │
  │   │   │  │Core│ │Core│ │Core│ │Core│                        │    │ │
  │   │   │  └────┘ └────┘ └────┘ └────┘                        │    │ │
  │   │   └─────────────────────────────────────────────────────┘    │ │
  │   │                                                              │ │
  │   │   ┌──────────┐  ┌──────────┐  ┌────────────────────────┐     │ │
  │   │   │ Texture  │  │ Raster   │  │ Render Output Units    │     │ │
  │   │   │  Units   │  │  Engine  │  │ (ROPs / Frame Buffer)  │     │ │
  │   │   └──────────┘  └──────────┘  └────────────────────────┘     │ │
  │   │                                                              │ │
  │   └──────────────────────────────────────────────────────────────┘ │
  │                              │                                     │
  │                              ▼                                     │
  │   ┌──────────────────────────────────────────────────────────────┐ │
  │   │              VRAM (Video Memory / GDDR6)                     │ │
  │   │         Stores frame buffer, textures, vertex data           │ │
  │   │                  Capacity: 4-24 GB                           │ │
  │   └──────────────────────────────────────────────────────────────┘ │
  │                                                                    │
  └────────────────────────────────────────────────────────────────────┘


  ◆ The Graphics Pipeline (as implemented in GPU hardware)

    The graphics pipeline is the sequence of processing stages that
    transform 3D scene data into a 2D image displayed on screen. This
    pipeline is the heart of GPU operation.

  ┌─────────────────────────────────────────────────────────────────────┐
  │                     GRAPHICS PIPELINE                               │
  │                                                                     │
  │   ┌────────────────────┐                                            │
  │   │  1. Application    │  CPU prepares scene data (vertices,        │
  │   │     Stage          │  transforms, draw calls). Sends to GPU.    │
  │   └────────┬───────────┘                                            │
  │            ▼                                                        │
  │   ┌────────────────────┐                                            │
  │   │  2. Vertex         │  Processes each vertex: applies model,     │
  │   │     Processing     │  view, and projection transforms.          │
  │   │     (Vertex Shader)│  Programmable stage (GLSL code runs here). │
  │   └────────┬───────────┘                                            │
  │            ▼                                                        │
  │   ┌────────────────────┐                                            │
  │   │  3. Primitive      │  Assembles vertices into primitives        │
  │   │     Assembly       │  (triangles, lines, points).               │
  │   └────────┬───────────┘                                            │
  │            ▼                                                        │
  │   ┌────────────────────┐                                            │
  │   │  4. Clipping       │  Removes primitives (or portions)          │
  │   │                    │  outside the view frustum.                 │
  │   └────────┬───────────┘                                            │
  │            ▼                                                        │
  │   ┌────────────────────┐                                            │
  │   │  5. Rasterization  │  Converts primitives to fragments          │
  │   │                    │  (potential pixels). Determines which      │
  │   │                    │  pixels are covered by each primitive.     │
  │   │                    │  Uses scan conversion algorithms           │
  │   │                    │  (Bresenham's, etc.) in hardware.          │
  │   └────────┬───────────┘                                            │ 
  │            ▼                                                        │
  │   ┌────────────────────┐                                            │
  │   │  6. Fragment       │  Processes each fragment: computes final   │
  │   │     Processing     │  color using lighting, texturing, and      │
  │   │     (Fragment      │  shading equations.                        │
  │   │      Shader)       │  Programmable stage (GLSL code runs here). │
  │   └────────┬───────────┘                                            │
  │            ▼                                                        │
  │   ┌────────────────────┐                                            │
  │   │  7. Per-Fragment   │  Depth test (z-buffer), stencil test,      │
  │   │     Operations     │  alpha blending, antialiasing.             │
  │   └────────┬───────────┘                                            │
  │            ▼                                                        │
  │   ┌────────────────────┐                                            │
  │   │  8. Frame Buffer   │  Final pixel colors written to frame       │
  │   │     Output         │  buffer → sent to display via DAC.         │
  │   └────────────────────┘                                            │
  │                                                                     │
  └─────────────────────────────────────────────────────────────────────┘


  ◆ How GPUs Transformed Computer Graphics

    ┌──────────────────────┬────────────────────────────────────────────┐
    │  BEFORE GPUs         │  AFTER GPUs                                │
    ├──────────────────────┼────────────────────────────────────────────┤
    │  CPU did all         │  GPU handles all graphics-intensive        │
    │  rendering — slow,   │  tasks — parallel processing enables       │
    │  software-only       │  real-time 3D rendering                    │
    ├──────────────────────┼────────────────────────────────────────────┤
    │  Simple wireframe    │  Photorealistic real-time rendering        │
    │  models only         │  with millions of polygons                 │
    ├──────────────────────┼────────────────────────────────────────────┤
    │  Fixed rendering     │  Programmable shaders allow custom         │
    │  pipeline            │  visual effects (water, fire, skin, etc.)  │
    ├──────────────────────┼────────────────────────────────────────────┤
    │  Minutes per frame   │  Billions of pixels per second             │
    │  (for complex scenes)│  (60+ FPS at 4K resolution)                │
    ├──────────────────────┼────────────────────────────────────────────┤
    │  Graphics only       │  GPGPU: machine learning, scientific       │
    │                      │  computing, cryptocurrency mining          │
    └──────────────────────┴────────────────────────────────────────────┘


  ► 1.7.3  Components of a Complete Graphics System
  ──────────────────────────────────────────────────

  A complete graphics system consists of the following components working
  together:

  ┌────────────────────────────────────────────────────────────────────────┐
  │                                                                        │
  │   ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐    │
  │   │   INPUT     │    │   PROCESSOR │    │   OUTPUT                │    │
  │   │   DEVICES   ├───►│   (CPU+GPU) ├───►│   DEVICES               │    │
  │   │             │    │             │    │                         │    │
  │   │  • Mouse    │    │  • CPU      │    │  • Monitor (CRT/LCD/    │    │
  │   │  • Keyboard │    │  • GPU      │    │    OLED)                │    │
  │   │  • Joystick │    │  • RAM      │    │  • Printer              │    │
  │   │  • Touch    │    │  • VRAM     │    │  • Plotter              │    │
  │   │    screen   │    │  • Frame    │    │  • VR Headset           │    │
  │   │  • Scanner  │    │    Buffer   │    │  • Projector            │    │
  │   │  • Tablet   │    │  • DAC      │    │                         │    │
  │   └─────────────┘    └─────────────┘    └─────────────────────────┘    │
  │                              │                                         │
  │                              ▼                                         │
  │                     ┌─────────────────┐                                │
  │                     │  STORAGE        │                                │
  │                     │  • Hard Disk    │                                │
  │                     │  • SSD          │                                │
  │                     │  • Optical Media│                                │
  │                     └─────────────────┘                                │
  │                                                                        │
  └────────────────────────────────────────────────────────────────────────┘



━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  CHAPTER SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  ┌────────────────────────────────────────────────────────────────────────┐
  │                                                                        │
  │  This chapter covered the foundational layer of computer graphics:     │
  │                                                                        │
  │    ✦ CG Definition & Types — Interactive vs. passive graphics.         │
  │                                                                        │
  │    ✦ Applications — CAD, simulation, scientific visualization,         │
  │      entertainment, medicine, education, and many more.                │
  │                                                                        │
  │    ✦ Recent Trends — VR, AR, real-time ray tracing, AI graphics,       │
  │      cloud rendering, GPU compute.                                     │
  │                                                                        │
  │    ✦ Input Devices — Six logical classes (Locator, Stroke, Valuator,   │
  │      Choice, String, Pick), physical devices (mouse, trackball,        │
  │      joystick, touch screen, data gloves), input modes (Request,       │
  │      Sample, Event).                                                   │
  │                                                                        │
  │    ✦ Display Devices — CRT structure and working, color CRT            │
  │      (beam penetration vs. shadow mask), flat panels (LCD, LED,        │
  │      OLED), and their detailed comparisons.                            │
  │                                                                        │
  │    ✦ Hard Copy Devices — Inkjet, laser, plotter, 3D printer.           │
  │                                                                        │
  │    ✦ Raster vs. Random Scan — Architecture, image storage,             │
  │      capabilities, comprehensive comparison table.                     │
  │                                                                        │
  │    ✦ Video Controller — Refresh operation, display processor,          │
  │      step-by-step refresh cycle.                                       │
  │                                                                        │
  │    ✦ DAC — Digital-to-analog conversion for driving displays.          │
  │                                                                        │
  │    ✦ Frame Buffer — Organization, bit depth, color depth,              │
  │      resolution, aspect ratio, refresh rate. Multiple solved           │
  │      examples of frame buffer size and refresh rate calculations.      │
  │                                                                        │
  │    ✦ GPU — Architecture, graphics pipeline stages, how GPUs            │
  │      transformed the field from software rendering to real-time        │
  │      photorealism.                                                     │
  │                                                                        │
  │    ✦ Graphics Software — APIs, shading languages, modeling tools,      │
  │      game engines.                                                     │
  │                                                                        │
  │  In the next chapter, we explore the algorithms that bridge the gap    │
  │  between mathematical geometry and the pixel grid — scan conversion    │
  │  algorithms for lines, circles, ellipses, and filled areas.            │ 
  │                                                                        │
  └────────────────────────────────────────────────────────────────────────┘


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


---

## 📝 Exam Practice Questions

### From AI-Generated Sets (aiQuestions.txt)

**Set 1, Q1:**
a. Explain the architecture of raster scan and random scan display systems with neat diagrams. Compare them on the basis of image quality, cost, memory usage, and application areas.
b. Describe the working principle of a CRT with a labeled diagram. Explain how a color CRT produces colors using the beam penetration method.

**Set 2, Q1:**
a. What is a video controller? Explain the refresh operation of a video controller with a neat diagram.
   *OR:* List and explain at least five applications of computer graphics in different fields such as CAD, entertainment, medicine, education, and simulation.
b. Explain the working principle of LCD display technology. How does it differ from CRT in terms of display mechanism?

**Set 3, Q1:**
a. What is a frame buffer? A raster system has a resolution of 1024 × 768 and supports 16 million colors. Calculate the size of the frame buffer in megabytes. Show all working.
b. Explain the classification of interactive input devices into six logical classes (Locator, Stroke, Valuator, Choice, String, Pick). Describe the working principle of any two physical input devices.

**Set 4, Q1:**
a. Discuss the evolution and recent trends in computer graphics technology such as Virtual Reality, Augmented Reality, and real-time ray tracing. How have GPUs transformed the field?
b. Explain the working mechanism of the Digital-to-Analog Converter (DAC) in a raster scan system. How does it contribute to producing the display output?

**Set 5, Q1:**
a. What are the major components of a raster graphics system? Explain each component with a block diagram.
   *OR:* Discuss the significance of computer graphics in Computer Aided Design (CAD). How has CAD changed the engineering design process?
b. Explain the working principle of a touch screen as an interactive input device. How does a capacitive touch screen differ from a resistive touch screen?

**Set 6, Q1:**
a. Explain the architecture of a random scan (vector) display system with a diagram. Why has it been largely replaced by raster scan systems?
b. What is the role of a display processor (graphics controller) in a graphical system? Explain how the display file is used to drive the display.

**Set 7, Q1:**
a. What is scan conversion? Explain the role of the frame buffer in the scan conversion process. If a display has a resolution of 1920 × 1080 and uses 32-bit true color, calculate the frame buffer size in megabytes.
b. Describe the three modes of input handling (Request, Sample, Event) used in interactive graphics systems. Give an example of each mode.

**Set 8, Q1:**
a. Classify display devices used in computer graphics. Explain the working principles of LED and OLED display technologies. How are they superior to traditional CRT displays?
b. What is a GPU? Explain the stages of the graphics pipeline as implemented in modern GPU hardware.

**Set 9, Q1:**
a. Define computer graphics. Explain its applications in medicine, education, and entertainment with examples.
   *OR:* What are the recent trends in computer graphics? Discuss the impact of real-time rendering, virtual reality, and augmented reality on modern graphics applications.
b. What is the difference between raster scan and random scan architectures? Calculate the refresh rate achievable if a video controller takes 15 ns per pixel for a 800 × 600 resolution display.

**Set 10, Q1:**
a. Explain the concept of resolution, aspect ratio, and refresh rate in a raster display system. How do these parameters affect the quality of the displayed image?
b. What are hard copy devices? Explain the working principles of an inkjet printer and a laser printer. Compare their suitability for graphics output.

---

### From Past Papers (Questions.txt)

**Set 1, Q1:**
a. Discuss video controller refresh operation with a neat diagram. If on average, it takes 20 ns for a video controller to access a pixel value from the frame buffer and glow on the screen, will it produce a flickering effect? (Screen resolution is 640 × 480)
   *OR:* Define computer graphics. Explain the applications of computer graphics in Computer Simulation, Scientific Visualization, and CAD.
b. Define CRT. Explain with a neat diagram the working principle of the Shadow Mask method.

**Set 2, Q1:**
a. What are the basic components of a graphical system? List out the areas of application of computer graphics by emphasizing your answer on CAD.
b. What role does a frame buffer play in graphical rendering? A raster graphics system can produce a total number of 16,777,216 different levels of intensities out of a single pixel on the screen. If the total resolution of the screen is 1280 × 800, what is the required size of the frame buffer of this system?

**Set 3, Q1:**
a. Define computer graphics with its types. How has the evolution of computer graphics technology impacted the gaming industry in terms of realism and player immersion?
b. Graphical systems are composed of DAC and frame buffer organization. Why? Explain the working principle of data gloves with an example.

---

### Related Short Notes Topics (from Q7)
- Hard copy devices — *aiQ Set 2*
- DAC and frame buffer organization — *aiQ Set 3*
- Modern graphics hardware (GPU architecture) — *aiQ Set 4*
- Beam penetration vs. shadow mask CRT — *aiQ Set 5*
- Color CRT monitors (shadow mask vs. beam penetration) — *aiQ Set 7*
- Joystick and trackball input devices — *aiQ Set 8*
- Aspect ratio and resolution — *aiQ Set 9*
- Interactive input devices and their classification — *aiQ Set 10*
- Raster vs. Random Scan System — *Q Set 1, Q Set 2, aiQ Set 3*
