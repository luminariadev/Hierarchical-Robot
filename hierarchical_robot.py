# ============================================================
#  HIERARCHICAL MODELING - OPENGL + MATRIX STACK
#  Objek Kompleks: Robot Sederhana (Proporsi Fix)
#
#  Mata Kuliah : Grafika Komputer (IF216004)
# ============================================================
#
#  Kontrol Keyboard (SAMA PERSIS DENGAN VERSI ASLI):
#  Q/A  = Rotasi keseluruhan robot (kiri/kanan)
#  W/S  = Rotasi lengan kiri atas (naik/turun)
#  E/D  = Rotasi lengan kanan atas (naik/turun)
#  R/F  = Rotasi forearm kiri (tekuk/lurus)
#  T/G  = Rotasi forearm kanan (tekuk/lurus)
#  Y/H  = Rotasi kaki kiri (maju/mundur)
#  U/J  = Rotasi kaki kanan (maju/mundur)
#  I/K  = Anggukan kepala
#  ESC  = Keluar
# ============================================================

try:
    from OpenGL.GL import *
    from OpenGL.GLUT import *
    from OpenGL.GLU import *
    import sys
    import math
except ImportError:
    print("=" * 55)
    print("  ERROR: Library PyOpenGL tidak ditemukan!")
    print("  Install dengan perintah: pip install PyOpenGL PyOpenGL_accelerate")
    print("=" * 55)
    sys.exit(1)

# ─────────────────────────────────────────────
#  STATE: Sudut rotasi tiap bagian tubuh
# ─────────────────────────────────────────────
state = {
    "robot_rotate"    : 0.0,   # Rotasi seluruh robot (sumbu Y)
    "left_arm"        : 30.0,  # Lengan kiri atas
    "right_arm"       : -30.0, # Lengan kanan atas
    "left_forearm"    : 0.0,   # Lengan bawah kiri
    "right_forearm"   : 0.0,   # Lengan bawah kanan
    "left_leg"        : 10.0,  # Kaki kiri
    "right_leg"       : -10.0, # Kaki kanan
    "head_nod"        : 0.0,   # Anggukan kepala
}

STEP = 5.0   # Besar perubahan sudut per tombol

# ─────────────────────────────────────────────
#  HELPER: Gambar berbagai bentuk 3D
# ─────────────────────────────────────────────
def draw_box(w, h, d):
    """Gambar sebuah kotak berpusat di origin."""
    hw, hh, hd = w/2, h/2, d/2
    glBegin(GL_QUADS)

    # Depan
    glNormal3f(0, 0, 1)
    glVertex3f(-hw, -hh,  hd)
    glVertex3f( hw, -hh,  hd)
    glVertex3f( hw,  hh,  hd)
    glVertex3f(-hw,  hh,  hd)

    # Belakang
    glNormal3f(0, 0, -1)
    glVertex3f( hw, -hh, -hd)
    glVertex3f(-hw, -hh, -hd)
    glVertex3f(-hw,  hh, -hd)
    glVertex3f( hw,  hh, -hd)

    # Kiri
    glNormal3f(-1, 0, 0)
    glVertex3f(-hw, -hh, -hd)
    glVertex3f(-hw, -hh,  hd)
    glVertex3f(-hw,  hh,  hd)
    glVertex3f(-hw,  hh, -hd)

    # Kanan
    glNormal3f(1, 0, 0)
    glVertex3f( hw, -hh,  hd)
    glVertex3f( hw, -hh, -hd)
    glVertex3f( hw,  hh, -hd)
    glVertex3f( hw,  hh,  hd)

    # Atas
    glNormal3f(0, 1, 0)
    glVertex3f(-hw,  hh,  hd)
    glVertex3f( hw,  hh,  hd)
    glVertex3f( hw,  hh, -hd)
    glVertex3f(-hw,  hh, -hd)

    # Bawah
    glNormal3f(0, -1, 0)
    glVertex3f(-hw, -hh, -hd)
    glVertex3f( hw, -hh, -hd)
    glVertex3f( hw, -hh,  hd)
    glVertex3f(-hw, -hh,  hd)

    glEnd()

