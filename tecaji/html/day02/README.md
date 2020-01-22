# Ponovitev prejsnjega dne

* Na hitrico pojdi skozi alineje prejsnjega dne
* Pomankljivosti surove html strani

# Problemi stiliranja z atributi

* Nimamo skupne tocke kjer bi lahko urejali razsprsene stilske atribute velike html datoteke
* Stevilo atributov se eksponentno povecuje
* HTML je bil definiran samo za ustvarjanje osnove (ne pa za stiliranje le teh)
* Nocna mora za programerje velikih spletnih strani

# Motivi CSS-a

* Lociti html stilskih atributov
* Imeti stile zbrane skupaj na eni tocki
* Omogociti reuse stilskih definicij po vecih html datotekah

# Hello world CSS (Cascading Style Sheets)

* (demo) Vstavljanje css v html dokument (dobre/slabe) strani
    * Inline css (why would you do this :( )
    * Internal css (prototyping, html bloating)
    * External css (code hinting, css reuse) => link
* Povej kako browser izbiro prioriteto css usage (css overriding)


# CSS sintaxa

* demonstracija pisanja css sintaxe
    * selector => z selektorjem poiscemo html element katerega zelimo stilirat.
    * {} => dekleracijski blok ki vsebuje eno ali vec stilskih dekleracij locenih z podpicjem.
    * stilska dekleracija => vsebuje css atribut in vrednost loceno z dvopicjem
    * css in html atribut sta razlicna!

# CSS selektorji

* Je jezik s katerim povemo katere elemente zelimo poiskati.
* Share selectors.html datoteko z razdelano strukturo za demo predstavitev.
* Selektorje razdelimo na 5 kategorij
* Enostavni
    * `element` selector
    * `#id` selector
    * `.class` class selector
    * `*` (universal) selector
    * `#id, .class, element` grouping selector
    * Cilj je da jih uporabljamo pametno/zmerno saj se drugace zgubimo v morju id-jev in classov
    * Uporaba div znacke
* Kombinackijski (izbiranje elementov glede na relacijo)
    * `div p` => selekcijoniranje potomstva
    * `div > p` => selekcijoniranje direktnega otroka starsa
    * `div + p` => selekcijoniranje vnuka detka.
    * `div ~ p` => selekcijoniranje bratov in sester elementa
* Psevdo-class
    * Izbiranje v primeru interakcije ali notranje pozicijev elementov
    * POZOR: vrstni red je pomemben
    * sintaxa => `selector:pseudo-class`
        * link => ne-aktivirani linki
        * active => aktivirani linki
        * hover => element pod misko
        * first-child => prvi (najstarejsi) otrok starsa
        * last-child => zadnji (najmlajsi) otrok starsa
        * nth-child(n) => n-ti otrok starsa od zacetka
        * nth-last-child(n) => n-ti otrok od konca
* Pseudo-element selectorji
    * Izbiranje notranjega besedila elementa
    * sintaxa => `selector::pseudo-element`
        * after
        * before
        * first-letter
        * first-line
        * selection
* Attribute selectors
    * selekciranje elementov z definiranim atributom/vrednostjo atributa
    * sintaxa => `selector[atribut]` ali `selector[attr=vrednost]`

# CSS atributi osnovno

* imena atributov
    * zdruzena v logicne enote `stars` ali `stars-otrok`
    * zdruzeni v pozicijske enote -empty-, -top-, -right-, -bottom-, -left-
    * vec nacinsko pisanje vrednosti atributov
        * margin => 20px
        * margin => 20px 20px || 20px 1px 5px 10px
        * margin-top => 10, margin-left => 5px

* definicije vrednosti
    * barve
        * ime: red, blue, lightblue, darkred, itd 
        * hex (16-tinski sistem 0-9 + a-f) : #{6 crk}
        * rgb: rgb(0-255,0-255,0-255)
        * rgba: rgb(0-255,0-255,0-255, 0-255)
        * color selectorji
    * velikost (px, %)

# Najpomembnejsi atributi

* color
* background
    * color
    * image `url("slika.png")`
    * repeat
    * attachment
    * position
    * `background: #ffffff url("img_tree.png") no-repeat right top;`
* width, height, max/min (width, height)
* BOX MODEL
    * border
        * style
        * width
        * color
        * radius
    * margin
        * auto
    * padding (enako kot margin)
* text
    * align
    * indent
    * shadow
* font
    * style
    * weight
    * size (vw => viewport width)
* position
    * static (default)
    * relative
        * top, bottom, right, left
    * fixed
        * top, bottom, right, left
* z-index (0 default)
* float
    * z div + float lahko nadomestimo tabelo iz 1. dneva 
    * right, left
    * problemi v primeru ce je otrok vecji od starsa
        * overflow: auto
* display
    * grid => [Grid layout css](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Grid_Layout)
        * template-areas
        * grid-area
        * gap
        * column-gap
        * row-gap

# CSS triki/knjiznice

* color picker
* googlefonts
* shadow generator
* fontawesome

# Novo pisanje portfolio strani