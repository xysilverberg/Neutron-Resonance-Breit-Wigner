# Panduan Praktikum Fisika Komputasi II: Studi Kasus dan Penilaian

Berikut adalah rancangan narasi studi kasus (*case-based*), pembagian 12 kelompok praktikum yang disesuaikan dengan data resmi anggota kelompok, serta rubrik penilaian praktikum fisika komputasi dalam 7 skala penilaian:

---

## **1. Narasi Studi Kasus Praktikum Fisika Komputasi (Case-Based)**

Setiap narasi kasus fisis di bawah ini diambil dari topik-topik komputasi penting yang terdapat di dalam buku referensi mata kuliah [2]:

*   **Kasus 1: Inversi Numerik Matriks dan Presisi Batas Mesin (Aljabar Linier)**
    *   *Narasi*: Kelompok ini ditugaskan untuk melakukan analisis inversi numerik dari matriks $A$ berukuran $3\times3$. Fokus fisis utama adalah memverifikasi hubungan matematis $AA^{-1} = A^{-1}A = I$ untuk mendeteksi akumulasi kesalahan pembulatan (*round-off error*) serta mengidentifikasi batas presisi mesin (*machine precision*) yang membatasi ketelitian pemodelan numerik dalam perhitungan fisika [2].
*   **Kasus 2: Mode Normal Getaran String (Eigenvalue Problem)**
    *   *Narasi*: Kelompok ini menganalisis gerak dari sejumlah beban identik terdistribusi seragam pada string teregang. Sistem persamaan linier simultan diformulasikan ke dalam bentuk masalah nilai batas matriks tridiagonal (*tridiagonal matrix eigenvalue problem*) menggunakan pustaka aljabar linier Python untuk mencari frekuensi eigen getaran sistem $\omega_n$ [2].
*   **Kasus 3: Keseimbangan Gaya Beban Tergantung Tali (Persamaan Non-Linier)**
    *   *Narasi*: Menggunakan sistem keseimbangan dua beban ($W_1 = 10\text{ N}, W_2 = 20\text{ N}$) yang digantungkan pada tiga utas tali dengan panjang tertentu. Hukum keseimbangan gaya menghasilkan sistem persamaan non-linier simultan yang diselesaikan menggunakan matriks turunan parsial Jacobian melalui metode Newton-Raphson multi-dimensi [2].
*   **Kasus 4: Rotasi Benda Tegar (Momentum Sudut dan Tensor Inersia)**
    *   *Narasi*: Memodelkan rotasi benda tegar berupa *barbell* dengan dua massa atau sebuah kubus padat dengan sisi $b=1$. Kelompok ini harus menghitung vektor momentum sudut benda tegar $\mathbf{L}$ dari perkalian matriks tensor inersia $[\mathbf{I}]$ dengan vektor kecepatan sudut $\omega$ ($\mathbf{L} = [\mathbf{I}]\omega$) menggunakan Python [2].
*   **Kasus 5: Analisis Distribusi Suhu Batang Logam (Fitting Linier)**
    *   *Narasi*: Menganalisis data eksperimen suhu batang logam ($T$ dalam °C) terhadap jarak sepanjang batang ($x$ dalam cm). Kasus diselesaikan dengan melakukan pencocokan garis lurus least-squares ($T(x) = a + bx$) dan membuktikan bahwa parameter kemiringan serta intersep yang diperoleh berhasil meminimalkan nilai chi-square ($\chi^2$) [2].
*   **Kasus 6: Hukum Hubble untuk Ekspansi Alam Semesta (Analisis Data Astronomi)**
    *   *Narasi*: Menggunakan data observasi astronomi jarak galaksi $r$ (megaparsec) versus kecepatan radial $v$ (km/s) dari 24 galaksi luar bimasakti. Data dicocokkan secara linier least-squares untuk menentukan konstanta Hubble ($H_0$) serta mengevaluasi sebaran statistik variansi kesalahannya [2].
*   **Kasus 7: Peluruhan Eksponensial Pion (Linierisasi Logaritma)**
    *   *Narasi*: Menganalisis peluruhan spontan partikel tidak stabil (pion) di mana laju peluruhan $dN(t)/dt$ dicocokkan dengan fungsi eksponensial $e^{-t/\tau}$. Proses fitting parameter diselesaikan melalui linierisasi logaritma ($\log N(t)$) terlebih dahulu untuk menghitung waktu hidup rata-rata pion ($\tau$) [2].
*   **Kasus 8: Resonansi Hamburan Neutron (Fitting Non-Linier Breit-Wigner)**
    *   *Narasi*: Mencocokkan data eksperimen penampang lintang hamburan neutron energi rendah pada inti karbon sebagai fungsi energi neutron menggunakan rumus Breit-Wigner. Sistem persamaan non-linier simultan ini diselesaikan menggunakan pendekatan Newton-Raphson dalam representasi matriks [2].
