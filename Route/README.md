# Route

_sun trip organisers:_
  - if there are checkpoints it will be only in China, and only if Chinese authoritories ask that.
  - pour clair et direct seuls les trois jours du prologue en France seront assistés, avec un accueil chaque soir pris en charge, et aussi pour votre arrivée à Canton.


At this time, we aim at holding the official departure in Lyon on June 15 or 16 (this is provisional information).

Then we should spend 3-4 days together on a prologue:
one night near the Bourget Lake (Savoie), near Aix-les-Bains & Chambéry. 
one night in the Bauges mountains (Savoie). 
one night in the Aravis mountains (Haute-Savoie), near Le Grand Bornand. To be confirmed. 
and then, the final base camp in Chamonix. 

The start proper should take place in Chamonix on June 19 or 20

## Route segments
    - Kazachstan : Uralsk - Zahrkent (approx. 3000km)
        - possible route through Kazachstan on what looks like paved roads all the way.
          Bicycling touring seems ok on section between Shymkent and Almaty, relatively "popular"
          No information on the other part...
          *TODO* Check if this is shorter than norther route (Graphhopper).

    - [Kiev-Krakow](https://www.bikemap.net/en/route/3290130-kiev-krakow-927km-1680hm/#/z11/49.9887595,20.1811981/terrain)
    - [Shanghai - Kazachstan](https://www.bikemap.net/en/route/818839-shanghai-to-kazakhstan/#/z6/41.1124688,101.3378906/google_roadmap)

## TO DO:

1. Check the raw_route manually for forbidden border crossings, check on paved roads and check if all roads are doable with a bicycle.

## Optimization

Least relief, most sun, shortest distance, least borders to cross?

After watching Sun Trip 2013 we definitely want to prefer paved roads to unpaved ones.
Especially since dodging stones and potholes is more difficult on a trike.

## Started routing :hear_no_evil:

~~
1. Started to make a track based on the profile of a "racingbike" on [graphhopper](https://www.graphhopper.com/). This profile prefers "roads", which I interpret as paved. It is the only route planner I found which is able to plan such a long distance and it comes pretty close to the straight line in Google Earth.

I converted the track to .kml to view in Google Earth and Google Maps.
~~
![track1](https://raw.githubusercontent.com/augustecolle/Suntrip/master/Route/images/route1.jpg)

Problem: check the route manually for bad things as crossing the border with Belarus, manual rerouting is needed. Also some paved roads are highways, for example:

![pichighway](https://raw.githubusercontent.com/augustecolle/Suntrip/master/Route/images/alsopavedroad.png)


2. :smirk_cat: Made new graphhopper that starts from correct starting location: Chamonix, France

