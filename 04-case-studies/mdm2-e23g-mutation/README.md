This tutorial notebook shows how to setup an alchemical protein mutation involving a charge changing-transformation. Specifically, the tutorial looks at the E23G salt-bridge breaking mutation in oncoprotein MDM2, [as part of this study](https://pubs.acs.org/doi/10.1021/acs.jctc.5c01648).

> [!CAUTION]
> This tutorial demonstates how to run a charge-changing mutation in SOMD2. It it does not demonstrate how to reproduce full ΔΔG values for the E23G mutation, as the protein system studied above represents a highly challenging case of FEP, due to:
> 1. Intrinsically disordered region present in the protein mutation site, requiring specialised protein forcefields and water models to model the IDR behaviour of the protein appropriately.
> 2. Salt-bridge breaking mutation which introduces significant flexibility to protein fold and will require long sampling times to converge. 