def draw_cylinder(radius, height, slices=16):
    """Gambar silinder berpusat di origin dengan sumbu Y."""
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    
    glPushMatrix()
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, radius, radius, height, slices, 1)
    glPopMatrix()
    
    gluDeleteQuadric(quad)

def draw_sphere(radius, slices=16, stacks=16):
    """Gambar sphere."""
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    gluSphere(quad, radius, slices, stacks)
    gluDeleteQuadric(quad)

def draw_cone(radius, height, slices=16):
    """Gambar kerucut."""
    quad = gluNewQuadric()
    gluQuadricNormals(quad, GLU_SMOOTH)
    glPushMatrix()
    glTranslatef(0, -height/2, 0)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(quad, radius, 0, height, slices, 1)
    glPopMatrix()
    gluDeleteQuadric(quad)

def set_color(r, g, b, a=1.0):
    """Set warna dengan efek metalik sederhana."""
    glColor4f(r, g, b, a)
    
    # Material properties
    ambient = [r*0.3, g*0.3, b*0.3, a]
    diffuse = [r, g, b, a]
    specular = [0.5, 0.5, 0.5, a]
    
    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
    glMaterialf(GL_FRONT, GL_SHININESS, 50.0)

# ─────────────────────────────────────────────
#  DRAW: Bagian-bagian robot dengan PROPORSI PRESISI
#  (Referensi tinggi total robot ~2.0 unit)
# ─────────────────────────────────────────────

def draw_head():
    """Kepala robot dengan desain futuristik."""
    glPushMatrix()
    
    # Kepala utama
    set_color(0.75, 0.75, 0.85)
    draw_sphere(0.38, 24, 24)
    
    # Visor
    glPushMatrix()
    glTranslatef(0.0, 0.08, 0.32)
    glScalef(1.2, 0.6, 0.3)
    set_color(0.2, 0.7, 1.0, 0.8)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    draw_sphere(0.18, 20, 16)
    glDisable(GL_BLEND)
    glPopMatrix()
    
    # Mata kiri
    glPushMatrix()
    glTranslatef(-0.13, 0.15, 0.35)
    set_color(0.0, 1.0, 1.0)
    draw_sphere(0.06, 12, 12)
    
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.02)
    set_color(0.0, 0.0, 0.0)
    draw_sphere(0.03, 8, 8)
    glPopMatrix()
    glPopMatrix()
    
    # Mata kanan
    glPushMatrix()
    glTranslatef(0.13, 0.15, 0.35)
    set_color(0.0, 1.0, 1.0)
    draw_sphere(0.06, 12, 12)
    
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.02)
    set_color(0.0, 0.0, 0.0)
    draw_sphere(0.03, 8, 8)
    glPopMatrix()
    glPopMatrix()
    
    # Antena kiri
    glPushMatrix()
    glTranslatef(-0.12, 0.4, 0.0)
    glRotatef(15, 0, 0, 1)
    set_color(0.9, 0.9, 0.2)
    draw_cylinder(0.04, 0.25, 8)
    
    glTranslatef(0.0, 0.15, 0.0)
    set_color(1.0, 0.3, 0.1)
    draw_sphere(0.06, 10, 10)
    glPopMatrix()
    
    # Antena kanan
    glPushMatrix()
    glTranslatef(0.12, 0.4, 0.0)
    glRotatef(-15, 0, 0, 1)
    set_color(0.9, 0.9, 0.2)
    draw_cylinder(0.04, 0.25, 8)
    
    glTranslatef(0.0, 0.15, 0.0)
    set_color(1.0, 0.3, 0.1)
    draw_sphere(0.06, 10, 10)
    glPopMatrix()
    
    # Mulut
    glPushMatrix()
    glTranslatef(0.0, -0.15, 0.32)
    set_color(0.3, 0.3, 0.3)
    draw_box(0.25, 0.05, 0.08)
    glPopMatrix()
    
    glPopMatrix()

