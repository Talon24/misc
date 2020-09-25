"""Write how to spell a (big) number."""

import sys
import json
import argparse


def number_speller(number: int, names: list, show_empty=False):
    names.insert(0, "")
    output = []
    for name in names[:-1]:
        current = number % 1000
        number //= 1000
        if not show_empty and current == 0:
            continue
        output.append(f"{current:3.0f} {name}")
        if number == 0:
            break
    if number > 0:
        output.append(f"{number:3.0f} {names[-1]}")
    return "\n".join(output[::-1])


def main():
    try:
        with open("numbers.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("numbers.json - File is missing!")
        sys.exit(1)
    parser = argparse.ArgumentParser()
    parser.add_argument("number", type=int, help="The number to be displayed.")
    parser.add_argument("--show-empty", "-e", help="Whether groups of zero "
                        "should be included.", action="store_true")
    parser.add_argument("--language", "-l", help="Target language",
                        default="German", choices=data.keys())
    arguments = parser.parse_args()
    names = data[arguments.language]
    result = number_speller(arguments.number, names,
                            show_empty=arguments.show_empty)
    print(result)

if __name__ == '__main__':
    main()
