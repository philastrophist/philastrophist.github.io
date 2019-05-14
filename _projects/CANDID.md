---
title: "CANDID"
excerpt: "Complete And Noiseless Distributions from Incomplete Data"
github: philastrophist/candid
collection: projects
---
CANDID - "Complete And Noiseless Distributions from Incomplete Data".

A flexible expectation-maximisation (EM) method that implements and builds upon the principles of [Extreme Deconvolution (Bovy+11)](https://github.com/jobovy/extreme-deconvolution). 

Unlike [PyGMMIS](https://github.com/pmelchior/pygmmis), CANDID's intended purpose is the full modelling of highly multi-dimensional galaxy property distributions when the data are missing are biased - an outstanding problem in astronomy with no one easy fix.

CANDID deals with the following issues, many of which have known solutions, just not ones that are implemented together. 

1.  **Heteroscedasticity**

    It is common for each data point to have its own uncertainty
    distribution. Moreover, the size of the uncertainty distribution
    frequently changes across the parameter space. In the fitting of
    simple models, heteroscedasticity is incorporated naturally with the
    addition of a $$\chi^2$$-like term into the likelihood. Extreme Deconvolution handles heteroscedasticity.

2.  **Non-Gaussianity**

    Assuming a Gaussian error distribution dramatically simplifies the
    posterior and hence the analysis. However, the Gaussian assumption
    is frequently incorrect and may lead to dramatically misleading
    results. For example, the uncertainty distribution of a flux
    measurement is easily approximated as Gaussian but given that the
    intrinsic value is strictly positive, this assumption breaks down at
    low signal-to-noise. resamples the uncertainty distribution of each
    data point consistently such that flux variables remain strictly
    positive. The Gaussian mixture EM algorithm can readily be extended
    to incorporate resampled data points instead of directly solving for
    the convolution of the data uncertainty and model components.
    resampled data).

3.  **Incompleteness**

    It is not possible to rerun the universe nor observe the entirety of
    a population in astronomy. Typically, incompleteness is addressed by
    methods such as $$1/V_{max}$$ or Monte Carlo simulations of point
    sources given an error map. However, when the
    number of dimensions grows, what is applicable to each variable
    individually becomes complicated when considering their covariation.
    aims to deal with incompleteness naturally by “imputing” the missing
    values from the approximated observed model given known selection
    criteria, following [PyGMMIS](https://github.com/pmelchior/pygmmis).

4.  **High dimensionality**

    The “curse of dimensionality” firmly applies to Gaussian mixture
    models since each Gaussian component contributes $$d(d+1)/2 + d + 1$$
    dimensions to the likelihood from its covariance matrix, mean vector
    and weight relative to the other components. Rejection sampling MCMC
    techniques start to fail at tens of parameters and interpolating
    ensemble MCMC (such as `emcee`) fails at hundreds of parameters. The
    EM algorithm is well suited to finding the peak of the posterior
    distribution. By dropping the need to sample the entire posterior
    distribution, we can iterate towards the maximum likelihood peak and
    then bootstrap, if need be, to sample its width.


This is very much a work in progress!