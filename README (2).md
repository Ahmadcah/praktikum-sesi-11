# Pendaftaran Kegiatan Mahasiswa

Praktikum Sesi 11 — **Advanced Widgets dan Event Handling** (Python Tkinter)

Aplikasi desktop sederhana untuk mendaftar kegiatan kemahasiswaan. Pengguna mengisi data diri, memilih kegiatan, menuliskan alasan, lalu melihat ringkasan pendaftaran langsung di dalam aplikasi.

## Tujuan

Membangun aplikasi GUI dengan Python Tkinter yang memanfaatkan berbagai widget, event handling, validasi input, menu, dan dialog.

## Fitur

### Tugas utama

| Kebutuhan | Implementasi |
|---|---|
| Input nama | `Entry` |
| Pilih program studi | `Combobox` (read-only, 10 pilihan) |
| Pilih jenis kelamin | `Radiobutton` (Laki-laki / Perempuan) |
| Pilih kegiatan | `Checkbutton` (6 kegiatan, boleh lebih dari satu) |
| Alasan mengikuti kegiatan | `Text` dengan scrollbar dan penghitung karakter |
| Tombol **Submit** dan **Reset** | `ttk.Button`; Reset mengosongkan formulir, Listbox, dan ringkasan |
| Ringkasan pendaftaran | Area informasi berupa `Text` read-only: nomor pendaftaran, waktu, nama, prodi, jenis kelamin, kegiatan, alasan |
| Notifikasi | `messagebox`: `showwarning` (validasi), `showinfo` (berhasil), `askyesno` (konfirmasi keluar) |
| Menu **File** | Reset Formulir dan **Keluar** |
| Jendela **About** | `Toplevel` bersifat modal, tidak bisa terbuka ganda, ditutup dengan tombol atau `Esc` |

### Tugas pengembangan

| Kebutuhan | Implementasi |
|---|---|
| Listbox pilihan kegiatan | `Listbox` diperbarui langsung saat Checkbutton dicentang; klik dua kali atau `Delete` membatalkan pilihan |
| Validasi nama tidak boleh kosong | Pesan peringatan, kolom nama ditandai merah, fokus pindah ke kolom tersebut |
| Menu **Bantuan** | Item *Tentang Aplikasi* membuka jendela About |
| Event keyboard | `Enter` menjalankan Submit (di kolom alasan, `Enter` tetap membuat baris baru) |
| Antarmuka rapi | `Frame`/`LabelFrame` dengan `pack` untuk kerangka halaman dan `grid` untuk isi formulir |

### Tambahan

- Validasi lengkap: nama hanya huruf (minimal 3), program studi dan jenis kelamin harus dipilih, minimal 1 kegiatan, alasan minimal 10 karakter. Semua kesalahan ditampilkan sekaligus dalam satu dialog.
- Status bar yang menampilkan aksi terakhir dan jumlah pendaftar.
- Kode berbentuk satu kelas (`AplikasiPendaftaran`) dengan konfigurasi di bagian atas file, sehingga daftar prodi dan kegiatan mudah diubah.

## Pintasan keyboard

| Tombol | Aksi |
|---|---|
| `Enter` | Submit |
| `Ctrl+R` | Reset formulir |
| `Ctrl+Q` | Keluar |
| `F1` | Buka jendela About |
| `Tab` / `Shift+Tab` | Pindah antar kolom (termasuk dari kolom alasan) |

## Cara menjalankan

Kebutuhan: **Python 3.8 atau lebih baru**. Tidak ada library tambahan, karena Tkinter sudah termasuk dalam instalasi Python.

```bash
git clone https://github.com/<username>/praktikum-tkinter-sesi-11.git
cd praktikum-tkinter-sesi-11
python main.py
```

Catatan per sistem operasi:

- **Windows / macOS**: Tkinter sudah ikut terpasang bersama Python dari python.org.
- **Linux (Debian/Ubuntu)**: pasang dulu dengan `sudo apt install python3-tk`.
- Bila perintah `python` tidak dikenali, gunakan `python3 main.py`.

## Screenshot

| Formulir terisi, Listbox menampilkan kegiatan dipilih | Peringatan validasi (formulir kosong) |
|---|---|
| ![Formulir terisi](screenshots/02-formulir-terisi.png) | ![Validasi gagal](screenshots/01-validasi-gagal.png) |

| Notifikasi pendaftaran berhasil | Ringkasan pendaftaran |
|---|---|
| ![Notifikasi berhasil](screenshots/03-notifikasi-berhasil.png) | ![Ringkasan pendaftaran](screenshots/04-ringkasan-pendaftaran.png) |

| Jendela About (Toplevel) |
|---|
| ![Jendela About](screenshots/05-jendela-about.png) |

## Struktur repository

```
praktikum-tkinter-sesi-11/
├── main.py            # program utama
├── README.md          # dokumentasi
└── screenshots/       # tangkapan layar aplikasi yang sedang berjalan
```

## Pengembang

Ahmad Cahya Fasshluhi (2595114018)
