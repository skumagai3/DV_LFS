# DV_LFS

Large data files for [DeepVoid](https://github.com/skumagai3/deepvoid), kept
apart from the code so that cloning the code does not download several
gigabytes. The files are stored with Git LFS.

## Files

All grids are periodic boxes in the `.fvol` format (a short header followed
by the values as float32). Read them with `deepvoid.io.read_fvol`. Axis order
is (x, y, z) and lengths are in h⁻¹ Mpc.

### `TNG/`: IllustrisTNG TNG300-3-Dark, redshift 0 (snapshot 99)

205 h⁻¹ Mpc box, 512³ cells of 0.40 h⁻¹ Mpc.

| File | Contents |
|---|---|
| `DM_DEN_snap99_Nm=512.fvol` | Dark-matter density from all particles |
| `TNG300-3-Dark-mask-Nm=512-th=0.65-sig=2.4.fvol` | T-web classes (0 void, 1 wall, 2 filament, 3 halo) from that density: Gaussian smoothing of 2.4 cells, eigenvalue threshold 0.65 |
| `subs1_mass_Nm512_L5_d_None_smooth.fvol` | Mass density of the most massive subhalos, kept so that their mean separation is 5 h⁻¹ Mpc |
| `subs1_mass_Nm512_L10_d_None_smooth.fvol` | The same at a mean separation of 10 h⁻¹ Mpc |

### `Bolshoi/`: the Bolshoi simulation, redshift 0

250 h⁻¹ Mpc box, 640³ cells.

| File | Contents |
|---|---|
| `Bolshoi_halo_CIC_640_L=0.122.fvol` | The dense field (mean separation 0.122 h⁻¹ Mpc) |
| `Bolshoi_bolshoi.delta416_mask_Nm=640_sig=0.916_thresh=0.65.fvol` | T-web classes, smoothing 0.916 h⁻¹ Mpc, threshold 0.65 |
| `Bolshoi_halo_CIC_640_L=5.0.fvol` | Halos at a mean separation of 5 h⁻¹ Mpc (cloud-in-cell) |
| `Bolshoi_halo_CIC_640_L=10.0.fvol` | The same at 10 h⁻¹ Mpc |

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
and were run at the NASA Ames Research Center.

**DeepVoid.** The grids and masks were made for

- Kumagai, S., Vogeley, M. S., Aragon-Calvo, M. A., Douglass, K. A.,
  BenZvi, S., & Neyrinck, M. 2025, DeepVoid: A Deep Learning Void Detector,
  [arXiv:2504.21134](https://arxiv.org/abs/2504.21134)
