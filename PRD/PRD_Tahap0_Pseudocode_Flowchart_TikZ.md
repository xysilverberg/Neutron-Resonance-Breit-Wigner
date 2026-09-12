# PRD Tahap 0: Perancangan Pseudocode & Flowchart (LaTeX TikZ)

## Posisi dalam Alur Pengerjaan Proyek

Tahap ini adalah **titik masuk (entry point) eksekusi** dari keseluruhan proyek dan **wajib dikerjakan sebelum** membaca atau mengimplementasikan PRD Tahap 1-7 maupun PRD Arsitektur Jupyter Notebook. Urutan alur kerja resmi proyek adalah sebagai berikut:

```
┌─────────────────────────────────────────────────────────────────┐
│  URUTAN ALUR PENGERJAAN PROYEK (WORKFLOW ORDER)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│   [1] PRD Tahap 0                                                │
│       Pseudocode & Flowchart (LaTeX TikZ)      <-- MULAI DI SINI │
│                        │                                         │
│                        ▼                                         │
│   [2] PRD Tahap 1 - Akuisisi Data & Pipeline CSV                 │
│                        │                                         │
│                        ▼                                         │
│   [3] PRD Tahap 2 - Gradien & Hessian                            │
│                        │                                         │
│                        ▼                                         │
│   [4] PRD Tahap 3 - Ekstraksi Tebakan Awal (p0)                  │
│                        │                                         │
│                        ▼                                         │
│   [5] PRD Tahap 4 - Solver Newton-Raphson                        │
│                        │                                         │
│                        ▼                                         │
│   [6] PRD Tahap 5 - Statistik & Kovariansi                       │
│                        │                                         │
│                        ▼                                         │
│   [7] PRD Tahap 6 - Uji Ketahanan Numerik (Noise Stress-Test)    │
│                        │                                         │
│                        ▼                                         │
│   [8] PRD Tahap 7 - Visualisasi Saintifik & Validasi Fisis       │
│                        │                                         │
│                        ▼                                         │
│   [9] PRD Arsitektur Jupyter Notebook (.ipynb)   <-- FINAL       │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

**Rasional urutan**: Pseudocode dan flowchart berfungsi sebagai peta logika keseluruhan sistem (blueprint algoritmik tingkat tinggi) sebelum masuk ke detail implementasi per-modul di Tahap 1-7. Dengan memahami alur logika penuh terlebih dahulu, setiap spesifikasi fungsional pada PRD Tahap 1-7 dapat dipetakan langsung ke node/langkah yang bersesuaian pada flowchart, dan struktur sel PRD Arsitektur Jupyter Notebook pada akhirnya menjadi representasi eksekutif dari flowchart yang sama.

---

## Tujuan & Deliverable

Membangun representasi algoritmik tingkat tinggi (pseudocode terstruktur) dan visualisasi diagram alir (flowchart) dari keseluruhan pipeline komputasi — mulai dari akuisisi data EXFOR hingga visualisasi hasil fitting Breit-Wigner — menggunakan sintaks LaTeX dengan paket TikZ, sebagai artefak rujukan algoritmik sebelum implementasi kode per-tahap dimulai.

**Deliverable**:
1. File `pseudocode_algoritma_utama.tex` — pseudocode lengkap seluruh pipeline (Tahap 1-7) dalam format `algorithm`/`algorithmic` atau `algorithm2e`.
2. File `flowchart_pipeline.tex` — flowchart penuh dalam sintaks TikZ (paket `tikz` dengan `library shapes.geometric, arrows.meta, positioning`).
3. (Opsional) File `flowchart_pipeline.pdf` hasil kompilasi, untuk disisipkan sebagai gambar referensi di Cell Markdown notebook (Tahap 0 pada PRD Arsitektur Jupyter Notebook).

## Spesifikasi Fungsional

### A. Pseudocode

- Mencakup **seluruh 7 tahap** pipeline dalam satu algoritma induk (`ALGORITHM MainPipeline`), dengan sub-prosedur bernomor mengikuti struktur modul:
  1. `FetchAndParseEXFOR()` — akuisisi & parsing data mentah (Tahap 1).
  2. `BreitWignerModel(E, p)`, `Chi2(p)`, `Gradient(p)`, `Hessian(p)` — formulasi analitik (Tahap 2).
  3. `EstimateInitialGuess(E, sigma)` — heuristik $\mathbf{p}_0$ (Tahap 3).
  4. `NewtonRaphsonSolve(p0, tol, max_iter)` — loop iteratif inti, termasuk kondisi berhenti dan pengecekan *condition number* (Tahap 4).
  5. `ComputeCovarianceAndErrors(p_opt, H_opt)` — evaluasi statistik akhir (Tahap 5).
  6. `NoiseStressTest(E, sigma_clean, noise_levels)` — simulasi Monte Carlo ketahanan (Tahap 6).
  7. `VisualizeResults(...)` — pembangkitan grafik akhir (Tahap 7).
- Notasi pseudocode menggunakan gaya baku akademik: `INPUT`, `OUTPUT`, `BEGIN...END`, indentasi blok `IF/WHILE/FOR`, dan komentar bertanda `▷` atau `//`.
- Setiap langkah kritis numerik (mis. solusi sistem linier $\mathbf{H}\Delta\mathbf{p} = -\mathbf{g}$, kriteria konvergensi $\Vert\Delta\mathbf{p}\Vert < \varepsilon$) dituliskan eksplisit sebagai baris pseudocode, bukan sekadar deskripsi naratif.

