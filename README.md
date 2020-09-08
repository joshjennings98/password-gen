# Diceware Password Generator
- [Diceware Password Generator](#diceware-password-generator)
  - [About](#about)
  - [Usage](#usage)

## About

Generate a password according to rules set out by the [diceware website](https://theworld.com/~reinhold/diceware.html).

The password uses `os.urandom()` to generate the random numbers so it [should be cryptographically secure](https://realpython.com/lessons/cryptographically-secure-random-data-python/).

## Usage

You can provide a combination of arguments: a dictionary file, the number of words, the number of characters to change. When specifying a number of characters to change, we only change one per word at maximum to make sure the passwords are easier to remember.

**Examples:**

* `python password-gen <dictionary file> <number of words> <number of characters to change>`

* `python password-gen <dictionary file> <number of words>`

* `python password-gen <number of words>`

* `python password-gen <dictionary file>`
  
* `python password-gen <number of words> <number of characters to change>`

* `python password-gen <dictionary file>`
  