def draw_torso():
    """Badan robot dengan detail armor."""
    glPushMatrix()
    
    # Badan utama
    set_color(0.25, 0.45, 0.85)
    draw_box(0.9, 1.15, 0.55)
    
    # Pelindung dada
    glPushMatrix()
    glTranslatef(0.0, 0.2, 0.28)
    set_color(0.9, 0.7, 0.1)
    draw_box(0.6, 0.45, 0.1)
    
    # Power core
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.06)
    set_color(0.0, 1.0, 0.8)
    draw_sphere(0.12, 16, 16)
    glPopMatrix()
    glPopMatrix()
    
    # Sabuk
    glPushMatrix()
    glTranslatef(0.0, -0.45, 0.0)
    set_color(0.6, 0.6, 0.7)
    draw_box(0.95, 0.12, 0.6)
    
    # Gesper
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.31)
    set_color(0.9, 0.8, 0.2)
    draw_box(0.2, 0.08, 0.05)
    glPopMatrix()
    glPopMatrix()
    
    # Bahu kiri
    glPushMatrix()
    glTranslatef(-0.55, 0.5, 0.0)
    glRotatef(10, 0, 1, 0)
    set_color(0.8, 0.2, 0.2)
    glScalef(1.1, 0.8, 1.3)
    draw_sphere(0.18, 16, 16)
    glPopMatrix()
    
    # Bahu kanan
    glPushMatrix()
    glTranslatef(0.55, 0.5, 0.0)
    glRotatef(-10, 0, 1, 0)
    set_color(0.8, 0.2, 0.2)
    glScalef(1.1, 0.8, 1.3)
    draw_sphere(0.18, 16, 16)
    glPopMatrix()
    
    # Leher
    glPushMatrix()
    glTranslatef(0.0, 0.65, 0.0)
    set_color(0.7, 0.7, 0.8)
    draw_cylinder(0.12, 0.18, 12)
    glPopMatrix()
    
    # Ventilasi samping kiri
    glPushMatrix()
    glTranslatef(-0.5, 0.1, 0.0)
    glRotatef(90, 0, 1, 0)
    set_color(0.4, 0.4, 0.5)
    draw_cylinder(0.08, 0.2, 8)
    glPopMatrix()
    
    # Ventilasi samping kanan
    glPushMatrix()
    glTranslatef(0.5, 0.1, 0.0)
    glRotatef(90, 0, 1, 0)
    set_color(0.4, 0.4, 0.5)
    draw_cylinder(0.08, 0.2, 8)
    glPopMatrix()
    
    glPopMatrix()

def draw_upper_arm():
    """Lengan atas dengan proporsi presisi."""
    glPushMatrix()
    
    # Lengan utama
    set_color(0.25, 0.45, 0.85)
    draw_box(0.28, 0.48, 0.3)
    
    # Armor plate
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.16)
    set_color(0.9, 0.7, 0.1)
    draw_box(0.22, 0.32, 0.06)
    glPopMatrix()
    
    # Sendi bahu
    glPushMatrix()
    glTranslatef(0.0, 0.2, 0.0)
    set_color(0.7, 0.7, 0.8)
    draw_sphere(0.15, 12, 12)
    glPopMatrix()
    
    glPopMatrix()

def draw_forearm():
    """Lengan bawah dengan proporsi presisi."""
    glPushMatrix()
    
    # Lengan bawah utama
    set_color(0.25, 0.45, 0.85)
    draw_box(0.25, 0.42, 0.26)
    
    # Armor plate
    glPushMatrix()
    glTranslatef(0.0, -0.05, 0.14)
    set_color(0.9, 0.7, 0.1)
    draw_box(0.19, 0.26, 0.06)
    glPopMatrix()
    
    # Sendi siku
    glPushMatrix()
    glTranslatef(0.0, 0.18, 0.0)
    set_color(0.7, 0.7, 0.8)
    draw_sphere(0.13, 12, 12)
    glPopMatrix()
    
    glPopMatrix()

