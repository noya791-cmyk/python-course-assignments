import argparse
import sys
from pcr_calculator import PCRCalculator

def display_results(volumes, preset_name="Green"):
    """Display results in a formatted table."""
    print("\n" + "="*50)
    print(f"PCR Reaction Volumes ({preset_name} preset)")
    print("="*50)
    print("Results (safety factor of 10% included):")
    print("-" * 50)
    
    for component in volumes.keys():
        print(f"{component:.<30} {volumes[component]:>6.2f} µL")
    
    print("-" * 50)
    print()

def get_numeric_input(prompt, allow_zero=False):
    """Get validated numeric input from user."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Error: Please enter a non-negative number.")
                continue
            if value == 0 and not allow_zero:
                print("Error: Please enter a number greater than 0.")
                continue
            return value
        except ValueError:
            print("Error: Please enter a valid number.")

def main():
    parser = argparse.ArgumentParser(
        description='PCR Reaction Calculator - Calculate reagent volumes for PCR reactions',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python pcr_calculator_cli.py --reactions 3
  python pcr_calculator_cli.py --reactions 3 --preset "Q5® (NEB)"
  python pcr_calculator_cli.py --reactions 2 --preset "Phusion®" --primer-conc 5
  python pcr_calculator_cli.py --reactions 5 --template-ng 50 --template-conc 100
        """
    )
    
    parser.add_argument('--reactions', type=float, 
                       help='Number of reactions')
    parser.add_argument('--preset', choices=["Green"] + list(PCRCalculator.PRESETS.keys()),
                       default="Green",
                       help='Polymerase preset to use (default: Green)')
    parser.add_argument('--primer-conc', type=float,
                       help='Primer stock concentration in µM (overrides preset default)')
    parser.add_argument('--reaction-vol', type=float,
                       help='Total reaction volume in µL (overrides preset default)')
    parser.add_argument('--template-ng', type=float,
                       help='Desired template DNA amount in ng')
    parser.add_argument('--template-conc', type=float,
                       help='Template DNA concentration in ng/µL')
    
    args = parser.parse_args()
    
    # Get number of reactions
    if args.reactions is not None:
        num_reactions = args.reactions
    else:
        num_reactions = get_numeric_input("Enter number of reactions: ", allow_zero=False)
    
    try:
        # Build kwargs for calculate_volumes
        kwargs = {"num_reactions": num_reactions}
        
        if args.preset != "Green":
            kwargs["preset"] = args.preset
            preset_display = args.preset
        else:
            preset_display = "Green Master Mix (default)"
        
        if args.primer_conc is not None:
            kwargs["primer_concentration"] = args.primer_conc
        
        if args.reaction_vol is not None:
            kwargs["reaction_volume"] = args.reaction_vol
        
        if args.template_ng is not None:
            kwargs["template_dna_ng"] = args.template_ng
        
        if args.template_conc is not None:
            kwargs["template_dna_concentration"] = args.template_conc
        
        # Calculate volumes
        volumes = PCRCalculator.calculate_volumes(**kwargs)
        
        # Display results
        display_results(volumes, preset_display)
        
    except ValueError as e:
        print(f"\n❌ Calculation Error: {str(e)}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()