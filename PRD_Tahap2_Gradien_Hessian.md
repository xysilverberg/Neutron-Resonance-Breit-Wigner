# PRD Tahap 2: Formulasi Analitik Gradien & Matriks Hessian

## Tujuan & Deliverable

Membangun fungsi matematis murni untuk model penampang lintang Breit-Wigner satu tingkat (*single-level*), fungsi objektif $\chi^2$, serta turunan analitik gradien $\mathbf{g}(\mathbf{p})$ ($4\times1$) dan matriks Hessian $\mathbf{H}(\mathbf{p})$ ($4\times4$) berbasis operasi vektorisasi NumPy tanpa diferensiasi numerik beda hingga.

## Spesifikasi Fungsional

**Model Fisis**:

$$\sigma(E_i; \mathbf{p}) = \sigma_{bg} + \sigma_0 \frac{(\Gamma / 2)^2}{(E_i - E_r)^2 + (\Gamma / 2)^2}$$

dengan parameter $\mathbf{p} = [E_r, \Gamma, \sigma_0, \sigma_{bg}]^T$.

**Fungsi Bobot Kuadrat Terkecil ($\chi^2$)**:

$$\chi^2(\mathbf{p}) = \sum_{i=1}^N \left( \frac{\sigma_i - \sigma(E_i; \mathbf{p})}{\Delta\sigma_i} \right)^2$$

**Gradien Analitik $\mathbf{g}(\mathbf{p}) = \nabla \chi^2$**:

Vektor $4 \times 1$ dari $\frac{\partial \chi^2}{\partial p_j} = -2 \sum_{i=1}^N \frac{\sigma_i - \sigma(E_i; \mathbf{p})}{(\Delta\sigma_i)^2} \frac{\partial \sigma(E_i; \mathbf{p})}{\partial p_j}$.

**Matriks Hessian Analitik $\mathbf{H}(\mathbf{p}) = \nabla^2 \chi^2$**:

Matriks simetris $4 \times 4$ berbasis aproksimasi kurvatur non-linier kuadratik:

$$H_{jk} \approx 2 \sum_{i=1}^N \frac{1}{(\Delta\sigma_i)^2} \left( \frac{\partial \sigma(E_i)}{\partial p_j} \frac{\partial \sigma(E_i)}{\partial p_k} \right)$$

## Struktur & Blueprint Kode

```python
# Modul: tahap2_analytic_derivatives.py
import numpy as np

def breit_wigner(E: np.ndarray, p: np.ndarray) -> np.ndarray:
    """Menghitung nilai teoritis penampang lintang sigma(E; p)."""
    Er, Gamma, sigma0, sigma_bg = p
    ...

def compute_residuals(p: np.ndarray, E: np.ndarray, sigma: np.ndarray, dsigma: np.ndarray) -> np.ndarray:
    """Menghitung residu terbobot: r_i = (sigma_i - model_i) / dsigma_i."""
    ...

def compute_chi2(p: np.ndarray, E: np.ndarray, sigma: np.ndarray, dsigma: np.ndarray) -> float:
    """Menghitung skalar chi-square total."""
    ...

def compute_gradient(p: np.ndarray, E: np.ndarray, sigma: np.ndarray, dsigma: np.ndarray) -> np.ndarray:
    """Menghitung vektor analitik gradien chi-square berukuran (4,)."""
    ...

def compute_hessian(p: np.ndarray, E: np.ndarray, sigma: np.ndarray, dsigma: np.ndarray) -> np.ndarray:
    """Menghitung matriks analitik Hessian berukuran (4, 4)."""
    ...
```
