import operator
import numpy as np
from typing import List


class Node(object):
    def __init__(self, name, matrix):
        self.name = name
        self.matrix = matrix
        self.child: List[Node] = []
        self.parent = None
        self.primerjava = None
        self.porocilo = None

    def sestavi_primerjave(self, alternative):
        if len(self.child) > 0:
            self.primerjava = Primerjaj(self.name, np.array(self.matrix), [child.name for child in self.child])
            for child in self.child:
                child.sestavi_primerjave(alternative)
        else:
            self.primerjava = Primerjaj(self.name, self.matrix, alternative)

    def sestavi_porocila(self):
        if len(self.child) > 0:
            for child in self.child:
                if len(child.child) > 0:
                    child.sestavi_porocila()
            data = []
            for child in self.child:
                if len(child.child) > 0:
                    data.append(child.porocilo)
                else:
                    data.append(child.primerjava)
            self.porocilo = Sestavi(self.name, self.primerjava, data)


class Primerjaj(object):
    """
    Ta razred izracuna prioritetni vektor in konsistentno razmerje
    positivne inverzne matrike.

    Argument "utezi" vsebuje prioritetni vektor
    kot slovar katerih kljuci so kriteriji in vrednosti so utezi kriteriji.

    Argument "konsistentno_razmerje" vsebuje izracunan consistentni faktor
    vhodne matrike kot decimalka.

    :param ime: beseda, ime primerjalnega objekta
    :param matrika: numpy matrika iz katere se izracuna prioritetni vektor
    :param kriteriji: spisek besed, kritefij matrike na enak nacin kot je pozicija vrednosti v matriki
    :param natancnost: stevilka, natancnost izracunanih prioritetnega vektorja
    :param primerjalni_tip: beseda, primerjalni tip vrednosti v matrik kvalitativni ali kvantitivni tip ('quant', 'qual')
    :param st_iteracij: stevilka, stevilo iteracij preden se izracuna bazni vektor
    :param nakljucni_index: beseda, 'dd', 'saaty'
    """

    def __init__(self, ime=None, matrika=None, kriteriji=None,
                 st_iteracij=100):
        self.ime = ime
        self.matrika = matrika
        self.kriterij = kriteriji
        self.dimenzija_matrike = matrika.shape[0]
        self.natancnost = 4
        self.st_iteracij = st_iteracij
        self.prioritetni_vektor = None
        self.konsistencni_faktor = None
        self.utezi = None

        self.izracunaj()

    def izracunaj(self):
        # Ce je primerjalni tip quantitativen se vnos normalizira
        # V nasprotnem primeru se izracuna prioritetni vektor in konsistentno razmerje
        self.izracunaj_prioritetni_vektor(self.matrika, self.st_iteracij)
        # Ustvari slovar utezi
        slovar_utezi = dict(zip(self.kriterij, self.prioritetni_vektor))
        self.utezi = {self.ime: slovar_utezi}

    def izracunaj_prioritetni_vektor(self, matrika, st_iteracij, primerjalni_bazni_vektor=None):
        kvadratna_matrika = np.linalg.matrix_power(matrika, 2)
        vsota_vrstic = np.sum(kvadratna_matrika, 1)
        skupna_vsota_vrstic = np.sum(vsota_vrstic)
        glavni_bazni_vektor = np.divide(vsota_vrstic, skupna_vsota_vrstic).round(self.natancnost)
        # Ustvari prazno matriko kot primerjalni bazni vektor ce je to prva iteracija
        if primerjalni_bazni_vektor is None:
            primerjalni_bazni_vektor = np.zeros(self.dimenzija_matrike)
        # Izracunal razliko med princ_eigenvector in primerjalnim_baznim_vektorjem
        ostanek = np.subtract(glavni_bazni_vektor, primerjalni_bazni_vektor).round(self.natancnost)
        # Ce je razlika med dvema baznima vektorjema 0
        # nastavi trenutni pric_eigenvector kot prioritetni vektor
        if not np.any(ostanek):
            self.prioritetni_vektor = glavni_bazni_vektor
            return
        # Rekurzivno zaganjaj funkcijo dokler ni nobene razlike med glavnim in primerjalnim baznim vektorjem ali pa ce zmanjka stevilo iteracij
        st_iteracij -= 1
        if st_iteracij > 0:
            return self.izracunaj_prioritetni_vektor(kvadratna_matrika, st_iteracij, glavni_bazni_vektor)
        else:
            self.prioritetni_vektor = glavni_bazni_vektor
            return

    def report(self):
        print('Ime:', self.ime)
        print('Utezi:')
        sortirane_utezi = sorted(self.utezi[self.ime].items(), key=operator.itemgetter(1), reverse=True)
        for k, v in sortirane_utezi:
            print('\t{}: {}'.format(k, round(v, self.natancnost)))
        print()


class Sestavi(object):

    def __init__(self, ime=None, stars=None, otrok=None):
        self.ime = ime
        self.stars = stars
        self.otrok = otrok
        self.utezi = dict()
        self.natancnost = 4

        self.izracunaj_skupno_prioriteto()
        self.normaliziraj_skupno_prioriteto()

    def izracunaj_skupno_prioriteto(self):
        for pk, pv in self.stars.utezi[self.stars.ime].items():
            for otrok in self.otrok:

                if pk in otrok.utezi:
                    for ck, cv in otrok.utezi[pk].items():
                        try:
                            self.utezi[ck] += np.multiply(pv, cv)
                        except KeyError:
                            self.utezi[ck] = np.multiply(pv, cv)
                    break

    def normaliziraj_skupno_prioriteto(self):
        skupna_vsota = sum(self.utezi.values())
        izracunane_utezi = {key: np.divide(value, skupna_vsota) for key, value in self.utezi.items()}
        self.utezi = {self.ime: izracunane_utezi}

    def porocilo(self):
        porocilo = f"{self.ime}:\n"
        print(self.ime + ":")
        sortirane_utezi = sorted(self.utezi[self.stars.ime].items(), key=operator.itemgetter(1), reverse=True)
        for k, v in sortirane_utezi:
            porocilo += f'- {k}: {np.round(v, self.natancnost)}\n'
        return porocilo


if __name__ == "__main__":
    alternatives = ('a1', 'a2')
    goal_arr = np.array([[1, 3, 4, 6],
                         [5, 3, 2, 9],
                         [2,5,3,6],
                         [3,5,7,4]])
    p1_arr = np.array([[1, 1], [1, 1]])
    p2_arr = np.array([[1, 1], [1, 1]])
    p11_arr = np.array([[1, 1], [1, 1]])
    p12_arr = np.array([[1, 1], [1, 1]])

    goal = Primerjaj('goal', goal_arr, ('p1', 'p2'))
    p1 = Primerjaj('p1', p1_arr, ('p11', 'p12'))
    p2 = Primerjaj('p2', p2_arr, alternatives)

    p11 = Primerjaj('p11', p11_arr, alternatives)
    p12 = Primerjaj('p12', p12_arr, alternatives)

    p1_r = Sestavi('p1', p1, (p11, p12))
    goar_r = Sestavi('goal', goal, (p1_r, p2))

    print(goar_r.porocilo())

    p11_node = Node('p11', p11_arr)
    p12_node = Node('p12', p12_arr)
    p1_node = Node('p1', p1_arr)
    p2_node = Node('p2', p2_arr)
    goal_node = Node('goal', goal_arr)

    goal_node.child = [p1_node, p2_node]
    p1_node.child = [p11_node, p12_node]

    goal_node.sestavi_primerjave(alternatives)
    goal_node.sestavi_porocila()
    print(goal_node.porocilo.porocilo())
