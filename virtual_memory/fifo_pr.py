def fifo_page_replacement():
    MAX_REFERENCES = 20
    MAX_FRAMES = 10

    print("FIFO Page Replacement Simulator")
    print("--------------------------------")

    # Input number of frames
    while True:
        try:
            frames_count = int(input(f"Enter number of page frames (1 to {MAX_FRAMES}): "))
            if 1 <= frames_count <= MAX_FRAMES:
                break
            print(f"Please enter a value between 1 and {MAX_FRAMES}.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

    # Input reference string
    while True:
        try:
            ref_input = input(
                f"Enter page reference string (max {MAX_REFERENCES}, separated by commas): "
            )

            reference_string = [int(x.strip()) for x in ref_input.split(",") if x.strip() != ""]

            if 1 <= len(reference_string) <= MAX_REFERENCES:
                break
            print(f"Please enter between 1 and {MAX_REFERENCES} numbers.")
        except ValueError:
            print("Invalid input. Please enter only integers separated by commas.")

fifo_page_replacement()