'''
Return if kt is a valid kennitala.

Notast var við eftirfarandi heimild:
https://is.wikipedia.org/wiki/Kennitala
'''
def validate_kennitala(kt):
    VALIDATON_CONSTANTS = [3, 2, 7, 6, 5, 4, 3, 2, 1]
    try:
        digits = [int(char) for char in kt]
    except ValueError:
        # Kennitala contains non-integer character
        return False

    weighted_sum = sum([k * d for k, d in zip(VALIDATON_CONSTANTS, digits)])
    return weighted_sum % 11 == 0
