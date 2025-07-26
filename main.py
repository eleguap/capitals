import random
import unicodedata
import data

BLACK   = "\033[30m"
RED     = "\033[31m"
GREEN   = "\033[32m"
YELLOW  = "\033[33m"
BLUE    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
WHITE   = "\033[37m"
RESET   = "\033[0m"
UP_ONE_LINE = "\033[F"
CLEAR_LINE = "\033[K"

def normalize(s: str) -> str:
    return (
        unicodedata.normalize("NFKD", s)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
        .strip()
    )

def ensure_list(val):
    return val if isinstance(val, list) else [val]

def main():
    capitals = data.Capitals()

    while True:
        ans = input(CYAN + "\nEnter Continent: " + RESET).strip().lower()

        if ans == "quit":
            print("Quitting…\n")
            return

        try:
            country_to_capital = capitals.capitals[ans]
            countries = list(country_to_capital.keys())
            break
        except KeyError:
            print(f"{ans} not found.")

    random.shuffle(countries)

    correct = 0
    incorrect = 0
    missed = []
    num_countries = len(countries)

    print(MAGENTA + f"\n=== {ans.capitalize() if ans != "us" else "US"} ===" + RESET)
    print("Type 'quit' to stop, 'skip' to move to the next country.")

    for country in countries:
        capitals = ensure_list(country_to_capital[country])
        needed = {normalize(c) for c in capitals}
        got = set()

        print(CYAN + f"\n{"Country" if ans != "us" else "State"}: {country}" + RESET)

        failed_once = False
        while True:
            ans = input(GREEN + "Capital: " + RESET).strip()
            if ans.lower() == "quit":
                print("\nQuitting…")
                print_score(correct, incorrect, missed, num_countries)
                return
            if ans.lower() == "skip":
                incorrect += 1
                missed.append((country, capitals))
                print(f"Skipped. Correct answer(s): {', '.join(capitals)}")
                break

            n = normalize(ans)
            if n in needed and n not in got:
                got.add(n)
                remaining = len(needed) - len(got)
                if remaining == 0:
                    if failed_once:
                        incorrect += 1
                        missed.append((country, capitals))
                        print(UP_ONE_LINE + CLEAR_LINE + f"Capital: {ans} ✅")

                    else:
                        correct += 1
                        print(UP_ONE_LINE + CLEAR_LINE + f"Capital: {ans} ✅")
                    break
                else:
                    print(UP_ONE_LINE + CLEAR_LINE + f"Capital: {ans} ✅")
            else:
                failed_once = True
                print(UP_ONE_LINE + CLEAR_LINE + f"Capital: {ans} ❌")

    print_score(correct, incorrect, missed, num_countries)

def print_score(correct, incorrect, missed, num_countries):
    print(MAGENTA + "\n=== Results ===" + RESET)
    print(GREEN +   "Correct:   " + RESET + f"{correct}")
    print(RED +     "Incorrect: " + RESET + f"{incorrect}")
    print(CYAN +    "Total:     " + RESET + f"{num_countries}")
    print(CYAN +    "Score:     " + RESET + f"{int(round(correct / num_countries, 2) * 100)}%")
    if missed:
        print(MAGENTA + "\nYou missed:" + RESET)
        for country, caps in missed:
            print(f" - {country}: {', '.join(caps)}")
    print("")

if __name__ == "__main__":
    main()
