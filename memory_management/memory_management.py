def get_int_list(prompt):
    while True:
        try:
            data = input(prompt).strip().split()
            values = [int(x) for x in data]
            if len(values) == 0:
                print("Input cannot be empty.")
                continue
            return values
        except ValueError:
            print("Invalid input. Enter numbers only separated by spaces.")


def print_layout(processes, partitions):
    print("\nPROCESSES              PARTITIONS\n")

    max_len = max(len(processes), len(partitions))

    for i in range(max_len):
        left = ""
        right = ""

        if i < len(processes):
            left = f"P{i+1} = {processes[i]} KB"

        if i < len(partitions):
            right = f"[ {partitions[i]} KB ]"

        print(f"{left:<22}{right}")


def main():
    print("===== MEMORY MANAGEMENT (MFT) =====\n")

    input("Press Enter to continue...\n")

    partitions = get_int_list("Enter fixed partitions (space separated): ")
    processes = get_int_list("Enter processes (space separated): ")

    print_layout(processes, partitions)


if __name__ == "__main__":
    main()