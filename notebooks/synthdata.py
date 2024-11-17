import numpy as np
import pandas as pd
import pyrolite.comp
from pyrolite.util.synthetic import normal_frame
from scipy.stats.distributions import poisson


def get_synthetic_data(
    columns=["CaO", "MgO", "SiO2", "FeO", "Na2O", "Ni", "Ti", "La", "Lu", "Te"],
    seed=24,
    **kwargs,
):
    # synthetic data with a multivariate normal distribution in log-transformed space
    df = normal_frame(columns=columns, seed=seed, **kwargs) * 100
    # simulate some ppm data in a fairly blunt way
    df[df.pyrochem.list_elements] *= 10
    # simulate some Sr isotope data
    df["Sr87/Sr86"] = (
        0.0700 / 0.0986
        + (np.random if seed is None else np.random.RandomState(seed)).randn(
            df.index.size
        )
        * 0.0001
    )
    return df


def count_based_signal(
    columns=["18O", "17O", "16O"],
    size=25,
    bias=np.array([0, 0]),
    strength=10e6,
    seed=14,
):
    """
    Generate approximate signals from a constant sample ratio (bias ratios)
    assuming the individual isotope signals are Poisson distributed.

    Parameters
    ----------
    columns : list
        Columns/isotopes to simulate.
    size : int
        Number of samples to draw (how many counting intervals of <strength> counts).
    strength : float
        Integrated signal strength across all signals for a single counting period.
    bias : numpy.ndarray
        Array of logratios [log(A/C), log(B/C)] for columns [A, B, C].

    Returns
    -------
    pandas.DataFrame

    Notes
    -----
    * Defaults to 1 million counts total
    """
    df = pd.DataFrame(bias * np.ones((1, len(columns) - 1)))
    # use the dataframe-based inverse ALR method from pyrolite.comp
    df = df.pyrocomp.inverse_ALR() * strength
    output = pd.DataFrame(
        poisson.rvs(df.T, size=(3, size), random_state=seed).T, columns=columns
    )
    output = output / output.sum(axis=1).values[:, None] * strength
    return output
