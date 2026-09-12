# Dokumen Kebutuhan Produk (Product Requirement Documents - PRD)
## Praktikum Fisika Komputasi II (Studi Kasus 8)

Direktori ini berisi seluruh dokumen spesifikasi teknis, rancangan arsitektur, penurunan matematis, dan standar pengujian (*Product Requirement Documents*) yang mendasari implementasi kode program, *Jupyter Notebook*, serta laporan praktikum.

---

## 📑 Indeks Dokumen PRD

| No. | Berkas PRD | Tahap / Komponen | Ruang Lingkup & Fokus Utama |
| :---: | :--- | :--- | :--- |
| **0** | [`PRD_Arsitektur_Jupyter_Notebook.md`](./PRD_Arsitektur_Jupyter_Notebook.md) | **Arsitektur Notebook** | Standar struktur sel, instalasi otomatis dependensi, narasi ilmiah markdown, dan integrasi visual interaktif. |
| **1** | [`PRD_Tahap0_Pseudocode_Flowchart_TikZ.md`](./PRD_Tahap0_Pseudocode_Flowchart_TikZ.md) | **Tahap 0: Desain Algoritma** | Spesifikasi diagram alir TikZ vektor, logika percabangan kondisi, kriteria toleransi, dan pseudocode algoritma. |
| **2** | [`PRD_Tahap1_Akuisisi_Data_Pipeline_CSV.md`](./PRD_Tahap1_Akuisisi_Data_Pipeline_CSV.md) | **Tahap 1: Pipeline Data** | Pengunduhan otomatis web stream IAEA-NDS EXFOR, pembersihan regex ASCII, filter energi $1.8 - 2.4\text{ MeV}$, dan ekspor CSV. |
| **3** | [`PRD_Tahap2_Gradien_Hessian.md`](./PRD_Tahap2_Gradien_Hessian.md) | **Tahap 2: Kalkulus Analitik** | Formulasi kalkulus eksak penampang lintang Breit-Wigner, matriks Jacobian $\mathbf{J}$, vektor Gradien $\mathbf{g}$, dan Hessian Gauss-Newton $\mathbf{H}$. |
| **4** | [`PRD_Tahap3_Initial_Guess.md`](./PRD_Tahap3_Initial_Guess.md) | **Tahap 3: Heuristik Parameter** | Ekstraksi otomatis tebakan parameter awal $\mathbf{p}_0 = [E_r^{(0)}, \Gamma^{(0)}, \sigma_0^{(0)}, \sigma_{bg}^{(0)}]^T$ berbasis karakteristik kurva data eksperimen. |
| **5** | [`PRD_Tahap4_Newton_Raphson_Solver.md`](./PRD_Tahap4_Newton_Raphson_Solver.md) | **Tahap 4: Solver Numerik** | Mesin solver optimasi multivariat $\mathbf{H}\Delta\mathbf{p} = -\mathbf{g}$, kriteria henti ganda $\varepsilon = 10^{-6}$, dan pemantauan bilangan kondisi $\kappa(\mathbf{H})$. |
| **6** | [`PRD_Tahap5_Statistik_Kovariansi.md`](./PRD_Tahap5_Statistik_Kovariansi.md) | **Tahap 5: Inferensi Statistik** | Perhitungan $\chi^2_{red}$, matriks kovariansi parameter asimptotik $\mathbf{C} = 2\mathbf{H}^{-1}$, matriks korelasi $\boldsymbol{\rho}$, dan residu terbobot. |
| **7** | [`PRD_Tahap6_Noise_Stress_Test.md`](./PRD_Tahap6_Noise_Stress_Test.md) | **Tahap 6: Uji Ketahanan Derau** | Simulasi Monte Carlo dengan perturbasi derau Gaussian proporsional ($5\%, 15\%, 30\%$), analisis degradasi konvergensi, dan kondisi singularitas. |
| **8** | [`PRD_Tahap7_Visualisasi.md`](./PRD_Tahap7_Visualisasi.md) | **Tahap 7: Visualisasi Publikasi** | Desain grafis publikasi ganda (fitting resonansi, distribusi residu, metrik konvergensi kuadratik, respon ketahanan derau). |

---

## 🎯 Hubungan Antar-Tahap dalam Pipeline

```
[Tahap 1: Data Pipeline CSV]
            │
            ▼
[Tahap 3: Heuristik Tebakan Awal p0] ──┐
            │                          │
            ▼                          ▼
[Tahap 2: Gradien & Hessian] ──> [Tahap 4: Solver Newton-Raphson]
                                               │
                                               ▼
[Tahap 7: Visualisasi] <── [Tahap 6: Noise Test] <── [Tahap 5: Statistik & Kovariansi]
```