### B. Flowchart (TikZ)

- Menggunakan simbol standar flowchart:
  - **Terminator** (oval/`ellipse`) untuk *Start*/*End*.
  - **Proses** (persegi panjang/`rectangle, rounded corners`) untuk langkah komputasi (mis. "Hitung Gradien & Hessian").
  - **Input/Output** (jajar genjang/`trapezium` atau `parallelogram`) untuk akuisisi data & ekspor CSV/plot.
  - **Decision** (belah ketupat/`diamond`) untuk titik percabangan logis: cek konvergensi ($\Vert\Delta\mathbf{p}\Vert < 10^{-6}$?), cek keberhasilan jaringan (fallback data), cek *ill-conditioning* ($\kappa(\mathbf{H})$ terlalu besar?).
  - **Panah berarah** (`arrows.meta`, gaya `-Stealth`) menghubungkan tiap node sesuai urutan eksekusi, termasuk **panah balik (loop-back)** dari node keputusan "Belum Konvergen" menuju node "Update $\mathbf{p}^{(k+1)} = \mathbf{p}^{(k)} + \Delta\mathbf{p}$".
- Flowchart mencakup satu alur besar dari *Start* (unduh data EXFOR) hingga *End* (visualisasi & validasi fisis), dengan percabangan eksplisit untuk:
  - Jalur *fallback* jika unduhan data EXFOR gagal (Tahap 1).
  - Loop iteratif Newton-Raphson beserta kondisi berhenti gandanya (Tahap 4).
  - Jalur tambahan cabang uji stress-test noise sebagai sub-alur paralel opsional (Tahap 6), digambarkan dengan node bertipe *subprocess* (`rectangle, double`).
- Layout flowchart disusun vertikal (top-to-bottom) agar dapat dibaca linear searah alur notebook, dengan pengelompokan visual (`\begin{scope}` atau `fit`/`background` layer) per tahap PRD 1-7 agar korespondensi tahap terlihat jelas.

## Struktur & Blueprint Kode

```latex
% File: pseudocode_algoritma_utama.tex
\documentclass{article}
\usepackage[ruled,vlined,linesnumbered]{algorithm2e}
\usepackage{amsmath}

\begin{document}

\begin{algorithm}[H]
\caption{MainPipeline -- Fitting Resonansi Breit-Wigner $^{12}$C(n,tot)}
\KwIn{Target nuklida, rentang energi $[E_{\min}, E_{\max}]$}
\KwOut{$\mathbf{p}^{*}$, $\chi^2_{red}$, matriks kovariansi $\mathbf{C}$, grafik hasil}

\tcp{Tahap 1: Akuisisi \& Parsing Data}
raw $\leftarrow$ FetchEXFORRaw(target, reaction)\;
\If{raw gagal diunduh}{
    raw $\leftarrow$ FallbackCalibratedDataset()\;
}
$(E, \sigma, \Delta\sigma) \leftarrow$ ParseEXFORAscii(raw)\;
ExportToCSV($E, \sigma, \Delta\sigma$)\;

\tcp{Tahap 3: Tebakan Awal}
$\mathbf{p}_0 \leftarrow$ EstimateInitialGuess($E$, $\sigma$)\;

\tcp{Tahap 4: Newton-Raphson Multivariat}
$\mathbf{p} \leftarrow \mathbf{p}_0$\;
\Repeat{$\Vert\Delta\mathbf{p}\Vert < \varepsilon$ \textbf{atau} $\vert\chi^2_{k+1}-\chi^2_k\vert < \varepsilon$ \textbf{atau} $k \geq k_{\max}$}{
    \tcp{Tahap 2: Turunan Analitik}
    $\mathbf{g} \leftarrow$ ComputeGradient($\mathbf{p}$, $E$, $\sigma$, $\Delta\sigma$)\;
    $\mathbf{H} \leftarrow$ ComputeHessian($\mathbf{p}$, $E$, $\sigma$, $\Delta\sigma$)\;
    $\kappa \leftarrow$ ConditionNumber($\mathbf{H}$)\;
    \If{$\kappa$ terlalu besar}{
        \textbf{tandai ill-conditioned}; \textbf{break}\;
    }
    Selesaikan $\mathbf{H}\, \Delta\mathbf{p} = -\mathbf{g}$ \tcp*{np.linalg.solve}
    $\mathbf{p} \leftarrow \mathbf{p} + \Delta\mathbf{p}$\;
    Simpan riwayat: $\mathbf{p}$, $\chi^2(\mathbf{p})$, $\Vert\mathbf{g}\Vert$, $\kappa$\;
}
$\mathbf{p}^{*} \leftarrow \mathbf{p}$\;

\tcp{Tahap 5: Statistik \& Kovariansi}
$\nu \leftarrow N - 4$\;
$\chi^2_{red} \leftarrow \chi^2(\mathbf{p}^{*}) / \nu$\;
$\mathbf{C} \leftarrow 2\,\mathbf{H}(\mathbf{p}^{*})^{-1}$\;
$\delta p_j \leftarrow \sqrt{C_{jj}\cdot \chi^2_{red}}$ untuk setiap $j$\;

\tcp{Tahap 6: Uji Ketahanan Noise (opsional/paralel)}
\ForEach{$\eta \in \{0.05, 0.15, 0.30\}$}{
    Ulangi solver Newton-Raphson pada data $\sigma + \mathcal{N}(0, \eta\sigma)$\;
    Catat $\kappa(\mathbf{H})$, $\lambda_{\min}$, status konvergensi\;
}

\tcp{Tahap 7: Visualisasi}
PlotResonanceFitting($E$, $\sigma$, $\Delta\sigma$, $\mathbf{p}^{*}$, $\delta p$)\;
PlotConvergenceMetrics(riwayat)\;

\Return{$\mathbf{p}^{*}$, $\chi^2_{red}$, $\mathbf{C}$}\;
\end{algorithm}

\end{document}
```

```latex
% File: flowchart_pipeline.tex
\documentclass[tikz, border=10pt]{standalone}
\usetikzlibrary{shapes.geometric, arrows.meta, positioning, fit, backgrounds}

\begin{document}
\begin{tikzpicture}[
    node distance=1.1cm and 1.6cm,
    start/.style   = {ellipse, draw, fill=green!15, minimum width=2.6cm, minimum height=0.9cm},
    io/.style      = {trapezium, trapezium left angle=70, trapezium right angle=110, draw, fill=blue!10, minimum width=3cm, minimum height=0.9cm, align=center},
    process/.style = {rectangle, rounded corners, draw, fill=yellow!15, minimum width=3.4cm, minimum height=0.9cm, align=center},
    decision/.style= {diamond, draw, fill=orange!15, aspect=2, align=center, inner sep=1pt},
    subproc/.style = {rectangle, double, draw, fill=purple!10, minimum width=3.4cm, minimum height=0.9cm, align=center},
    endnode/.style = {ellipse, draw, fill=red!15, minimum width=2.6cm, minimum height=0.9cm},
    arrow/.style   = {-Stealth, thick}
]

% --- Tahap 1 ---
\node[start] (start) {Start};
\node[io, below=of start] (fetch) {Unduh data EXFOR\\ (Tahap 1)};
\node[decision, below=of fetch] (netok) {Jaringan\\ berhasil?};
\node[io, right=2.4cm of netok] (fallback) {Gunakan data\\ fallback kalibrasi};
\node[process, below=of netok] (parse) {Parsing ASCII (Regex)\\ $\rightarrow$ Ekspor CSV};

% --- Tahap 3 ---
\node[process, below=of parse] (p0) {Estimasi $\mathbf{p}_0$\\ (peak, FWHM) (Tahap 3)};

% --- Tahap 2 & 4 ---
\node[process, below=of p0] (gradhess) {Hitung $\mathbf{g}(\mathbf{p})$, $\mathbf{H}(\mathbf{p})$\\ (Tahap 2)};
\node[process, below=of gradhess] (solve) {Selesaikan $\mathbf{H}\Delta\mathbf{p}=-\mathbf{g}$\\ Update $\mathbf{p} \leftarrow \mathbf{p}+\Delta\mathbf{p}$ (Tahap 4)};
\node[decision, below=of solve] (conv) {Konvergen?\\ ($\Vert\Delta\mathbf{p}\Vert<10^{-6}$)};

% --- Tahap 5 ---
\node[process, below=of conv] (stats) {Hitung $\chi^2_{red}$, $\mathbf{C}$,\\ $\delta p_j$, $\rho_{jk}$ (Tahap 5)};

% --- Tahap 6 (paralel) ---
\node[subproc, right=3.2cm of stats] (stress) {Noise Stress-Test\\ $\eta=5\%,15\%,30\%$ (Tahap 6)};

% --- Tahap 7 ---
\node[process, below=of stats] (viz) {Plot fitting, residual,\\ konvergensi $\chi^2$ (Tahap 7)};
\node[endnode, below=of viz] (end) {End};

% --- Arrows ---
\draw[arrow] (start) -- (fetch);
\draw[arrow] (fetch) -- (netok);
\draw[arrow] (netok) -- node[right]{Tidak} (fallback);
\draw[arrow] (fallback) |- (parse);
\draw[arrow] (netok) -- node[left]{Ya} (parse);
\draw[arrow] (parse) -- (p0);
\draw[arrow] (p0) -- (gradhess);
\draw[arrow] (gradhess) -- (solve);
\draw[arrow] (solve) -- (conv);
\draw[arrow] (conv.east) -- ++(1.8,0) |- node[pos=0.25, right]{Belum} (gradhess.east);
\draw[arrow] (conv) -- node[left]{Ya} (stats);
\draw[arrow] (stats) -- (viz);
\draw[arrow] (stats.east) -- (stress.west);
\draw[arrow] (stress.south) |- (viz.east);
\draw[arrow] (viz) -- (end);

% --- Pengelompokan visual per PRD tahap (opsional) ---
\begin{scope}[on background layer]
\node[fit=(fetch)(netok)(fallback)(parse), draw=blue!40, dashed, inner sep=6pt, label=left:{\scriptsize PRD T1}] {};
\node[fit=(gradhess), draw=teal!40, dashed, inner sep=6pt, label=left:{\scriptsize PRD T2}] {};
\node[fit=(p0), draw=violet!40, dashed, inner sep=6pt, label=left:{\scriptsize PRD T3}] {};
\node[fit=(solve)(conv), draw=orange!50, dashed, inner sep=6pt, label=left:{\scriptsize PRD T4}] {};
\node[fit=(stats), draw=brown!50, dashed, inner sep=6pt, label=left:{\scriptsize PRD T5}] {};
\node[fit=(stress), draw=purple!50, dashed, inner sep=6pt, label=right:{\scriptsize PRD T6}] {};
\node[fit=(viz), draw=red!40, dashed, inner sep=6pt, label=left:{\scriptsize PRD T7}] {};
\end{scope}

\end{tikzpicture}
\end{document}
```

## Kriteria Penerimaan (Acceptance Criteria)

- Kedua file `.tex` dapat dikompilasi tanpa error menggunakan distribusi LaTeX standar (mis. TeX Live) dengan paket `algorithm2e` dan `tikz` (`shapes.geometric`, `arrows.meta`, `positioning`, `fit`, `backgrounds`).
- Setiap node/langkah pada flowchart memiliki **korespondensi satu-ke-satu** dengan minimal satu poin spesifikasi fungsional pada PRD Tahap 1-7, ditandai label tahap (`PRD T1`...`PRD T7`) pada flowchart.
- Pseudocode mencakup seluruh formula kunci (model Breit-Wigner, $\chi^2$, gradien, Hessian, kriteria konvergensi, kovariansi) secara eksplisit, bukan hanya nama fungsi.
- Output PDF hasil kompilasi (jika dibuat) siap disisipkan sebagai gambar pada Cell Markdown tambahan di awal notebook (lihat catatan integrasi di bawah).

## Catatan Integrasi dengan PRD Arsitektur Jupyter Notebook

Karena Tahap 0 dikerjakan **sebelum** PRD Arsitektur Jupyter Notebook, disarankan menambahkan **Cell Markdown baru di posisi paling awal notebook** (sebelum Cell 1 pada struktur asli, atau disisipkan sebagai bagian dari Cell 1) yang berisi:
- Gambar hasil render `flowchart_pipeline.pdf`/`.png` sebagai peta alur keseluruhan.
- Cuplikan pseudocode `MainPipeline` sebagai rujukan algoritmik sebelum narasi teori dimulai pada Cell 2-3.

Dengan demikian, urutan pembacaan dokumen proyek secara keseluruhan menjadi:

**PRD Tahap 0 (Pseudocode & Flowchart) → PRD Tahap 1 → PRD Tahap 2 → PRD Tahap 3 → PRD Tahap 4 → PRD Tahap 5 → PRD Tahap 6 → PRD Tahap 7 → PRD Arsitektur Jupyter Notebook**
