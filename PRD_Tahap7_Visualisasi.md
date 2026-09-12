# PRD Tahap 7: Visualisasi Saintifik & Validasi Fisis

## Tujuan & Deliverable

Menghasilkan visualisasi kurva resonansi terstandarisasi publikasi ilmiah, subplot residual terbobot, peta konvergensi $\chi^2$, serta memvalidasi kesesuaian nilai $E_r$ dan $\Gamma$ terhadap data nuklir standar inti $^{12}\text{C}$.

## Spesifikasi Fungsional

- Menampilkan kurva fitting Breit-Wigner kontinu bersama titik data eksperimen dan *error bars*.
- Menampilkan panel residual terstandarisasi: $R_i = (\sigma_i - \sigma_{fit}) / \Delta\sigma_i$.
- Menampilkan grafik semilog penurunan $\chi^2$ dan $\kappa(\mathbf{H})$ terhadap nomor iterasi untuk membuktikan laju konvergensi kuadratik.
- Membandingkan nilai akhir $E_r$ terhadap nilai literatur ($E_r^{lit} \approx 2.078\text{ MeV}$).

## Struktur & Blueprint Kode

```python
# Modul: tahap7_visualization.py
import matplotlib.pyplot as plt
import numpy as np

def plot_resonance_fitting(E, sigma, dsigma, p_opt, p_err) -> None:
    """Visualisasi utama: Titik eksperimen, kurva kontinu fitting, dan residual plot."""
    ...

def plot_convergence_metrics(history: dict) -> None:
    """Visualisasi 2-panel: Penurunan chi-square dan dinamika condition number per iterasi."""
    ...
```
