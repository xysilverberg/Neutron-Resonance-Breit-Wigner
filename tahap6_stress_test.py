"""
Modul Tahap 6: Uji Ketahanan Numerik (Noise Stress-Test)
Sesuai PRD Tahap 6 - Praktikum Fisika Komputasi II (Kasus 8)
Group H: Airin Khairunnisa Nur Raerah (182241045) & Hendra Maulana (182241043)
Departemen Fisika FST Universitas Airlangga
"""

import numpy as np
from tahap3_initial_guess import extract_initial_parameters
from tahap4_newton_raphson_solver import solve_newton_raphson

def run_noise_stress_test(
    E: np.ndarray, 
    sigma_clean: np.ndarray, 
    dsigma: np.ndarray, 
    noise_levels: list = [0.05, 0.15, 0.30], 
    n_trials: int = 10,
    random_seed: int = 42
) -> dict:
    """
    Simulasi Monte Carlo ketahanan numerik terhadap noise:
    sigma_noisy = sigma_clean + N(0, eta * sigma_clean)
    
    Parameters:
        E            : np.ndarray, array energi neutron (MeV)
        sigma_clean  : np.ndarray, data penampang lintang tanpa perturbasi (barn)
        dsigma       : np.ndarray, ketidakpastian dasar (barn)
        noise_levels : list of float, level fraksi noise gaussian eta
        n_trials     : int, jumlah pengulangan Monte Carlo per level noise
        random_seed  : int, seed generator bilangan acak
        
    Returns:
        dict berisi ringkasan hasil per level noise:
            'noise_levels': list,
            'results': dict per level noise dengan metrik:
                - success_rate (float)
                - avg_iterations (float)
                - avg_cond_H (float)
                - min_eigenval (float)
                - param_deviations_mean (np.ndarray)
                - param_deviations_std (np.ndarray)
    """
    rng = np.random.default_rng(random_seed)
    
    # Dapatkan baseline parameter bersih terlebih dahulu
    p0_clean = extract_initial_parameters(E, sigma_clean)
    clean_fit = solve_newton_raphson(p0_clean, E, sigma_clean, dsigma)
    p_clean_opt = clean_fit["p_opt"]
    
    stress_results = {}
    
    for eta in noise_levels:
        converged_count = 0
        iters_list = []
        cond_list = []
        min_eig_list = []
        p_opt_list = []
        
        for _ in range(n_trials):
            # Injeksi Gaussian Noise proporsional: N(0, eta * sigma_clean)
            noise = rng.normal(loc=0.0, scale=eta * sigma_clean)
            sigma_noisy = np.maximum(sigma_clean + noise, 0.05)  # Penampang lintang selalu bernilai positif
            
            # Sesuaikan ketidakpastian eksperimental dengan penambahan noise
            dsigma_effective = np.sqrt(dsigma**2 + (eta * sigma_clean)**2)
            
            # Ekstraksi tebakan awal dari data berisik
            p0_noisy = extract_initial_parameters(E, sigma_noisy)
            
            # Eksekusi solver
            fit_res = solve_newton_raphson(p0_noisy, E, sigma_noisy, dsigma_effective, max_iter=60)
            
            if fit_res["converged"]:
                converged_count += 1
                iters_list.append(fit_res["iterations"])
                H_end = fit_res["H_final"]
                cond_list.append(np.linalg.cond(H_end))
                eigvals = np.linalg.eigvalsh(H_end)
                min_eig_list.append(np.min(eigvals))
                p_opt_list.append(fit_res["p_opt"])
                
        success_rate = converged_count / float(n_trials)
        avg_iter = float(np.mean(iters_list)) if iters_list else np.nan
        avg_cond = float(np.mean(cond_list)) if cond_list else np.nan
        min_eig = float(np.mean(min_eig_list)) if min_eig_list else np.nan
        
        if p_opt_list:
            deviations = [np.abs(p - p_clean_opt) for p in p_opt_list]
            param_dev_mean = np.mean(deviations, axis=0)
            param_dev_std = np.std(deviations, axis=0)
        else:
            param_dev_mean = np.full(4, np.nan)
            param_dev_std = np.full(4, np.nan)
            
        stress_results[eta] = {
            "success_rate": success_rate,
            "avg_iterations": avg_iter,
            "avg_cond_H": avg_cond,
            "min_eigenval": min_eig,
            "param_deviations_mean": param_dev_mean,
            "param_deviations_std": param_dev_std,
            "p_opt_samples": p_opt_list
        }
        
    return {
        "noise_levels": noise_levels,
        "p_clean_opt": p_clean_opt,
        "results": stress_results
    }

if __name__ == "__main__":
    print("=== Menjalankan Verifikasi Tahap 6 ===")
    import csv
    
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
    
    stress_output = run_noise_stress_test(E, sigma, dsigma, noise_levels=[0.05, 0.15, 0.30], n_trials=10)
    
    print("\nRingkasan Stress-Test Noise Gaussian:")
    print(f"{'Noise (eta)':<12} | {'Success':<10} | {'Avg Iter':<10} | {'Mean cond(H)':<14} | {'Min Eigenval':<14} | {'|Delta Er| (MeV)':<16}")
    print("-" * 85)
    for eta, res in stress_output["results"].items():
        suc = f"{res['success_rate']*100:.0f}%"
        it = f"{res['avg_iterations']:.1f}"
        cH = f"{res['avg_cond_H']:.2e}"
        e_min = f"{res['min_eigenval']:.2e}"
        d_Er = f"{res['param_deviations_mean'][0]:.6f}"
        print(f"{eta*100:<10.0f}% | {suc:<10} | {it:<10} | {cH:<14} | {e_min:<14} | {d_Er:<16}")

