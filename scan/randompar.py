"""Generate random parameter points in single-mediator models"""


import numpy as np
from scipy.stats import unitary_group


def random_unitary(n):
    """Random matrix from the unitary group U(n)"""
    m = unitary_group.rvs(n)
    return m


def random_complex(n, norm=1):
    """Random complex nxn matrix"""
    m = np.random.rand(n, n) + 1j * np.random.rand(n, n)
    r = m / np.sqrt(2) * norm
    if n == 1:
        return r[0, 0]
    return r


def random_hermitian(n, norm=1):
    """Random hermitian nxn matrix"""
    m = random_complex(n, norm=norm)
    return (m + m.T.conj()) / 2


def random_log_uniform(low, high, size=1):
    """Random number between `low` and `high` with a uniform distribution
    for its logarithm"""
    r = np.exp(np.random.uniform(np.log(low), np.log(high), size))
    if size == 1:
        return r[0]
    return r

def random_omega1():
    p = {}
    g = random_log_uniform(1e-3, 1e-1)
    p['yomega1eu'] = np.array([g * random_complex(3)])
    p['yomega1ql'] = np.array([g * random_complex(3)])
    p['Momega1'] = [random_log_uniform(500, 20000)]
    return {'p': p, 'scale': p['Momega1'][0]}
