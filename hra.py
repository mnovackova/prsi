# cd /mnt/data/Majulka/ploglamovani/prsi/


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
        self.ber_kartu = False
        self.kolikrat_beru_kartu = 1

    def zahaj_hru(self):
        print("\nKaretní hra Prší. \nDobíráš 2 karty na 7, pokud žádnou nemáš, a 4 karty na pikového krále, pokud nemáš pikového kluka. \nPrvní karta na odkládacím balíčku se nepočítá.\n")

        #vytvoreni balicku
        druhy_karet = [str(x) for x in list(range(7,11))] + ["J", "Q", "K", "A"]
        for symbol in ["♠", "♥", "♦", "♣"]:
            for a in druhy_karet:
                self.balicek.append(a+symbol)

        random.shuffle(self.balicek)

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
        if self.ber_kartu:
            self.ktera_karta(hrac)
        else:
            if self.vybrana_karta[0] == "Q":
                self.hozeni_karty_na_balicek(hrac)
                self.dama()
                self.ma_brat_dalsi_hrac_kartu()
            else:
                self.vyhodnoceni_hrane_karty(hrac)
                self.ma_brat_dalsi_hrac_kartu()

    def ktera_karta(self, hrac):
        if self.odkladaci_balicek[-1][0] == "7":
            self.brani_karet_na_sedmicku(hrac)
        elif self.odkladaci_balicek[-1] == "K♠":
             self.brani_karet_na_pikace(hrac)
        elif self.odkladaci_balicek[-1][0] == "A":
            self.stoji_na_eso(hrac)
        else:
            self.vyhodnoceni_hrane_karty(hrac)

    def stoji_na_eso(self, hrac):
        if self.vybrana_karta[0] != "A":
            print("Stojíš jedno kolo.")
            self.ber_kartu = False
        else:
            self.hozeni_karty_na_balicek(hrac)

    def brani_karet_na_sedmicku(self, hrac):
        if self.vybrana_karta[0] != "7":
            print("Na 7 musíš hrát 7! Vezmi si {} karty!".format(self.kolikrat_beru_kartu*2))
            for a in range(self.kolikrat_beru_kartu*2):
                self.pridej_kartu(hrac)
            self.kolikrat_beru_kartu = 1
            self.ber_kartu = False
            return
        elif self.vybrana_karta[0] == "7":
            self.kolikrat_beru_kartu += 1
            self.hozeni_karty_na_balicek(hrac)

    def brani_karet_na_pikace(self, hrac):
        if self.vybrana_karta != "J♠":
            print("Na pikového krále musíš hrát kluka! Vezmi si 4 karty!")
            for a in range(4):
                self.pridej_kartu(hrac)
            self.ber_kartu = False
            return
        else:
            self.hozeni_karty_na_balicek(hrac)


    def vyhodnoceni_hrane_karty(self, hrac):
        if self.vybrana_karta[0] == self.odkladaci_balicek[-1][0] or self.vybrana_karta[-1] == self.odkladaci_balicek[-1][-1]:
            self.hozeni_karty_na_balicek(hrac)
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
            print("Konec hry. Vyhrál hráč č.", hrac.cislo_hrace)
            sys.exit()

    def kontrola_balicku(self):
        if self.balicek == []:
            posledni_karta = self.odkladaci_balicek.pop()
            self.balicek =  list(self.odkladaci_balicek)
            for karta in self.balicek:
                #odstrani vyzskyt srdicek a pod
                if len(karta) == 1:
                    self.balicek.remove(karta)
            random.shuffle(self.balicek)
            self.odkladaci_balicek = [posledni_karta]

    def hozeni_karty_na_balicek(self, hrac):
        self.kontrola_stavu_balicku_hrace = hrac.odeber_kartu_z_balicku()
        self.odkladaci_balicek.append(self.vybrana_karta)

    def ma_brat_dalsi_hrac_kartu(self):
        if self.vybrana_karta[0] in ("7", "A") or self.vybrana_karta == "K♠":
            self.ber_kartu = True
        else:
            self.ber_kartu = False

    def dama(self):
        if self.vybrana_karta[0] == "Q":
            barva = int(input("Na kterou barvu měníš? (1=♠, 2=♥, 3=♦, 4=♣) "))
            if barva == 1:
                vyber = "♠"
            elif barva == 2:
                vyber = "♥"
            elif barva == 3:
                vyber = "♦"
            elif barva == 4:
                vyber = "♣"
            self.odkladaci_balicek.append(vyber)

'''
kterou chces hrat

zhodnot
    pokracuj
    vem si xx
    lizni

vyhodnoceni

'''


if __name__ == "__main__":
    hra = Hra()
    hra.zahaj_hru()
