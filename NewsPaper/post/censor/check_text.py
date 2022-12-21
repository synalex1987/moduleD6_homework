_forbidden_words = ['рамках', 'элемент', 'шанс']


def return_clear_text(text: str, replace_symbol='*', forbidden_words=_forbidden_words):
    for w in forbidden_words:
        text = text.replace(w, replace_symbol * len(w))
    return text