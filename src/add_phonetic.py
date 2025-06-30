import eng_to_ipa as ipa
import os

def add_phonetics_to_wordlist(filepath):
    """
    Reads a wordlist file, adds IPA phonetic transcription, and overwrites the file.

    The expected format for each line is:
    word  definition

    The output format will be:
    word  [phonetic]  definition
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return

    lines_to_write = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print("Processing wordlist...")
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t', 1)
            if len(parts) == 2:
                word, definition = parts
                # Check if phonetics are already added
                if '[' not in definition.split('\t')[0] and ']' not in definition.split('\t')[0]:
                    try:
                        phonetic = ipa.convert(word)
                        new_line = f"{word}\t[{phonetic}]\t{definition}"
                        lines_to_write.append(new_line)
                        print(f"  Processed '{word}'")
                    except Exception as e:
                        print(f"Could not process '{word}': {e}")
                        lines_to_write.append(line) # keep original if error
                else:
                    lines_to_write.append(line) # already has phonetics
            else:
                # Keep lines that don't fit the format as they are
                lines_to_write.append(line)
        
        # Write back to the file
        with open(filepath, 'w', encoding='utf-8') as f:
            for line in lines_to_write:
                f.write(line + '\n')
        
        print(f"\nSuccessfully processed {len(lines_to_write)} lines.")
        print(f"The file '{filepath}' has been updated with phonetic notations.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    add_phonetics_to_wordlist('wordlist.txt') 