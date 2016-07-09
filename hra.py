import random
import sys

NECHCI_HRAT_KARTU = "xx"


class Hrac():
    def __init__(self, cislo_hrace, karty_hrace):
        self.karty_hrace = karty_hrace
        self.cislo_hrace = cislo_hrace
        self.vybrana_karta = ""

    def dej_kartu_na_odkladaci_balik(self):
        print("Hraje hrac", self.cislo_hrace)
        print(self.karty_hrace)
        while True:
            try:
                self.vybrana_karta = int(input("Kterou kartu chceš hrát? "))-1
            except ValueError:
                print("Napiš číslo!")
            if self.vybrana_karta == -1: #pridat nulu jako chci si liznout kartu
                return NECHCI_HRAT_KARTU
            elif 0 <= self.vybrana_karta < len(self.karty_hrace): #bere cisla jen v rozsahu
                return self.karty_hrace[self.vybrana_karta]

    def odeber_kartu_z_balicku(self):
        self.karty_hrace.pop(self.vybrana_karta)
        if self.karty_hrace == []:
            return "!"
        else:
            return ""


class Hra():
    def __init__(self):
        self.seznam_hracu = []
        self.balicek = []
        self.odkladaci_balicek = []
        self.vybrana_karta = ""
        self.kontrola_stavu_balicku_hrace = ""
        self.ber_kartu = True
        self.kolikrat_beru_kartu = 1

    def zahaj_hru(self):
        #vytvoreni balicku
        druhy_karet = [str(x) for x in list(range(7,11))] + ["J", "Q", "K", "A"]
        for symbol in ["♠", "♥", "♦", "♣"]:
            for a in druhy_karet:
                self.balicek.append(a+symbol)

        random.shuffle(self.balicek)
        #print(self.balicek)

        #pocet hracu
        karty_hrace = []

        for a in range(int(input("Zadej počet hráčů (2-4):"))):
            karty_hrace = [self.balicek.pop(), self.balicek.pop(), self.balicek.pop(), self.balicek.pop()]
            hrac = Hrac(a+1, karty_hrace)
            self.seznam_hracu.append(hrac)

        self.odkladaci_balicek.append(self.balicek.pop())

        while True:
            for hrac in self.seznam_hracu:
                print("-" * 10)
                print("Karta na odkladacim balicku:", self.odkladaci_balicek[-1])
                self.vybrana_karta = hrac.dej_kartu_na_odkladaci_balik()
                self.kontrola_balicku()
                self.vyhodnoceni_tahu(hrac)
                self.vyhodnoceni_hry(hrac)

    def vyhodnoceni_tahu(self, hrac):
        #poresi brani karet na 7
        #if self.odkladaci_balicek[-1][0] == "7":
        #    self.pridej_kartu()

        if self.vybrana_karta[0] == self.odkladaci_balicek[-1][0] or self.vybrana_karta[-1] == self.odkladaci_balicek[-1][-1]:
            #brani na sedmicku
            if self.odkladaci_balicek[-1][0] == "7":
                if self.vybrana_karta[0] != "7" and self.ber_kartu == True:
                    print("Na 7 musíš hrát 7! Vezmi si {} karty!".format(self.kolikrat_beru_kartu*2))
                    for a in range(self.kolikrat_beru_kartu*2):
                        self.pridej_kartu(hrac)
                    self.kolikrat_beru_kartu = 1
                    self.ber_kartu = False
                    return
                elif self.vybrana_karta[0] == "7":
                    self.kolikrat_beru_kartu += 1
                    self.ber_kartu = True
            #kontrola dam a es a sedmicek a pikacu ve spesl metode
            self.kontrola_stavu_balicku_hrace = hrac.odeber_kartu_z_balicku()
            self.odkladaci_balicek.append(self.vybrana_karta)
        elif self.vybrana_karta == NECHCI_HRAT_KARTU:
            self.pridej_kartu(hrac)
            print("Škoda, že nemáš kartu. Lízni si.")
        else:
            self.pridej_kartu(hrac)
            print("Tuto kartu hrát nemůžeš. Lízni si.")


    def pridej_kartu(self, hrac):
        hrac.karty_hrace.append(self.balicek.pop())

    def vyhodnoceni_hry(self, hrac):
        if self.kontrola_stavu_balicku_hrace == "!":
            self.seznam_hracu.remove(hrac)
        if len(self.seznam_hracu) == 1:
            print("Konec hry")
            sys.exit()

    def kontrola_balicku(self):
        if self.balicek == []:
            posledni_karta = self.odkladaci_balicek.pop()
            self.balicek =  list(self.odkladaci_balicek)
            random.shuffle(self.balicek)
            self.odkladaci_balicek = [posledni_karta]


'''
kterou chces hrat

zhodnot
    pokracuj
    vem si xx
    lizni

vyhodnoceni

'''



hra = Hra()
hra.zahaj_hru()
