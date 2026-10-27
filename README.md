# CFKS: Continuum-Feature Kernel PDE Solvers

**Research code accompanying the manuscript _CFKS: Continuum-Feature Kernel PDE Solvers_.**

This repository contains Python and Jupyter notebook implementations of the continuum-feature kernel solver (CFKS) and the numerical experiments discussed in the manuscript.

## Method overview

CFKS analytically averages Gaussian radial basis function (RBF) features over prescribed, bounded distributions of feature centers. The resulting deterministic mean kernel and its analytically differentiated operator kernels are used to construct numerical approximations to differential equations. Unlike a finite random-feature implementation, CFKS does not require selecting a finite RBF feature count or sampling individual feature centers. The user still specifies kernel widths, center distributions, collocation sites, and regularization settings.

The examples include linear operator-kernel collocation, enforcement of physical constraints, residual-guided collocation enrichment, sequential space--time-slab solutions, and a nonlinear least-squares formulation for viscous Burgers' equation.

## Repository contents

The existing top-level directories are organized by numerical experiment:

| Path | Numerical experiment |
| --- | --- |
| `ODE_FO/` | First-order oscillatory ODE |
| `ODE_SO/` | Second-order oscillatory ODE |
| `ODE_MS/` | Multiscale ODE |
| `POISSON/` | Poisson equation on an irregular five-petal domain |
| `BIH/` | Biharmonic equation on an irregular five-petal domain |
| `SPP/` | Singularly perturbed boundary-value problem |
| `ADV/` | Periodic advection of one Gaussian pulse |
| `ADV_DIFF/` | Advection--diffusion of a Gaussian pulse |
| `ADV2_GAUSSIAN/` | Periodic advection of two Gaussian pulses |
| `BURGERS_0.01_FINAL/` | Viscous Burgers' equation at viscosity `nu = 0.01` |
| `CONVERGE/` | Finite-feature-to-continuum convergence study |
| `CONDITION/` | Kernel conditioning and regularization study |
| `kapi_onet_publication_style.py` | Shared plotting utilities used in publication figures |

## Installation

A Python environment with **Python 3.10 or newer** is recommended. On Ubuntu or another Linux distribution, run the following commands from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
jupyter lab
```

The initial `requirements.txt` lists the core packages directly used by the available Burgers notebooks and plotting utilities. Other experiments should be checked for any additional dependencies before the repository is designated as a fully reproducible release. Exact package versions for the archived publication release should also be recorded.

## Running the experiments

Open the relevant notebook in its experiment directory and run its cells in order. Some notebooks generate intermediate data and figures that are needed by later processing stages. The required inputs and output paths should be checked before execution.

### Burgers predictor--corrector workflow

The viscous Burgers experiment has three logical stages:

1. **Stage 1 (predictor):** solve 40 sequential space--time slabs with coarse collocation and evaluate independent residual indicators. The predictor produces `CFKS_BURGERS_MS_NU001_STAGE01_ATTENTION.npz`.
2. **Stage 2 (corrector):** load the Stage-1 attention file, independently restart the temporal march from the original initial condition, and solve with residual-adaptive collocation and narrower prescribed Gaussian widths. The corrector produces `CFKS_BURGERS_MS_NU001_STAGE02_RESULTS.npz`.
3. **Publication post-processing:** load both `.npz` files to generate the solution figures, attention maps, collocation-level visualization, and a summary CSV under `publication_figures/`.

For this workflow, run the notebooks with the **Burgers experiment directory as the working directory**, keeping both generated `.npz` files in that directory. The publication post-processing notebook imports `kapi_onet_publication_style.py`; make sure that module is available in its Python import path (for example, by copying it from the repository root into the Burgers experiment directory if needed).

The predictor and corrector use **different Gaussian kernel widths**, so the improvement in the nonlinear benchmark reflects both residual-driven collocation refinement and kernel-scale refinement. These contributions were not isolated in the reported experiment.

## Reproducibility notes

- Kernel mean functions are evaluated analytically; the numerical implementations do not require sampled Gaussian feature centers.
- The collocation points, Gaussian widths, center-support intervals, and regularization parameters are still prescribed numerical choices.
- In sequential time-dependent problems, terminal profiles may be interpolated for transfer between slabs; this introduces a separate numerical approximation.
- Figure-generation code may rely on files generated by earlier notebooks. Avoid deleting intermediate outputs until the complete workflow has been reproduced.
- Runtime measurements depend on the machine, numerical libraries, and execution environment.

## Citation

Please refer to [`CITATION.cff`](CITATION.cff) for software citation information. The bibliographic details of the associated journal article and any archived software DOI will be added when available.

## License

A software license has not yet been selected. The repository being publicly accessible does not by itself grant permission to reuse or redistribute the code. License information will be added after the appropriate author and institutional permissions have been confirmed.
