import operator
import numpy as np
from typing import List

class Node(object):
    def __init__(self, name, matrix):
        self.name = name
        self.matrix = matrix
        self.child:List[Node]  = []
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
                    data.append(self.porocilo)
                else:
                    data.append(self.primerjava)
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
                 natancnost=4, primerjalni_tip='qual', st_iteracij=100):
        self.ime = ime
        self.matrika = matrika
        self.kriterij = kriteriji
        self.dimenzija_matrike = matrika.shape[0]
        self.primerjalni_tip = primerjalni_tip
        self.natancnost = natancnost
        self.st_iteracij = st_iteracij
        self.prioritetni_vektor = None
        self.konsistencni_faktor = None
        self.utezi = None

        self.izracunaj()

    def izracunaj(self):
        # Ce je primerjalni tip quantitativen se vnos normalizira
        if self.primerjalni_tip == 'quant':
            self.normaliziraj()
        # V nasprotnem primeru se izracuna prioritetni vektor in konsistentno razmerje
        else:
            self.izracunaj_prioritetni_vektor(self.matrika, self.st_iteracij)
            self.izracunaj_konsistentni_faktor()
        # Ustvari slovar utezi
        slovar_utezi = dict(zip(self.kriterij, self.prioritetni_vektor))
        self.utezi = {self.ime: slovar_utezi}

    def izracunaj_prioritetni_vektor(self, matrika, st_iteracij, primerjalni_bazni_vektor=None):
        kvadratna_matrika = np.linalg.matrix_power(matrika, 2)
        vsota_vrstic = np.sum(kvadratna_matrika, 1)
        skupna_vsota_vrstic = np.sum(vsota_vrstic)
        glavni_bazni_vektor = np.divide(vsota_vrstic, skupna_vsota_vrstic).round(self.natancnost)
        print(glavni_bazni_vektor)
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

    def izracunaj_konsistentni_faktor(self):
        if self.dimenzija_matrike < 3:
            self.konsistencni_faktor = 0.0
            return

        # Nakljucni index
        ri_dict = {3: 0.52, 4: 0.89, 5: 1.11, 6: 1.25, 7: 1.35, 8: 1.40, 9: 1.45,
                   10: 1.49, 11: 1.52, 12: 1.54, 13: 1.56, 14: 1.58, 15: 1.59}

        try:
            random_index = ri_dict[self.dimenzija_matrike]
        except KeyError:
            import bisect
            s = sorted(ri_dict)
            smaller = s[bisect.bisect_left(s, self.dimenzija_matrike) - 1]
            larger = s[bisect.bisect_right(s, self.dimenzija_matrike)]
            estimate = (ri_dict[larger] - ri_dict[smaller]) / (larger - smaller)
            random_index = estimate * (self.dimenzija_matrike - smaller) + ri_dict[smaller]

        # Najdi Perron-Frobenius eigenvalue matrike
        lambda_max = np.linalg.eigvals(self.matrika).max()
        konsistencni_index = (lambda_max - self.dimenzija_matrike) / (self.dimenzija_matrike - 1)
        # Izracunaj konsistecni faktor
        self.konsistencni_faktor = np.real(konsistencni_index / random_index).round(self.natancnost)

    def normaliziraj(self):
        """
        Izracunaj prioritetni vektor matrike z normalizacijo in nato nastavi konsistencni faktor na 0
        """
        total_sum = float(np.sum(self.matrika))
        self.prioritetni_vektor = np.divide(self.matrika, total_sum).round(self.natancnost).reshape(1, len(self.matrika))[0]
        self.konsistencni_faktor = 0.0

    def report(self):
        print('Ime:', self.ime)
        print('Konsistencni faktor:', self.konsistencni_faktor)
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
        self.natancnost = None

        self.izracunaj_natancnost()
        self.izracunaj_skupno_prioriteto()
        self.normaliziraj_skupno_prioriteto()

    def izracunaj_natancnost(self):
        natancnost = np.min([child.natancnost for child in self.otrok])
        if natancnost < self.stars.natancnost:
            self.natancnost = natancnost
        else:
            self.natancnost = self.stars.natancnost

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
    experience = np.array([[1, .25, 4], [4, 1, 9], [.25, 1/9., 1]])
    education = np.array([[1, 3, .2], [1/3., 1, 1/7.], [5, 7, 1]])
    charisma = np.array([[1, 5, 9], [.2, 1, 4], [1/9., .25, 1]])
    age = np.array([[1, 1/3., 5], [3, 1, 9], [.2, 1/9., 1]])
    criteria = np.array([[1, 4, 3, 7], [.25, 1, 1/3., 3], [1/3., 3, 1, 5], [1/7., 1/3., .2, 1]])
    exp1= np.array([[1, .25, 4], [4, 1, 9], [.25, 1/9., 1]])
    exp2 = np.array([[1, .25, 4], [4, 1, 9], [.25, 1/9., 1]])

    alt2 = []
    alt1 = ['Tom', 'Dick', 'Harry']

    cri = Primerjaj('goal', criteria, ('exp', 'age'))
    exp = Primerjaj('exp', experience, ('edu', 'sha'))
    edu = Primerjaj('edu', education, alt1)
    cha = Primerjaj('cha', charisma, alt1)
    age = Primerjaj('age', age, alt1)

    exp = Sestavi('exp', exp, ())

    exp = Sestavi('exp', exp, [exp1, exp2])
    Sestavi('goal', cri, [exp, edu, cha, age]).report()
'''
<g> ========================
		a1	a2	a3
p1:		5,	7,	8,
p2:		5,	7,	8,
p3:		5,	7,	8,

<p1> ========================
		a1	a2	a3
p11:		5,	7,	8,
p22:		5,	7,	8,
p33:		5,	7,	8,

<g> ========================
		p1	p2	p3
Values:		5,	7,	8,

<p1> ========================
		p11	p22	p33
Values:		5,	7,	8,

'''