def _get_part_text(text: str, start: int, page_size: int) -> str and int:
    text = text[start:]
    punctuation_marks = ',.!:;?'
    new_text = ''
    line = ''
    for i in range(page_size):
        if i == len(text): break

        line += text[i]
        if (text[i] in punctuation_marks) and (i+1 == len(text) or text[i+1] not in punctuation_marks):
            new_text += line
            line = ''

    return new_text, len(new_text)


def prepare_book(path: str, page_size: int = 1050) -> dict[int: str]:
    book = {}
    start = 0
    count = 1
    with open(file=path, mode='r', encoding='utf-8-sig') as file:
        content = ''
        for line in file:
            content += line

            if len(content) >= page_size * count:
                text, l = _get_part_text(content, start, page_size)
                start += l
                book[count] = text.lstrip()
                count += 1

        text, l = _get_part_text(content, start, len(content))
        book[count] = text.lstrip()
        return book