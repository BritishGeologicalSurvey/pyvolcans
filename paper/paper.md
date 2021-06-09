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
  - name: Vyron Christodoulou^[Now at The Data Lab, The Bayes Centre, Edinburgh, UK]
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

There are over 1,400 volcanoes on Earth that have either erupted or shown signs of volcanic activity (e.g. fumaroles or hot springs) in, approximately, the last 12,000 years.
Of these, around 40-50 are erupting at any given time [@Siebert:2010; @GVP:2013].
Volcanoes provide a range of economic benefits, such as fertile soils, geothermal energy or valuable mineralizations and attract fascination and create a sense of belonging among visitors and local populations.
However, volcanic systems can also generate hazardous phenomena, threatening local inhabitants, tourists and infrastructure at distances of up to tens or hundreds of kilometres.

In order to understand and quantify volcanic hazard, volcano scientists are faced with many questions.
How often do eruptions occur?
How big are they?
What style of eruption is possible (e.g. producing mainly pyroclastic flows and/or volcanic ash clouds)?
From where on the volcano is eruptive activity sourced?
What areas around the volcanic system may be impacted?
Are there any warning signals?

Quantitative data to address these questions are scarce [@Loughlin:2015].
While a handful of volcanoes (e.g. Etna, Italy; Kīlauea, USA; Merapi, Indonesia) have been extensively studied, hundreds of volcanic systems around the world remain poorly-understood.
One possible mitigation to the issue of data scarcity in volcanology and volcanic hazard assessment is the use of _analogue volcanoes_ [@Newhall:2002; @Newhall:2017].
These are volcanoes with similar characteristics to a data-scarce volcano of interest.
Data and insights from the well-studied volcano can be used to provide estimates for important variables, such as the number of eruptions during specific time windows or the size of those eruptions.


# Statement of need

`PyVOLCANS` (Python VOLCano ANalogues Search) is an open-source tool that addresses the need for an objective, data-driven method for selection of analogue volcanoes.
It is based on the results of VOLCANS [@Tierz:2019], a first-of-its-kind method to quantify the analogy (or similarity) between volcanic systems, based on a structured combination of five volcanological criteria: tectonic setting, rock geochemistry, volcano morphology, eruption size, and eruption style.
`PyVOLCANS` provides a command-line interface to make the results from the VOLCANS study easily accessible to a wide audience.
`PyVOLCANS` is a versatile tool for volcano scientists, with potential applications ranging from investigating commonalities between volcanic systems [@Cashman:2014] to supporting probabilistic volcanic hazard assessment at local, regional and global scales.
It can also be used as a tool for [teaching and scientific outreach](https://twitter.com/Xeno_lith/status/1384416032526266369?s=20).

Users can easily derive data-driven sets of _top_ analogue volcanoes (i.e. those with highest analogy) to any volcanic system listed in the reference database for recent global volcanism: the [Volcanoes of the World Database](https://volcano.si.edu/list_volcano_holocene.cfm), hosted by the Global Volcanism Program of the Smithsonian Institution [@GVP:2013].
The users are given full flexibility to explore any number of top analogue volcanoes, as well as to customise the importance (i.e. weight) that is given to each of the five aforementioned volcanological criteria.
Additionally, users can select a number of _a priori_ analogue volcanoes (i.e. volcanoes deemed as analogues by other means, such as expert knowledge) and assess their values of analogy with the target volcano to see how well they match on different criteria and if other volcanoes could be a better choice (\autoref{fig:figure1}).

![Values of single-criterion (colours) and total analogy (bar heights) between an example target volcano, Fuego (Guatemala)\*, and five _a priori_ analogues [please see @Tierz:2019, for more details].
ATs: Analogy in Tectonic setting; AG: Analogy in rock Geochemistry; AM: Analogy in volcano Morphology; ASz: Analogy in eruption Size; ASt: Analogy in eruption Style.
\*Number between brackets denotes the unique volcano identifier used by the GVP database.
\label{fig:figure1}](figure.png) 

The results from the VOLCANS study have already been used in recent research: e.g. exploring the volcanological factors that influence the development of particular volcano morphologies [@White:2020]; constraining potential hazardous phenomena and hazard scenarios at a given target volcano, based on its analogue volcanoes [@Simmons:2020]; quantifying probability distributions of eruption sizes and probabilities of occurrence of diverse hazardous phenomena [@Tierz:2020]; or even exploring volcano analogies at regional scales, by generating sets of analogue volcanoes for tens of volcanic systems [@Crummy:2021].
The last two example applications have played a key role in developing quantitative hazard analyses for Ethiopian volcanoes, within the [RiftVolc project](https://www.bgs.ac.uk/geology-projects/volcanoes/riftvolc/).

We hope that the release of `PyVOLCANS` will encourage studies based on data-driven selection of analogue volcanoes and that such analyses will continue to grow in number and diversity of their scientific purposes.


# Acknowledgements

The research leading to these results has been mainly supported by the Innovation Flexible Fund of the British Geological Survey, NC grant NEE7147S.
We would like to warmly thank Eliza Calder for all her work during the development of the VOLCANS method, and Sarah Ogburn for being one of the first people who _convinced_ us that we should develop an open-access application of VOLCANS, sooner rather than later.
Declan Valters is thanked for support with Python programming.
Moreover, we would like to sincerely thank a number of colleagues with whom we shared very insightful conversations about analogue volcanoes and/or PyVOLCANS: Chris Newhall, Isla Simmons, Adriano Pimentel, Julia Crummy, Gezahegn Yirgu, Charlotte Vye-Brown, Lara Smale, Karen Fontijn, Ben Clarke, Susanna Jenkins, Elly Tennant, Pierre Barbillon, Elaine Spiller, Philippa White, Teresa Ubide, Sebastián García, Victoria Olivera, Jeremy Pesicek, Vanesa Burgos Delgado, Eitnat Lev, Jonty Rougier, Willy Aspinall, Paolo Papale, Monse Cascante and Thomas Giachetti.

# References
