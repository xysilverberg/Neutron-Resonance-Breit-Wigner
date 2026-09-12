# PRD Tahap 3: Ekstraksi Otomatis Tebakan Parameter Awal ($\mathbf{p}_0$)

## Tujuan & Deliverable

Membangun modul heuristik fisika eksperimen untuk mengekstraksi nilai tebakan awal $\mathbf{p}_0 = [E_r^{(0)}, \Gamma^{(0)}, \sigma_0^{(0)}, \sigma_{bg}^{(0)}]^T$ secara otomatis dari bentuk kurva data terukur, mengeliminasi tebakan acak yang berisiko memicu divergensi pada Newton-Raphson.

## Spesifikasi Fungsional

- Menentukan $E_r^{(0)}$ dari posisi energi dengan nilai penampang lintang maksimum ($\arg\max \sigma_i$).
- Menentukan $\sigma_{bg}^{(0)}$ dari kuantil bawah atau rata-rata batas tepi energi ($E_{\min}, E_{\max}$).
- Menghitung $\sigma_0^{(0)} = \sigma_{\max} - \sigma_{bg}^{(0)}$.
- Mengestimasi $\Gamma^{(0)}$ melalui algoritma interpolasi lebar separuh puncak (*Full Width at Half Maximum* / FWHM) di atas tingkat $\sigma_{half} = \sigma_{bg}^{(0)} + 0.5 \sigma_0^{(0)}$.

## Struktur & Blueprint Kode

```python
# Modul: tahap3_initial_guess.py
import numpy as np

def extract_initial_parameters(E: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    """
    Ekstraksi otomatis parameter awal fisis:
    Returns: p0 = np.array([Er_0, Gamma_0, sigma0_0, sigma_bg_0])
    """
    idx_peak = np.argmax(sigma)
    Er_0 = E[idx_peak]
    sigma_bg_0 = float(np.min([sigma[0], sigma[-1]]))
    sigma0_0 = float(sigma[idx_peak] - sigma_bg_0)

    # FWHM heuristic
    half_val = sigma_bg_0 + 0.5 * sigma0_0
    mask_above = sigma >= half_val
    energies_above = E[mask_above]
    Gamma_0 = float(energies_above[-1] - energies_above[0]) if len(energies_above) > 1 else 0.05

    return np.array([Er_0, Gamma_0, sigma0_0, sigma_bg_0], dtype=np.float64)
```
