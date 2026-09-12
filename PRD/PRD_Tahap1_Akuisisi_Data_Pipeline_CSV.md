# PRD Tahap 1: Akuisisi Data, Parsing ASCII, & Pipeline CSV

## Tujuan & Deliverable

Membangun modul ekstraksi data eksperimen penampang lintang hamburan neutron inti $^{12}\text{C}$ dari repositori IAEA-NDS EXFOR via HTTP request, mem-parsing format ASCII mentah menggunakan Regular Expression, serta mengekspor data numerik bersih ke dalam file `exfor_c12_resonance.csv`.

## Spesifikasi Fungsional

- Mengunduh data penampang lintang reaksi $^{12}\text{C}(n,\text{tot})$ atau $^{12}\text{C}(n,\text{el})$ pada rentang energi $1.8\text{ MeV} \le E \le 2.4\text{ MeV}$.
- Menangani kegagalan jaringan secara otomatis melalui mekanisme *fallback* data kalibrasi standar EXFOR jika server tidak merespons.
- Mengekstrak 3 kolom numerik presisi ganda (`float64`): Energi Neutron $E_i$ (MeV), Penampang Lintang $\sigma_i$ (barn), dan Ketidakpastian Eksperimental $\Delta\sigma_i$ (barn).
- Menghasilkan file CSV standar RFC 4180 lengkap dengan metadata header fisis.

## Struktur & Blueprint Kode

```python
# Modul: tahap1_data_pipeline.py
import urllib.request
import re
import csv
import numpy as np

def fetch_exfor_raw(target="C-12", reaction="N,TOT") -> str:
    """Mengambil raw ASCII stream dari endpoint web IAEA-NDS dengan fallback dataset terkalibrasi."""
    ...

def parse_exfor_ascii(raw_text: str) -> np.ndarray:
    """Filter baris non-data via Regex; mengembalikan array (N, 3) [E, sigma, dsigma]."""
    ...

def export_to_csv(data: np.ndarray, output_path: str = "exfor_c12_resonance.csv") -> None:
    """Menulis header metadata dan 3 kolom numerik ke format CSV."""
    ...
```
