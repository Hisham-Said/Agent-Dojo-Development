from attacks.ignore_previous import IgnorePreviousAttack
from attacks.important_message import ImportantMessageAttack


def main():
    original = "Please review the project report."

    attacks = [
        IgnorePreviousAttack(),
        ImportantMessageAttack(),
    ]

    for attack in attacks:
        result = attack.apply(original)

        print(f"\nAttack: {attack.name}")
        print(result)


if __name__ == "__main__":
    main()