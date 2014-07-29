from django.core.management.base import BaseCommand
from optparse import make_option
from bankmaker.models import Card
import re


class Command(BaseCommand):
    """
    Lets you create, modify, delete credit card users
    """
    option_list = BaseCommand.option_list + (
        make_option(
            '-c',
            '--clear',
            action='store_true',
            default=False,
            dest='clear',
            help='Clear all credit cards in the database.'),
    )

    def handle(self, *args, **options):
        if options['clear']:
            print "Clearing all credit cards."
            Card.objects.all().delete()

        self.init_project()

    def init_project(self):
        card_list = self.card_input_to_list(
            raw_input("Please enter something: "))

        if card_list[0] == "Add":
            self.card_add(card_list)

        if card_list[0] == "Charge":
            self.card_charge(card_list)

        if card_list[0] == "Credit":
            self.card_credit(card_list)

        if card_list[0] == "Delete":
            self.card_delete(card_list)

        if card_list[0] == "Info":
            self.card_info(card_list)

        if card_list[0] == "All":
            self.card_display_all()

        if card_list[0] == "Help":
            print "Please see the readme for further instructions."
        # Add another if to catch when not those four maybe?

        # Check and see if the user wants to do more
        another_process = raw_input("Would you like to do more? y/n ")
        if another_process == "y" or another_process == "Y":
            self.init_project()
        else:
            print "Goodbye!"

    def card_luhn(self, card_number):
        # Checks to make sure that the card passes a luhn mod-10 checksum
        sum = 0
        num_digits = len(card_number)
        oddeven = num_digits & 1

        for count in range(0, num_digits):
            digit = int(card_number[count])

            if not ((count & 1) ^ oddeven):
                digit = digit * 2
            if digit > 9:
                digit = digit - 9

            sum = sum + digit

        return ((sum % 10) == 0)

    def card_input_to_list(self, card_input):
        # Turn the input into a list
        card_input.split(" ")
        return re.sub("[^\w]", " ",  card_input).split()

    def remove_dollar(self, amount):
        # Remove the dollar from a string, make it an int
        return int(amount.replace('$', ''))

    def card_add(self, card_list):
        # Create a new card
        name = card_list[1]
        if self.card_luhn(card_list[2]) is True and len(str(card_list[2])) <= 19:
            limit = self.remove_dollar(card_list[3])
            card = Card(
                name=name,
                card_number=card_list[2],
                luhn_check=True,
                limit=limit,
            )
            card.save()
            print "%s: $%s" % (card.name, card.balance)
        else:
            print "%s: error" % name

    def card_charge(self, card_list):
        # Charge a card
        name = card_list[1]
        try:
            card = Card.objects.get(name=name)
            if card.luhn_check is False:
                print "%s: $%s" % (card.name, card.balance)
            else:
                charge = self.remove_dollar(card_list[2])
                if charge + card.balance > card.limit:
                    print "%s: $%s" % (card.name, card.balance)
                else:
                    card.balance = card.balance + charge
                    card.save()
                    print "%s: $%s" % (card.name, card.balance)
        except Card.DoesNotExist:
            print "A card for %s doesn't exist." % name

    def card_credit(self, card_list):
        # Credit a card
        name = card_list[1]
        try:
            card = Card.objects.get(name=name)
            if card.luhn_check is False:
                print "%s: $%s" % (card.name, card.balance)
            else:
                credit = self.remove_dollar(card_list[2])
                card.balance = card.balance - credit
                card.save()
                print "%s: $%s" % (card.name, card.balance)
        except Card.DoesNotExist:
            print "A card for %s doesn't exist." % name

    def card_delete(self, card_list):
        # Delete a card
        name = card_list[1]
        try:
            card = Card.objects.get(name=name)
            keep_going = raw_input(
                "You sure you want to delete this card? y/n ")
            if keep_going == "y" or keep_going == "Y":
                card.delete()
                print "The card for %s has been deleted." % name
            else:
                print "You decided to not delete %s. Cool." % name
        except Card.DoesNotExist:
            print "A card for %s doesn't exist." % name

    def card_info(self, card_list):
        # Get info about a card
        name = card_list[1]
        try:
            card = Card.objects.get(name=name)
            print "Name: %s\nCard: %s\nLuhn: %s\nLimit: %s\nBalance: %s" % (
                card.name,
                card.card_number,
                card.luhn_check,
                card.limit,
                card.balance
            )
        except Card.DoesNotExist:
            print "%s doesn't exist" % name

    def card_display_all(self):
        cards = Card.objects.all().order_by('name')
        if cards.count() > 0:
            for card in cards:
                print "Name: %s\nCard: %s\nLuhn: %s\nLimit: %s\nBalance: %s\n ###" % (
                    card.name,
                    card.card_number,
                    card.luhn_check,
                    card.limit,
                    card.balance
                )
        else:
            print "No cards. Maybe you should add one? Live your life!"