def draw_hand():
    """Tangan robot dengan jari-jari sederhana."""
    glPushMatrix()
    
    # Pergelangan
    set_color(0.7, 0.7, 0.8)
    draw_box(0.26, 0.12, 0.18)
    
    # Telapak tangan
    glPushMatrix()
    glTranslatef(0.0, -0.1, 0.0)
    set_color(0.75, 0.75, 0.8)
    draw_box(0.3, 0.18, 0.22)
    
    # Jari-jari (sederhana)
    for x_offset in [-0.1, 0.1, -0.03, 0.03]:
        glPushMatrix()
        glTranslatef(x_offset, 0.08, 0.12)
        set_color(0.7, 0.7, 0.75)
        draw_box(0.05, 0.12, 0.05)
        glPopMatrix()
    
    # Ibu jari
    glPushMatrix()
    glTranslatef(-0.12, -0.02, 0.08)
    glRotatef(20, 0, 0, 1)
    set_color(0.7, 0.7, 0.75)
    draw_box(0.06, 0.1, 0.06)
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

def draw_upper_leg():
    """Paha dengan proporsi presisi."""
    glPushMatrix()
    
    # Paha utama
    set_color(0.25, 0.45, 0.85)
    draw_box(0.32, 0.6, 0.32)
    
    # Armor
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.17)
    set_color(0.9, 0.7, 0.1)
    draw_box(0.26, 0.4, 0.07)
    glPopMatrix()
    
    # Sendi pinggul
    glPushMatrix()
    glTranslatef(0.0, 0.25, 0.0)
    set_color(0.7, 0.7, 0.8)
    draw_sphere(0.17, 12, 12)
    glPopMatrix()
    
    glPopMatrix()

def draw_lower_leg():
    """Betis dengan proporsi presisi."""
    glPushMatrix()
    
    # Betis utama
    set_color(0.25, 0.45, 0.85)
    draw_box(0.28, 0.55, 0.28)
    
    # Armor
    glPushMatrix()
    glTranslatef(0.0, -0.05, 0.15)
    set_color(0.9, 0.7, 0.1)
    draw_box(0.22, 0.32, 0.07)
    glPopMatrix()
    
    # Sendi lutut
    glPushMatrix()
    glTranslatef(0.0, 0.2, 0.1)
    set_color(0.7, 0.7, 0.8)
    draw_sphere(0.15, 12, 12)
    glPopMatrix()
    
    glPopMatrix()

def draw_foot():
    """Kaki dengan proporsi presisi."""
    glPushMatrix()
    
    # Sepatu utama
    set_color(0.2, 0.2, 0.25)
    draw_box(0.34, 0.16, 0.45)
    
    # Sol
    glPushMatrix()
    glTranslatef(0.0, -0.1, 0.0)
    set_color(0.4, 0.4, 0.4)
    draw_box(0.38, 0.06, 0.5)
    glPopMatrix()
    
    # Detail depan
    glPushMatrix()
    glTranslatef(0.0, 0.02, 0.23)
    set_color(0.8, 0.8, 0.1)
    draw_box(0.2, 0.08, 0.08)
    glPopMatrix()
    
    # Detail tumit
    glPushMatrix()
    glTranslatef(0.0, 0.02, -0.2)
    set_color(0.6, 0.6, 0.6)
    draw_box(0.28, 0.1, 0.1)
    glPopMatrix()
    
    glPopMatrix()

# ─────────────────────────────────────────────
#  DRAW: Lengan dengan hierarki yang benar
# ─────────────────────────────────────────────

def draw_left_arm():
    glPushMatrix()
    
    # Posisi bahu kiri
    glTranslatef(-0.55, 0.45, 0.0)
    
    # Rotasi bahu
    glRotatef(state["left_arm"], 1, 0, 0)
    
    # Lengan atas
    glTranslatef(0.0, -0.15, 0.0)
    draw_upper_arm()

    # Lengan bawah
    glPushMatrix()
    glTranslatef(0.0, -0.3, 0.0)
    glRotatef(state["left_forearm"], 1, 0, 0)
    glTranslatef(0.0, -0.15, 0.0)
    draw_forearm()
    
    # Tangan
    glPushMatrix()
    glTranslatef(0.0, -0.25, 0.0)
    draw_hand()
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

