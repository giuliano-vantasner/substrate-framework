---
status: active
owner: giuliano
canonical_issue: https://github.com/vantasnerdan/substrate-framework/issues/225
updated: '2026-10-28'
---

# Ni/H collective-response solution map

The objective is a material-calibrated many-region simulation, a defensible lattice comparison, and an explicit nuclear-transition/energy-disposal construction. This map keeps that whole objective visible. Nodes are scientific outputs, not approval checkpoints. The user's 28 October instruction is to reuse real existing solutions, solve the missing core nodes, and avoid process minutiae. The authoritative scope is [P254](proposal.yaml).

## Core scientific work

Solid arrows identify material inputs needed by a result. The nuclear mechanism can be investigated now; its material predictions eventually consume the calculated response. No open node is marked complete merely because a helper or a finite example works.

```mermaid
flowchart TD
    R["R · Common material reference and initial state\nIN PROGRESS"]
    S["S · Spatial and inter-region coupling\nOPEN"]
    E["E · Material field, environment and fluctuations\nOPEN"]
    D["D · Actual many-region dynamics and correlations\nOPEN"]
    C["C · Controlled lattice comparison\nOPEN"]
    N["N · Nuclear transition and energy disposal\nOPEN"]
    R --> S
    R --> E
    R --> D
    S --> D
    E --> D
    D --> C
    E --> N
    D --> N
    C --> N
```

| Node | Required scientific output | Current work |
| --- | --- | --- |
| R | A declared full-material state with consistent density, force and curvature accounting; reference drift and approximation error remain visible. | Extend the accepted full-grid population recipe beyond the selected Gamma state and consume the existing material operators. |
| S | Material-derived finite-wavevector and inter-region operators, with the actual ionic/electronic spatial coverage. | Construct the missing rectangular Bloch-sector coupling; distinguish available frozen curvature from missing ionic-wavevector data. |
| E | A physical material/field/environment construction with its corresponding fluctuations and energy transfer. | Evaluate retained electronic degrees of freedom and sourced response reductions; no fitted damping constant substitutes for an unsolved environment. |
| D | Actual material trajectories after local excitation, baseline motion, connected space/time correlations and energy accounting. | Compose the completed R/S/E solutions with the existing evolution machinery. |
| C | Matched lattice comparisons whose conclusions survive relevant numerical, size and physical controls. | Reuse completed material structures; calculate missing comparative response, rather than rank hydrogen inventory. |
| N | A sourced transition operator and medium coupling with explicit energy/product disposal. | Investigate concrete mechanisms and available physical inputs; electronic or vibrational correlation alone does not supply a nuclear rate. |

The integrated result receives one complete scientific review and its necessary corrections, then the required distinct-authorized merge. These are delivery work, not extra scientific nodes.

## What is complete and reusable

These are completed constructions at their recorded scopes. The entries below identify existing solutions only; they do not imply an existing solution for every open node.

```mermaid
flowchart LR
    G["COMPLETE · Saved Ni/H material structures and original data"]
    O["COMPLETE · Saved-density H0/K and full-PW ionic/observable operators"]
    B["COMPLETE · Finite ionic scalar, full Bloch representation and neutral population recipe"]
    T["COMPLETE · Prepared mean/tangent/covariance evolution on finite examples"]
    Q["COMPLETE · Exact finite matter/bath and response algebra"]
    G --> R["R · Material reference"]
    O --> R
    B --> R
    B --> S["S · Spatial coupling"]
    O --> S
    Q --> E["E · Field/environment"]
    O --> E
    T --> D["D · Material dynamics"]
    G --> C["C · Lattice comparison"]
```

| Existing solution | Reuse | Evidence and scope |
| --- | --- | --- |
| Saved full-host material structures and original electronic files | Material geometry, species, masses and source wavefunctions; matched structural controls. | [Primary-material completion](https://github.com/vantasnerdan/substrate-framework/issues/225#issuecomment-6414684011). Declared coarse stationary inputs are complete; numerical calibration and coupled spectra are not thereby complete. |
| Matched saved-density Hamiltonian/kernel and full-PW force/number factors | Existing `qe_material_hamiltonian.py` and material factor/readback APIs, rather than another DFT reconstruction. | [A25 admission](attempts/0025/review-admission.json), with actual-material output and separate readback. This does not select a physical equilibrium state. |
| Full-coordinate material maps and prepared-state evolution | Existing `PreparedReference`, `PreparedFactorDynamics`, prepared covariance and observable consumers. | [A26 admission](attempts/0026/review-admission.json). Actual material maps are complete; finite-time prepared evolution was exercised on a synthetic system, not a completed material trajectory. |
| Finite ionic scalar/common force reference; lazy full Bloch grid; conditional neutral preparation | Existing ionic, `qe_bloch_*`, `material_preparation_*` and authenticated saved-output consumers. | [A27 admission](attempts/0027/review-admission.json). Full electronic representation and population ledger are complete; actual raw preparation/readout covers one selected Gamma sector. Finite ionic sums are not a convergence certificate. |
| Exact matter/field/bath elimination and finite-fermion response identities | Existing `material_matter_field.py` and the admitted finite-fermion constructions. | [A1](attempts/0001/receipt.json) and [A7](attempts/0007/receipt.json), also identified in [the source inventory](proposal.yaml). These supply algebra, not Ni-specific loss parameters or a nuclear mechanism. |

## Current focus

R is the first integration target. Independent investigations are finding the concrete S, E and N constructions while R advances. Existing passed results remain in use; they are not rerun to increase a validation tally. Computation and new equations will be checked where they produce a useful result. The remaining physical objective is not reduced to the available inventory.

Source and result details stay in the linked attempts. This document changes when a core result changes, not for every administrative action.
