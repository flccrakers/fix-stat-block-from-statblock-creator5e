import argparse
import re
import sys

import pyperclip

# Définir le parser en global
parser = argparse.ArgumentParser(description="Fix the statblock to be compatible to homebrewery.")
parser.add_argument('-file', type=str, help="The file to fix.")
args = parser.parse_args()
print(args.file)


def remove_greaters(line: str) -> str:
    line = line.replace("> - ", "")
    line = line.replace("> ", "")
    line = line.replace(">\n", ":\n")
    line = line.replace(">", "")
    return line


def fix_carac(line: str) -> str:
    line = line.replace("**Armor Class**", "**Armor Class** ::")
    line = line.replace("**Hit Points**", "**Hit Points** ::")
    line = line.replace("**Speed**", "**Speed** ::")
    line = line.replace("**Damage Immunities**", "**Damage Immunities** ::")
    line = line.replace("**Damage Resistances**", "**Damage Resistances** ::")
    line = line.replace("**Damage Vulnerabilities**", "**Damage Vulnerabilities** ::")
    line = line.replace("**Condition Immunities**", "**Condition Immunities** ::")
    line = line.replace("**Senses**", "**Senses** ::")
    line = line.replace("**Languages**", "**Languages** ::")
    line = line.replace("**Challenge**", "**Challenge** ::")
    return line


# Function to convert feet to meters
def convert_ft_to_m(feet):
    meters = feet * 0.3048
    return round(meters, 2)  # Round to 2 decimal places


# Function to replace 'ft.' with 'm.' and convert the number
def convert_ft_to_m_in_text(text):
    # Regex pattern to find occurrences of numbers followed by 'ft.'
    pattern = r'(\d+)\s*ft\.'  # Capturing the number before 'ft.'

    # Function to replace the match with the converted value in meters
    def replacer(match):
        feet = int(match.group(1))  # Get the number in feet from the match
        meters = convert_ft_to_m(feet)  # Convert to meters
        return f'{meters} m.'  # Return the result as a string in meters

    # Replace all occurrences in the text
    converted_text = re.sub(pattern, replacer, text)

    return converted_text


def treat_line(line: str) -> str:
    line = remove_greaters(line)
    line = fix_carac(line)
    line = convert_ft_to_m_in_text(line)

    return line

def copy_file_to_clipboard(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()  # Read the content of the file
            pyperclip.copy(content)  # Copy content to the clipboard
            print(f"Content of {filename} has been copied to the clipboard.")
    except FileNotFoundError:
        print(f"Error: The file {filename} was not found.")
    except IOError as e:
        print(f"Error reading the file {filename}: {e}")


def fix_file(file):
    # create an ouptut file by adding _fixed to the name
    output_file = file.replace(".md", "_fixed.md")
    fixed_content = []

    try:
        with open(file, 'r') as f:
            with open(output_file, 'w') as out:

                content = f.readlines()
                count = 0
                for line in content:
                    count += 1
                    if count == 1:
                        continue
                    line = treat_line(line)
                    fixed_content.append(line)
                    out.write(line)
        copy_file_to_clipboard(output_file)
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{file}' n'a pas été trouvé.")
        sys.exit(1)  # Quitter avec un code d'erreur
    except IOError as e:
        print(f"Erreur lors de la lecture du fichier '{file}': {e}")
        sys.exit(1)


def main():
    try:
        # Récupérer les arguments avec le parseur global

        fix_file(args.file)
    except SystemExit as e:
        # Gérer la sortie du programme en cas d'erreur
        print("Le programme a échoué.")
        sys.exit(e.code)  # Renvoyer le même code de sortie


if __name__ == '__main__':
    main()
