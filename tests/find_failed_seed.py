# find_first_failing_seed.py

# Import your main program (change this import!)
from main import test  # assumes test(seed) -> True or raises error


def find_first_failing_seed(start_seed=0, max_seed=10_000_000):
    """
    Runs test(seed) starting from start_seed,
    returns the first seed that fails.
    """
    for seed in range(start_seed, max_seed):
        try:
            result = test(seed)

            if result is True:
                print(f"Seed {seed} passed.")
                continue

            # If the function returns something weird
            print(f"Seed {seed} returned non-True value: {result}")
            return seed

        except Exception as e:
            print(f"Seed {seed} FAILED with error: {e}")
            return seed

    print("No failing seed found in range.")
    return None


if __name__ == "__main__":
    failing_seed = find_first_failing_seed()

    if failing_seed is not None:
        print(f"\n*** First failing seed: {failing_seed} ***")
    else:
        print("\nNo failing seeds found.")
