# PRD Arsitektur File Jupyter Notebook (`.ipynb`)

## Tujuan & Deliverable

File notebook praktikum dirancang linear, modular, dan memisahkan secara tegas antara narasi dasar fisika/matematis, sel eksekusi kode, serta pembahasan numerik kritis.

## Struktur File

**Nama File**: `resonance_breit_wigner_fitting.ipynb`

| Cell | Tipe | Konten |
|---|---|---|
| 1 | Markdown | **Header Identitas & Abstrak Masalah Fisis**<br>- Judul Praktikum: Kasus 8 - Resonansi Hamburan Neutron Karbon (Breit-Wigner)<br>- Identitas Mahasiswa & Kelompok Resmi<br>- Abstrak studi kasus dan target komputasi |
| 2 | Markdown | **Teori Dasar 1: Model Resonansi Breit-Wigner**<br>- Persamaan fisis penampang lintang hamburan nuklir satu tingkat<br>- Interpretasi fisis parameter: Er, Gamma (FWHM), sigma_0, sigma_bg |
| 3 | Markdown | **Teori Dasar 2: Metode Newton-Raphson Multivariat & Formulasi Matriks**<br>- Minimisasi Chi-Square terbobot<br>- Penurunan analitik vektor gradien g(p) dan matriks kelengkungan Hessian H(p)<br>- Formula koreksi langkah: H * Delta_p = -g |
| 4 | Code | **Setup Lingkungan & Dependensi**<br>- Import pustaka: numpy, scipy, matplotlib, urllib, csv, re<br>- Konfigurasi parameter visualisasi Matplotlib (DPI, font family, LaTeX style) |
| 5 | Markdown | **Tahap 1: Ingesti Data IAEA-NDS EXFOR & Parsing CSV**<br>- Penjelasan struktur format ASCII EXFOR<br>- Alur ekstraksi tiga kolom fisis (E, sigma, dsigma) |
| 6 | Code | **Eksekusi Tahap 1**<br>- Definisi parser Regex dan pipeline unduh<br>- Ekspor hasil bersih ke `exfor_c12_resonance.csv`<br>- Validasi keberadaan file CSV di direktori lokal |
| 7 | Markdown | **Tahap 2: Implementasi Fungsi Penampang Lintang, Gradien, & Hessian**<br>- Detail rumus turunan parsial terhadap masing-masing 4 parameter<br>- Verifikasi sifat simetri matriks Hessian |
| 8 | Code | **Eksekusi Tahap 2**<br>- Deklarasi fungsi Python: `breit_wigner`, `compute_chi2`, `compute_gradient`, `compute_hessian`<br>- Unit test kalkulasi gradien dan Hessian pada dummy input |
| 9 | Markdown | **Tahap 3: Algoritma Ekstraksi Nilai Awal Fisis (p0)**<br>- Justifikasi fisis penentuan tebakan awal berbasis data<br>- Estimasi empiris posisi resonansi puncak dan FWHM |
| 10 | Code | **Eksekusi Tahap 3**<br>- Ekstraksi p0 dari dataset CSV<br>- Output display vektor parameter awal |
| 11 | Markdown | **Tahap 4: Algoritma Newton-Raphson Multivariat**<br>- Logika pembaruan iteratif dan kriteria toleransi henti<br>- Monitoring konvergensi kuadratik dan evaluasi condition number |
| 12 | Code | **Eksekusi Tahap 4**<br>- Eksekusi loop solver Newton-Raphson<br>- Tabel ringkasan iterasi: nomor iterasi, chi-square, delta_p, condition number Hessian |
| 13 | Markdown | **Tahap 5: Evaluasi Statistik, Matriks Kovariansi, & Propagasi Galat**<br>- Perhitungan reduced chi-square (kualitas fitting)<br>- Evaluasi batas ketidakpastian parameter dari elemen diagonal inversi Hessian |
| 14 | Code | **Eksekusi Tahap 5**<br>- Komputasi reduced chi-square, matriks kovariansi C, dan korelasi rho<br>- Cetak hasil akhir parameter: Value +/- Error fisis |
| 15 | Markdown | **Tahap 6: Uji Ketahanan Numerik (Stress-Test Noise)**<br>- Metodologi injeksi Gaussian noise (5%, 15%, 30%)<br>- Analisis stabilitas nilai eigen matriks kelengkungan terhadap data berisik |
| 16 | Code | **Eksekusi Tahap 6**<br>- Loop pengujian noise bertingkat<br>- Evaluasi batas toleransi kegagalan matriks Hessian (singularitas) |
| 17 | Markdown | **Tahap 7: Visualisasi Hasil & Interpretasi Fisis**<br>- Panduan interpretasi grafik fitting dan distribusi residual |
| 18 | Code | **Eksekusi Tahap 7**<br>- Plot Kurva Fitting Breit-Wigner + Data Eksperimen + Error Bars<br>- Subplot residual terbobot<br>- Plot lintasan penurunan chi-square (semilog) |
| 19 | Markdown | **Analisis Hasil Komputasi & Diskusi Kritis**<br>- Evaluasi laju konvergensi orde dua Newton-Raphson<br>- Pembahasan nilai reduced chi-square terhadap kelayakan model<br>- Diskusi matriks korelasi (korelasi silang Gamma vs sigma_0)<br>- Evaluasi batasan numerik metode ketika tebakan awal dijauhkan atau noise diperbesar |
| 20 | Markdown | **Kesimpulan Fisis & Rekomendasi**<br>- Rangkuman nilai parameter resonansi 12C(n,tot) hasil komputasi vs literatur nuklir<br>- Pernyataan penutup tentang performa dan batasan metode Newton-Raphson matriks |
