"""
Modul Tahap 5: Evaluasi Statistik, Matriks Kovariansi, & Analisis Galat
Sesuai PRD Tahap 5 - Praktikum Fisika Komputasi II (Kasus 8)
Group H: Airin Khairunnisa Nur Raerah (182241045) & Hendra Maulana (182241043)
Departemen Fisika FST Universitas Airlangga
"""

import numpy as np

def compute_statistics_and_covariance(
    p_opt: np.ndarray, 
    H_opt: np.ndarray, 
    chi2_min: float, 
    n_data: int
) -> dict:
    """
    Kalkulasi reduced chi-square, matriks kovariansi, ketidakpastian parameter,
    serta matriks korelasi ternormalisasi.
    
    Parameters:
        p_opt    : np.ndarray, parameter optimal [Er, Gamma, sigma0, sigma_bg]
        H_opt    : np.ndarray, matriks Hessian (4x4) pada titik optimal
        chi2_min : float, nilai chi-square minimum
        n_data   : int, jumlah titik data eksperimen (N)
        
    Returns:
        dict berisi:
            'dof': int, derajat kebebasan (nu = N - 4)
            'chi2_red': float, reduced chi-square (chi2_min / nu)
            'cov_matrix': np.ndarray, matriks kovariansi parameter C (4x4)
            'param_errors': np.ndarray, standar deviasi parameter delta_p (4,)
            'corr_matrix': np.ndarray, matriks korelasi ternormalisasi rho (4x4)
    """
    m = len(p_opt)  # 4 parameter
    dof = n_data - m
    if dof <= 0:
        raise ValueError(f"Derajat kebebasan tidak valid: N ({n_data}) <= m ({m})")
        
    chi2_red = chi2_min / float(dof)
    
    # Inversi matriks kelengkungan Hessian: C = 2 * H^(-1)
    try:
        H_inv = np.linalg.inv(H_opt)
    except np.linalg.LinAlgError as err:
        raise ValueError(f"Matriks Hessian singular, gagal diinversi: {err}")
        
    cov_matrix = 2.0 * H_inv
    # Penegakan simetri numerik
    cov_matrix = 0.5 * (cov_matrix + cov_matrix.T)
    
    # Standar deviasi parameter: delta_p_j = sqrt(C_jj * chi2_red)
    # Catatan: Jika chi2_red terkalibrasi baik (~1), pengali chi2_red mencerminkan scatter data riil
    diag_cov = np.diag(cov_matrix)
    # Lindungi dari kemungkinan elemen diagonal negatif akibat pembulatan numerik
    param_errors = np.sqrt(np.maximum(diag_cov * chi2_red, 0.0))
    
    # Matriks korelasi: rho_jk = C_jk / sqrt(C_jj * C_kk)
    corr_matrix = np.zeros_like(cov_matrix)
    for j in range(m):
        for k in range(m):
            denom = np.sqrt(abs(cov_matrix[j, j] * cov_matrix[k, k]))
            if denom > 1e-15:
                corr_matrix[j, k] = cov_matrix[j, k] / denom
            else:
                corr_matrix[j, k] = 0.0
                
    return {
        "dof": dof,
        "chi2_red": chi2_red,
        "cov_matrix": cov_matrix,
        "param_errors": param_errors,
        "corr_matrix": corr_matrix
    }

if __name__ == "__main__":
    print("=== Menjalankan Verifikasi Tahap 5 ===")
    import csv
    from tahap3_initial_guess import extract_initial_parameters
    from tahap4_newton_raphson_solver import solve_newton_raphson
    
    # Muat dataset
    energies, sigmas, dsigmas = [], [], []
    with open("exfor_c12_resonance.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or row[0].startswith("#") or row[0] == "energy_mev":
                continue
            energies.append(float(row[0]))
            sigmas.append(float(row[1]))
            dsigmas.append(float(row[2]))
            
    E = np.array(energies)
    sigma = np.array(sigmas)
    dsigma = np.array(dsigmas)
    
    p0 = extract_initial_parameters(E, sigma)
    res = solve_newton_raphson(p0, E, sigma, dsigma)
    
    stats = compute_statistics_and_covariance(res["p_opt"], res["H_final"], res["chi2_final"], len(E))
    
    print(f"Jumlah Titik Data (N)     : {len(E)}")
    print(f"Derajat Kebebasan (nu)    : {stats['dof']}")
    print(f"Chi-Square Minimum        : {res['chi2_final']:.4f}")
    print(f"Reduced Chi-Square (chi2_red): {stats['chi2_red']:.4f}")
    
    param_names = ["Er (MeV)", "Gamma (MeV)", "sigma0 (barn)", "sigma_bg (barn)"]
    print("\nHasil Estimasi Parameter & Ketidakpastian:")
    for name, val, err in zip(param_names, res["p_opt"], stats["param_errors"]):
        print(f"  {name:<16}: {val:.6f} +/- {err:.6f}")
        
    print("\nMatriks Korelasi Parameter (rho):")
    header_str = " " * 16 + " ".join([f"{n[:8]:>10}" for n in param_names])
    print(header_str)
    for i, row in enumerate(stats["corr_matrix"]):
        row_str = f"{param_names[i]:<16}" + " ".join([f"{val:>10.4f}" for val in row])
        print(row_str)

