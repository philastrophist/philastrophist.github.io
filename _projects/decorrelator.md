---
title: "Decorrelator"
excerpt: "Simple Bayesian partial correlation"
github: philastrophist/decorrelator
collection: projects
---
Analysing correlations between parameters whilst controlling for the effects of others (Fancy partial correlation).

This code is an evolution of the one used in [The Far-Infrared Radio Correlation at low radio frequency with LOFAR/H-ATLAS](/publication/2018-11-00-The-Far-Infrared-Radio-Correlation-at-low-radio-frequency-with-LOFAR-H-ATLAS).

![alt text](/images/q_mirdd_lofar_new-page-001.jpg "Measuring the FIRC with LOFAR and H-ATLAS")

I borrowed heavily from [PyMC3](https://docs.pymc.io/)'s [Covariance estimation notebook](https://docs.pymc.io/notebooks/LKJ.html) and added some other syntax to allow you to easily specify additional correlates without worrying about priors, starting points, step method, and all of that jazz!
