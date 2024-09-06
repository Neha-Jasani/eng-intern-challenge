
import sys

# Define the Braille dictionary for letters, numbers, and special characters
braille_dict = {
    'a': 'O.....', 'b': 'O.O...', 'c': 'OO....', 'd': 'OO.O..', 'e': 'O..O..', 'f': 'OOO...', 'g': 'OOOO..', 'h': 'O.OO..',
    'i': '.OO...', 'j': '.OOO..', 'k': 'O...O.', 'l': 'O.O.O.', 'm': 'OO..O.', 'n': 'OO.OO.', 'o': 'O..OO.', 'p': 'OOO.O.',
    'q': 'OOOOO.', 'r': 'O.OOO.', 's': '.OO.O.', 't': '.OOOO.', 'u': 'O...OO', 'v': 'O.O.OO', 'w': '.OOO.O', 'x': 'OO..OO',
    'y': 'OO.OOO', 'z': 'O..OOO', ' ': '......',
    '1': 'O.....', '2': 'O.O...', '3': 'OO....', '4': 'OO.O..', '5': 'O..O..', '6': 'OOO...', '7': 'OOOO..', '8': 'O.OO..',
    '9': '.OO...', '0': '.OOO..',
    'capital': '.....O', 'number': '.O.OOO', 'space': '......'
}

# Reverse dictionary to map Braille to characters
reverse_braille_dict = {v: k for k, v in braille_dict.items()}

def is_braille(input_string):
    """Check if the input is Braille (i.e., only contains 'O' and '.' characters)."""
    return all(c in 'O.' for c in input_string)

def braille_to_english(braille):
    """Translate Braille string to English."""
    result = []
    i = 0
    capitalize = False
    number_mode = False
    
    while i < len(braille):
        symbol = braille[i:i + 6]
        
        # Check if symbol indicates capital letter
        if symbol == braille_dict['capital']:
            capitalize = True
            i += 6
            continue
        
        # Check if symbol indicates number mode
        if symbol == braille_dict['number']:
            number_mode = True
            i += 6
            continue
        
        # Handle number pattern
        if number_mode:
            if symbol in reverse_braille_dict:
                char = reverse_braille_dict[symbol]
                if char.isdigit():
                    result.append(char)
                else:
                    result.append('?')  # Unknown pattern
                number_mode = False  # End number mode after processing digit
            else:
                result.append('?')  # Unknown pattern
            i += 6
        else:
            # Handle letter pattern
            if symbol == braille_dict['number']:  # Number pattern
                number_mode = True
                i += 6
                continue

            if symbol == braille_dict['space']:  # Handle space
                result.append(' ')
            else:
                char = reverse_braille_dict.get(symbol, '')
                if char:
                    if capitalize:
                        char = char.upper()
                        capitalize = False
                    result.append(char)
                else:
                    result.append('?')  # Unknown pattern
            i += 6
    
    return ''.join(result).strip()

def english_to_braille(english):
    """Translate English string to Braille."""
    result = []
    words = english.split(' ')  # Split input into words by spaces
    for i, word in enumerate(words):
        j = 0
        while j < len(word):
            if word[j].isdigit():
                # Detect the entire sequence of digits
                num_start = j
                while j < len(word) and word[j].isdigit():
                    j += 1
                num_str = word[num_start:j]
                result.append(braille_dict['number'])
                result.append(''.join(braille_dict[digit] for digit in num_str))
            elif word[j].isalpha():
                if word[j].isupper():
                    result.append(braille_dict['capital'])
                    result.append(braille_dict[word[j].lower()])
                else:
                    result.append(braille_dict[word[j]])
                j += 1
            elif word[j] == ' ':
                # Spaces are handled in the split step
                j += 1
            else:
                j += 1  # Skip any other characters (e.g., punctuation)
        
        # Add Braille space after each word except the last one
        if i < len(words) - 1:
            result.append(braille_dict['space'])
    
    return ''.join(result).strip()

def main():
    """Main function to determine if input is Braille or English and translate accordingly."""
    if len(sys.argv) < 2:
        print("Usage: python3 translator.py <string>")
        return
    
    # Join all command-line arguments into a single string, preserving spaces
    input_text = ' '.join(sys.argv[1:])
    
    if is_braille(input_text):
        print(braille_to_english(input_text))
    else:
        braille_output = english_to_braille(input_text)
        print(braille_output)

if __name__ == "__main__":
    main()
