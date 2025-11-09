import argparse

def calculate_pcr_volumes(num_reactions):
    # Add 10% extra volume for pipetting errors
    safety_factor = 1.1
    
    # Base volumes per reaction
    volumes = {
        "2× Green Master Mix": 7.5,
        "Primer Forward (10 µM)": 0.5,
        "Primer Reverse (10 µM)": 0.5,
        "Template DNA": 1.0,
        "Water (ddH₂O)": 5.5
    }
    
    # Calculate and print results
    print("\nResults (safety factor of 10% included):")
    print("-" * 40)
    for component, base_volume in volumes.items():
        total_volume = base_volume * float(num_reactions) * safety_factor
        print(f"{component}:\t{total_volume:.2f} µL")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='PCR Reaction Calculator')
    parser.add_argument('--value', type=float, help='Number of reactions')
    
    args = parser.parse_args()
    
    # If no argument provided, ask for input
    if args.value is None:
        while True:
            try:
                num_reactions = float(input("Enter number of reactions: "))
                if num_reactions > 0:
                    break
                print("Please enter a positive number.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        num_reactions = args.value
    
    calculate_pcr_volumes(num_reactions)

if __name__ == "__main__":
    main()