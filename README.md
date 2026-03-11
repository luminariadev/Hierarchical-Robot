# 🤖 Hierarchical Modeling — Robot OpenGL + Matrix Stack

> **Tugas Kelompok — Grafika Komputer (IF216004)**
> Implementasi *Hierarchical Modeling* pada OpenGL menggunakan **Matrix Stack** untuk pemodelan objek kompleks berbentuk Robot Sederhana.

---

## 👥 Kelompok 6

| Nama | NIM |
|------|-----|
| Ratu Qurratul Aini | 1237050084 |
| Rizkia Nuari Fujiana | 1237050063 |
| Rizki Maulana | 1237050088 |
| Alya Khansa D | 1247050105 |

> Jurusan Informatika · Fakultas Sains dan Teknologi · UIN Sunan Gunung Djati Bandung · 2022


## 📋 Deskripsi Tugas

Mengimplementasikan **Hierarchical Modeling** pada OpenGL menggunakan **Matrix Stack** untuk objek kompleks bebas. Program menampilkan robot 3D yang setiap bagian tubuhnya dapat digerakkan secara independen menggunakan keyboard, dengan transformasi yang dikelola melalui `glPushMatrix()` dan `glPopMatrix()`.

---

## 📁 Struktur Repository

```
├── hierarchical_robot.py     # Program utama OpenGL
├── keyboard_guide.png        # Panduan tombol kontrol
└── README.md
```

---

## 🌳 Scene Graph — Struktur Hierarki

Objek robot diorganisasikan dalam hierarki **parent–child** berikut:

```
ROBOT  (root)
├── HEAD         → anggukan kepala
└── TORSO
    ├── LEFT_ARM
    │   └── LEFT_FOREARM  → tangan kiri
    ├── RIGHT_ARM
    │   └── RIGHT_FOREARM → tangan kanan
    ├── LEFT_LEG
    │   └── LEFT_LOWER_LEG  → sepatu kiri
    └── RIGHT_LEG
        └── RIGHT_LOWER_LEG → sepatu kanan
```

Setiap node child **mewarisi transformasi dari parent-nya**. Misalnya, saat badan (TORSO) diputar, seluruh lengan dan kaki ikut bergerak mengikuti badan.

---

## 🔑 Konsep Matrix Stack

Program menggunakan pasangan `glPushMatrix()` / `glPopMatrix()` pada setiap sendi:

```python
glPushMatrix()                          # Simpan state matrix parent
    glTranslatef(x_sendi, y_sendi, 0)   # Pindah ke titik sendi (pivot)
    glRotatef(sudut, 1, 0, 0)           # Rotasi di titik sendi
    glTranslatef(0, -panjang/2, 0)      # Pindah ke tengah segmen
    draw_upper_arm()                     # Gambar segmen

    glPushMatrix()                       # Child: forearm mewarisi posisi siku
        glTranslatef(0, -panjang, 0)     # Turun ke ujung lengan atas (siku)
        glRotatef(sudut_siku, 1, 0, 0)  # Rotasi di siku
        draw_forearm()                   # Gambar forearm
    glPopMatrix()                        # Kembali ke state siku

glPopMatrix()                            # Kembali ke state parent (bahu)
```

---

## 🎮 Kontrol Keyboard

![Keyboard Control Guide](keyboard_guide.png)

| Tombol | Bagian Tubuh | Gerakan |
|--------|-------------|---------|
| `Q` / `A` | Seluruh Robot | Putar kiri / kanan |
| `W` / `S` | Lengan Kiri Atas | Naik / turun |
| `E` / `D` | Lengan Kanan Atas | Naik / turun |
| `R` / `F` | Siku Kiri | Tekuk / lurus |
| `T` / `G` | Siku Kanan | Tekuk / lurus |
| `Y` / `H` | Kaki Kiri | Maju / mundur |
| `U` / `J` | Kaki Kanan | Maju / mundur |
| `I` / `K` | Kepala | Angguk atas / bawah |
| `ESC` | — | Keluar program |

---

## ⚙️ Requirements

```
Python  >= 3.7
PyOpenGL
PyOpenGL_accelerate
```

Install dependencies:

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

---

## 🚀 Cara Menjalankan

1. **Clone repository ini:**

```bash
git clone https://github.com/username/hierarchical-robot-opengl.git
cd hierarchical-robot-opengl
```

2. **Install dependencies:**

```bash
pip install PyOpenGL PyOpenGL_accelerate
```

3. **Jalankan program:**

```bash
python hierarchical_robot.py
```

---

## 💡 Penjelasan Teknis

### Mengapa Matrix Stack?

Tanpa matrix stack, transformasi pada parent akan terus terakumulasi dan mempengaruhi semua objek berikutnya secara global. Dengan `glPushMatrix()` dan `glPopMatrix()`, setiap node dapat menerapkan transformasinya secara **lokal** tanpa mengganggu node lain di hierarki.

### Alur Scene Graph Traversal (Depth-First)

```
1. PUSH ROBOT    → rotasi seluruh tubuh
   2. PUSH HEAD  → anggukan kepala
   2. POP HEAD
   2. PUSH TORSO → gambar badan
      3. PUSH LEFT_ARM  → rotasi bahu kiri
         4. PUSH LEFT_FOREARM → rotasi siku kiri
         4. POP
      3. POP LEFT_ARM
      3. PUSH RIGHT_ARM → rotasi bahu kanan
         4. PUSH RIGHT_FOREARM → rotasi siku kanan
         4. POP
      3. POP RIGHT_ARM
   2. POP TORSO
   2. PUSH LEFT_LEG  → rotasi pinggul kiri
      3. PUSH LEFT_LOWER_LEG
      3. POP
   2. POP LEFT_LEG
   2. PUSH RIGHT_LEG → rotasi pinggul kanan
      3. PUSH RIGHT_LOWER_LEG
      3. POP
   2. POP RIGHT_LEG
1. POP ROBOT
```

---

## 📚 Referensi

1. Donald Hearn, M. Pauline Baker. *Computer Graphics C Version*. Prentice-Hall. 1997 *(Pustaka Utama)*
2. Max K. Agoston. *Computer Graphics and Geometric Modeling: Implementation and Algorithms*. Springer *(Pustaka Pendukung)*
3. Edhi Nugroho. *Grafika Komputer (Teori dan Praktek) menggunakan Delphi dan OpenGL* *(Pustaka Pendukung)*
4. Achmad Basuki & Nana Ramadijanti. 2016. *Grafika Komputer – Teori Dan Implementasi*. Penerbit ANDI: Yogyakarta *(Pustaka Pendukung)*
5. Pulung Nurtantio Andono & T. Sutoyo. *Konsep Grafika Komputer*. Penerbit ANDI: Yogyakarta *(Pustaka Pendukung)*
6. [www.opengl.org](https://www.opengl.org) *(Pustaka Utama)*
7. MIT OCW 6.837 Computer Graphics — [Lecture Notes Lec04](https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-837-computer-graphics-fall-2012/lecture-notes/MIT6_837F12_Lec04.pdf)
