"""
Modul Tahap 2: Formulasi Analitik Gradien & Matriks Hessian
Sesuai PRD Tahap 2 - Praktikum Fisika Komputasi II (Kasus 8)
Group H: Airin Khairunnisa Nur Raerah (182241045) & Hendra Maulana (182241043)
Departemen Fisika FST Universitas Airlangga
"""

import numpy as np

def breit_wigner(E: np.ndarray, p: np.ndarray) -> np.ndarray:
    """
    Menghitung penampang lintang teoritis Breit-Wigner satu tingkat:
    sigma(E; p) = sigma_bg + sigma_0 * (Gamma/2)^2 / [(E - Er)^2 + (Gamma/2)^2]
    
    Parameters:
        E : np.ndarray, energi neutron (MeV)
        p : np.ndarray, vektor parameter [Er, Gamma, sigma0, sigma_bg]
    Returns:
        np.ndarray, penampang lintang teoritis (barn)
    """
    Er, Gamma, sigma0, sigma_bg = p
    half_gamma = 0.5 * Gamma
    half_gamma_sq = half_gamma**2
    denominator = (E - Er)**2 + half_gamma_sq
    return sigma_bg + sigma0 * (half_gamma_sq / denominator)

def compute_model_jacobian(p: np.ndarray, E: np.ndarray) -> np.ndarray:
    """
    Menghitung matriks Jacobian dari model fisis terhadap parameter:
    J[i, j] = d(sigma(E_i; p)) / d(p_j)
    Bentuk output: (N, 4)
    Kolom 0: d(sigma)/dEr
    Kolom 1: d(sigma)/dGamma
    Kolom 2: d(sigma)/dsigma0
    Kolom 3: d(sigma)/dsigma_bg
    """
    Er, Gamma, sigma0, sigma_bg = p
    half_gamma = 0.5 * Gamma
    half_gamma_sq = half_gamma**2
    diff_E = E - Er
    diff_E_sq = diff_E**2
    denom = diff_E_sq + half_gamma_sq
    denom_sq = denom**2
    
    N = len(E)
    J = np.zeros((N, 4), dtype=np.float64)
    
    # d(sigma)/dEr = 2 * sigma0 * (Gamma/2)^2 * (E - Er) / denom^2
    J[:, 0] = 2.0 * sigma0 * half_gamma_sq * diff_E / denom_sq
    
    # d(sigma)/dGamma = sigma0 * (Gamma/2) * (E - Er)^2 / denom^2
    J[:, 1] = sigma0 * half_gamma * diff_E_sq / denom_sq
    
    # d(sigma)/dsigma0 = (Gamma/2)^2 / denom
    J[:, 2] = half_gamma_sq / denom
    
    # d(sigma)/dsigma_bg = 1.0
    J[:, 3] = 1.0
    
    return J

def compute_residuals(p: np.ndarray, E: np.ndarray, sigma: np.ndarray, dsigma: np.ndarray) -> np.ndarray:
    """
    Menghitung residu terbobot:
    r_i = (sigma_i - sigma_model(E_i; p)) / dsigma_i
    """
    model = breit_wigner(E, p)
    return (sigma - model) / dsigma

def compute_chi2(p: np.ndarray, E: np.ndarray, sigma: np.ndarray, dsigma: np.ndarray) -> float:
    """
    Menghitung skalar Chi-Square total:
    chi2(p) = sum [ (sigma_i - sigma_model_i) / dsigma_i ]^2
    """
    r = compute_residuals(p, E, sigma, dsigma)
    return float(np.sum(r**2))

