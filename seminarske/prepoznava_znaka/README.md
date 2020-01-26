# Instalacija

    pip install -r requirements.txt
    
# Example

* [Data set](https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/published-archive.html)
* [Template matching](https://docs.opencv.org/2.4/doc/tutorials/imgproc/histograms/template_matching/template_matching.html)

# Navodila
Pripravite testno aplikacijo - demonstracijo, kjer lahko podate neko sliko (vašo, s spleta, ...) in aplikacija v njen poišče vse znake. 
Hkrati nam pokaže, katere šablone so se ujemale s katerim znakom.

Opravite eksperiment, s katerim zmerite natančnost vašega detektorja. To pomeni, da obdelate vse testne slike v zbirki, ki jo uporabljate (koliko časa potrebujete za eno sliko?). 
Vaše detekcije nato primerjate z dejanskimi lokacijami znakov v teh slikah. 
Implementiran algoritem za ovrednotenje detekcij najdete na strani uporabljene zbirke in lahko uporabite tistega. 
Lahko uporabite tudi lasten pristop, ki bo morda manj rigorozen.

Pripravite nekaj lastnih slik (dovolj slik, da se bo na njih skupaj nahajalo vsaj 20 znakov) in opravite detekcije na teh slikah.
 S tem ovrednotite natančnost vaše metode.


Vse skupaj povzemite v poročilu (lahko dodelate vaše trenutno poročilo). 
Dodajte 2 tabeli, ki bosta prikazovali rezulate obeh eksperimentov ter nekaj slik pripravljene aplikacije/demonstratorja,
 kjer se vidi kateri znak je bil detektiran in katera je bila ujemajoča šablona.