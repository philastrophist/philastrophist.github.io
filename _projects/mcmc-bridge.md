---
title: "MCMC-Bridge"
excerpt: "Have the best of both worlds: emcee and PyMC3"
github: philastrophist/mcmc-bridge
collection: projects
---
[PyMC3](https://docs.pymc.io/) is a platform in which to specify your Bayesian hierarchical model. It is a probabilistic language but also contains it's own samplers.

{% highlight python %}
import pymc3 as pm
with pm.model() as model:
    mu = pm.Normal('mu', mu=0, sd=1)  # set priors
    sd = pm.HalfCauchy('sd', 10)
    observed = pm.Normal('observed', mu=mu, sd=sd, observed=data)
    trace = pm.sample(1000)
{% endhighlight %}

[emcee](http://emcee.readthedocs.io/) is a ubiquitous, perhaps the go-to sampler for astronomers. It is probably the first sampler you'll come across in the literature because it is very powerful.
[emcee](http://emcee.readthedocs.io/) is an affine-invariant sampler, so it can deal with complex multi-dimensional likelihoods. 
[PyMC3](https://docs.pymc.io/) just doesn't have a comparable sampler in its arsenal and integrating them is actually not straightforward.

Here's where MCMC-Bridge comes in.

{% highlight python %}
from mcmc_bridge import EmceeTrace, export_to_emcee, get_start_point
with model:
    sampler = export_to_emcee(nwalker_multiple=nwalker_multiple)
    start = get_start_point(sampler) 
    sampler.run_mcmc(start, steps)
    trace = EmceeTrace(sampler)  # pymc3 trace object!
{% endhighlight %}

You can simply write your model as before but then export to the emcee sampler to run it! We can then easily turn the emcee trace back into the flexible PyMC3 trace object and continue on our way.
Emcee can utilise MPI and multi-processing and so MCMC-Bridge allows the easy use of cluster resources by adding a `pool` or `threads` option to `export_to_emcee`.