*   **Kasus 9: Spektrum Radiasi Benda Hitam (Satelit COBE NASA)**
    *   *Narasi*: Menganalisis data intensitas radiasi latar belakang kosmik gelombang mikro (CMB) asli dari satelit COBE milik NASA. Kelompok dituntut mencocokkan kurva radiasi benda hitam Planck menggunakan estimasi least-squares non-linier untuk membuktikan keselarasan data eksperimen dengan teori kosmologi [2].
*   **Kasus 10: Lintasan Proyektil dengan Hambatan Udara (PDB Orde-2)**
    *   *Narasi*: Memodelkan gerak jatuh bebas atau lintasan proyektil dengan memasukkan pengaruh gaya gesek udara yang bergantung pada kecepatan ($v$, $v^{1.5}$, atau $v^2$). Persamaan diferensial diselesaikan secara numerik menggunakan algoritma integrasi (Verlet atau Runge-Kutta) untuk melihat dampaknya terhadap jangkauan proyektil [2].
*   **Kasus 11: Dinamika Chaos Osilator Duffing (Visualisasi Fasa)**
    *   *Narasi*: Menyelesaikan persamaan diferensial non-linier dari osilator Duffing ($\ddot{x} + 2\gamma\dot{x} + \alpha x + \beta x^3 = F\cos\omega t$) menggunakan algoritma Runge-Kutta Orde 4 (RK4). Hasil disimulasikan dalam grafik posisi-waktu dan lintasan orbit di ruang fasa untuk mengidentifikasi perilaku kaotis [2].
*   **Kasus 12: Pendulum Realistik Damped-Driven (Diagram Bifurkasi)**
    *   *Narasi*: Menganalisis gerak pendulum non-linier yang dipengaruhi oleh torsi pemaksa periodik dan gaya gesek viskos. Kelompok bertugas memetakan kecepatan sudut ekstrem pendulum pada tiap periode gaya penggerak ke dalam diagram bifurkasi untuk mendeteksi transisi menuju fasa chaos [2].

---

## **2. Pembagian 12 Kelompok Praktikan Resmi (2 Orang per Kelompok)**

Sesuai dengan daftar kelompok resmi yang terdapat pada data praktikum [1, 2, 3, 4], berikut adalah pembagian kelompok mahasiswa beserta studi kasus fisis yang wajib dikerjakan:

| Kelompok | Anggota Kelompok Resmi | Studi Kasus yang Ditugaskan |
| :--- | :--- | :--- |
| **Group A** | **ALHENA ANKAA ALDEBARAN** (182231012)<br>**INTAN PERMATA** (182231048) [1] | Kasus 1: Inversi Numerik Matriks & Presisi Mesin [7] |
| **Group B** | **ASTRI DWI PRATIWI** (182241002)<br>**SARAH HAFIDHAH** (182241009) [1] | Kasus 2: Mode Normal Getaran String [7] |
| **Group C** | **AISAH** (182241012)<br>**NAILA ZHAFIRA QURROTU 'AINI** (182241010) [1] | Kasus 3: Keseimbangan Gaya Beban Tali [7] |
| **Group D** | **NAUFAL LUTFIAN HAKIM** (182241015)<br>**PRADITHYA PUTRA GALANG ISLAMI** (182241014) [2] | Kasus 4: Rotasi Benda Tegar & Tensor Inersia [7] |
| **Group E** | **ABDURRAHMAN RAFIF** (182241023)<br>**MUHAMMAD FARHAN FAUZAN** (182241024) [2] | Kasus 5: Analisis Suhu Batang Logam [7] |
| **Group F** | **DWI SAFAATIN** (182241025)<br>**JONATAN ADITIA SIHOMBING** (182241028) [2] | Kasus 6: Hukum Hubble & Ekspansi Alam Semesta [7] |
| **Group G** | **TENIA CESTRI AZMIYANTI** (182241041)<br>**ZUANIDA INDRI AGUSTIN** (182241029) [2, 3] | Kasus 7: Peluruhan Eksponensial Pion [7] |
| **Group H** | **AIRIN KHAIRUNNISA NUR RAERAH** (182241045)<br>**HENDRA MAULANA** (182241043) [3] | Kasus 8: Resonansi Hamburan Neutron [7] |
| **Group I** | **MAYTA RAHMAWATI** (182241049)<br>**PUTRI BALQISH PRITA AULIA** (182241051) [3] | Kasus 9: Radiasi Benda Hitam COBE [7] |
| **Group J** | **CAROLINE PUTRI KADRI** (182241052)<br>**MOHAMMAD AKHSAN ZAAKY** (182241054) [3, 4] | Kasus 10: Lintasan Proyektil & Hambatan Udara [7] |
| **Group K** | **EVA KHOIRUN NISA** (182241055)<br>**MOH. NAZRIL ILHAM ADZANI** (182241056) [4] | Kasus 11: Dinamika Chaos Osilator Duffing [7] |
| **Group L** | **DEA AYU KISSTIA** (182241062)<br>**GANDANI PUTRI LUNAGUSTAMA** (182241060) [4] | Kasus 12: Pendulum Realistik Damped-Driven [8] |

