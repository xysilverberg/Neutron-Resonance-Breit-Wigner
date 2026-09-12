"""
Modul Tahap 3: Ekstraksi Otomatis Tebakan Parameter Awal (p0)
Sesuai PRD Tahap 3 - Praktikum Fisika Komputasi II (Kasus 8)
Group H: Airin Khairunnisa Nur Raerah (182241045) & Hendra Maulana (182241043)
Departemen Fisika FST Universitas Airlangga
"""

import numpy as np

def extract_initial_parameters(E: np.ndarray, sigma: np.ndarray) -> np.ndarray:
    """
    Ekstraksi heuristik fisika eksperimen untuk parameter awal Breit-Wigner:
    p0 = [Er_0, Gamma_0, sigma0_0, sigma_bg_0]^T
    
    Menghilangkan tebakan acak yang berisiko memicu divergensi pada Newton-Raphson.
    
    Parameters:
        E : np.ndarray, array energi neutron (MeV)
        sigma : np.ndarray, array penampang lintang eksperimen (barn)
        
    Returns:
        p0 : np.ndarray bertipe float64 berukuran (4,)
    """
    # 1. Posisi energi puncak resonansi (Er_0)
    idx_peak = np.argmax(sigma)
    Er_0 = float(E[idx_peak])
    
    # 2. Baseline kontinum latar belakang (sigma_bg_0)
    # Diambil dari nilai minimum pada kedua ujung sayap spektrum energi
    sigma_bg_0 = float(np.min([sigma[0], sigma[-1]]))
    
    # 3. Tinggi puncak resonansi murni (sigma0_0)
    sigma0_0 = float(sigma[idx_peak] - sigma_bg_0)
    
    # 4. Lebar separuh puncak maksimum / FWHM (Gamma_0)
    half_val = sigma_bg_0 + 0.5 * sigma0_0
    mask_above = sigma >= half_val
    energies_above = E[mask_above]
    
    if len(energies_above) > 1:
        Gamma_0 = float(energies_above[-1] - energies_above[0])
    else:
        Gamma_0 = 0.05  # Fallback nilai lebar resonansi tipikal neutron
        
    p0 = np.array([Er_0, Gamma_0, sigma0_0, sigma_bg_0], dtype=np.float64)
    return p0

if __name__ == "__main__":
    print("=== Menjalankan Verifikasi Tahap 3 ===")
    import csv
    
    # Muat data dari CSV Tahap 1
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
    
    p0 = extract_initial_parameters(E, sigma)
    print(f"Vektor Tebakan Awal p0:\n  Er^(0)       = {p0[0]:.4f} MeV")
    print(f"  Gamma^(0)    = {p0[1]:.4f} MeV")
    print(f"  sigma0^(0)   = {p0[2]:.4f} barn")
    print(f"  sigma_bg^(0) = {p0[3]:.4f} barn")

