"""
Unicode Monospace Font Converter

Converts regular text to monospace unicode characters to preserve the signature
style of the profile (𝙷𝚘𝚕𝚊 𝚂𝚘𝚢 𝙰𝚗𝚐𝚎𝚕).
"""

# Monospace unicode character mapping
MONOSPACE_MAP = {
    # Uppercase letters
    'A': '𝙰', 'B': '𝙱', 'C': '𝙲', 'D': '𝙳', 'E': '𝙴', 'F': '𝙵', 'G': '𝙶',
    'H': '𝙷', 'I': '𝙸', 'J': '𝙹', 'K': '𝙺', 'L': '𝙻', 'M': '𝙼', 'N': '𝙽',
    'O': '𝙾', 'P': '𝙿', 'Q': '𝚀', 'R': '𝚁', 'S': '𝚂', 'T': '𝚃', 'U': '𝚄',
    'V': '𝚅', 'W': '𝚆', 'X': '𝚇', 'Y': '𝚈', 'Z': '𝚉',

    # Lowercase letters
    'a': '𝚊', 'b': '𝚋', 'c': '𝚌', 'd': '𝚍', 'e': '𝚎', 'f': '𝚏', 'g': '𝚐',
    'h': '𝚑', 'i': '𝚒', 'j': '𝚓', 'k': '𝚔', 'l': '𝚕', 'm': '𝚖', 'n': '𝚗',
    'o': '𝚘', 'p': '𝚙', 'q': '𝚚', 'r': '𝚛', 's': '𝚜', 't': '𝚝', 'u': '𝚞',
    'v': '𝚟', 'w': '𝚠', 'x': '𝚡', 'y': '𝚢', 'z': '𝚣',

    # Numbers
    '0': '𝟶', '1': '𝟷', '2': '𝟸', '3': '𝟹', '4': '𝟺',
    '5': '𝟻', '6': '𝟼', '7': '𝟽', '8': '𝟾', '9': '𝟿',
}


def to_monospace(text: str, enabled: bool = True) -> str:
    """
    Convert text to monospace unicode characters.

    Args:
        text: The text to convert
        enabled: If False, returns original text without conversion

    Returns:
        The converted monospace text (or original if disabled)

    Examples:
        >>> to_monospace("Hola Soy Angel")
        '𝙷𝚘𝚕𝚊 𝚂𝚘𝚢 𝙰𝚗𝚐𝚎𝚕'
        >>> to_monospace("Tecnologias 2024")
        '𝚃𝚎𝚌𝚗𝚘𝚕𝚘𝚐𝚒𝚊𝚜 𝟸𝟶𝟸𝟺'
    """
    if not enabled:
        return text

    return ''.join(MONOSPACE_MAP.get(char, char) for char in text)


def preserve_emoji_and_convert(text: str, enabled: bool = True) -> str:
    """
    Convert text to monospace while preserving emojis and special characters.

    Args:
        text: The text to convert
        enabled: If False, returns original text without conversion

    Returns:
        The converted text with emojis preserved
    """
    if not enabled:
        return text

    # Emojis and special characters are preserved (not in MONOSPACE_MAP)
    return to_monospace(text, enabled)


if __name__ == "__main__":
    # Test the converter
    test_strings = [
        "Hola! Soy Angel Maldonado",
        "Siempre viendo la vida con la mejor actitud",
        "Tecnologias",
        "Proyectos Destacados",
        "Estadisticas",
    ]

    print("Unicode Monospace Converter Test:\n")
    for test in test_strings:
        converted = to_monospace(test)
        print(f"Original:  {test}")
        print(f"Converted: {converted}")
        print()
