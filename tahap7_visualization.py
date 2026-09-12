"""
Modul Tahap 7: Visualisasi Saintifik & Validasi Fisis
Sesuai PRD Tahap 7 - Praktikum Fisika Komputasi II (Kasus 8)
Group H: Airin Khairunnisa Nur Raerah (182241045) & Hendra Maulana (182241043)
Departemen Fisika FST Universitas Airlangga
"""

import matplotlib.pyplot as plt
import numpy as np
from tahap2_analytic_derivatives import breit_wigner, compute_residuals

# Konfigurasi gaya visualisasi standar publikasi
plt.rcParams.update({
    "font.family": "serif",
    "font.size": 11,
    "axes.labelsize": 12,
    "axes.titlesize": 13,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.titlesize": 14,
    "figure.dpi": 300,
    "lines.linewidth": 1.8,
    "axes.grid": True,
    "grid.alpha": 0.4,
    "grid.linestyle": "--"
})

def plot_resonance_fitting(
    E: np.ndarray, 
    sigma: np.ndarray, 
    dsigma: np.ndarray, 
    p_opt: np.ndarray, 
    p_err: np.ndarray,
    chi2_red: float,
    save_path: str = "resonance_fitting_plot.png"
) -> plt.Figure:
    """
    Visualisasi utama:
    - Panel atas: Titik eksperimen + error bar dan kurva kontinu Breit-Wigner
    - Panel bawah: Residu terstandarisasi R_i = (sigma_i - sigma_fit) / dsigma_i
    """
    fig, (ax_main, ax_res) = plt.subplots(
        nrows=2, ncols=1, figsize=(9, 7.5), 
        gridspec_kw={"height_ratios": [3, 1], "hspace": 0.08},
        sharex=True
    )
    
    # 1. Panel Atas: Fitting Resonansi
    # Titik data eksperimen dengan error bar
    ax_main.errorbar(
        E, sigma, yerr=dsigma, fmt="o", markersize=4.5,
        color="#1f77b4", ecolor="#6baed6", elinewidth=1.2, capsize=2.5,
        label="Data Eksperimen EXFOR $^{12}\\text{C}(n,\\text{tot})$"
    )
    
    # Kurva kontinu model Breit-Wigner
    E_dense = np.linspace(np.min(E), np.max(E), 500)
    sigma_dense = breit_wigner(E_dense, p_opt)
    ax_main.plot(E_dense, sigma_dense, color="#d62728", lw=2.2, label="Fitting Breit-Wigner (Newton-Raphson)")
    
    # Baseline latar belakang
    ax_main.axhline(p_opt[3], color="#7f7f7f", linestyle=":", lw=1.5, label=f"Kontinum $\\sigma_{{bg}} = {p_opt[3]:.3f}\\text{{ barn}}$")
    
    # Garis vertikal posisi puncak Er
    ax_main.axvline(p_opt[0], color="#2ca02c", linestyle="--", lw=1.2, alpha=0.8, label=f"$E_r = {p_opt[0]:.4f}\\text{{ MeV}}$")
    
    ax_main.set_ylabel("Penampang Lintang $\\sigma$ (barn)")
    ax_main.set_title("Resonansi Hamburan Hamburan Neutron $^{12}\\text{C}(n,\\text{tot})$: Fitting Breit-Wigner", pad=12)
    ax_main.legend(loc="upper right", framealpha=0.92)
    
    # Kotak informasi parameter fisis
    param_text = (
        f"$\\mathbf{{Parameter\\ Optimal:}}$\n"
        f"$E_r = {p_opt[0]:.4f} \\pm {p_err[0]:.4f}\\text{{ MeV}}$\n"
        f"$\\Gamma = {p_opt[1]:.4f} \\pm {p_err[1]:.4f}\\text{{ MeV}}$\n"
        f"$\\sigma_0 = {p_opt[2]:.3f} \\pm {p_err[2]:.3f}\\text{{ barn}}$\n"
        f"$\\sigma_{{bg}} = {p_opt[3]:.3f} \\pm {p_err[3]:.3f}\\text{{ barn}}$\n"
        f"$\\chi^2_{{red}} = {chi2_red:.3f}$"
    )
    ax_main.text(
        0.03, 0.95, param_text, transform=ax_main.transAxes,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.9, edgecolor="#cccccc")
    )
    
    # 2. Panel Bawah: Residu Terstandarisasi
    residuals = compute_residuals(p_opt, E, sigma, dsigma)
    ax_res.axhline(0, color="black", linestyle="-", lw=1.0)
    ax_res.axhline(1, color="gray", linestyle=":", lw=0.9)
    ax_res.axhline(-1, color="gray", linestyle=":", lw=0.9)
    ax_res.axhline(2, color="red", linestyle="--", lw=0.8, alpha=0.6)
    ax_res.axhline(-2, color="red", linestyle="--", lw=0.8, alpha=0.6)
    
    ax_res.errorbar(
        E, residuals, yerr=np.ones_like(residuals), fmt="s", markersize=4,
        color="#2ca02c", ecolor="#a1d99b", elinewidth=1.0, capsize=2
    )
    ax_res.set_xlabel("Energi Neutron $E$ (MeV)")
    ax_res.set_ylabel("Residu $\\frac{\\sigma_i - \\sigma_{fit}}{\\Delta\\sigma_i}$")
    ax_res.set_ylim(-3.2, 3.2)
    
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[Tahap 7] Grafik fitting resonansi disimpan ke '{save_path}'.")
    return fig

