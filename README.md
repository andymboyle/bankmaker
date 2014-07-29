# Bankmaker

I wanted to learn more about taking user inputs on the command line and doing things with them, so I made a silly little app that keeps track of credit card transactions. It's not perfect, but it's kind of nifty.

## Pip Install

Be sure to create a virtualenv and then pip install -r requirements.txt

Then you'll need to sync your models with the database:

`./manage.py syncdb`

Then you'll need to, in the root directory, run this to get to the actual tool:

`./manage.py creditcardify`

In there, you should be able to enter your commands -- Add, Charge, Credit, Delete, Info, All. If you'd like to clear all of the current cards in the system, you can run:

`./manage.py --clear`

## Other functions

Also, I added a few functions that I thought were kind of necessary, as mentioned above:

`Info Name`

You type in Info and then give a specific name. It'll return you all the information about this card. If that card doesn't exist, it returns an error.

`Delete Name`

You type in Delete and then a specific name of a card. It'll delete this card. If that card doesn't exist, it returns that it doesn't exist.

`All`

Type in All and it will display all the cards. If there are no cards, it will display that.

## Testing

If you'd like to run the tests, which just creates, adds to the balance and credits to the balance, here's the command:

`./manage.py test bankmaker`

## Anything else?

At its most basic level, it just takes a simple input, checks what you wrote follows certain protocols given, and then goes to the function that does whatever is specified (Add, Credit, Charge, etc.). As you'll see, I've tried to include some test checks in here, but it's not the best and they probably could be better.

After each entry, it asks if you're done, and gives you a y/n way to go. I prefer users knowing what's going to happen next and trying to give excess information, so it gives you an option to leave, other than forcing someone to Ctrl + C their way out.
