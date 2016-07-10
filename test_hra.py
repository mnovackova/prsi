import pytest
from hra import Hra, Hrac


def test_vlozeni_esa():
    game = Hra()
    player = Hrac(1, ["A♠", "9♠"])
    game.odkladaci_balicek = ["8♠"]
    game.vybrana_karta = "A♠"
    player.vybrana_karta = 0

    game.vyhodnoceni_tahu(player)
    assert "A♠" in game.odkladaci_balicek
    assert "A♠" not in player.karty_hrace

def test_vlozeni_esa_na_eso():
    game = Hra()
    player = Hrac(1, ["A♠", "9♠"])
    game.odkladaci_balicek = ["A♣"]
    game.vybrana_karta = "A♠"
    player.vybrana_karta = 0

    game.vyhodnoceni_tahu(player)
    assert "A♠" in game.odkladaci_balicek
    assert "A♠" not in player.karty_hrace

def test_vlozeni_neesa_na_eso_a_stat():
    game = Hra()
    player = Hrac(1, ["8♠", "9♠"])
    game.odkladaci_balicek = ["A♠"]
    game.vybrana_karta = "8♠"
    player.vybrana_karta = 0
    game.ber_kartu = True

    game.vyhodnoceni_tahu(player)
    assert "8♠" not in game.odkladaci_balicek
    assert "8♠" in player.karty_hrace