def plot_convergence_metrics(history: list, save_path: str = "convergence_metrics_plot.png") -> plt.Figure:
    """
    Visualisasi 2-panel profil konvergensi:
    - Kiri : Penurunan Chi-Square dan Step Norm ||Delta_p|| terhadap iterasi (skala semilog)
    - Kanan: Dinamika Bilangan Kondisi Matriks Hessian cond(H) terhadap iterasi
    """
    iters = [h["iteration"] for h in history]
    chi2_vals = [h["chi2"] for h in history]
    grad_norms = [h["grad_norm"] for h in history]
    step_norms = [h["step_norm"] for h in history[:-1]]  # step terakhir konvergensi 0
    conds = [h["cond_H"] for h in history]
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(11, 4.8))
    
    # Panel Kiri: Penurunan Chi2 dan Norma Gradien
    ax1.plot(iters, chi2_vals, "o-", color="#d62728", label="$\\chi^2$ (Total)")
    ax1.plot(iters, grad_norms, "s--", color="#1f77b4", label="$\\|\\mathbf{g}\\|_2$ (Norma Gradien)")
    if step_norms:
        ax1.plot(iters[:-1], step_norms, "^-.", color="#2ca02c", label="$\\|\\Delta\\mathbf{p}\\|_2$ (Langkah Update)")
    ax1.set_yscale("log")
    ax1.set_xlabel("Nomor Iterasi ($k$)")
    ax1.set_ylabel("Magnitudo (Skala Logaritmik)")
    ax1.set_title("Laju Konvergensi Orde-2 Newton-Raphson")
    ax1.legend(loc="upper right", framealpha=0.9)
    
    # Panel Kanan: Dinamika Bilangan Kondisi
    ax2.plot(iters, conds, "D-", color="#9467bd", lw=2, label="$\\kappa(\\mathbf{H}) = \\|\\mathbf{H}\\| \\cdot \\|\\mathbf{H}^{-1}\\|$")
    ax2.axhline(1e12, color="red", linestyle="--", alpha=0.7, label="Batas Singularitas ($10^{12}$)")
    ax2.set_yscale("log")
    ax2.set_xlabel("Nomor Iterasi ($k$)")
    ax2.set_ylabel("Bilangan Kondisi $\\kappa(\\mathbf{H})$")
    ax2.set_title("Stabilitas Kurvatur Matriks Hessian")
    ax2.legend(loc="center right", framealpha=0.9)
    
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[Tahap 7] Grafik metrik konvergensi disimpan ke '{save_path}'.")
    return fig