---

## **3. Rubrik Penilaian Praktikum Fisika Komputasi (7 Skala)**

Sesuai sistematika wajib laporan praktikum (Dasar Teori, Studi Kasus, Algoritma, Flowchart, Program, Analisa Hasil, dan Kesimpulan), rubrik penilaian ini dirancang menggunakan **7 skala tingkat performa** [10]:

### **A. Kriteria Penilaian dan Bobot**
1. **Dasar Teori & Studi Kasus Fisika (Bobot 20%)**: Ketepatan konsep fisika dan pemahaman masalah fisis nyata [10].
2. **Algoritma & Flowchart (Bobot 20%)**: Logika sistematis runut sebelum pengkodean dilakukan [10].
3. **Program/Kode Python (Bobot 30%)**: Fungsionalitas kode, efisiensi pemrograman (`numpy`, `matplotlib`), dan bebas error [10].
4. **Analisa Hasil & Kesimpulan (Bobot 30%)**: Kedalaman analisis numerik, ketepatan fisis, evaluasi error komputasi, dan penarikan kesimpulan [10].

### **B. Deskriptor Performa 7 Skala Penilaian**
*   **Skala 7 (Istimewa/Sempurna - Nilai 95-100)**
    *   *Kriteria*: Dasar teori fisis sangat mendalam; studi kasus dimodelkan dengan sempurna. Algoritma dan flowchart terstruktur secara profesional. Kode Python ditulis secara optimal (berbasis vektorisasi), bersih, terdokumentasi dengan baik, serta menghasilkan grafik/animasi visual yang sangat informatif dan presisi. Analisis hasil kritis, tajam, komprehensif mengevaluasi kestabilan numerik dan akumulasi error, serta kesimpulan merangkum esensi fisis secara utuh [11].
*   **Skala 6 (Sangat Baik - Nilai 86-94)**
    *   *Kriteria*: Teori fisis tepat dan studi kasus diulas dengan sangat baik. Algoritma dan flowchart runut. Program Python fungsional sepenuhnya tanpa error, grafiknya rapi dilengkapi label sumbu dan legenda yang jelas. Analisis hasil mendalam dengan interpretasi fisis yang matang serta pembahasan akurasi numerik yang relevan [11].
*   **Skala 5 (Baik - Nilai 78-85)**
    *   *Kriteria*: Pemahaman konsep fisika baik dengan studi kasus yang relevan. Logika pemrograman dituangkan dengan jelas pada flowchart. Kode Python berjalan lancar (mungkin ada redundansi penulisan logika ringan), grafik fisis terplot dengan benar. Analisis hasil sudah mengaitkan hasil numerik dengan perilaku fisika riil secara logis [11].
*   **Skala 4 (Cukup/Memenuhi Standar - Nilai 70-77)**
    *   *Kriteria*: Teori fisika mendasar terpenuhi namun studi kasus kurang dikaitkan secara spesifik. Flowchart dan algoritma ada tetapi memiliki beberapa celah logika. Program Python berfungsi, namun visualisasi data kurang optimal (misal, ukuran grafik tidak proporsional atau parameter visual kurang lengkap). Analisis hasil bersifat deskriptif dasar tanpa evaluasi error komputasi yang mendalam [11].
*   **Skala 3 (Cukup Kurang - Nilai 62-69)**
    *   *Kriteria*: Terdapat miskonsepsi minor pada teori fisika. Flowchart kurang runtut dan tidak selaras dengan kode program. Kode Python memerlukan revisi agar dapat berjalan dengan lancar (sering terjadi kegagalan logika parameter input). Analisis data sangat minim dan kesimpulan hanya berupa pengulangan ringkasan data [11].
*   **Skala 2 (Kurang - Nilai 40-61)**
    *   *Kriteria*: Dasar teori fisika tidak kuat dan studi kasus salah diinterpretasikan. Tidak ada algoritma/flowchart yang memadai. Program Python mengandung *syntax error* atau *runtime error* yang menghentikan eksekusi program. Analisis hasil tidak logis atau tidak sesuai dengan prinsip fisika numerik [11].
*   **Skala 1 (Sangat Kurang - Nilai < 40)**
    *   *Kriteria*: Laporan tidak lengkap; tidak menunjukkan pemahaman fisis maupun komputasional sama sekali. Program tidak dapat dijalankan atau sekadar menyalin kode tanpa modifikasi studi kasus [11].
