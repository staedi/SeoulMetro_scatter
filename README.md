# SeoulMetro_scatter
Visualization of Seoul Metropolitan subway systems passengers 

## Motivation

[Visualizing MBTA Data](http://mbtaviz.github.io/#trains): `D3.js`-based cool-looking and intensive visualization of Greater Boston Area Public Transit
[Visualizing 24 Hours of Subway Activity in NYC](https://willgeary.github.io/data/2016/12/06/subway-activity.html): Animated MTA activity visualization, which can be replicated with `Python` or `R`.

## Initial Objectives

* Subway lines: Main subway lines within Greater Seoul Areas (Line 1 through 9, Bundang/Suwon-Incheon Line, Ui-Sinseol Line)
* Timeline: Hourly, as it can show clearly how passenger loads change according to rush-hour/taffic-light time
* Graphing method: `Scatterplot` on top of `PathLayer` of (Pydeck)[https://deckgl.readthedocs.io)

`PathLayer` [Source: [https://deckgl.readthedocs.io](https://deckgl.readthedocs.io)]
![](https://deckgl.readthedocs.io/en/latest/_images/path_layer.png)

## Modifications

* Timeline: Due to limitations of source data, I was forced to visualize **daily** changes rather than *hourly* ones.
* Graphing method: `PathLayer` didn't work well as I picture, subway lines on a real map looked rough. I changed to plot `Scatterplot` on top of the map.

## Source

* Subway Dataset: [Seoul Metropolitan Government OpenData](http://data.seoul.go.kr)
* Location Data: Online
* Map Data: Mapbox, OpenStreetMap

## Sample Result

![](https://github.com/staedi/SeoulMetro_scatter/raw/master/images/SeoulMetro.png)

## Future developments

* Straighten out Subway Maps using Mixed Integer Programming Optimization methods (phenomenal algorithm of *Nollenburg, M., & Wolff, A.*)
* Replace Pydeck map charts with optimized subway maps (`Networkx`, `ggnetwork` Module or simple charting libraries such as `ggplot2`) 