def plot_noise_stress_test(stress_results: dict, save_path: str = "noise_stress_test_plot.png") -> plt.Figure:
    """
    Visualisasi ketahanan noise:
    - Kiri : Tingkat keberhasilan konvergensi & rata-rata iterasi vs level noise
    - Kanan: Pembengkakan bilangan kondisi cond(H) vs level noise
    """
    noise_lvls = [lvl * 100 for lvl in stress_results["noise_levels"]]
    success_rates = [stress_results["results"][lvl]["success_rate"] * 100 for lvl in stress_results["noise_levels"]]
    avg_iters = [stress_results["results"][lvl]["avg_iterations"] for lvl in stress_results["noise_levels"]]
    avg_conds = [stress_results["results"][lvl]["avg_cond_H"] for lvl in stress_results["noise_levels"]]
    er_devs = [stress_results["results"][lvl]["param_deviations_mean"][0] * 1000 for lvl in stress_results["noise_levels"]] # ke keV
    
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, figsize=(11, 4.8))
    
    # Panel Kiri: Success Rate & Iterasi
    color1 = "#1f77b4"
    ax1.set_xlabel("Tingkat Gangguan Noise Gaussian $\\eta$ (%)")
    ax1.set_ylabel("Tingkat Keberhasilan (%)", color=color1)
    line1 = ax1.plot(noise_lvls, success_rates, "o-", color=color1, lw=2, label="Success Rate (%)")
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.set_ylim(-5, 110)
    
    ax1_twin = ax1.twinx()
    color2 = "#ff7f0e"
    ax1_twin.set_ylabel("Rata-rata Iterasi", color=color2)
    line2 = ax1_twin.plot(noise_lvls, avg_iters, "s--", color=color2, lw=2, label="Rata-rata Iterasi")
    ax1_twin.tick_params(axis="y", labelcolor=color2)
    
    # Gabung legenda
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="center left", framealpha=0.9)
    ax1.set_title("Ketahanan Konvergensi vs Tingkat Noise")
    
    # Panel Kanan: Bilangan Kondisi & Deviasi Parameter Er
    color3 = "#9467bd"
    ax2.set_xlabel("Tingkat Gangguan Noise Gaussian $\\eta$ (%)")
    ax2.set_ylabel("Rata-rata $\\kappa(\\mathbf{H})$ (Skala Log)", color=color3)
    line3 = ax2.plot(noise_lvls, avg_conds, "D-", color=color3, lw=2, label="cond(H)")
    ax2.set_yscale("log")
    ax2.tick_params(axis="y", labelcolor=color3)
    
    ax2_twin = ax2.twinx()
    color4 = "#d62728"
    ax2_twin.set_ylabel("Rata-rata Deviasi $|\\Delta E_r|$ (keV)", color=color4)
    line4 = ax2_twin.plot(noise_lvls, er_devs, "^-.", color=color4, lw=2, label="$|\\Delta E_r|$ (keV)")
    ax2_twin.tick_params(axis="y", labelcolor=color4)
    
    lines_right = line3 + line4
    labels_right = [l.get_label() for l in lines_right]
    ax2.legend(lines_right, labels_right, loc="upper left", framealpha=0.9)
    ax2.set_title("Sensitivitas Kelengkungan & Presisi Parameter")
    
    plt.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"[Tahap 7] Grafik stress-test noise disimpan ke '{save_path}'.")
    return fig

def validate_physical_results(p_opt: np.ndarray, p_err: np.ndarray) -> None:
    """Membandingkan hasil fitting terhadap data literatur nuklir standar."""
    Er_calc = p_opt[0]
    Er_err = p_err[0]
    Er_lit = 2.0780  # Nilai literatur resonansi 12C(n,tot) D-wave (MeV)
    
    discrepancy = abs(Er_calc - Er_lit)
    rel_discrepancy = (discrepancy / Er_lit) * 100.0
    
    print("\n" + "=" * 65)
    print("VALIDASI FISIS TERHADAP LITERATUR NUKLIR RESMI")
    print("=" * 65)
    print(f"Energi Resonansi Komputasi (Er) : {Er_calc:.6f} +/- {Er_err:.6f} MeV")
    print(f"Energi Resonansi Literatur (Er) : {Er_lit:.6f} MeV (IAEA Nuclear Data)")
    print(f"Discrepancy Mutlak (|Er - Er_lit|): {discrepancy:.6f} MeV ({discrepancy*1000:.2f} keV)")
    print(f"Persentase Deviasi Relatif       : {rel_discrepancy:.4f} %")
    if rel_discrepancy < 0.5:
        print("Status Validasi: SANGAT AKURAT (Deviasi fisis < 0.5% dari benchmark).")
    else:
        print("Status Validasi: CUKUP BAIK.")
    print("=" * 65)

if __name__ == "__main__":
    print("=== Menjalankan Verifikasi Tahap 7 ===")
    import csv
    from tahap3_initial_guess import extract_initial_parameters
    from tahap4_newton_raphson_solver import solve_newton_raphson
    from tahap5_statistical_analysis import compute_statistics_and_covariance
    from tahap6_stress_test import run_noise_stress_test
    
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
    
    # Pembangkitan grafik
    plot_resonance_fitting(E, sigma, dsigma, res["p_opt"], stats["param_errors"], stats["chi2_red"])
    plot_convergence_metrics(res["history"])
    
    stress_output = run_noise_stress_test(E, sigma, dsigma, noise_levels=[0.05, 0.15, 0.30], n_trials=8)
    plot_noise_stress_test(stress_output)
    
    # Validasi fisis
    validate_physical_results(res["p_opt"], stats["param_errors"])
