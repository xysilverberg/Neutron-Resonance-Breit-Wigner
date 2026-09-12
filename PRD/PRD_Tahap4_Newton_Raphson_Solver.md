# PRD Tahap 4: Mesin Solver Newton-Raphson Multivariat

## Tujuan & Deliverable

Membangun algoritma iterasi berbasis inversi/penyelesaian matriks linier simultan $[\mathbf{H}] \Delta \mathbf{p} = -\mathbf{g}$ untuk memperbarui parameter $\mathbf{p}^{(k+1)} = \mathbf{p}^{(k)} + \Delta \mathbf{p}$ hingga mencapai konvergensi kuadratik, lengkap dengan pelacakan *condition number* matriks dan proteksi divergensi.

## Spesifikasi Fungsional

- Menyelesaikan pergeseran parameter $\Delta \mathbf{p}$ menggunakan `np.linalg.solve` (bukan inversi langsung untuk stabilitas numerik).
- Menghitung bilangan kondisi matriks Hessian $\kappa(\mathbf{H}) = \Vert{}\mathbf{H}\Vert{} \cdot \Vert{}\mathbf{H}^{-1}\Vert{}$ pada tiap iterasi untuk mendeteksi *ill-conditioning*.
- Memantau kriteria berhenti (*stopping criteria*): $\Vert{}\Delta \mathbf{p}\Vert{} < 10^{-6}$ atau $\vert{}\chi^2_{(k+1)} - \chi^2_{(k)}\vert{} < 10^{-6}$.
- Merekam riwayat konvergensi: nilai parameter, nilai $\chi^2$, norma gradien, dan $\kappa(\mathbf{H})$ per iterasi.

## Struktur & Blueprint Kode

```python
# Modul: tahap4_newton_raphson_solver.py
import numpy as np

def solve_newton_raphson(
    p0: np.ndarray, 
    E: np.ndarray, 
    sigma: np.ndarray, 
    dsigma: np.ndarray, 
    tol: float = 1e-6, 
    max_iter: int = 50
) -> dict:
    """
    Eksekusi iterasi Newton-Raphson multivariat.
    Returns: dict berisi 'p_opt', 'history', 'converged', 'iterations', 'H_final'
    """
    ...
```
