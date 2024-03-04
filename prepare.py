import os
import re

def remove_non_utf8_chars(file_path):
    with open(file_path, 'rb') as f:
        byte_sequence = f.read()

    try:
        decoded_text = byte_sequence.decode('utf-8')
    except UnicodeDecodeError:
        decoded_text = byte_sequence.decode('latin-1')
    finally:
        # unify newline style
        decoded_text = decoded_text.replace("\r", "\n")

        # collapse multiple whitespace
        decoded_text = re.sub(r'[^\S\n]+', " ", decoded_text)

        # remove whitespace preceding commas
        decoded_text = re.sub(r' +,', ",", decoded_text)

        # replace fancy doublequotes
        decoded_text = decoded_text.replace('""', '"')

        # replace fancy singlequotes
        decoded_text = decoded_text.replace("''", "'")

        # replace fancy ellipses
        decoded_text = decoded_text.replace("\u2026", "...")

        # remove whitespace preceding a comma or bang
        decoded_text = re.sub(r' +([,!])', r'\1', decoded_text)

        # remove leading whitespace
        decoded_text = re.sub(r'^ +([^ ])', r'\1', decoded_text, flags=re.MULTILINE)

        # remove trailing whitespace
        decoded_text = re.sub(r'([^ ]) +$', r'\1', decoded_text, flags=re.MULTILINE)

        # remove initial empty lines
        #decoded_text = re.sub(r'^\n+', '', decoded_text)

        # remove other empty lines
        #decoded_text = re.sub(r'\n+', '\n', decoded_text)

        # replace fully-non-alphanumeric lines with chapter breaks
        #decoded_text = re.sub(r'^[^a-z0-9]+$', '***', decoded_text, flags=re.MULTILINE)

        decoded_text = re.sub(r'\n\n', '\n', decoded_text)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(decoded_text)

directory_path = './txt/pool/'
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        remove_non_utf8_chars(file_path)