def draw_right_arm():
    glPushMatrix()
    
    # Posisi bahu kanan
    glTranslatef(0.55, 0.45, 0.0)
    
    # Rotasi bahu
    glRotatef(state["right_arm"], 1, 0, 0)
    
    # Lengan atas
    glTranslatef(0.0, -0.15, 0.0)
    draw_upper_arm()

    # Lengan bawah
    glPushMatrix()
    glTranslatef(0.0, -0.3, 0.0)
    glRotatef(state["right_forearm"], 1, 0, 0)
    glTranslatef(0.0, -0.15, 0.0)
    draw_forearm()
    
    # Tangan
    glPushMatrix()
    glTranslatef(0.0, -0.25, 0.0)
    draw_hand()
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

# ─────────────────────────────────────────────
#  DRAW: Kaki dengan hierarki yang benar
# ─────────────────────────────────────────────

def draw_left_leg():
    glPushMatrix()
    
    # Posisi pinggul kiri
    glTranslatef(-0.25, -0.65, 0.0)
    
    # Rotasi pinggul
    glRotatef(state["left_leg"], 1, 0, 0)
    
    # Paha
    glTranslatef(0.0, -0.2, 0.0)
    draw_upper_leg()

    # Betis
    glPushMatrix()
    glTranslatef(0.0, -0.35, 0.0)
    glTranslatef(0.0, -0.2, 0.0)
    draw_lower_leg()
    
    # Kaki
    glPushMatrix()
    glTranslatef(0.0, -0.32, 0.1)
    draw_foot()
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

def draw_right_leg():
    glPushMatrix()
    
    # Posisi pinggul kanan
    glTranslatef(0.25, -0.65, 0.0)
    
    # Rotasi pinggul
    glRotatef(state["right_leg"], 1, 0, 0)
    
    # Paha
    glTranslatef(0.0, -0.2, 0.0)
    draw_upper_leg()

    # Betis
    glPushMatrix()
    glTranslatef(0.0, -0.35, 0.0)
    glTranslatef(0.0, -0.2, 0.0)
    draw_lower_leg()
    
    # Kaki
    glPushMatrix()
    glTranslatef(0.0, -0.32, 0.1)
    draw_foot()
    glPopMatrix()
    
    glPopMatrix()
    glPopMatrix()

# ─────────────────────────────────────────────
#  DRAW: Seluruh Robot
# ─────────────────────────────────────────────

def draw_robot():
    glPushMatrix()
    
    # Rotasi seluruh robot
    glRotatef(state["robot_rotate"], 0, 1, 0)

    # Kepala
    glPushMatrix()
    glTranslatef(0.0, 0.9, 0.0)
    glRotatef(state["head_nod"], 1, 0, 0)
    draw_head()
    glPopMatrix()

    # Badan
    glPushMatrix()
    glTranslatef(0.0, 0.0, 0.0)
    draw_torso()
    
    # Lengan
    draw_left_arm()
    draw_right_arm()
    
    glPopMatrix()

    # Kaki
    draw_left_leg()
    draw_right_leg()

    glPopMatrix()

# ─────────────────────────────────────────────
#  DRAW: Lantai dan Environment (DIPERBAIKI)
# ─────────────────────────────────────────────

