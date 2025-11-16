class PCRCalculator:
    # Preset reactions with different polymerases
    PRESETS = {
        "Q5® (NEB)": {
            "name": "Q5® Hot Start High-Fidelity 2× Master Mix (NEB)",
            "description": "High-fidelity polymerase",
            "master_mix": 7.5,
            "primer_forward": 0.3,
            "primer_reverse": 0.3,
            "template_dna": 1.0,
            "primer_concentration": 10.0,  # µM
            "reaction_volume": 15.0,  # µL
        },
        "Phusion®": {
            "name": "Phusion® High-Fidelity PCR Master Mix (Thermo, 2×)",
            "description": "High accuracy, fast extension",
            "master_mix": 7.5,
            "primer_forward": 0.4,
            "primer_reverse": 0.4,
            "template_dna": 1.0,
            "primer_concentration": 10.0,  # µM
            "reaction_volume": 15.0,  # µL
        },
        "Taq": {
            "name": "Taq DNA Polymerase Master Mix (standard Taq, 2×)",
            "description": "Regular Taq (no dye)",
            "master_mix": 7.5,
            "primer_forward": 0.45,
            "primer_reverse": 0.45,
            "template_dna": 1.0,
            "primer_concentration": 10.0,  # µM
            "reaction_volume": 15.0,  # µL
        },
        "Platinum™ II": {
            "name": "Platinum™ II Hot-Start PCR Master Mix (Invitrogen, 2×)",
            "description": "Fast, specific, multiplex-friendly",
            "master_mix": 7.5,
            "primer_forward": 0.3,
            "primer_reverse": 0.3,
            "template_dna": 1.0,
            "primer_concentration": 10.0,  # µM
            "reaction_volume": 15.0,  # µL
        }
    }
    
    # Default (Green) components
    BASE_VOLUMES = {
        "2× Green Master Mix": 7.5,
        "Primer Forward (10 µM)": 0.5,
        "Primer Reverse (10 µM)": 0.5,
        "Template DNA": 1.0,
        "Water (ddH₂O)": 5.5
    }
    
    COMPONENTS = [
        "2× Green Master Mix",
        "Primer Forward (10 µM)",
        "Primer Reverse (10 µM)",
        "Template DNA",
        "Water (ddH₂O)"
    ]
    
    SAFETY_FACTOR = 1.1  # 10% extra volume for pipetting errors
    
    @staticmethod
    def calculate_volumes(num_reactions, preset=None, primer_concentration=None, 
                         reaction_volume=None, template_dna_ng=None, template_dna_concentration=None):
        """
        Calculate PCR reaction volumes for given number of reactions.
        
        Args:
            num_reactions (float): Number of reactions to calculate for
            preset (str): Optional preset name from PRESETS dict
            primer_concentration (float): Optional primer stock concentration in µM
            reaction_volume (float): Optional total reaction volume in µL
            template_dna_ng (float): Optional desired template DNA amount in ng
            template_dna_concentration (float): Optional template DNA concentration in ng/µL
            
        Returns:
            dict: Component names as keys and calculated volumes as values
            
        Raises:
            ValueError: If num_reactions <= 0 or invalid parameters provided
        """
        # Validate num_reactions
        if num_reactions <= 0:
            raise ValueError("Number of reactions must be greater than 0")
        
        num_reactions = float(num_reactions)
        
        # Use preset if specified
        if preset and preset in PCRCalculator.PRESETS:
            preset_data = PCRCalculator.PRESETS[preset]
            master_mix_vol = preset_data["master_mix"]
            primer_f_vol = preset_data["primer_forward"]
            primer_r_vol = preset_data["primer_reverse"]
            template_vol = preset_data["template_dna"]
            primer_conc = primer_concentration or preset_data["primer_concentration"]
            total_rxn_vol = reaction_volume or preset_data["reaction_volume"]
        else:
            # Use defaults
            master_mix_vol = 7.5
            primer_f_vol = 0.5
            primer_r_vol = 0.5
            template_vol = 1.0
            primer_conc = primer_concentration or 10.0
            total_rxn_vol = reaction_volume or 15.0
        
        # Calculate template DNA volume if concentration is provided
        if template_dna_concentration and template_dna_ng:
            if template_dna_concentration <= 0:
                raise ValueError("Template DNA concentration must be greater than 0")
            if template_dna_ng < 0:
                raise ValueError("Template DNA amount cannot be negative")
            template_vol = template_dna_ng / template_dna_concentration
        
        # Adjust primer volumes based on primer concentration if different from 10 µM
        if primer_concentration and primer_concentration != 10.0:
            # Scale primers inversely: lower concentration needs more volume for same final concentration
            primer_f_vol = primer_f_vol * (10.0 / primer_concentration)
            primer_r_vol = primer_r_vol * (10.0 / primer_concentration)
        
        # Calculate water volume
        water_vol = total_rxn_vol - (master_mix_vol + primer_f_vol + primer_r_vol + template_vol)
        
        if water_vol < 0:
            raise ValueError("Component volumes exceed total reaction volume. Adjust parameters.")
        
        # Calculate total volumes with safety factor
        volumes = {
            "Master Mix": master_mix_vol * num_reactions * PCRCalculator.SAFETY_FACTOR,
            "Primer Forward": primer_f_vol * num_reactions * PCRCalculator.SAFETY_FACTOR,
            "Primer Reverse": primer_r_vol * num_reactions * PCRCalculator.SAFETY_FACTOR,
            "Template DNA": template_vol * num_reactions * PCRCalculator.SAFETY_FACTOR,
            "Water (ddH₂O)": water_vol * num_reactions * PCRCalculator.SAFETY_FACTOR
        }
        
        return volumes
    
    @staticmethod
    def calculate_volumes_legacy(num_reactions):
        """
        Legacy method for backward compatibility - calculates default Green Master Mix.
        
        Args:
            num_reactions (float): Number of reactions to calculate for
            
        Returns:
            dict: Component names as keys and calculated volumes as values
            
        Raises:
            ValueError: If num_reactions <= 0
        """
        return PCRCalculator.calculate_volumes(num_reactions)