def compute_gradient(p: np.ndarray, E: np.ndarray, sigma: np.ndarray, dsigma: np.ndarray) -> np.ndarray:
    """
    Menghitung vektor analitik gradien chi-square berukuran (4,):
    g_j = d(chi2)/d(p_j) = -2 * sum [ (sigma_i - model_i) / (dsigma_i)^2 * d(model_i)/d(p_j) ]
    Dalam notasi matriks: g = -2 * J^T * W * (sigma - model)
    """
    model = breit_wigner(E, p)
    diff = sigma - model
    weights = 1.0 / (dsigma**2)
    J = compute_model_jacobian(p, E)
    
    # Perkalian vektor terbobot: J^T @ (weights * diff)
    grad = -2.0 * np.dot(J.T, weights * diff)
    return grad

def compute_hessian(p: np.ndarray, E: np.ndarray, sigma: np.ndarray, dsigma: np.ndarray) -> np.ndarray:
    """
    Menghitung matriks analitik Hessian berukuran (4, 4) menggunakan
    aproksimasi kelengkungan kuadratik Gauss-Newton:
    H_jk = 2 * sum [ 1/(dsigma_i)^2 * d(model_i)/d(p_j) * d(model_i)/d(p_k) ]
    Dalam notasi matriks: H = 2 * J^T * W * J
    Matriks ini secara fundamental dijamin simetris dan semi-positif definit.
    """
    weights = 1.0 / (dsigma**2)
    J = compute_model_jacobian(p, E)
    
    # J.T @ diag(weights) @ J ekuivalen efisien dengan: (J.T * weights) @ J
    H = 2.0 * np.dot(J.T * weights, J)
    
    # Penegakan simetri numerik
    H = 0.5 * (H + H.T)
    return H

def test_derivatives_accuracy():
    """Unit test komparasi gradien analitik vs diferensiasi numerik beda-hingga."""
    # Dummy data
    E_test = np.linspace(1.9, 2.3, 20)
    p_true = np.array([2.078, 0.045, 2.85, 4.65], dtype=np.float64)
    sigma_test = breit_wigner(E_test, p_true) + 0.02 * np.sin(E_test)
    dsigma_test = np.full_like(E_test, 0.08)
    
    p_eval = np.array([2.070, 0.050, 2.70, 4.60], dtype=np.float64)
    
    # Gradien analitik
    g_analytic = compute_gradient(p_eval, E_test, sigma_test, dsigma_test)
    
    # Gradien numerik (central difference)
    h = 1e-6
    g_numeric = np.zeros(4)
    for j in range(4):
        p_plus = p_eval.copy()
        p_minus = p_eval.copy()
        p_plus[j] += h
        p_minus[j] -= h
        chi_plus = compute_chi2(p_plus, E_test, sigma_test, dsigma_test)
        chi_minus = compute_chi2(p_minus, E_test, sigma_test, dsigma_test)
        g_numeric[j] = (chi_plus - chi_minus) / (2.0 * h)
        
    rel_err = np.abs(g_analytic - g_numeric) / (np.abs(g_numeric) + 1e-12)
    
    # Hessian symmetry test
    H = compute_hessian(p_eval, E_test, sigma_test, dsigma_test)
    asym = np.max(np.abs(H - H.T))
    eigvals = np.linalg.eigvalsh(H)
    
    print("[Tahap 2 Unit Test] Evaluasi Turunan Analitik:")
    print(f"  Gradien Analitik: {g_analytic}")
    print(f"  Gradien Numerik : {g_numeric}")
    print(f"  Max Relative Error Gradien: {np.max(rel_err):.2e}")
    print(f"  Asimetri Hessian: {asym:.2e}")
    print(f"  Nilai Eigen Hessian: {eigvals}")
    
    assert np.max(rel_err) < 1e-4, "Galat gradien analitik melebihi batas toleransi!"
    assert asym < 1e-12, "Matriks Hessian tidak simetris!"
    assert np.all(eigvals > 0), "Matriks Hessian tidak positif definit!"
    print("  => Semua pengujian analitik Tahap 2 BERHASIL (PASSED).")

if __name__ == "__main__":
    print("=== Menjalankan Verifikasi Tahap 2 ===")
    test_derivatives_accuracy()

