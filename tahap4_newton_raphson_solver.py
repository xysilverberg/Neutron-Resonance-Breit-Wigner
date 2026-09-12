"""
Modul Tahap 4: Mesin Solver Newton-Raphson Multivariat
Sesuai PRD Tahap 4 - Praktikum Fisika Komputasi II (Kasus 8)
Group H: Airin Khairunnisa Nur Raerah (182241045) & Hendra Maulana (182241043)
Departemen Fisika FST Universitas Airlangga
"""

import numpy as np
from tahap2_analytic_derivatives import compute_chi2, compute_gradient, compute_hessian

def solve_newton_raphson(
    p0: np.ndarray, 
    E: np.ndarray, 
    sigma: np.ndarray, 
    dsigma: np.ndarray, 
    tol: float = 1e-6, 
    max_iter: int = 50
) -> dict:
    """
    Eksekusi iterasi Newton-Raphson multivariat untuk minimisasi chi-square:
    H(p^(k)) * Delta_p = -g(p^(k))
    p^(k+1) = p^(k) + Delta_p
    
    Parameters:
        p0 : np.ndarray, vektor tebakan awal [Er, Gamma, sigma0, sigma_bg]
        E : np.ndarray, data energi neutron (MeV)
        sigma : np.ndarray, data penampang lintang eksperimen (barn)
        dsigma : np.ndarray, ketidakpastian eksperimental (barn)
        tol : float, toleransi konvergensi kuadratik (default: 1e-6)
        max_iter : int, batas maksimum iterasi (default: 50)
        
    Returns:
        dict berisi:
            'p_opt': np.ndarray, parameter optimal hasil konvergensi
            'history': list of dict, rekam jejak iterasi komputasi
            'converged': bool, status keberhasilan konvergensi
            'iterations': int, total iterasi yang dieksekusi
            'H_final': np.ndarray, matriks Hessian di titik optimal
            'chi2_final': float, nilai chi-square minimum
    """
    p = np.array(p0, dtype=np.float64).copy()
    history = []
    converged = False
    
    chi2_prev = compute_chi2(p, E, sigma, dsigma)
    
    for k in range(max_iter):
        # 1. Komputasi analitik gradien dan Hessian
        g = compute_gradient(p, E, sigma, dsigma)
        H = compute_hessian(p, E, sigma, dsigma)
        
        grad_norm = float(np.linalg.norm(g))
        
        # 2. Evaluasi bilangan kondisi matriks Hessian
        cond_H = float(np.linalg.cond(H))
        
        # Proteksi numerik: deteksi singularitas atau ill-conditioning ekstrem
        if cond_H > 1e14 or np.isnan(cond_H) or np.isinf(cond_H):
            print(f"[Tahap 4 Peringatan] Hessian ill-conditioned (cond = {cond_H:.2e}) pada iterasi {k}.")
            break
            
        # 3. Solusi sistem linier H * delta_p = -g
        # Menggunakan np.linalg.solve (dekomposisi LAPACK GESV) untuk stabilitas numerik
        try:
            delta_p = np.linalg.solve(H, -g)
        except np.linalg.LinAlgError as err:
            print(f"[Tahap 4 Error] Gagal menyelesaikan sistem linier pada iterasi {k}: {err}")
            break
            
        step_norm = float(np.linalg.norm(delta_p))
        
        # 4. Rekam histori sebelum update
        history.append({
            "iteration": k,
            "p": p.copy(),
            "chi2": chi2_prev,
            "grad_norm": grad_norm,
            "step_norm": step_norm,
            "cond_H": cond_H
        })
        
        # 5. Pembaruan parameter
        p = p + delta_p
        chi2_curr = compute_chi2(p, E, sigma, dsigma)
        delta_chi2 = abs(chi2_curr - chi2_prev)
        
        # 6. Evaluasi kriteria henti ganda
        if step_norm < tol or delta_chi2 < tol:
            converged = True
            # Catat titik akhir konvergensi
            g_end = compute_gradient(p, E, sigma, dsigma)
            H_end = compute_hessian(p, E, sigma, dsigma)
            history.append({
                "iteration": k + 1,
                "p": p.copy(),
                "chi2": chi2_curr,
                "grad_norm": float(np.linalg.norm(g_end)),
                "step_norm": 0.0,
                "cond_H": float(np.linalg.cond(H_end))
            })
            break
            
        chi2_prev = chi2_curr
        
    H_final = compute_hessian(p, E, sigma, dsigma)
    chi2_final = compute_chi2(p, E, sigma, dsigma)
    
    return {
        "p_opt": p,
        "history": history,
        "converged": converged,
        "iterations": len(history) - 1 if converged else len(history),
        "H_final": H_final,
        "chi2_final": chi2_final
    }

if __name__ == "__main__":
    print("=== Menjalankan Verifikasi Tahap 4 ===")
    import csv
    from tahap3_initial_guess import extract_initial_parameters
    
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
    
    print(f"Status Konvergensi : {res['converged']}")
    print(f"Total Iterasi      : {res['iterations']}")
    print(f"Chi2 Minimum       : {res['chi2_final']:.4f}")
    print("\nTabel Riwayat Konvergensi Newton-Raphson:")
    print(f"{'Iter':<5} | {'Chi2':<12} | {'||g||':<12} | {'||Delta_p||':<12} | {'cond(H)':<12} | {'Er (MeV)':<10} | {'Gamma (MeV)':<10}")
    print("-" * 80)
    for h in res["history"]:
        it = h["iteration"]
        c2 = h["chi2"]
        gn = h["grad_norm"]
        sn = h["step_norm"]
        cH = h["cond_H"]
        er = h["p"][0]
        gm = h["p"][1]
        print(f"{it:<5} | {c2:<12.4f} | {gn:<12.4e} | {sn:<12.4e} | {cH:<12.2e} | {er:<10.6f} | {gm:<10.6f}")
        
    print("\nParameter Optimal Hasil Fitting:")
    names = ["Er (MeV)", "Gamma (MeV)", "sigma0 (barn)", "sigma_bg (barn)"]
    for name, val in zip(names, res["p_opt"]):
        print(f"  {name:<16}: {val:.6f}")

