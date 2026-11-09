"""
Pendaftaran Kegiatan Mahasiswa
==============================
Praktikum Sesi 11 - Advanced Widgets dan Event Handling (Python Tkinter)

Aplikasi GUI untuk mendaftar kegiatan kemahasiswaan. Menggunakan widget
Entry, Combobox, Radiobutton, Checkbutton, Text, Listbox, Menu, Messagebox,
dan Toplevel, lengkap dengan validasi input dan event keyboard.

Cara menjalankan:
    python main.py
"""

import tkinter as tk
from datetime import datetime
from tkinter import font as tkfont
from tkinter import messagebox, ttk

# ---------------------------------------------------------------------------
# Konfigurasi aplikasi (ubah di sini, tidak perlu menyentuh logika program)
# ---------------------------------------------------------------------------
APP_NAMA = "Pendaftaran Kegiatan Mahasiswa"
APP_VERSI = "1.0"
APP_SUBJUDUL = "Praktikum Sesi 11  ·  Advanced Widgets dan Event Handling"
PENGEMBANG = "Ahmad Cahya Fasshluhi"
NIM = "2595114018"

PILIH_PRODI = "-- Pilih Program Studi --"
PROGRAM_STUDI = [
    "Teknik Informatika",
    "Sistem Informasi",
    "Teknik Industri",
    "Teknik Sipil",
    "Manajemen",
    "Akuntansi",
    "Agroteknologi",
    "Pendidikan Bahasa Inggris",
    "Hukum",
    "Psikologi",
]

JENIS_KELAMIN = ("Laki-laki", "Perempuan")

KEGIATAN = [
    "Seminar Teknologi",
    "Lomba Coding",
    "Workshop Python",
    "Bakti Sosial",
    "Pelatihan Leadership",
    "Turnamen E-Sport",
]

MIN_NAMA = 3        # jumlah huruf minimal pada nama
MIN_ALASAN = 10     # jumlah karakter minimal pada alasan

BULAN = (
    "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
    "Agustus", "September", "Oktober", "November", "Desember",
)

# Palet warna: dipakai konsisten di seluruh antarmuka
WARNA = {
    "latar": "#EEF2F7",
    "kartu": "#FFFFFF",
    "garis": "#CBD5E1",
    "utama": "#1E3A8A",
    "aksen": "#2563EB",
    "aksen_gelap": "#1D4ED8",
    "aksen_muda": "#DBEAFE",
    "teks": "#1F2937",
    "redup": "#64748B",
    "sukses": "#15803D",
    "bahaya": "#DC2626",
    "bahaya_muda": "#FEF2F2",
    "kolom_info": "#F8FAFC",
}


