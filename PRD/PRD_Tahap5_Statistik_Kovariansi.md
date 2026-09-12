# PRD Tahap 5: Evaluasi Statistik, Matriks Kovariansi, & Analisis Galat

## Tujuan & Deliverable

Menghitung ketidakpastian statistik parameter optimal hasil fitting, matriks korelasi antar-parameter, dan parameter kelayakan fisis *reduced chi-square* ($\chi^2_{red}$).

## Spesifikasi Fungsional

- Menghitung derajat kebebasan: $\nu = N - m$, dengan $N$ jumlah titik data dan $m = 4$ parameter.
- Menghitung *Reduced Chi-Square*: $\chi^2_{red} = \chi^2_{\min} / \nu$.
- Menghitung Matriks Kovariansi Asimptotik Parameter: $\mathbf{C} = 2 [\mathbf{H}(\mathbf{p}^*)]^{-1}$.
- Mengekstrak simpangan baku parameter: $\delta p_j = \sqrt{C_{jj} \cdot \chi^2_{red}}$.
- Menghitung Matriks Korelasi Ternormalisasi: $\rho_{jk} = C_{jk} / \sqrt{C_{jj} C_{kk}}$ untuk mengidentifikasi derajat korelasi silang antara $\Gamma$ dan $\sigma_0$.

## Struktur & Blueprint Kode

```python
# Modul: tahap5_statistical_analysis.py
import numpy as np

def compute_statistics_and_covariance(
    p_opt: np.ndarray, 
    H_opt: np.ndarray, 
    chi2_min: float, 
    n_data: int
) -> dict:
    """
    Kalkulasi reduksi chi-square, matriks kovariansi, dan batas ketidakpastian parameter.
    Returns: dict berisi 'chi2_red', 'cov_matrix', 'param_errors', 'corr_matrix'
    """
    ...
```
