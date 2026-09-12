# PRD Tahap 6: Uji Ketahanan Numerik (*Noise Stress-Test*)

## Tujuan & Deliverable

Menguji batas kestabilan dan titik kegagalan (*failure modes*) algoritma Newton-Raphson terhadap degradasi data eksperimen dengan menginjeksikan gangguan *Gaussian noise* bertingkat ($\pm 5\%$, $\pm 15\%$, $\pm 30\%$).

## Spesifikasi Fungsional

- Menghasilkan data perturbasi sintetik: $\sigma_{noisy} = \sigma_{clean} + \mathcal{N}(0, \eta \cdot \sigma_{clean})$.
- Menjalankan fitting Newton-Raphson pada tiap tingkatan noise $\eta \in [0.01, 0.35]$.
- Memetakan korelasi antara level noise $\eta$ terhadap lonjakan bilangan kondisi matriks $\kappa(\mathbf{H})$, pergeseran nilai eigen terendah ($\lambda_{\min} \le 0$), serta jumlah iterasi menuju divergensi.

## Struktur & Blueprint Kode

```python
# Modul: tahap6_stress_test.py
import numpy as np

def run_noise_stress_test(
    E: np.ndarray, 
    sigma_clean: np.ndarray, 
    dsigma: np.ndarray, 
    noise_levels: list = [0.05, 0.15, 0.30], 
    n_trials: int = 10
) -> dict:
    """
    Simulasi Monte Carlo ketahanan numerik terhadap noise.
    Returns: dict ringkasan keberhasilan konvergensi, mean condition number, dan deviasi parameter.
    """
    ...
```