def draw_floor():
    glPushMatrix()
    glTranslatef(0.0, -1.8, 0.0)
    
    # Lantai utama
    set_color(0.15, 0.15, 0.25)
    draw_box(10.0, 0.1, 10.0)
    
    # Grid - DIPERBAIKI: Gunakan glBegin/End terpisah untuk setiap segmen
    glDisable(GL_LIGHTING)
    glLineWidth(1.5)
    
    # Grid horizontal dan vertical
    glColor3f(0.3, 0.6, 1.0)
    for i in range(-5, 6):
        glBegin(GL_LINES)
        # Garis searah X
        glVertex3f(i * 1.0, 0.06, -5.0)
        glVertex3f(i * 1.0, 0.06, 5.0)
        glEnd()
        
        glBegin(GL_LINES)
        # Garis searah Z
        glVertex3f(-5.0, 0.06, i * 1.0)
        glVertex3f(5.0, 0.06, i * 1.0)
        glEnd()
    
    # Garis tengah putih
    glLineWidth(3.0)
    glColor3f(1.0, 1.0, 1.0)
    
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.07, -5.0)
    glVertex3f(0.0, 0.07, 5.0)
    glEnd()
    
    glBegin(GL_LINES)
    glVertex3f(-5.0, 0.07, 0.0)
    glVertex3f(5.0, 0.07, 0.0)
    glEnd()
    
    # Lingkaran di sekitar robot
    glLineWidth(1.5)
    glColor3f(0.5, 0.8, 1.0)
    glBegin(GL_LINE_LOOP)
    for i in range(36):
        angle = 2.0 * math.pi * i / 36
        glVertex3f(2.0 * math.cos(angle), 0.07, 2.0 * math.sin(angle))
    glEnd()
    
    glEnable(GL_LIGHTING)
    glPopMatrix()

def draw_ambient_lights():
    """Tambahkan lampu-lampu dekoratif."""
    glDisable(GL_LIGHTING)
    
    # Titik-titik cahaya
    glPointSize(8.0)
    
    glBegin(GL_POINTS)
    glColor3f(1.0, 0.3, 0.3)
    glVertex3f(1.5, 0.2, 1.5)
    
    glColor3f(0.3, 1.0, 0.3)
    glVertex3f(-1.5, 0.2, 1.5)
    
    glColor3f(0.3, 0.3, 1.0)
    glVertex3f(1.5, 0.2, -1.5)
    
    glColor3f(1.0, 1.0, 0.3)
    glVertex3f(-1.5, 0.2, -1.5)
    glEnd()
    
    glEnable(GL_LIGHTING)

# ─────────────────────────────────────────────
#  DRAW: HUD dengan informasi
# ─────────────────────────────────────────────

def draw_text(x, y, text, color=(1, 1, 1)):
    """Draw text pada layar."""
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    w = glutGet(GLUT_WINDOW_WIDTH)
    h = glutGet(GLUT_WINDOW_HEIGHT)
    gluOrtho2D(0, w, 0, h)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    glColor3f(*color)
    glRasterPos2f(x, y)
    
    for ch in text:
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(ch))
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

def draw_hud():
    """Tampilkan informasi kontrol di layar."""
    h = glutGet(GLUT_WINDOW_HEIGHT)
    
    # Judul
    draw_text(20, h - 30, "HIERARCHICAL MODELING - ROBOT PRESISI", (1.0, 0.9, 0.2))
    draw_text(20, h - 50, "Grafika Komputer IF216004 - UIN SGD Bandung", (0.7, 0.9, 1.0))
    
    # Kontrol robot
    controls = [
        ("ROBOT ROTATION", f"{state['robot_rotate']:6.0f}°", "[Q/A]"),
        ("LEFT ARM", f"{state['left_arm']:6.0f}°", "[W/S]"),
        ("RIGHT ARM", f"{state['right_arm']:6.0f}°", "[E/D]"),
        ("LEFT FOREARM", f"{state['left_forearm']:6.0f}°", "[R/F]"),
        ("RIGHT FOREARM", f"{state['right_forearm']:6.0f}°", "[T/G]"),
        ("LEFT LEG", f"{state['left_leg']:6.0f}°", "[Y/H]"),
        ("RIGHT LEG", f"{state['right_leg']:6.0f}°", "[U/J]"),
        ("HEAD NOD", f"{state['head_nod']:6.0f}°", "[I/K]"),
    ]
    
    y_pos = h - 90
    for name, value, key in controls:
        draw_text(30, y_pos, f"{name:15s} : {value:>6s}  {key}", (0.3, 1.0, 0.3))
        y_pos -= 22
    
    # Informasi tambahan
    draw_text(30, y_pos - 10, "ESC - Keluar", (1.0, 0.5, 0.5))
    
    # Status proporsi
    draw_text(400, h - 90, "PROPORSI PRESISI (Tinggi ~2.0 unit)", (0.2, 1.0, 0.2))
    draw_text(400, h - 115, "REFERENSI TUBUH MANUSIA", (0.2, 1.0, 0.2))

