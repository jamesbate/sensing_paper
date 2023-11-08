from qutip import qobj


def quantum_fischer_information(rho: qobj, generator):
    (eig_energies, eig_states) = rho.eigenstates()
    generator_diag = generator.transform(
        eig_states)
    F = 0
    for j, ej in enumerate(eig_energies):
        for k, ek in enumerate(eig_energies):
            if abs(ej - ek) < 1e-10:
                continue
            F += 2 * (ej - ek) ** 2 / (ej + ek) * abs(
                generator_diag.full()[j, k]) ** 2
    return F
