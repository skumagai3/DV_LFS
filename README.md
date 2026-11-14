# DV_LFS

Large data files for [DeepVoid](https://github.com/skumagai3/deepvoid), kept
apart from the code so that cloning the code does not download several
gigabytes. The files are stored with Git LFS.

## Files

All grids are periodic boxes stored as compressed NumPy `.npz` files. Axis
order is (x, y, z) and lengths are in h⁻¹ Mpc. Each file holds:

- `data`: the values, as uint8 for the class masks (0 void, 1 wall,
  2 filament, 3 halo) and float32 for everything else;
- `header`: a JSON string with the box size and where the file came from;
- `fvol_header`: the 256-byte header of the original `.fvol` file.

```python
import numpy as np
grid = np.load("TNG/DM_DEN_snap99_Nm=512.npz")["data"]
```

or, with DeepVoid installed, `deepvoid.io.load_volume(path)`.

These files replaced the original `.fvol` files in November 2026. No value was
changed: every original file can be rebuilt byte for byte, and its SHA-256
checksum (kept in `header`) matches the one Git LFS recorded for it.

```python
import hashlib, json, numpy as np
f = np.load("TNG/DM_DEN_snap99_Nm=512.npz")
raw = f["fvol_header"].tobytes() + f["data"].astype("<f4").tobytes()
assert hashlib.sha256(raw).hexdigest() == json.loads(str(f["header"]))["meta"]["source_sha256"]
open("DM_DEN_snap99_Nm=512.fvol", "wb").write(raw)
```

The `.fvol` files are still in this repository's history.

### `TNG/`: IllustrisTNG TNG300-3-Dark, redshift 0 (snapshot 99)

205 h⁻¹ Mpc box, 512³ cells of 0.40 h⁻¹ Mpc.

| File | Contents |
|---|---|
| `DM_DEN_snap99_Nm=512.npz` | Dark-matter density from all particles |
| `TNG300-3-Dark-mask-Nm=512-th=0.65-sig=2.4.npz` | T-web classes (0 void, 1 wall, 2 filament, 3 halo) from that density: Gaussian smoothing of 2.4 cells, eigenvalue threshold 0.65 |
| `subs1_mass_Nm512_L5_d_None_smooth.npz` | Mass density of the most massive subhalos, kept so that their mean separation is 5 h⁻¹ Mpc |
| `subs1_mass_Nm512_L10_d_None_smooth.npz` | The same at a mean separation of 10 h⁻¹ Mpc |

### `Bolshoi/`: the Bolshoi simulation, redshift 0

250 h⁻¹ Mpc box, 640³ cells.

| File | Contents |
|---|---|
| `Bolshoi_halo_CIC_640_L=0.122.npz` | The dense field (mean separation 0.122 h⁻¹ Mpc) |
| `Bolshoi_bolshoi.delta416_mask_Nm=640_sig=0.916_thresh=0.65.npz` | T-web classes, smoothing 0.916 h⁻¹ Mpc, threshold 0.65 |
| `Bolshoi_halo_CIC_640_L=5.0.npz` | Halos at a mean separation of 5 h⁻¹ Mpc (cloud-in-cell) |
| `Bolshoi_halo_CIC_640_L=10.0.npz` | The same at 10 h⁻¹ Mpc |

## Credit

**IllustrisTNG.** The TNG data are provided by the IllustrisTNG
collaboration (https://www.tng-project.org). If you use them, cite the
TNG100/TNG300 introductory papers and the public data release:

- Springel, V., et al. 2018, MNRAS, 475, 676
- Pillepich, A., et al. 2018, MNRAS, 475, 648
- Nelson, D., et al. 2018, MNRAS, 475, 624
- Naiman, J. P., et al. 2018, MNRAS, 477, 1206
- Marinacci, F., et al. 2018, MNRAS, 480, 5113
- Nelson, D., et al. 2019, Computational Astrophysics and Cosmology, 6, 2

**Bolshoi.** If you use the Bolshoi files, cite the simulation, and the
halo finder for the halo grids:

- Klypin, A. A., Trujillo-Gomez, S., & Primack, J. 2011, ApJ, 740, 102
  (the Bolshoi simulation)
- Klypin, A., & Holtzman, J. 1997, arXiv:astro-ph/9712217 (the Bound
  Density Maxima halo finder)

The Bolshoi simulations were performed within the Bolshoi project of the
University of California High-Performance AstroComputing Center (UC-HiPACC)
and were run at the NASA Ames Research Center. The Bolshoi data were
obtained from the CosmoSim database, which asks for this acknowledgment:
"The CosmoSim database used in this paper is a service by the
Leibniz-Institute for Astrophysics Potsdam (AIP). The MultiDark database was
developed in cooperation with the Spanish MultiDark Consolider Project
CSD2009-00064."

**DeepVoid.** The grids and masks were made for

- Kumagai, S., Vogeley, M. S., Aragon-Calvo, M. A., Douglass, K. A.,
  BenZvi, S., & Neyrinck, M. 2025, DeepVoid: A Deep Learning Void Detector,
  [arXiv:2504.21134](https://arxiv.org/abs/2504.21134)
