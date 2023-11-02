from bidict import bidict

power_enumerator = bidict({
    'nosignal': 0,
    '-27.5db': 1,
    '-25.5db': 2,
    '-24.5db': 3,
    '-24db': 4,
    '-23.5db': 5,
    '-23db': 6,
})
setting_enumerator = bidict({
    'entangledsensing': 0,
    'entangledsensingnonoise': 1,
    'productsensing': 2
})