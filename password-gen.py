# password-gen.py

from os import urandom, sys
from typing import Dict, List, Tuple
from urllib.request import urlopen 


def randomInt(start : int = 0, end : int = 255, iterations : int = 1000) -> int:
    """
    Generate a random integer using os.urandom().
    For $iterations generate random numbers and pick the final one.
    The random integers (and consequently the final random integer) will be between $start and $end (inclusive).
    """
    if start < 0 or end > 255: # byte must be between 0x00 and 0xFF (255)
        raise Exception("0 <= start, end < 256")

    byte = [] # os.urandom returns a list of bytes even when it is only one element in lize
    for _ in range(iterations):
        byte = urandom(1) # os.urandom() is cryptographically secure

    return int.from_bytes(byte, byteorder='big', signed=False) % (end - start + 1) + start # modulo it to get in correct range and add offset


def rollDice(offset : str = 0) -> int:
    """
    Generate a random integer between 1 and 6 (inclusive).
    """
    return randomInt(0, 5) + offset


def is_integer(n : str) -> bool:
    """
    Return whether a string $n is an integer.
    """
    try:
        float(n) # we can easily convert string to float so do that and check the float instead
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def getCharsToChange(numCharsToChange : int, wordLengths : List[int]) -> Dict[int, Tuple[int, str]]:
    """
    Given a number of characters to change ($numCharsToChange) and a list of word lengths ($wordLengths), 
    return a dictionary of <indexes of words, (index of character, new character (as a string))>.
    """
    extraChars = [ # these are the characters to swap with according to http://world.std.com/~reinhold/diceware.html
        ["~", "!", "#", "$", "%", "^"],
        ["&", "*", "(", ")", "-", "="],
        ["+", "[", "]", "\\", "{", "}"],
        [":", ";", "\"", "'", "<", ">"],
        ["?", "/", "0", "1", "2", "3"],
        ["4", "5", "6", "7", "8", "9"]
    ]
    
    charsToChange = {} # use of dict means that collisions don't matter since they will be overwritten and we can just run the loop until there are no collisions
    while(len(charsToChange) < numCharsToChange):
        wordIdx = randomInt(0, len(wordLengths)-1)
        charIdx = randomInt(0, wordLengths[wordIdx] - 1)
        
        charsToChange[wordIdx] = (charIdx, extraChars[rollDice()][rollDice()])
    
    return charsToChange


def replaceChars(words : List[str], dictionary : Dict[int, Tuple[int, str]]) -> List[str]:
    """
    Given a $dictionary of <word index, (character index, character)> and a list of words ($words), return $words with the characters changed according to $dictionary.
    """
    for wordIdx, (charIdx, char) in dictionary.items():
        word = words[wordIdx]
        word = word[:charIdx] + char + word[charIdx + 1:] # strings are immutable so we need to create a new one
        words[wordIdx] = word

    return words


def generatePassword(dictionary : Dict[str, str], wordNum : int = 5, extra : int = 0) -> str:
    """
    Given a $dictionary of <str, str> return a string of $wordNum elements from that dictionary.
    If $extra is specified, randomly change one of the characters in that many words in the generated to a random character (or number).
    """
    if extra > wordNum: # we only want one character changed per word for simplicity and ease of remembering
        raise ValueError("Insert one symbol per word at maximum.")
    
    words = []
    
    for _ in range(wordNum):
        rolls = "".join([str(rollDice(1)) for i in range(5)]) # rolls must be between 11111 and 66666
        words.append(dictionary[rolls])

    charsToChange = getCharsToChange(extra, [len(w) for w in words])
    words = replaceChars(words, charsToChange)
    
    return " ".join(words) # add spaces between words since it'll increase entropy (marginally)


def getDictionary(filename : str = "") -> Dict[str, str]:
    """
    If given a $filename, parse that file as a dictionary according to diceware wbsite.
    If no filename is provided, then attempt to download the file from the diceware website.
    """
    if filename == "":
        try:
            response = urlopen('http://world.std.com/~reinhold/diceware.wordlist.asc') # the dictionary provided here http://world.std.com/~reinhold/diceware.html
        except:
            raise Exception("Cannot find default diceware list from http://world.std.com/~reinhold/diceware.wordlist.asc, please provide an offline file instead.")
        
        dictionary = dict([line.split('\\t') for line in str(response.read()).split('\\n') if "\\t" in line])
    else:
        try:
            with open(filename, "r") as f:
                data = f.read().splitlines()
                dictionary = dict([line.split('\t') for line in data if "\t" in line])
        except:
            raise Exception("Issue with formatting of provided file. See http://world.std.com/~reinhold/diceware.html for details.")

    if dictionary == {}: # We shouldn't have an empty dictionary
        raise Exception("Dictionary empty, file must be an invalid dictionary.")

    return dictionary


def main(argv : List[str]) -> None:
    """
    Main function. Parse $argv and print a password with the specified parameters.
    """
    if len(argv) == 1: # no args provided
        dictionary = getDictionary()
        password = generatePassword(dictionary)
    elif len(argv) == 2: # dictionary or number of words provided
        try:
            if is_integer(argv[1]):
                dictionary = getDictionary()
                password = generatePassword(dictionary, int(argv[1]))
            else:
                dictionary = getDictionary(argv[1])
                password = generatePassword(dictionary)
        except:
            raise Exception(f"Invalid argument '{argv[1]}'. Argument must be a number of words or a filepath.")
    elif len(argv) == 3: # dictionary and number of words provided, or number of words and number of characters to change provided
        try:
            if is_integer(argv[1]) and is_integer(argv[2]):
                dictionary = getDictionary()
                password = generatePassword(dictionary, int(argv[1]), int(argv[2]))
            else:
                dictionary = getDictionary(argv[1])
                password = generatePassword(dictionary, int(argv[2]))
        except:
            raise Exception(f"Invalid arguments '{argv[1]}', '{argv[2]}'. Arguments must be a filepath and a number of words, or a number of words, and a number of characters to change (max one change per word).")
    elif len(argv) == 4: # dictionary, number of words, and number of characters to change provided
        try:
            dictionary = getDictionary(argv[1])
            password = generatePassword(dictionary, int(argv[2]), int(argv[3]))
        except:
            raise Exception(f"Invalid arguments '{argv[1]}', '{argv[2]}', '{argv[3]}'. Arguments must be a filepath, a number of words, and a number of characters to change (max one change per word).")
    else:
        raise Exception(f"Invalid of arguments. {argv}.")

    print(password)


if __name__ == "__main__":
        
    # To Do: do that thing where you have to move the mouse around when generating the password in order to generate entropy

    main(sys.argv)