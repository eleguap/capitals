import random
import unicodedata
import data
import time

BLACK       = "\033[30m"
RED         = "\033[31m"
GREEN       = "\033[32m"
YELLOW      = "\033[33m"
BLUE        = "\033[34m"
MAGENTA     = "\033[35m"
CYAN        = "\033[36m"
WHITE       = "\033[37m"
RESET       = "\033[0m"
UP_ONE_LINE = "\033[F"
CLEAR_LINE  = "\033[K"

def normalize(s: str) -> str:
    return (
        unicodedata.normalize("NFKD", s)
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
        .strip()
    )

def ensure_list(val: str | list[str]) -> list:
    return val if isinstance(val, list) else [val]

def print_score(correct: int, incorrect: int, missed: int, num_countries: int, start: float, end: float) -> None:
    elapsed = end - start
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    time = f"{minutes}:{seconds:02d}"

    print(MAGENTA + "\n=== Results ===" + RESET)
    print(GREEN +   "Correct:   " + RESET + f"{correct}")
    print(RED +     "Incorrect: " + RESET + f"{incorrect}")
    print(CYAN +    "Total:     " + RESET + f"{num_countries}")
    print(CYAN +    "Score:     " + RESET + f"{int(round(correct / num_countries, 2) * 100)}%")
    print(CYAN +    "Time:      " + RESET + time)

    if missed:
        print(MAGENTA + "\nYou missed:" + RESET)
        for country, caps in missed:
            print(f" - {country}: {', '.join(caps)}")
        print("")
        for country, caps in missed:
            print(f"'{country}': {caps}")
    print(MAGENTA + "=" * 15 + RESET)

def main() -> None:
    capitals = data.Capitals()

    while True:
        print(MAGENTA + "\n=== CAPITALS ===" + RESET)
        print(GREEN + "Type 'quit' or 'clear' to stop" + RESET)

        # Region
        while True:
            print(CYAN + "\nRegions: " + RESET + MAGENTA + ", ".join(capitals.capitals.keys()) + RESET)
            ans = input(CYAN + "Enter Region: " + RESET).strip().lower()

            if ans in ("quit", "clear"):
                print("Quitting…\n")
                return

            try:
                country_to_capital = capitals.capitals[ans]
                countries = list(country_to_capital.keys())
                break
            except KeyError:
                print(f"{ans} not found.")

        # Game
        random.shuffle(countries)
        correct = 0
        incorrect = 0
        missed = []
        num_countries = len(countries)
        quit = False

        print(MAGENTA + f"\n=== {ans.upper()} ===" + RESET)
        print(GREEN + "Type 'quit' or 'clear' to stop, 'skip' to move to the next country." + RESET)

        start = time.time()
        for country in countries:
            country_capitals = ensure_list(country_to_capital[country])
            needed = {normalize(c) for c in country_capitals}
            got = set()

            print(CYAN + f"\n{"Country" if ans != "us" else "State"}: {country}" + RESET)

            failed_once = False
            while True:
                ans = input("Capital: ").strip()
                if ans.lower() in ("quit", "clear"):
                    print_score(correct, incorrect, missed, num_countries, start, time.time())
                    print("Quitting…")
                    quit = True
                    break
                if ans.lower() == "skip":
                    incorrect += 1
                    missed.append((country, country_capitals))
                    print(UP_ONE_LINE + CLEAR_LINE + YELLOW + "Capital: " + RESET + "skip")
                    print(f"Skipped. Correct answer(s): {', '.join(country_capitals)}")
                    break

                n = normalize(ans)
                if n in needed and n not in got:
                    got.add(n)
                    remaining = len(needed) - len(got)
                    if remaining == 0:
                        if failed_once:
                            incorrect += 1
                            missed.append((country, country_capitals))
                            print(UP_ONE_LINE + CLEAR_LINE + GREEN + "Capital: " + RESET + f"{ans} ✅")

                        else:
                            correct += 1
                            print(UP_ONE_LINE + CLEAR_LINE + GREEN + "Capital: " + RESET + f"{ans} ✅")
                        break
                    else:
                        print(UP_ONE_LINE + CLEAR_LINE + GREEN + "Capital: " + RESET + f"{ans} ✅")
                elif n in needed and n in got:
                    print(UP_ONE_LINE + CLEAR_LINE + YELLOW + "Capital: " + RESET + f"{ans} ⚠️ (Already given)")
                else:
                    failed_once = True
                    print(UP_ONE_LINE + CLEAR_LINE + RED + "Capital: " + RESET + f"{ans}" + (" " if ans.strip() else "") + "❌")

            if quit is True:
                break

        if quit is False:
            print_score(correct, incorrect, missed, num_countries, start, time.time())

if __name__ == "__main__":
    main()
