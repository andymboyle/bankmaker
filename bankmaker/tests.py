from django.test import TestCase
from bankmaker.models import Card

CARD_1_ATTRS = {
    "name": "Andy",
    "card_number": "123123123",
    "luhn_check": False,
    "limit": "1200",
    "balance": "0"
}

CARD_2_ATTRS = {
    "name": "Tom",
    "card_number": "49927398716",
    "luhn_check": True,
    "limit": "500",
    "balance": "0"
}


class TestCard(TestCase):
    def test_create_card(self):
        card = Card.objects.create(**CARD_1_ATTRS)
        card.save()

        self.assertEqual(card.name, CARD_1_ATTRS["name"])
        self.assertEqual(card.card_number, CARD_1_ATTRS["card_number"])
        self.assertEqual(card.luhn_check, CARD_1_ATTRS["luhn_check"])
        self.assertEqual(card.limit, CARD_1_ATTRS["limit"])
        self.assertEqual(card.balance, CARD_1_ATTRS["balance"])

        card_2 = Card.objects.create(**CARD_2_ATTRS)
        card.save()
        self.assertEqual(card_2.name, CARD_2_ATTRS["name"])
        self.assertEqual(card_2.card_number, CARD_2_ATTRS["card_number"])
        self.assertEqual(card_2.luhn_check, CARD_2_ATTRS["luhn_check"])
        self.assertEqual(card_2.limit, CARD_2_ATTRS["limit"])
        self.assertEqual(card_2.balance, CARD_2_ATTRS["balance"])

    def charge_card(self):
        card = Card.objects.create(**CARD_1_ATTRS)
        card.save()
        card.balance = card.balance + 15
        card.save()
        self.assertEqual(card.balance, 15)

    def credit_card(self):
        card = Card.objects.create(**CARD_2_ATTRS)
        card.save()
        card.balance = card.balance - 30
        card.save()
        self.assertEqual(card.balance, -30)
