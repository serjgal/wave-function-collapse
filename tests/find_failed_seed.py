# find_first_failing_seed.py

# Import your test function (change this import!)
from main import test   # test(seed) -> True, False, or raises error


def find_first_failing_seed(start_seed=10, max_seed=10_000_000):
    """
    For each seed:
        Loop test(seed) until:
          - test returns True  -> seed passes, move to next seed
          - test raises error  -> seed fails, return seed
          - test returns False -> keep looping same seed
    """
    for seed in range(start_seed, max_seed):
        print(f"Testing seed {seed}...")

        while True:
            try:
                result = test(seed)

                if result is True:
                    # Seed finally succeeded → go to next seed
                    print(f"Seed {seed} passed.")
                    break

            except Exception as e:
                print(f"Seed {seed} FAILED with error: {e}")
                return seed

    print("No failing seeds found in range.")
    return None


if __name__ == "__main__":
    failing_seed = find_first_failing_seed()

    if failing_seed is not None:
        print(f"\n*** First failing seed: {failing_seed} ***")
    else:
        print("\nNo failing seeds found.")
