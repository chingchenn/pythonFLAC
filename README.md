# pythonFLAC

Python post-processing and analysis tools for FLAC (Fast Lagrangian Analysis of Continua) geodynamic simulations. Developed for the Master's thesis at National Taiwan University (2022) on flat slab subduction.

`flac.py` is originally from [tan2/geoflac-old](https://github.com/tan2/geoflac-old). See also the personal FLAC solver fork at [chingchenn/geoflac](https://github.com/chingchenn/geoflac).

## Related Publication

**Origin and Evolution of Flat Slab Subduction: Insights From Numerical Geodynamics Modelling**  
Ji-Ching Chen, National Taiwan University, 2022  
DOI: [10.6342/NTU202300033](http://dx.doi.org/10.6342/NTU202300033)

## Usage

Basic workflow:

1. Run `Main_creat_database.py` to process and organize model output
2. Run individual analysis scripts (e.g. `2.plate_dip_gem.py`, `8.check_flat_slab.py`) for specific analyses
3. Run `Main_snapshot.py` for visualization of a specific time frame

## Main Scripts

| File | Description |
|------|-------------|
| `Main_creat_database.py` | Main code for model analysis |
| `Main_snapshot.py` | Analysis for a specific time frame |
| `function_for_flac.py` | Core utility functions |
| `15.slab_analysis.py` | Slab analysis (see requirements below) |

## Notes

> ⚠️ `15.slab_analysis.py` requires GMT with extra `.grd`, `.cpt`, and `kkk.csv` files, and can only be run on:
> - `140.115.20.181`
> - `140.109.81.186`
> - `140.110.148.11`

> ⚠️ `getDistance` in `function_for_flac.py` is **Python 3 only** (2021-12-03)