# ─────────────────────────────────────────────
#  OPENGL CALLBACKS
# ─────────────────────────────────────────────

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # Kamera
    gluLookAt(
        2.5, 1.5, 5.5,
        0.0, 0.2, 0.0,
        0.0, 1.0, 0.0
    )

    draw_floor()
    draw_ambient_lights()
    draw_robot()
    draw_hud()

    glutSwapBuffers()

def reshape(w, h):
    if h == 0:
        h = 1
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, w / h, 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    key = key.decode('utf-8').lower() if isinstance(key, bytes) else key.lower()

    controls = {
        'q': ('robot_rotate',  +STEP),
        'a': ('robot_rotate',  -STEP),
        'w': ('left_arm',      +STEP),
        's': ('left_arm',      -STEP),
        'e': ('right_arm',     +STEP),
        'd': ('right_arm',     -STEP),
        'r': ('left_forearm',  +STEP),
        'f': ('left_forearm',  -STEP),
        't': ('right_forearm', +STEP),
        'g': ('right_forearm', -STEP),
        'y': ('left_leg',      +STEP),
        'h': ('left_leg',      -STEP),
        'u': ('right_leg',     +STEP),
        'j': ('right_leg',     -STEP),
        'i': ('head_nod',      +STEP),
        'k': ('head_nod',      -STEP),
    }

    if key == '\x1b':   # ESC
        sys.exit(0)

    if key in controls:
        attr, delta = controls[key]
        state[attr] += delta
        
        # Batasi sudut
        if attr in ['left_arm', 'right_arm']:
            state[attr] = max(-90, min(90, state[attr]))
        elif attr in ['left_forearm', 'right_forearm']:
            state[attr] = max(-30, min(120, state[attr]))
        elif attr in ['left_leg', 'right_leg']:
            state[attr] = max(-45, min(45, state[attr]))
        elif attr == 'head_nod':
            state[attr] = max(-40, min(40, state[attr]))

    glutPostRedisplay()

def init_lighting():
    """Setup pencahayaan."""
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)
    
    # Ambient light
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
    
    # Lampu 1 (utama)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [3.0, 5.0, 5.0, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [1.0, 1.0, 1.0, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
    
    # Lampu 2 (samping)
    glEnable(GL_LIGHT1)
    glLightfv(GL_LIGHT1, GL_POSITION, [-3.0, 2.0, 3.0, 1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE,  [0.3, 0.5, 1.0, 1.0])
    
    glClearColor(0.03, 0.03, 0.08, 1.0)

# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1200, 800)
    glutInitWindowPosition(50, 50)
    glutCreateWindow(b"Hierarchical Modeling - Robot Presisi | Grafika Komputer IF216004")

    init_lighting()

    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)

    print("=" * 80)
    print("  HIERARCHICAL MODELING — ROBOT PRESISI (REFERENSI TUBUH MANUSIA)")
    print("  Grafika Komputer IF216004 | UIN Sunan Gunung Djati Bandung")
    print("=" * 80)
    print("  PROPORSI PRESISI:")
    print("  • Tinggi total: ~2.0 unit (kepala 0.38, badan 1.15, kaki 1.3)")
    print("  • Lengan atas/bawah diperpendek untuk proporsi realistis")
    print("=" * 80)
    print("  KONTROL KEYBOARD:")
    print("  Q/A → Putar robot   | W/S → Lengan kiri   | E/D → Lengan kanan")
    print("  R/F → Siku kiri      | T/G → Siku kanan   | Y/H → Kaki kiri")
    print("  U/J → Kaki kanan     | I/K → Angguk kepala | ESC → Keluar")
    print("=" * 80)

    glutMainLoop()

if __name__ == "__main__":
    main()