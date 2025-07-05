# -*- coding: utf-8 -*-
import os

# 词性映射表
POS_MAP = {
    'Verb': 'v.',
    'Noun': 'n.',
    'Adjective': 'adj.',
    'Adverb': 'adv.',
    'Pronoun': 'pron.',
    'Pre-noun adjectival': 'pren.',
    'Expression': 'expr.',
    'Conjunction': 'conj.',
    'Suffix': 'suf.',
    'Prefix': 'pref.',
    'Numeric': 'num.',
    'Katakana': 'kat.',
    'Wasei': 'wasei',
    'Temporal noun': 'temp.',
    'Suru verb': 'suru',
    'な-adjective': 'na-adj.',
    'い-adjective': 'i-adj.',
    'Godan verb': 'u.',
    'Ichidan verb': 'ru.',
    'Irregular verb': 'irr.',
    'Transitive verb': 't.',
    'Intransitive verb': 'i.',
}

# 主要词性（只保留一个）
MAIN_POS = [
    'Verb', 'Noun', 'Adjective', 'Adverb', 'Pronoun', 'Pre-noun adjectival',
    'Expression', 'Conjunction', 'Suffix', 'Prefix', 'Numeric', 'Katakana',
    'Wasei', 'Temporal noun', 'Suru verb', 'な-adjective', 'い-adjective'
]

# 修饰性词性（括号包裹，可多个）
MODIFIER_POS = [
    'Godan verb', 'Ichidan verb', 'Irregular verb', 'Transitive verb', 'Intransitive verb',
    'な-adjective', 'い-adjective', 'Katakana', 'Wasei', 'Temporal noun', 'Suru verb'
]

INPUT_PATH = os.path.join(os.path.dirname(__file__), '../../wordlists/japanese/n4.txt')
INPUT_PATH = os.path.normpath(INPUT_PATH)

def simplify_pos(pos_str):
    parts = [p.strip() for p in pos_str.split(',')]
    main = None
    modifiers = []
    for p in parts:
        if p in MAIN_POS and main is None:
            main = POS_MAP[p]
        elif p in MODIFIER_POS:
            modifiers.append(POS_MAP[p])
        elif p in POS_MAP and main is None:
            main = POS_MAP[p]
    if not main:
        main = parts[0] if parts else ''
    if modifiers:
        return f"{main}({ ' '.join(modifiers) })"
    else:
        return main

def process_file():
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    new_lines = []
    for line in lines:
        if not line.strip():
            new_lines.append(line)
            continue
        cols = line.rstrip('\n').split('\t')
        if len(cols) < 4:
            new_lines.append(line)
            continue
        cols[2] = simplify_pos(cols[2])
        new_lines.append('\t'.join(cols) + '\n')
    with open(INPUT_PATH, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == '__main__':
    process_file() 