---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

Download cv [here](/cv.pdf)

## Summary
%FORMAT[summary][FILL] %%\n

%FORMAT[affiliations][LIST] *%0%, %1%*\n


## Research Interests
%FORMAT[interests][LIST]* **%name%**: %desc%


## Experience
%FORMAT[experience][LIST]**%name%**  \n*%location%*, %start% - %end%  \n%info%  \n%output%  \n%bullets%\n
%FORMAT[other_experience][LIST]**%name%**  \n*%location%*, %start% - %end%  \n%info%  \n%output%  \n%bullets%\n


## Education
%FORMAT[education][LIST]**%qualification%**  \n*%location%*, %start% - %end%  \n%notes%\n


## Publications
  <ul>{% for post in site.publications %}
    {% include archive-single-cv.html %}
  {% endfor %}</ul>
  
  
## Submitted and in preparation
%FORMAT[unpublished][LIST]* *%title%*, %authors% - %pub%


## Presentations
%FORMAT[presentations][LIST]* **%meeting%**, %location%  \n%organiser%  \n%what%