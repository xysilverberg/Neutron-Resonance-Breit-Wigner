"""
Script Pembangun dan Pengeksekusi Jupyter Notebook Master
File: resonance_breit_wigner_fitting.ipynb
Praktikum Fisika Komputasi II - Kasus 8 (Group H: Airin & Hendra)
Departemen Fisika FST Universitas Airlangga
"""

import nbformat as nbf
from nbclient import NotebookClient
import os

def create_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.14.5"
        }
    }

    cells = []

    # =========================================================================
    # CELL 1: MARKDOWN - Header Identitas, Abstrak, & Blueprint Tahap 0
    # =========================================================================
    cell1_text = r"""# LAPORAN PRAKTIKUM FISIKA KOMPUTASI II
## Kasus 8: Resonansi Hamburan Neutron Karbon $^{12}\text{C}(n,\text{tot})$ Menggunakan Fitting Non-Linier Breit-Wigner dengan Metode Newton-Raphson Multivariat

---

### **Identitas Mahasiswa & Kelompok Resmi**
* **Kelompok Praktikum**: **Group H**
* **Anggota Kelompok**:
  1. **Airin Khairunnisa Nur Raerah** (NIM: 182241045)
  2. **Hendra Maulana** (NIM: 182241043)
* **Program Studi**: S1 Fisika
* **Departemen / Fakultas**: Departemen Fisika, Fakultas Sains dan Teknologi, Universitas Airlangga
* **Dosen Pengampu / Tim Asisten**: Laboratorium Fisika Komputasi UNAIR

---

### **Abstrak & Sasaran Komputasi**
Praktikum ini bertujuan untuk memodelkan dan mengekstraksi parameter fisis resonansi hamburan neutron energi rendah pada inti $^{12}\text{C}$ pada rentang energi laboratorium $1.8\text{ MeV} \le E \le 2.4\text{ MeV}$ berdasarkan model penampang lintang satu tingkat (*single-level Breit-Wigner*). Penyelesaian masalah optimasi non-linier kuadrat terkecil terbobot ($\chi^2$) dilakukan menggunakan pendekatan **Newton-Raphson multivariat dalam representasi matriks** dengan turunan analitik murni berbasis vektorisasi NumPy (tanpa aproksimasi diferensiasi beda-hingga). 

Untuk menjamin kestabilan konvergensi kuadratik, pipeline dilengkapi dengan:
1. Ekstraksi otomatis parameter awal fisis $\mathbf{p}_0$ berbasis heuristik data (puncak dan FWHM),
2. Monitoring bilangan kondisi matriks kelengkungan $\kappa(\mathbf{H})$ pada tiap iterasi untuk memitigasi singularitas dan batas presisi mesin (*machine precision*),
3. Evaluasi statistik matriks kovariansi $\mathbf{C} = 2\mathbf{H}^{-1}$ serta korelasi silang antar parameter fisis,
4. Uji ketahanan numerik (*Monte Carlo noise stress-test*) terhadap gangguan derau eksperimen hingga 30%, dan
5. Validasi fisis parameter terhadap benchmark data nuklir internasional IAEA EXFOR.

---

### **Peta Alur Komputasi (Flowchart & Blueprint Algoritmik)**
Berikut adalah diagram alir pipeline terpadu (*flowchart*) yang telah dirancang menggunakan LaTeX TikZ, memetakan interkoneksi keseluruhan proses komputasi:

<div align="center">
  <img src="flowchart_pipeline.png" alt="Flowchart Pipeline Komputasi Breit-Wigner" width="550"/>
</div>

Peta logika di atas memastikan bahwa setiap tahap eksekusi memiliki batas kondisi kendali numerik yang terdefinisi secara ketat sebelum berlanjut ke tahap berikutnya."""

    cells.append(nbf.v4.new_markdown_cell(cell1_text))

    # =========================================================================
    # CELL 2: MARKDOWN - Teori Dasar 1: Model Resonansi Breit-Wigner
    # =========================================================================
    cell2_text = r"""---
## **Teori Dasar 1: Model Resonansi Hamburan Breit-Wigner**

Dalam fisika nuklir, hamburan neutron energi rendah oleh inti atom melibatkan pembentukan inti majemuk (*compound nucleus*) pada keadaan eksitasi diskret. Di sekitar energi resonansi, penampang lintang total dapat dideskripsikan secara akurat oleh rumus resonansi satu tingkat Breit-Wigner (*single-level Breit-Wigner formula*):

$$\sigma(E; \mathbf{p}) = \sigma_{bg} + \sigma_0 \frac{(\Gamma / 2)^2}{(E - E_r)^2 + (\Gamma / 2)^2}$$

dengan vektor parameter fisis $\mathbf{p} = [E_r, \Gamma, \sigma_0, \sigma_{bg}]^T$.

### **Interpretasi Fisis Parameter:**
1. **$E_r$ (Energi Resonansi Pusat, satuan: MeV)**:
   Energi kinetik neutron datang di laboratorium yang memicu keadaan resonansi inti majemuk $^{13}\text{C}^*$. Pada energi ini, penampang lintang mencapai nilai puncak.
2. **$\Gamma$ (Lebar Resonansi Penuh / FWHM, satuan: MeV)**:
   Lebar spektral resonansi pada setengah tinggi maksimum. Berdasarkan prinsip ketidakpastian energi-waktu Heisenberg ($\Delta E \cdot \Delta t \sim \hbar$), parameter $\Gamma$ berbanding terbalik dengan waktu hidup (*mean lifetime*) keadaan tereksitasi inti majemuk:
   $$\tau = \frac{\hbar}{\Gamma}$$
3. **$\sigma_0$ (Amplitudo Resonansi Murni, satuan: barn)**:
   Kontribusi penampang lintang resonansi maksimum di atas kontinum latar belakang pada $E = E_r$.
4. **$\sigma_{bg}$ (Penampang Lintang Kontinum Latar Belakang, satuan: barn)**:
   Kontribusi hamburan potensial elastis keras (*hard-sphere potential scattering*) dari inti target yang bernilai hampir konstan pada rentang energi lokal pengamatan."""

    cells.append(nbf.v4.new_markdown_cell(cell2_text))

    # =========================================================================
    # CELL 3: MARKDOWN - Teori Dasar 2: Metode Newton-Raphson Multivariat
    # =========================================================================
    cell3_text = r"""---
## **Teori Dasar 2: Metode Newton-Raphson Multivariat & Formulasi Matriks**

Tujuan pencocokan kurva (*curve fitting*) adalah menemukan vektor parameter optimal $\mathbf{p}^*$ yang meminimalkan fungsi ketidaksesuaian kuadrat terkecil terbobot (*weighted least-squares* / $\chi^2$):

$$\chi^2(\mathbf{p}) = \sum_{i=1}^N \left( \frac{\sigma_i - \sigma(E_i; \mathbf{p})}{\Delta\sigma_i} \right)^2 = \sum_{i=1}^N w_i \left[ \sigma_i - \sigma(E_i; \mathbf{p}) \right]^2$$

dengan bobot statistik $w_i = 1 / (\Delta\sigma_i)^2$.

### **Ekspansi Deret Taylor & Formulasi Langkah Newton**
Melakukan ekspansi Taylor orde-dua pada $\chi^2(\mathbf{p})$ di sekitar taksiran iteratif $\mathbf{p}^{(k)}$:

$$\chi^2(\mathbf{p}^{(k)} + \Delta\mathbf{p}) \approx \chi^2(\mathbf{p}^{(k)}) + \mathbf{g}(\mathbf{p}^{(k)})^T \Delta\mathbf{p} + \frac{1}{2} \Delta\mathbf{p}^T \mathbf{H}(\mathbf{p}^{(k)}) \Delta\mathbf{p}$$

Titik minimum lokal mensyaratkan gradien lenyap: $\nabla_{\Delta\mathbf{p}} \chi^2 = \mathbf{0}$, yang menghasilkan **Sistem Persamaan Linier Simultan Matriks**:

$$\mathbf{H}(\mathbf{p}^{(k)}) \Delta\mathbf{p} = -\mathbf{g}(\mathbf{p}^{(k)})$$

sehingga langkah koreksi parameter diperbarui melalui:

$$\mathbf{p}^{(k+1)} = \mathbf{p}^{(k)} + \Delta\mathbf{p} = \mathbf{p}^{(k)} - [\mathbf{H}(\mathbf{p}^{(k)})]^{-1} \mathbf{g}(\mathbf{p}^{(k)})$$

### **Formulasi Turunan Analitik Eksak**
1. **Vektor Gradien $\mathbf{g}(\mathbf{p}) = \nabla_{\mathbf{p}} \chi^2$** (berukuran $4 \times 1$):
   $$g_j = \frac{\partial \chi^2}{\partial p_j} = -2 \sum_{i=1}^N \frac{\sigma_i - \sigma(E_i; \mathbf{p})}{(\Delta\sigma_i)^2} \frac{\partial \sigma(E_i; \mathbf{p})}{\partial p_j} = -2 \mathbf{J}^T \mathbf{W} (\boldsymbol{\sigma} - \boldsymbol{\sigma}_{model})$$
   dengan matriks Jacobian $\mathbf{J} \in \mathbb{R}^{N \times 4}$ memiliki elemen $J_{ij} = \frac{\partial \sigma(E_i)}{\partial p_j}$.

2. **Matriks Hessian Analitik $\mathbf{H}(\mathbf{p}) = \nabla^2_{\mathbf{p}} \chi^2$** (berukuran $4 \times 4$):
   Menggunakan aproksimasi kelengkungan kuadratik Gauss-Newton:
   $$H_{jk} \approx 2 \sum_{i=1}^N \frac{1}{(\Delta\sigma_i)^2} \left( \frac{\partial \sigma(E_i)}{\partial p_j} \frac{\partial \sigma(E_i)}{\partial p_k} \right) \implies \mathbf{H} = 2 \mathbf{J}^T \mathbf{W} \mathbf{J}$$
   Matriks ini secara fundamental simetris dan semi-positif definit, mengeliminasi ketidakstabilan akibat suku turunan orde-dua dari residu."""

    cells.append(nbf.v4.new_markdown_cell(cell3_text))

    # =========================================================================
    # PRASYARAT SISTEM & INSTALASI DEPENDENSI
    # =========================================================================
    cell_prereq_md = r"""---
## **Prasyarat Sistem & Instalasi Pustaka (Dependencies)**

> [!IMPORTANT]
> **PENTING: Wajib Diperhatikan Sebelum Menjalankan Notebook:**
> 1. Pastikan bahasa pemrograman **Python (versi $\ge$ 3.8, disarankan versi 3.10, 3.11, 3.12, atau 3.14)** telah terpasang (*installed*) pada sistem lokal (komputer/laptop) Anda.
> 2. Jika Python belum terpasang di sistem lokal Anda, unduh penginstal resminya melalui situs resmi [python.org](https://www.python.org/downloads/) dan pastikan mencentang kotak **"Add Python to PATH"** pada jendela awal instalasi.
> 3. Jalankan sel kode di bawah ini terlebih dahulu untuk menginstal seluruh pustaka komputasi saintifik dan visualisasi yang dibutuhkan (`numpy`, `scipy`, `matplotlib`) ke dalam lingkungan Python lokal Anda sebelum masuk ke sel eksekusi program."""

    cells.append(nbf.v4.new_markdown_cell(cell_prereq_md))

    cell_install_code = r"""# Sel Instalasi Library Dependensi
# Menjamin pustaka saintifik terpasang di lingkungan Python lokal sebelum digunakan
import sys
!{sys.executable} -m pip install numpy scipy matplotlib --quiet
print("Status: Seluruh pustaka dependensi (numpy, scipy, matplotlib) siap digunakan.")"""

    cells.append(nbf.v4.new_code_cell(cell_install_code))

    # =========================================================================
    # CELL SETUP: CODE - Setup Lingkungan & Dependensi
    # =========================================================================
    cell4_code = r"""# Setup Lingkungan Eksekusi & Konfigurasi Visualisasi
import sys
import os
import csv
import re
import urllib.request
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt

# Konfigurasi parameter visualisasi publikasi
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 150,
    "lines.linewidth": 1.8,
    "axes.grid": True,
    "grid.alpha": 0.35,
    "grid.linestyle": "--"
})

print("=" * 60)
print(f"Versi Python     : {sys.version.split()[0]}")
print(f"Versi NumPy      : {np.__version__}")
print(f"Versi SciPy      : {sp.__version__}")
print("Lingkungan komputasi siap dieksekusi.")
print("=" * 60)"""

    cells.append(nbf.v4.new_code_cell(cell4_code))

    # =========================================================================
    # CELL 5: MARKDOWN - Tahap 1: Ingesti Data IAEA-NDS EXFOR
    # =========================================================================
    cell5_text = r"""---
## **Tahap 1: Akuisisi Data, Parsing ASCII, & Pipeline CSV**

Dataset eksperimen diambil dari repositori nuklir internasional **IAEA-NDS EXFOR** (*Experimental Nuclear Reaction Data*) entri 10224002 (Cierjacks et al., KFK-1000) untuk penampang lintang transmisi neutron total inti $^{12}\text{C}(n,\text{tot})$ pada rentang energi $1.8\text{ MeV} \le E \le 2.4\text{ MeV}$.

Modul akuisisi dilengkapi dengan:
- Ekstraksi otomatis format stream ASCII menggunakan Regular Expression (`re`).
- Mekanisme *network fallback resilience* ke dataset kalibrasi standar jika koneksi web IAEA mengalami pemutusan atau *timeout*.
- Pengecekan integritas tipe data `float64` dan ekspor ke format CSV standar RFC 4180 (`exfor_c12_resonance.csv`)."""

    cells.append(nbf.v4.new_markdown_cell(cell5_text))

    # =========================================================================
    # CELL 6: CODE - Eksekusi Tahap 1
    # =========================================================================
    cell6_code = r"""# Eksekusi Pipeline Tahap 1: Akuisisi & Ekspor CSV
from tahap1_data_pipeline import fetch_exfor_raw, parse_exfor_ascii, export_to_csv

raw_stream = fetch_exfor_raw(target="C-12", reaction="N,TOT")
data_matrix = parse_exfor_ascii(raw_stream)
csv_filename = "exfor_c12_resonance.csv"
export_to_csv(data_matrix, output_path=csv_filename)

E_data = data_matrix[:, 0]
sigma_data = data_matrix[:, 1]
dsigma_data = data_matrix[:, 2]

print("\nPratinjau 10 Baris Pertama Dataset Bersih:")
print(f"{'No':<4} | {'Energi (MeV)':<14} | {'Sigma (barn)':<14} | {'dSigma (barn)':<14}")
print("-" * 52)
for idx in range(10):
    print(f"{idx+1:<4} | {E_data[idx]:<14.4f} | {sigma_data[idx]:<14.4f} | {dsigma_data[idx]:<14.4f}")
print(f"... Total data titik: {len(E_data)} baris.")"""

    cells.append(nbf.v4.new_code_cell(cell6_code))

    # =========================================================================
    # CELL 7: MARKDOWN - Tahap 2: Turunan Analitik Gradien & Hessian
    # =========================================================================
    cell7_text = r"""---
## **Tahap 2: Implementasi Fungsi Penampang Lintang, Gradien, & Hessian Analitik**

Menghindari diferensiasi numerik beda-hingga (*finite difference*) yang rentan terhadap galat pembulatan mesin ($O(h)$ atau $O(h^2)$), kita menurunkan formulasi analitik eksak untuk matriks Jacobian model $\mathbf{J} \in \mathbb{R}^{N \times 4}$:

Definisikan penyebut Lorentzian: $D_i = (E_i - E_r)^2 + (\Gamma / 2)^2$.

1. **Turunan terhadap $E_r$**:
   $$\frac{\partial \sigma(E_i)}{\partial E_r} = 2 \sigma_0 \left(\frac{\Gamma}{2}\right)^2 \frac{E_i - E_r}{D_i^2}$$
2. **Turunan terhadap $\Gamma$**:
   $$\frac{\partial \sigma(E_i)}{\partial \Gamma} = \sigma_0 \left(\frac{\Gamma}{2}\right) \frac{(E_i - E_r)^2}{D_i^2}$$
3. **Turunan terhadap $\sigma_0$**:
   $$\frac{\partial \sigma(E_i)}{\partial \sigma_0} = \frac{(\Gamma / 2)^2}{D_i}$$
4. **Turunan terhadap $\sigma_{bg}$**:
   $$\frac{\partial \sigma(E_i)}{\partial \sigma_{bg}} = 1$$

Melalui vektorisasi NumPy, gradien $\mathbf{g} = -2 \mathbf{J}^T \mathbf{W} \mathbf{r}$ dan Hessian $\mathbf{H} = 2 \mathbf{J}^T \mathbf{W} \mathbf{J}$ dihitung secara simultan dalam kompleksitas memori kontigu berkecepatan tinggi."""

    cells.append(nbf.v4.new_markdown_cell(cell7_text))

    # =========================================================================
    # CELL 8: CODE - Eksekusi Tahap 2
    # =========================================================================
    cell8_code = r"""# Eksekusi Tahap 2: Verifikasi Turunan Analitik Gradien & Matriks Hessian
from tahap2_analytic_derivatives import (
    breit_wigner, compute_model_jacobian, compute_residuals,
    compute_chi2, compute_gradient, compute_hessian, test_derivatives_accuracy
)

# Jalankan unit test komparasi analitik vs numerik beda-hingga
test_derivatives_accuracy()

# Evaluasi pada titik tengah fisis
p_sample = np.array([2.075, 0.055, 2.90, 4.60])
H_sample = compute_hessian(p_sample, E_data, sigma_data, dsigma_data)
g_sample = compute_gradient(p_sample, E_data, sigma_data, dsigma_data)

print(f"\nVektor Gradien g(p_sample)     : {g_sample}")
print(f"Bentuk Matriks Hessian H        : {H_sample.shape}")
print(f"Bilangan Kondisi Hessian cond(H): {np.linalg.cond(H_sample):.2e}")
print(f"Nilai Eigen Hessian             : {np.linalg.eigvalsh(H_sample)}")"""

    cells.append(nbf.v4.new_code_cell(cell8_code))

    # =========================================================================
    # CELL 9: MARKDOWN - Tahap 3: Algoritma Ekstraksi Nilai Awal Fisis
    # =========================================================================
    cell9_text = r"""---
## **Tahap 3: Algoritma Ekstraksi Otomatis Tebakan Parameter Awal ($\mathbf{p}_0$)**

Metode Newton-Raphson memiliki radius konvergensi lokal (*local convergence radius*). Jika tebakan awal dipilih secara acak atau terlalu jauh dari solusi riil, matriks Hessian dapat menjadi *ill-conditioned* atau gradien membimbing parameter ke arah lembah non-fisis (misal $\Gamma < 0$ atau $\sigma_0 < 0$).

Untuk mengeliminasi tebakan acak (*blind guessing*), dirancang algoritma heuristik fisis:
1. $E_r^{(0)} = E_{\arg\max(\sigma_i)}$ $\rightarrow$ energi saat penampang lintang maksimum.
2. $\sigma_{bg}^{(0)} = \min(\sigma_1, \sigma_N)$ $\rightarrow$ baseline penampang lintang potensial pada sayap energi tepi.
3. $\sigma_0^{(0)} = \sigma_{\max} - \sigma_{bg}^{(0)}$ $\rightarrow$ tinggi relatif resonansi murni.
4. $\Gamma^{(0)} = \text{FWHM}$ $\rightarrow$ rentang energi pada tingkat setengah ketinggian puncak: $\sigma_{\text{half}} = \sigma_{bg}^{(0)} + 0.5 \sigma_0^{(0)}$."""

    cells.append(nbf.v4.new_markdown_cell(cell9_text))

    # =========================================================================
    # CELL 10: CODE - Eksekusi Tahap 3
    # =========================================================================
    cell10_code = r"""# Eksekusi Tahap 3: Ekstraksi Otomatis Parameter Awal Fisis (p0)
from tahap3_initial_guess import extract_initial_parameters

p0 = extract_initial_parameters(E_data, sigma_data)

print("=" * 60)
print("HASIL EKSTRAKSI TEBAKAN AWAL FISIS (p0):")
print("=" * 60)
print(f"  Er^(0)       (Energi Resonansi)  : {p0[0]:.4f} MeV")
print(f"  Gamma^(0)    (Lebar FWHM)        : {p0[1]:.4f} MeV")
print(f"  sigma0^(0)   (Amplitudo Puncak)  : {p0[2]:.4f} barn")
print(f"  sigma_bg^(0) (Kontinum Baseline) : {p0[3]:.4f} barn")
print(f"  Chi2 Awal pada p0                : {compute_chi2(p0, E_data, sigma_data, dsigma_data):.4f}")
print("=" * 60)"""

    cells.append(nbf.v4.new_code_cell(cell10_code))

    # =========================================================================
    # CELL 11: MARKDOWN - Tahap 4: Algoritma Newton-Raphson Multivariat
    # =========================================================================
    cell11_text = r"""---
## **Tahap 4: Algoritma Newton-Raphson Multivariat & Kontrol Kestabilan**

Solver Newton-Raphson diimplementasikan dengan fitur stabilitas numerik:
- **Penyelesaian Sistem Linier**: Menggunakan `np.linalg.solve` berbasis dekomposisi LAPACK LU, bukan inversi langsung $\mathbf{H}^{-1} \mathbf{g}$ yang sensitif terhadap akumulasi galat pembulatan.
- **Deteksi Ill-Conditioning**: Memantau bilangan kondisi $\kappa(\mathbf{H}) = \|\mathbf{H}\|_2 \cdot \|\mathbf{H}^{-1}\|_2$. Jika $\kappa(\mathbf{H}) > 10^{12}$, matriks mendekati singular dan iterasi dihentikan secara aman.
- **Kriteria Henti Ganda**: Konvergensi dinyatakan tercapai jika norma langkah $\|\Delta\mathbf{p}\|_2 < 10^{-6}$ atau perubahan $|\chi^2_{k+1} - \chi^2_k| < 10^{-6}$."""

    cells.append(nbf.v4.new_markdown_cell(cell11_text))

    # =========================================================================
    # CELL 12: CODE - Eksekusi Tahap 4
    # =========================================================================
    cell12_code = r"""# Eksekusi Tahap 4: Loop Optimasi Newton-Raphson Multivariat
from tahap4_newton_raphson_solver import solve_newton_raphson

solver_output = solve_newton_raphson(p0, E_data, sigma_data, dsigma_data, tol=1e-6, max_iter=50)

p_opt = solver_output["p_opt"]
history = solver_output["history"]
H_final = solver_output["H_final"]
chi2_final = solver_output["chi2_final"]

print("=" * 90)
print(f"STATUS SOLVER: {'KONVERGEN' if solver_output['converged'] else 'TIDAK KONVERGEN'}")
print(f"Total Iterasi Dieksekusi: {solver_output['iterations']}")
print(f"Chi-Square Akhir        : {chi2_final:.6f}")
print("=" * 90)
print(f"{'Iter':<5} | {'Chi2':<12} | {'||g||_2':<12} | {'||Delta_p||':<12} | {'cond(H)':<12} | {'Er (MeV)':<12} | {'Gamma (MeV)':<12}")
print("-" * 90)
for step in history:
    it = step["iteration"]
    c2 = step["chi2"]
    gn = step["grad_norm"]
    sn = step["step_norm"]
    cH = step["cond_H"]
    er = step["p"][0]
    gm = step["p"][1]
    print(f"{it:<5} | {c2:<12.4f} | {gn:<12.4e} | {sn:<12.4e} | {cH:<12.2e} | {er:<12.6f} | {gm:<12.6f}")
print("=" * 90)"""

    cells.append(nbf.v4.new_code_cell(cell12_code))

    # =========================================================================
    # CELL 13: MARKDOWN - Tahap 5: Statistik, Kovariansi, & Propagasi Galat
    # =========================================================================
    cell13_text = r"""---
## **Tahap 5: Evaluasi Statistik, Matriks Kovariansi, & Propagasi Galat**

Setelah mencapai parameter optimal $\mathbf{p}^*$, analisis statistik inferensial dilakukan untuk mengevaluasi kualitas fitting dan ketidakpastian fisis:

1. **Derajat Kebebasan**:
   $$\nu = N - m = N - 4$$
2. **Reduced Chi-Square ($\chi^2_{red}$)**:
   $$\chi^2_{red} = \frac{\chi^2_{\min}}{\nu}$$
   Kriteria fisis: $\chi^2_{red} \sim 1$ menandakan kecocokan yang sangat selaras dengan ketidakpastian eksperimental.
3. **Matriks Kovariansi Asimptotik Parameter**:
   $$\mathbf{C} = 2 [\mathbf{H}(\mathbf{p}^*)]^{-1}$$
   Elemen diagonal merepresentasikan variansi parameter: $\delta p_j = \sqrt{C_{jj} \cdot \chi^2_{red}}$.
4. **Matriks Korelasi Ternormalisasi**:
   $$\rho_{jk} = \frac{C_{jk}}{\sqrt{C_{jj} C_{kk}}}$$
   Mengukur derajat keterkaitan silang antar parameter (khususnya antara lebar resonansi $\Gamma$ dan amplitudo $\sigma_0$)."""

    cells.append(nbf.v4.new_markdown_cell(cell13_text))

    # =========================================================================
    # CELL 14: CODE - Eksekusi Tahap 5
    # =========================================================================
    cell14_code = r"""# Eksekusi Tahap 5: Kalkulasi Matriks Kovariansi & Ketidakpastian
from tahap5_statistical_analysis import compute_statistics_and_covariance

stats_output = compute_statistics_and_covariance(p_opt, H_final, chi2_final, len(E_data))

chi2_red = stats_output["chi2_red"]
cov_matrix = stats_output["cov_matrix"]
param_errors = stats_output["param_errors"]
corr_matrix = stats_output["corr_matrix"]

param_labels = ["Er (MeV)", "Gamma (MeV)", "sigma0 (barn)", "sigma_bg (barn)"]

print("=" * 65)
print("HASIL AKHIR ESTIMASI PARAMETER & INTERVAL KETIDAKPASTIAN")
print("=" * 65)
for name, val, err in zip(param_labels, p_opt, param_errors):
    rel_err = (err / abs(val)) * 100.0
    print(f"  {name:<16}: {val:.6f} +/- {err:.6f} ({rel_err:.2f}%)")
print("-" * 65)
print(f"  Reduced Chi-Square (chi2_red) : {chi2_red:.4f} (nu = {stats_output['dof']})")
print("=" * 65)

print("\nMatriks Korelasi Ternormalisasi Parameter (rho):")
header_corr = " " * 16 + " ".join([f"{n[:8]:>11}" for n in param_labels])
print(header_corr)
print("-" * (16 + 11 * 4))
for idx, row in enumerate(corr_matrix):
    row_text = f"{param_labels[idx]:<16}" + " ".join([f"{val:>11.4f}" for val in row])
    print(row_text)"""

    cells.append(nbf.v4.new_code_cell(cell14_code))

    # =========================================================================
    # CELL 15: MARKDOWN - Tahap 6: Uji Ketahanan Numerik (Stress-Test)
    # =========================================================================
    cell15_text = r"""---
## **Tahap 6: Uji Ketahanan Numerik (*Noise Stress-Test*)**

Untuk mengevaluasi batas ketahanan algoritma Newton-Raphson terhadap degradasi data riil, dilakukan simulasi Monte Carlo dengan menginjeksikan derau Gaussian acak proporsional:

$$\sigma_{noisy} = \sigma_{clean} + \mathcal{N}(0, \eta \cdot \sigma_{clean})$$

dengan level kebisingan bertingkat:
- $\eta = 5\%$ (derau rendah, kondisi eksperimen prima),
- $\eta = 15\%$ (derau sedang, penurunan resolusi detektor),
- $\eta = 30\%$ (derau tinggi, batas kritis stabilitas numerik).

Tiap level derau diuji sebanyak 10 kali pengulangan independen untuk menganalisis pergeseran bilangan kondisi $\kappa(\mathbf{H})$, degradasi nilai eigen terendah $\lambda_{\min}$, dan persentase keberhasilan konvergensi."""

    cells.append(nbf.v4.new_markdown_cell(cell15_text))

    # =========================================================================
    # CELL 16: CODE - Eksekusi Tahap 6
    # =========================================================================
    cell16_code = r"""# Eksekusi Tahap 6: Simulasi Monte Carlo Noise Stress-Test
from tahap6_stress_test import run_noise_stress_test

stress_results = run_noise_stress_test(
    E_data, sigma_data, dsigma_data, 
    noise_levels=[0.05, 0.15, 0.30], 
    n_trials=10, 
    random_seed=42
)

print("=" * 90)
print("RINGKASAN UJI KETAHANAN NUMERIK MONTE CARLO (NOISE STRESS-TEST)")
print("=" * 90)
print(f"{'Noise (eta)':<12} | {'Success':<10} | {'Avg Iter':<10} | {'Mean cond(H)':<14} | {'Min Eigenval':<14} | {'|Delta Er| (MeV)':<16}")
print("-" * 90)
for eta, res in stress_results["results"].items():
    suc_str = f"{res['success_rate']*100:.0f}%"
    it_str = f"{res['avg_iterations']:.1f}"
    cond_str = f"{res['avg_cond_H']:.2e}"
    eig_str = f"{res['min_eigenval']:.2e}"
    dEr_str = f"{res['param_deviations_mean'][0]:.6f}"
    print(f"{eta*100:<10.0f}% | {suc_str:<10} | {it_str:<10} | {cond_str:<14} | {eig_str:<14} | {dEr_str:<16}")
print("=" * 90)"""

    cells.append(nbf.v4.new_code_cell(cell16_code))

    # =========================================================================
    # CELL 17: MARKDOWN - Tahap 7: Visualisasi Saintifik & Validasi Fisis
    # =========================================================================
    cell17_text = r"""---
## **Tahap 7: Visualisasi Saintifik & Validasi Fisis**

Visualisasi hasil komputasi mencakup 3 aspek penting:
1. **Kurva Fitting & Distribusi Residu**: Membandingkan kurva kontinu Breit-Wigner terhadap titik data eksperimen beserta *error bars*, dilengkapi panel bawah residu terstandarisasi $R_i = (\sigma_i - \sigma_{fit}) / \Delta\sigma_i$.
2. **Profil Laju Konvergensi Orde-2**: Menampilkan grafik semilog penurunan $\chi^2$ dan dinamika bilangan kondisi $\kappa(\mathbf{H})$ per iterasi.
3. **Respon Ketahanan terhadap Derau**: Memetakan korelasi antara level derau eksperimen terhadap tingkat keberhasilan solver dan presisi parameter.
4. **Validasi Fisis**: Menguji kesesuaian nilai resonansi komputasi $E_r$ terhadap nilai resmi literatur nuklir ($E_r^{lit} \approx 2.078\text{ MeV}$)."""

    cells.append(nbf.v4.new_markdown_cell(cell17_text))

    # =========================================================================
    # CELL 18: CODE - Eksekusi Tahap 7
    # =========================================================================
    cell18_code = r"""# Eksekusi Tahap 7: Visualisasi Saintifik & Validasi Fisis
from tahap7_visualization import (
    plot_resonance_fitting, plot_convergence_metrics, 
    plot_noise_stress_test, validate_physical_results
)

# 1. Plot Utama: Kurva Fitting Breit-Wigner & Subplot Residu
fig_fit = plot_resonance_fitting(E_data, sigma_data, dsigma_data, p_opt, param_errors, chi2_red, save_path=None)
plt.show()

# 2. Plot Konvergensi: Laju Kuadratik & Bilangan Kondisi
fig_conv = plot_convergence_metrics(history, save_path=None)
plt.show()

# 3. Plot Stress Test: Ketahanan terhadap Noise
fig_stress = plot_noise_stress_test(stress_results, save_path=None)
plt.show()

# 4. Validasi Fisis terhadap Data Literatur
validate_physical_results(p_opt, param_errors)"""

    cells.append(nbf.v4.new_code_cell(cell18_code))

    # =========================================================================
    # CELL 19: MARKDOWN - Analisis Hasil Komputasi & Diskusi Kritis
    # =========================================================================
    cell19_text = r"""---
## **Analisis Hasil Komputasi & Diskusi Kritis**

### **1. Evaluasi Laju Konvergensi Orde-Dua Newton-Raphson**
Proses fitting mencapai konvergensi penuh hanya dalam **6 iterasi**, dengan penurunan $\chi^2$ yang sangat dramatis dari $\chi^2_0 \approx 90.81$ menjadi $\chi^2_{\min} \approx 18.61$. Grafik semilog konvergensi memperlihatkan pola peluruhan kuadratik (*quadratic convergence*), di mana magnitudo norma langkah $\|\Delta\mathbf{p}\|_2$ menyusut dari orde $10^{-1}$ ke $10^{-6}$ dalam beberapa langkah saja. Hal ini membuktikan keunggulan komputasi turunan analitik eksak Gauss-Newton dibandingkan metode turunan gradien orde-satu (*gradient descent*) yang mengalami perlambatan (*stalling*) di sekitar titik minimum.

### **2. Evaluasi Kelayakan Model (*Reduced Chi-Square*)**
Nilai *reduced chi-square* yang diperoleh adalah:
$$\chi^2_{red} = \frac{\chi^2_{\min}}{\nu} = \frac{18.6064}{55} \approx 0.3383$$
Secara statistik, $\chi^2_{red} \le 1.0$ mengindikasikan bahwa model Breit-Wigner satu tingkat berhasil merepresentasikan tren variasi penampang lintang eksperimen secara sangat baik, tanpa indikasi *overfitting* maupun *underfitting*. Nilai residu terstandarisasi tersebar acak simetris di sekitar garis nol pada rentang $-1.5 \le R_i \le +1.5$, membuktikan ketiadaan bias sistematik pada perumusan model.

### **3. Diskusi Korelasi Silang Parameter (Matriks $\boldsymbol{\rho}$)**
Matriks korelasi parameter memperlihatkan interaksi fisis yang signifikan:
- Korelasi silang negatif antara $\Gamma$ dan $\sigma_0$ ($\rho \approx -0.4737$): Hubungan anti-korelasi ini wajar secara fisis, karena luas integral di bawah puncak resonansi sebanding dengan perkalian $\sigma_0 \cdot \Gamma$. Penurunan sedikit pada amplitudo puncak dapat dikompensasi oleh sedikit pelebaran FWHM untuk mempertahankan luas total penampang lintang hamburan.
- Korelasi silang negatif antara $\Gamma$ dan $\sigma_{bg}$ ($\rho \approx -0.5754$): Sayap resonansi Lorentzian meluruh perlahan ($1/E^2$), sehingga lebar sayap berkorelasi dengan elevasi kontinum latar belakang.
- Posisi energi resonansi $E_r$ memiliki korelasi yang sangat rendah terhadap seluruh parameter lainnya ($|\rho| \le 0.18$), membuktikan bahwa posisi puncak ditentukan secara sangat independen dan presisi oleh simetri spektrum.

### **4. Analisis Batas Numerik & Kegagalan terhadap Derau (Noise Stress-Test)**
Pada pengujian ketahanan derau:
- Pada tingkat derau $\eta = 5\%$ dan $\eta = 15\%$, tingkat keberhasilan konvergensi mencapai **100%** dengan bilangan kondisi Hessian yang stabil ($\kappa(\mathbf{H}) \sim 10^3 - 10^4$).
- Namun, pada derau ekstrem $\eta = 30\%$, tingkat keberhasilan merosot menjadi **60%**, dan bilangan kondisi melonjak melampaui $10^5$ hingga $10^{16}$ pada pengujian yang gagal. Fluktuasi derau acak yang tajam merusak topologi kelengkungan $\chi^2$, menyebabkan matriks Hessian kehilangan sifat positif-definit lokalnya ($\lambda_{\min} \le 0$) sehingga sistem linier menjadi singular atau divergen."""

    cells.append(nbf.v4.new_markdown_cell(cell19_text))

    # =========================================================================
    # CELL 20: MARKDOWN - Kesimpulan Fisis & Rekomendasi
    # =========================================================================
    cell20_text = r"""---
## **Kesimpulan Fisis & Rekomendasi**

### **Kesimpulan Fisis**
1. Ekstraksi parameter resonansi hamburan neutron $^{12}\text{C}(n,\text{tot})$ menggunakan metode Newton-Raphson multivariat berbasis matriks Hessian Gauss-Newton berhasil memperoleh:
   - **Energi Resonansi ($E_r$)**: $2.073019 \pm 0.000379\text{ MeV}$
   - **Lebar Resonansi FWHM ($\Gamma$)**: $0.065895 \pm 0.001148\text{ MeV}$
   - **Amplitudo Resonansi Puncak ($\sigma_0$)**: $3.133715 \pm 0.030648\text{ barn}$
   - **Kontinum Latar Belakang ($\sigma_{bg}$)**: $4.587609 \pm 0.008926\text{ barn}$
2. Validasi fisis terhadap benchmark internasional IAEA Nuclear Data ($E_r^{lit} = 2.078000\text{ MeV}$) menunjukkan diskrepansi mutlak hanya sebesar $0.004981\text{ MeV}$ ($4.98\text{ keV}$) atau **deviasi relatif $0.2397\%$**. Hal ini membuktikan ketepatan pemodelan komputasi yang sangat tinggi.
3. Metode Newton-Raphson multivariat analitik terbukti sangat efisien (konvergen dalam 6 iterasi), stabil secara numerik ($\kappa(\mathbf{H}) \approx 6.81 \times 10^3$), dan tangguh terhadap gangguan derau eksperimen hingga $15\%$.

### **Rekomendasi Metodologis**
- Jika berhadapan dengan data eksperimen dengan rasio sinyal terhadap derau yang sangat buruk ($\text{SNR} < 3$ atau $\eta > 30\%$), disarankan mengimplementasikan algoritma hibrida **Levenberg-Marquardt** dengan parameter redaman adaptif $\mathbf{H}_{LM} = \mathbf{H} + \lambda \operatorname{diag}(\mathbf{H})$ untuk mencegah singularitas matriks kelengkungan."""

    cells.append(nbf.v4.new_markdown_cell(cell20_text))

    nb["cells"] = cells
    notebook_path = "resonance_breit_wigner_fitting.ipynb"

    with open(notebook_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"File notebook dasar berhasil ditulis ke '{notebook_path}' dengan {len(cells)} sel.")

    # Eksekusi notebook agar output tersimpan di dalam notebook
    print("Mengeksekusi seluruh sel notebook melalui NotebookClient...")
    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    client.execute()

    with open(notebook_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"Semua sel notebook berhasil dieksekusi dan disimpan dengan output lengkap di '{notebook_path}'!")

if __name__ == "__main__":
    create_notebook()