class AplikasiPendaftaran:
    """Jendela utama aplikasi Pendaftaran Kegiatan Mahasiswa."""

    def __init__(self, root):
        self.root = root
        self.jendela_about = None      # referensi jendela About (agar tidak dobel)
        self.daftar_pendaftar = []     # semua pendaftaran selama aplikasi berjalan
        self._kegiatan_tampil = []     # isi Listbox saat ini (nama kegiatan)

        self._siapkan_jendela()
        self._siapkan_gaya()
        self._buat_variabel()
        self._buat_menu()
        self._buat_tata_letak()
        self._pasang_event()

        self.reset_form(senyap=True)
        self._atur_ukuran_jendela()
        self.ent_nama.focus_set()

    # ------------------------------------------------------------------
    # Persiapan jendela, gaya, dan variabel
    # ------------------------------------------------------------------
    def _siapkan_jendela(self):
        self.root.title(APP_NAMA)
        self.root.configure(bg=WARNA["latar"])
        self.root.protocol("WM_DELETE_WINDOW", self.keluar)

    def _pilih_font(self):
        """Pilih font terbaik yang tersedia di komputer pengguna."""
        tersedia = set(tkfont.families(self.root))
        for nama in ("Segoe UI", "Inter", "Helvetica Neue", "Noto Sans",
                     "DejaVu Sans", "Arial"):
            if nama in tersedia:
                return nama
        return "Helvetica"

    def _siapkan_gaya(self):
        self.font = self._pilih_font()
        f = self.font
        w = WARNA

        gaya = ttk.Style(self.root)
        gaya.theme_use("clam")

        gaya.configure(".", font=(f, 10), background=w["latar"], foreground=w["teks"])
        gaya.configure("TFrame", background=w["latar"])
        gaya.configure("Kartu.TFrame", background=w["kartu"])
        gaya.configure("Kartu.TLabel", background=w["kartu"], foreground=w["teks"])
        gaya.configure("Redup.Kartu.TLabel", foreground=w["redup"], font=(f, 9))
        gaya.configure("Judul.Kartu.TLabel", font=(f, 10, "bold"))

        gaya.configure("Kartu.TLabelframe", background=w["kartu"],
                       bordercolor=w["garis"], lightcolor=w["garis"], darkcolor=w["garis"])
        gaya.configure("Kartu.TLabelframe.Label", background=w["kartu"],
                       foreground=w["utama"], font=(f, 11, "bold"))

        for nama in ("Kartu.TRadiobutton", "Kartu.TCheckbutton"):
            gaya.configure(nama, background=w["kartu"], focuscolor=w["kartu"])
            gaya.map(nama, background=[("active", w["kartu"])],
                     indicatorcolor=[("selected", w["aksen"]), ("pressed", w["aksen"])])

        gaya.configure("TEntry", padding=6, fieldbackground="white",
                       bordercolor=w["garis"], lightcolor=w["garis"], darkcolor=w["garis"])
        gaya.map("TEntry", bordercolor=[("focus", w["aksen"])],
                 lightcolor=[("focus", w["aksen"])], darkcolor=[("focus", w["aksen"])])
        gaya.configure("Salah.TEntry", fieldbackground=w["bahaya_muda"],
                       bordercolor=w["bahaya"], lightcolor=w["bahaya"], darkcolor=w["bahaya"])
        gaya.map("Salah.TEntry", bordercolor=[("focus", w["bahaya"])],
                 lightcolor=[("focus", w["bahaya"])], darkcolor=[("focus", w["bahaya"])])

        gaya.configure("TCombobox", padding=6, arrowsize=14, bordercolor=w["garis"],
                       lightcolor=w["garis"], darkcolor=w["garis"])
        gaya.map("TCombobox", fieldbackground=[("readonly", "white")],
                 selectbackground=[("readonly", "white")],
                 selectforeground=[("readonly", w["teks"])],
                 bordercolor=[("focus", w["aksen"])])
        self.root.option_add("*TCombobox*Listbox.font", (f, 10))

        gaya.configure("Vertical.TScrollbar", arrowsize=13, background="#C5CEDB",
                       troughcolor="#E9EEF5", bordercolor="#E9EEF5",
                       lightcolor="#C5CEDB", darkcolor="#C5CEDB", arrowcolor=w["redup"])
        gaya.map("Vertical.TScrollbar", background=[("active", "#A9B6C8")],
                 lightcolor=[("active", "#A9B6C8")], darkcolor=[("active", "#A9B6C8")])

        gaya.configure("Utama.TButton", background=w["aksen"], foreground="white",
                       bordercolor=w["aksen"], lightcolor=w["aksen"], darkcolor=w["aksen"],
                       focuscolor=w["aksen"], padding=(24, 8), font=(f, 10, "bold"))
        gaya.map("Utama.TButton",
                 background=[("pressed", w["utama"]), ("active", w["aksen_gelap"])],
                 bordercolor=[("pressed", w["utama"]), ("active", w["aksen_gelap"])],
                 lightcolor=[("pressed", w["utama"]), ("active", w["aksen_gelap"])],
                 darkcolor=[("pressed", w["utama"]), ("active", w["aksen_gelap"])])
        gaya.configure("Sekunder.TButton", background="#E2E8F0", foreground=w["teks"],
                       bordercolor="#E2E8F0", lightcolor="#E2E8F0", darkcolor="#E2E8F0",
                       focuscolor="#E2E8F0", padding=(24, 8), font=(f, 10))
        gaya.map("Sekunder.TButton",
                 background=[("pressed", "#CBD5E1"), ("active", "#D7DFEA")],
                 bordercolor=[("pressed", "#CBD5E1"), ("active", "#D7DFEA")],
                 lightcolor=[("pressed", "#CBD5E1"), ("active", "#D7DFEA")],
                 darkcolor=[("pressed", "#CBD5E1"), ("active", "#D7DFEA")])

    def _buat_variabel(self):
        """Variabel Tkinter yang terhubung ke widget formulir."""
        self.var_nama = tk.StringVar()
        self.var_prodi = tk.StringVar(value=PILIH_PRODI)
        self.var_jk = tk.StringVar()
        self.var_kegiatan = {k: tk.BooleanVar(value=False) for k in KEGIATAN}
        self.var_counter = tk.StringVar()
        self.var_status = tk.StringVar()
        self.var_total = tk.StringVar()

    # ------------------------------------------------------------------
    # Menu
    # ------------------------------------------------------------------
    def _buat_menu(self):
        bar = tk.Menu(self.root)

        self.menu_file = tk.Menu(bar, tearoff=False)
        self.menu_file.add_command(label="Reset Formulir", accelerator="Ctrl+R",
                                   command=self.reset_form)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Keluar", accelerator="Ctrl+Q",
                                   command=self.keluar)
        bar.add_cascade(label="File", menu=self.menu_file)

        self.menu_bantuan = tk.Menu(bar, tearoff=False)
        self.menu_bantuan.add_command(label="Tentang Aplikasi", accelerator="F1",
                                      command=self.tampilkan_about)
        bar.add_cascade(label="Bantuan", menu=self.menu_bantuan)

        self.root.configure(menu=bar)

    # ------------------------------------------------------------------
    # Tata letak: header (pack), body 2 kolom (grid), status bar (pack)
    # ------------------------------------------------------------------
    def _buat_tata_letak(self):
        w = WARNA
        f = self.font

        # Header
        header = tk.Frame(self.root, bg=w["utama"])
        header.pack(side="top", fill="x")
        tk.Label(header, text=APP_NAMA, bg=w["utama"], fg="white",
                 font=(f, 18, "bold")).pack(anchor="w", padx=24, pady=(14, 0))
        tk.Label(header, text=APP_SUBJUDUL, bg=w["utama"], fg="#BFD2F8",
                 font=(f, 10)).pack(anchor="w", padx=24, pady=(2, 14))

        # Status bar (dipasang sebelum body agar selalu tampak di bawah)
        status = tk.Frame(self.root, bg="#E2E8F0")
        status.pack(side="bottom", fill="x")
        self.lbl_status = tk.Label(status, textvariable=self.var_status, bg="#E2E8F0",
                                   fg=w["redup"], font=(f, 9), anchor="w")
        self.lbl_status.pack(side="left", padx=14, pady=5)
        tk.Label(status, textvariable=self.var_total, bg="#E2E8F0", fg=w["redup"],
                 font=(f, 9)).pack(side="right", padx=14, pady=5)

        # Body: kolom kiri (formulir) dan kolom kanan (kegiatan + ringkasan)
        body = ttk.Frame(self.root, padding=(20, 16))
        body.pack(side="top", fill="both", expand=True)
        body.columnconfigure(0, weight=3, uniform="kolom")
        body.columnconfigure(1, weight=2, uniform="kolom")
        body.rowconfigure(0, weight=1)

        self._buat_formulir(body).grid(row=0, column=0, sticky="nsew", padx=(0, 16))
        self._buat_panel_kanan(body).grid(row=0, column=1, sticky="nsew")

    def _buat_formulir(self, induk):
        f = self.font
        kartu = ttk.Labelframe(induk, text=" Formulir Pendaftaran ",
                               style="Kartu.TLabelframe", padding=(18, 10, 18, 14))
        kartu.columnconfigure(1, weight=1)

        def label(teks, baris, sticky="w"):
            ttk.Label(kartu, text=teks, style="Kartu.TLabel").grid(
                row=baris, column=0, sticky=sticky, padx=(0, 14), pady=8)

        # 1. Nama -> Entry
        label("Nama Lengkap *", 0)
        self.ent_nama = ttk.Entry(kartu, textvariable=self.var_nama)
        self.ent_nama.grid(row=0, column=1, sticky="ew", pady=8)

        # 2. Program studi -> Combobox
        label("Program Studi *", 1)
        self.cmb_prodi = ttk.Combobox(kartu, textvariable=self.var_prodi,
                                      values=PROGRAM_STUDI, state="readonly")
        self.cmb_prodi.grid(row=1, column=1, sticky="ew", pady=8)

        # 3. Jenis kelamin -> Radiobutton
        label("Jenis Kelamin *", 2)
        baris_jk = ttk.Frame(kartu, style="Kartu.TFrame")
        baris_jk.grid(row=2, column=1, sticky="w", pady=8)
        self.rad_jk = []
        for nilai in JENIS_KELAMIN:
            rb = ttk.Radiobutton(baris_jk, text=nilai, value=nilai, variable=self.var_jk,
                                 style="Kartu.TRadiobutton", command=self._jk_dipilih)
            rb.pack(side="left", padx=(0, 22))
            self.rad_jk.append(rb)

        # 4. Kegiatan -> Checkbutton (2 kolom)
        label("Kegiatan *", 3, sticky="nw")
        kotak_kegiatan = ttk.Frame(kartu, style="Kartu.TFrame")
        kotak_kegiatan.grid(row=3, column=1, sticky="ew", pady=8)
        kotak_kegiatan.columnconfigure(0, weight=1, uniform="cek")
        kotak_kegiatan.columnconfigure(1, weight=1, uniform="cek")
        self.cek_kegiatan = {}
        for i, nama in enumerate(KEGIATAN):
            cb = ttk.Checkbutton(kotak_kegiatan, text=nama, variable=self.var_kegiatan[nama],
                                 style="Kartu.TCheckbutton", command=self._perbarui_listbox)
            cb.grid(row=i // 2, column=i % 2, sticky="w", pady=3)
            self.cek_kegiatan[nama] = cb

        # 5. Alasan -> Text + Scrollbar
        label("Alasan Mengikuti *", 4, sticky="nw")
        kotak_alasan = ttk.Frame(kartu, style="Kartu.TFrame")
        kotak_alasan.grid(row=4, column=1, sticky="nsew", pady=8)
        kotak_alasan.columnconfigure(0, weight=1)
        kotak_alasan.rowconfigure(0, weight=1)
        self.txt_alasan = tk.Text(kotak_alasan, height=5, width=28, wrap="word",
                                  font=(f, 10), relief="flat", padx=8, pady=6,
                                  bg="white", fg=WARNA["teks"], insertbackground=WARNA["teks"],
                                  highlightthickness=1, highlightbackground=WARNA["garis"],
                                  highlightcolor=WARNA["aksen"], undo=True)
        self.txt_alasan.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(kotak_alasan, orient="vertical", command=self.txt_alasan.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.txt_alasan.configure(yscrollcommand=sb.set)
        kartu.rowconfigure(4, weight=1)

        ttk.Label(kartu, textvariable=self.var_counter, style="Redup.Kartu.TLabel").grid(
            row=5, column=1, sticky="e")

        # 6. Tombol Submit dan Reset
        baris_tombol = ttk.Frame(kartu, style="Kartu.TFrame")
        baris_tombol.grid(row=6, column=0, columnspan=2, sticky="w", pady=(14, 4))
        self.btn_submit = ttk.Button(baris_tombol, text="Submit", style="Utama.TButton",
                                     command=self.submit)
        self.btn_submit.pack(side="left", padx=(0, 10))
        self.btn_reset = ttk.Button(baris_tombol, text="Reset", style="Sekunder.TButton",
                                    command=self.reset_form)
        self.btn_reset.pack(side="left")

        ttk.Label(kartu, text="* wajib diisi   ·   Enter = Submit   ·   Ctrl+R = Reset",
                  style="Redup.Kartu.TLabel").grid(row=7, column=0, columnspan=2,
                                                   sticky="w", pady=(6, 0))
        return kartu

    def _buat_panel_kanan(self, induk):
        f = self.font
        w = WARNA
        panel = ttk.Frame(induk)
        panel.columnconfigure(0, weight=1)
        panel.rowconfigure(1, weight=1)

        # --- Listbox: kegiatan yang sedang dipilih
        self.kartu_pilihan = kartu_pilihan = ttk.Labelframe(
            panel, text=" Kegiatan Dipilih ", style="Kartu.TLabelframe",
            padding=(16, 8, 16, 10))
        kartu_pilihan.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        kartu_pilihan.columnconfigure(0, weight=1)

        self.lst_kegiatan = tk.Listbox(kartu_pilihan, height=6, activestyle="none",
                                       exportselection=False, relief="flat",
                                       font=(f, 10), bg=w["kolom_info"], fg=w["teks"],
                                       selectbackground=w["aksen_muda"],
                                       selectforeground=w["teks"],
                                       highlightthickness=1, highlightbackground=w["garis"],
                                       highlightcolor=w["aksen"])
        self.lst_kegiatan.grid(row=0, column=0, sticky="ew")
        ttk.Label(kartu_pilihan,
                  text="Klik dua kali (atau tekan Delete) untuk membatalkan pilihan.",
                  style="Redup.Kartu.TLabel").grid(row=1, column=0, sticky="w", pady=(6, 0))

        # --- Text (read-only): area informasi / ringkasan pendaftaran
        kartu_info = ttk.Labelframe(panel, text=" Ringkasan Pendaftaran ",
                                    style="Kartu.TLabelframe", padding=(12, 8, 12, 12))
        kartu_info.grid(row=1, column=0, sticky="nsew")
        kartu_info.columnconfigure(0, weight=1)
        kartu_info.rowconfigure(0, weight=1)

        self.txt_ringkasan = tk.Text(kartu_info, height=10, width=34, wrap="word",
                                     state="disabled", cursor="arrow", font=(f, 10),
                                     relief="flat", padx=12, pady=10, bg=w["kolom_info"],
                                     fg=w["teks"], highlightthickness=1,
                                     highlightbackground=w["garis"], highlightcolor=w["garis"])
        self.txt_ringkasan.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(kartu_info, orient="vertical", command=self.txt_ringkasan.yview)
        sb.grid(row=0, column=1, sticky="ns")
        self.txt_ringkasan.configure(yscrollcommand=sb.set)

        t = self.txt_ringkasan
        t.tag_configure("baris", tabs=("112",), lmargin2=112, spacing3=4)
        t.tag_configure("label", foreground=w["redup"], font=(f, 10, "bold"))
        t.tag_configure("nilai", foreground=w["teks"])
        t.tag_configure("judul", foreground=w["sukses"], font=(f, 13, "bold"), spacing3=2)
        t.tag_configure("redup", foreground=w["redup"], spacing3=8)
        return panel

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------
    def _pasang_event(self):
        # Keyboard: Enter = Submit, Ctrl+R = Reset, Ctrl+Q = Keluar, F1 = About
        self.root.bind("<Return>", self._saat_enter)
        self.root.bind("<KP_Enter>", self._saat_enter)
        self.root.bind("<Control-r>", lambda e: self.reset_form())
        self.root.bind("<Control-q>", lambda e: self.keluar())
        self.root.bind("<F1>", self.tampilkan_about)

        # Entry nama: hilangkan tanda merah begitu isinya berubah (ketik maupun paste)
        self.var_nama.trace_add("write", self._nama_berubah)

        # Combobox: dipicu saat item dipilih
        self.cmb_prodi.bind("<<ComboboxSelected>>", self._prodi_dipilih)

        # Text alasan: hitung karakter; Tab berpindah kolom (bukan menyisipkan tab)
        self.txt_alasan.bind("<<Modified>>", self._alasan_berubah)
        for urutan, arah in (("<Tab>", 1), ("<Shift-Tab>", -1), ("<ISO_Left_Tab>", -1)):
            try:
                self.txt_alasan.bind(urutan, lambda e, a=arah: self._pindah_fokus(e, a))
            except tk.TclError:
                pass  # keysym tidak dikenal di sistem operasi ini

        # Listbox: klik dua kali / Delete membatalkan pilihan kegiatan
        self.lst_kegiatan.bind("<Double-Button-1>", self._batalkan_pilihan)
        self.lst_kegiatan.bind("<Delete>", self._batalkan_pilihan)

    def _saat_enter(self, event):
        fokus = self.root.focus_get()
        if isinstance(fokus, tk.Text):
            return None            # di kolom alasan, Enter = baris baru
        if fokus is self.btn_reset:
            self.reset_form()
        else:
            self.submit()
        return "break"

    def _pindah_fokus(self, event, arah):
        tujuan = event.widget.tk_focusNext() if arah > 0 else event.widget.tk_focusPrev()
        if tujuan:
            tujuan.focus_set()
        return "break"

    def _nama_berubah(self, *_args):
        self.ent_nama.configure(style="TEntry")

    def _prodi_dipilih(self, _event=None):
        self.cmb_prodi.selection_clear()
        self._set_status("Program studi: " + self.var_prodi.get())

    def _jk_dipilih(self):
        self._set_status("Jenis kelamin: " + self.var_jk.get())

    def _alasan_berubah(self, _event=None):
        if self.txt_alasan.edit_modified():
            self._perbarui_counter()
            self.txt_alasan.edit_modified(False)

    def _batalkan_pilihan(self, _event=None):
        pilih = self.lst_kegiatan.curselection()
        if not pilih or not self._kegiatan_tampil:
            return
        nama = self._kegiatan_tampil[pilih[0]]
        self.var_kegiatan[nama].set(False)
        self._perbarui_listbox()
        self._set_status("Pilihan dibatalkan: " + nama)

    # ------------------------------------------------------------------
    # Pembaruan tampilan
    # ------------------------------------------------------------------
    def _kegiatan_terpilih(self):
        return [k for k in KEGIATAN if self.var_kegiatan[k].get()]

    def _perbarui_listbox(self):
        self._kegiatan_tampil = self._kegiatan_terpilih()
        self.lst_kegiatan.delete(0, "end")
        if self._kegiatan_tampil:
            for nama in self._kegiatan_tampil:
                self.lst_kegiatan.insert("end", "  " + nama)
        else:
            self.lst_kegiatan.insert("end", "  (belum ada kegiatan dipilih)")
            self.lst_kegiatan.itemconfig(0, fg=WARNA["redup"])
        self.kartu_pilihan.configure(text=" Kegiatan Dipilih ({} dari {}) ".format(
            len(self._kegiatan_tampil), len(KEGIATAN)))

    def _perbarui_counter(self):
        jumlah = len(self.txt_alasan.get("1.0", "end-1c").strip())
        self.var_counter.set("{} karakter (minimal {})".format(jumlah, MIN_ALASAN))

    def _perbarui_total(self):
        self.var_total.set("Pendaftar tercatat: {}".format(len(self.daftar_pendaftar)))

    def _set_status(self, teks, jenis="info"):
        warna = {"info": WARNA["redup"], "sukses": WARNA["sukses"],
                 "galat": WARNA["bahaya"]}[jenis]
        self.var_status.set(teks)
        self.lbl_status.configure(fg=warna)

    def _isi_ringkasan(self, isi):
        """Menulis ke Text ringkasan (read-only). `isi` = fungsi yang menyisipkan teks."""
        t = self.txt_ringkasan
        t.configure(state="normal")
        t.delete("1.0", "end")
        isi(t)
        t.configure(state="disabled")
        t.yview_moveto(0)

    def _ringkasan_kosong(self):
        def isi(t):
            t.insert("end", "Belum ada pendaftaran\n", "judul")
            t.tag_configure("judul", foreground=WARNA["redup"])
            t.insert("end", "Isi formulir di sebelah kiri, lalu tekan tombol Submit "
                            "atau tombol Enter untuk melihat ringkasannya di sini.", "redup")
        self._isi_ringkasan(isi)

    def _tampilkan_ringkasan(self, data):
        def baris(t, nama, nilai, lanjutan=()):
            t.insert("end", nama + "\t", ("baris", "label"))
            t.insert("end", nilai + "\n", ("baris", "nilai"))
            for teks in lanjutan:
                t.insert("end", "\t" + teks + "\n", ("baris", "nilai"))

        def isi(t):
            t.tag_configure("judul", foreground=WARNA["sukses"])
            t.insert("end", "Pendaftaran Berhasil\n", "judul")
            t.insert("end", "No. {}  ·  {}\n".format(
                data["nomor"], self._format_waktu(data["waktu"])), "redup")
            baris(t, "Nama", data["nama"])
            baris(t, "Program Studi", data["prodi"])
            baris(t, "Jenis Kelamin", data["jk"])
            baris(t, "Kegiatan", ", ".join(data["kegiatan"]))
            alasan = data["alasan"].splitlines() or [""]
            baris(t, "Alasan", alasan[0], [x for x in alasan[1:] if x.strip()])
        self._isi_ringkasan(isi)

    @staticmethod
    def _format_waktu(waktu):
        return "{:02d} {} {}, {:%H:%M}".format(waktu.day, BULAN[waktu.month - 1],
                                              waktu.year, waktu)

    def _atur_ukuran_jendela(self):
        """Ukuran awal 980x700 (atau lebih besar bila isi memerlukan), di tengah layar."""
        self.root.update_idletasks()
        lebar = max(980, self.root.winfo_reqwidth())
        tinggi = max(700, self.root.winfo_reqheight())
        lebar = min(lebar, self.root.winfo_screenwidth() - 40)
        tinggi = min(tinggi, self.root.winfo_screenheight() - 80)
        x = (self.root.winfo_screenwidth() - lebar) // 2
        y = max(0, (self.root.winfo_screenheight() - tinggi) // 2 - 20)
        self.root.geometry("{}x{}+{}+{}".format(lebar, tinggi, x, y))
        self.root.minsize(min(self.root.winfo_reqwidth(), lebar),
                          min(self.root.winfo_reqheight(), tinggi))

    # ------------------------------------------------------------------
    # Aksi: validasi, submit, reset, keluar
    # ------------------------------------------------------------------
    def _validasi(self):
        """Kembalikan daftar (pesan, widget). Daftar kosong berarti semua valid."""
        galat = []
        nama = " ".join(self.var_nama.get().split())

        if not nama:
            galat.append(("Nama tidak boleh kosong.", self.ent_nama))
        elif not all(c.isalpha() or c in " .'-" for c in nama):
            galat.append(("Nama hanya boleh berisi huruf, spasi, titik, apostrof, "
                          "dan tanda hubung.", self.ent_nama))
        elif sum(c.isalpha() for c in nama) < MIN_NAMA:
            galat.append(("Nama minimal {} huruf.".format(MIN_NAMA), self.ent_nama))

        if self.var_prodi.get() not in PROGRAM_STUDI:
            galat.append(("Program studi belum dipilih.", self.cmb_prodi))
        if not self.var_jk.get():
            galat.append(("Jenis kelamin belum dipilih.", self.rad_jk[0]))
        if not self._kegiatan_terpilih():
            galat.append(("Pilih minimal satu kegiatan.",
                          self.cek_kegiatan[KEGIATAN[0]]))
        if len(self.txt_alasan.get("1.0", "end-1c").strip()) < MIN_ALASAN:
            galat.append(("Alasan mengikuti kegiatan minimal {} karakter.".format(MIN_ALASAN),
                          self.txt_alasan))
        return galat

    def submit(self, _event=None):
        galat = self._validasi()
        if galat:
            if any(widget is self.ent_nama for _, widget in galat):
                self.ent_nama.configure(style="Salah.TEntry")
            daftar = "\n".join("•  " + pesan for pesan, _ in galat)
            self._set_status("Pendaftaran belum dapat diproses: periksa kembali isian.",
                             "galat")
            messagebox.showwarning("Data Belum Lengkap",
                                   "Mohon perbaiki isian berikut:\n\n" + daftar,
                                   parent=self.root)
            galat[0][1].focus_set()
            return

        data = {
            "nama": " ".join(self.var_nama.get().split()),
            "prodi": self.var_prodi.get(),
            "jk": self.var_jk.get(),
            "kegiatan": self._kegiatan_terpilih(),
            "alasan": self.txt_alasan.get("1.0", "end-1c").strip(),
            "waktu": datetime.now(),
        }
        data["nomor"] = "KM-{}-{:03d}".format(data["waktu"].year,
                                              len(self.daftar_pendaftar) + 1)
        self.daftar_pendaftar.append(data)

        self._tampilkan_ringkasan(data)
        self._perbarui_total()
        self._set_status("Pendaftaran {} berhasil disimpan.".format(data["nomor"]), "sukses")
        messagebox.showinfo(
            "Pendaftaran Berhasil",
            "Terima kasih, {}!\n\nPendaftaran Anda tercatat dengan nomor {}.\n"
            "Jumlah kegiatan yang diikuti: {}.".format(
                data["nama"], data["nomor"], len(data["kegiatan"])),
            parent=self.root)

    def reset_form(self, _event=None, senyap=False):
        """Kosongkan formulir, Listbox, dan area ringkasan."""
        self.var_nama.set("")
        self.var_prodi.set(PILIH_PRODI)
        self.var_jk.set("")
        for var in self.var_kegiatan.values():
            var.set(False)
        self.txt_alasan.delete("1.0", "end")
        self.ent_nama.configure(style="TEntry")

        self._perbarui_listbox()
        self._perbarui_counter()
        self._perbarui_total()
        self._ringkasan_kosong()
        self.ent_nama.focus_set()
        if senyap:
            self._set_status("Siap. Isi formulir lalu tekan Submit.")
        else:
            self._set_status("Formulir telah di-reset.")

    def keluar(self):
        if messagebox.askyesno("Konfirmasi Keluar", "Yakin ingin menutup aplikasi?",
                               parent=self.root):
            self.root.destroy()

    # ------------------------------------------------------------------
    # Jendela About (Toplevel)
    # ------------------------------------------------------------------
    def tampilkan_about(self, _event=None):
        if self.jendela_about is not None and self.jendela_about.winfo_exists():
            self.jendela_about.lift()
            self.jendela_about.focus_force()
            return

        w = WARNA
        f = self.font
        win = tk.Toplevel(self.root)
        self.jendela_about = win
        win.title("Tentang Aplikasi")
        win.configure(bg=w["kartu"])
        win.resizable(False, False)
        win.transient(self.root)

        band = tk.Frame(win, bg=w["utama"])
        band.pack(fill="x")
        tk.Label(band, text=APP_NAMA, bg=w["utama"], fg="white",
                 font=(f, 14, "bold")).pack(anchor="w", padx=22, pady=(16, 0))
        tk.Label(band, text="Versi " + APP_VERSI, bg=w["utama"], fg="#BFD2F8",
                 font=(f, 9)).pack(anchor="w", padx=22, pady=(0, 14))

        isi = tk.Frame(win, bg=w["kartu"])
        isi.pack(fill="both", expand=True, padx=22, pady=(16, 6))
        tk.Label(isi, text="Aplikasi untuk mendaftar kegiatan kemahasiswaan: mengisi data "
                           "diri, memilih kegiatan, lalu melihat ringkasan pendaftaran.",
                 bg=w["kartu"], fg=w["teks"], font=(f, 10), justify="left",
                 wraplength=360).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        rincian = (
            ("Praktikum", "Sesi 11, Advanced Widgets dan Event Handling"),
            ("Pengembang", "{} ({})".format(PENGEMBANG, NIM)),
            ("Teknologi", "Python 3, Tkinter / ttk"),
            ("Widget", "Entry, Combobox, Radiobutton, Checkbutton, Text, Listbox, "
                       "Menu, Messagebox, Toplevel"),
        )
        for i, (nama, nilai) in enumerate(rincian, start=1):
            tk.Label(isi, text=nama, bg=w["kartu"], fg=w["redup"],
                     font=(f, 9, "bold")).grid(row=i, column=0, sticky="nw", padx=(0, 14), pady=3)
            tk.Label(isi, text=nilai, bg=w["kartu"], fg=w["teks"], font=(f, 10),
                     justify="left", wraplength=270).grid(row=i, column=1, sticky="w", pady=3)

        tombol = ttk.Button(win, text="Tutup", style="Utama.TButton", command=win.destroy)
        tombol.pack(pady=(10, 18))
        tombol.focus_set()
        win.bind("<Escape>", lambda e: win.destroy())
        win.bind("<Return>", lambda e: win.destroy())

        # Letakkan di tengah jendela utama, lalu jadikan modal
        win.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - win.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - win.winfo_height()) // 2
        win.geometry("+{}+{}".format(max(0, x), max(0, y)))
        try:
            win.wait_visibility()
            win.grab_set()
        except tk.TclError:
            pass  # beberapa sistem menolak grab; jendela tetap berfungsi


def main():
    root = tk.Tk()
    AplikasiPendaftaran(root)
    root.mainloop()


if __name__ == "__main__":
    main()
