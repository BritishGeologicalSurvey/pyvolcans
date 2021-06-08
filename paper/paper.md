---
title: 'PyVOLCANS: A Python package to flexibly explore similarities and differences between volcanic systems'
tags:
  - Python
  - volcanology
  - volcanic hazard assessment
  - data scarcity
  - analogue volcanoes
authors:
  - name: Pablo Tierz^[Corresponding author]
    orcid: 0000-0001-8889-9900
    affiliation: 1
  - name: Vyron Christodoulou^[Now at The Data Lab, University of Edinburgh, Edinburgh, UK]
    orcid: 0000-0003-3835-3891
    affiliation: 1
  - name: John A. Stevenson
    orcid: 0000-0002-2245-1334
    affiliation: 1
  - name: Susan C. Loughlin
    affiliation: 1
affiliations:
 - name: British Geological Survey, The Lyell Centre, Edinburgh, UK.
   index: 1
date: 13 May 2021
bibliography: paper.bib
---

# Summary

Volcanic systems are fascinating geological environments that connect the inner layers
of the Earth with the surface of the lithosphere, and the other _spheres_ in the planet:
hydrosphere, atmosphere and biosphere. Volcanoes have also a unique interaction with human
populations, compared to hazardous phenomena such as earthquakes, floods or landslides.
On the one hand, volcanic systems are able to attract fascination and create a sense
of belonging among visitors and local populations. Volcanoes also provide a range of economic
benefits, such as fertile soils, geothermal energy or valuable mineralizations. However,
these benefits are compounded with the fact that volcanic systems can also generate a great
variety of hazardous phenomena, which pose a significant risk to inhabitants, tourists and
infrastructure at distances from few metres to tens/hundreds of kilometres from where volcanic
activity is taking place.

In order to understand and quantify volcanic hazard, volcano scientists must tackle
the following complex questions: When an eruption (or a change in volcanic activity)
may occur? From where volcanic activity may be sourced? What type of volcanic phenomena
may be generated (e.g. lava flows, pyroclastic flows, volcanic bombs, etc.)? What scale
or size these phenomena may reach? What areas on and around the volcanic system may be
impacted as a result? Etc.

The available data to answer these questions, quantitatively, are scarce at the vast
majority of volcanoes worldwide [@Loughlin:2015]. While a handful of volcanoes (e.g.
Etna, Italy; Kīlauea, USA; Merapi, Indonesia) have been extensively studied,
hundreds of volcanic systems around the world remain relatively poorly-understood.
One possible solution to partially relax the serious issue of data scarcity in volcanology,
and volcanic hazard assessment, has been to seek for _analogue volcanoes_ [@Newhall:2002;
@Newhall:2017], which are volcanoes that are similar enough to a given data-scarce volcano,
as to justify the use of data and information from the former to approximate the values of
uncertain variables of interest at the latter (e.g. number of eruptions in specific time
windows, locations of eruptive vents, magnitudes and/or intensities of past eruptions, etc).

# Statement of need

`PyVOLCANS` (Python VOLCano ANalogues Search) is an open-source package to derive data-driven
sets of analogue volcanoes, and help tackle some of the aforementioned issues. The code builds up
from the development of VOLCANS [@Tierz:2019], a first-of-its-kind method to quantify the analogy
(or similarity) between volcanic systems, based on a structured, overarching combination of five
volcanological criteria: tectonic setting, rock geochemistry, volcano morphology, eruption size,
and eruption style.

`PyVOLCANS` offers any of its users a previously unavailable opportunity to easily derive data-driven
sets of _top_ analogue volcanoes (i.e. those with highest analogy) to any volcanic system listed in
the reference database for recent global volcanism (Holocene period, last ~12,000 yr): the
[Volcanoes of the World Database](https://volcano.si.edu/list_volcano_holocene.cfm), hosted by the
Global Volcanism Program (GVP) of the Smithsonian Institution.

To generate these sets of analogue volcanoes, the users of `PyVOLCANS` are given full flexibility to
explore any number of top analogue volcanoes, as well as to customise the importance (i.e. weight) that
is given to each of the five aforementioned volcanological criteria. Additionally, the users can select
a number of _a priori_ analogue volcanoes (i.e. volcanoes deemed as analogues by other means, such as
expert knowledge) and assess their values of analogy with the target volcano (\autoref{fig:figure1}).
The users can also analyse the proportion of volcanoes in the GVP database that have higher values of
analogy with the target volcano, compared to each of the _a priori_ analogue volcanoes provided. All these
features make `PyVOLCANS` a versatile tool for volcano scientists, with applications that can range from
investigating commonalities in unique volcanic systems [@Cashman:2014] to supporting probabilistic volcanic
hazard assessment at local, regional and global scales. The tool could even be used for [teaching and
scientific outreach](https://twitter.com/Xeno_lith/status/1384416032526266369?s=20).

![Values of single-criterion (colours) and total analogy (bar heights) between an example target volcano, Fuego (Guatemala)\*, and five _a priori_ analogues [please see @Tierz:2019, for more details]. ATs: Analogy in Tectonic setting; AG: Analogy in rock Geochemistry; AM: Analogy in volcano Morphology; ASz: Analogy in eruption Size; ASt: Analogy in eruption Style. \*Number between brackets denotes the unique volcano identifier used by the GVP database.\label{fig:figure1}](figure.png)

Some of the potentialities of `PyVOLCANS` have already been shown in recent applications: e.g. exploring
the volcanological factors that influence the development of particular volcano morphologies [@White:2020];
constraining potential hazardous phenomena and hazard scenarios at a given target volcano, based on its
analogue volcanoes [@Simmons:2020]; quantifying probability distributions of eruption sizes and probabilities
of occurrence of diverse hazardous phenomena [@Tierz:2020]; or even exploring volcano analogies at regional
scales, by generating sets of analogue volcanoes for tens of volcanic systems [@Crummy:2021]. The last two
example applications have played a key role in developing quantitative hazard analyses for Ethiopian volcanoes,
within the [RiftVolc project](https://www.bgs.ac.uk/geology-projects/volcanoes/riftvolc/). We hope that future
applications of `PyVOLCANS` will continue to grow in number and diversity of their scientific purposes.

# Acknowledgements

The research leading to these results has been mainly supported by the Innovation Flexible Fund of the
British Geological Survey, NC grant NEE7147S. We would like to warmly thank Eliza Calder for all her work
during the development of the VOLCANS method, and Sarah Ogburn for being one of the first people who
_convinced_ us that we should develop an open-access application of VOLCANS, sooner rather than later.
Declan Valters is thanked for support with Python programming. Moreover, we would like to sincerely thank
a number of colleagues with whom we shared very insightful conversations about analogue volcanoes and/or
PyVOLCANS: Chris Newhall, Isla Simmons, Adriano Pimentel, Julia Crummy, Charlotte Vye-Brown, Lara Smale,
Karen Fontijn, Ben Clarke, Susanna Jenkins, Elly Tennant, Pierre Barbillon, Elaine Spiller, Philippa White,
Teresa Ubide, Sebastián García, Victoria Olivera, Jeremy Pesicek, Vanesa Burgos Delgado, Eitnat Lev,
Jonty Rougier, Willy Aspinall, Paolo Papale, Monse Cascante and Thomas Giachetti.

# References
