# L1 Camera-Family Visual Review

## Decision

**L1 status: PARTIAL PASS.**

The Camera Grammar remains viable. The main issue discovered is not a grammar defect, but a validation-fixture imbalance and two overconfident fixture labels from CRVM V1.

## What is stable

### CG-A
CG-A is strongly represented by the current package. The following are clean positives:

- RDR-F02 GOTHAM HOTEL
- RDR-F03 ECONOMY CANDY
- RDR-F04 GOOD EARTH BAR
- RDR-F05 RAJA GROCERY
- RDR-F06 LOANS / OSCARS
- SC-B01 PEEP SHOW
- SC-D02 M&G SOUL FOOD

SC-D01 BASIC METAL is a moderate but still useful CG-A example.

### CG-B
Two independent fixtures are strong:

- RDR-F01 L. KATZENSTEIN / DAVE'S CORNER
- SC-B02 NEON HOTEL STREET

RDR-F07 DAVE'S CORNER is **not an additional independent example**. It is pixel-identical to RDR-F01 despite the different filename/format.

## Boundary corrections

### SC-D03 CONDOS FOR SALE
V1 provisionally mapped this to CG-B. Visual review shows that this is too strong.

The image contains oblique urban depth, but the composition is a distributed urban field rather than a facade/corner-dominant architectural view. It is more useful as a **NON_DIAGNOSTIC negative control**.

### SC-D06 PHARMACY OUTPUT
V1 mapped this to CG-B. The image is actually a useful **A/B boundary**.

The pharmacy facade dominates and stays close to elevation, favoring CG-A, while the side street creates meaningful recession associated with CG-B. Classification:

**BOUNDARY_A_B_LEAN_A**

This is exactly the type of fixture we want to retain for boundary calibration.

## Coverage result

The current package is heavily biased toward CG-A. That is expected from the RDR heritage material, but it means L1 cannot by itself prove that CG-B behaves consistently across VP00, VP01 and VP02.

Therefore the correct next step is not to rewrite the grammar. It is to make L2 deliberately balanced.

## L2 required cells

| Profile | CG-A | CG-B |
|---|---|---|
| VP00 | required | required |
| VP01 | required | required |
| VP02 | required | required |

Each cell must use a controlled source/task where the selected camera family is structurally justified.

## Gate

L2 may begin now.

Before final validation, we should have at least:
- 3 independent clean CG-A outputs, one per profile;
- 3 independent clean CG-B outputs, one per profile;
- 1 A/B boundary case;
- 1 source-locked CG-S case;
- confirmed Fear City CG-FC tests in L3.
