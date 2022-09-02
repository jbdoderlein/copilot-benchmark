import numpy as np
import scipy.stats
from scipy.special import comb

def pass_at_k(n, c, k):
    """
    Compute the pass@k metric for a given number of samples and number of correct samples.

    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$
    """
    if n - c < k:
        return 1.0
    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))

def pass_at_k_2(n_1, c_1, k_1, n_2, c_2, k_2):
    """
    Compute the pass@k metric for a given number of samples and number of correct samples 
    from 2 distributions.
    """
    if n_1 - c_1 < k_1:
        return 1.0
    if n_2 - c_2 < k_2:
        return 1.0
    return 1.0 - (np.prod(1.0 - k_1 / np.arange(n_1 - c_1 + 1, n_1 + 1)) * np.prod(1.0 - k_2 / np.arange(n_2 - c_2 + 1, n_2 + 1)))

def pass_k(problems, n, k):
    """
    Compute the pass@k metric for a given list of problems.

    :param problems: list of problems total number of correct samples
    :param n: total number of samples
    :param k: k in pass@$k$
    """
    res = 0
    for problem in problems:
        res += pass_at_k(n, problem, k)
    return res/len(problems)
