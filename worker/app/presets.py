# =================================================================
# FILE: worker/app/presets.py (PROFESSIONAL STUDIO-GRADE COOKBOOK)
# This is the complete professional preset system designed to compete
# with $100,000 studio chains. Each preset is a carefully crafted
# signal chain that delivers genuinely premium results.
# =================================================================

PRO_COOKBOOK_DEFINITIVE_FINAL = {
    
    # ===============================================================
    # FLAGSHIP PODCAST PRESETS - THE MONEY MAKERS
    # ===============================================================
    "podcast_pro_male": {
        "lufs_target": -16.0,
        
        # STAGE 1: Surgical Frequency Sculpting
        "character_eq": [
            "highpass", "75",                    # Remove rumble
            "equalizer", "120", "2.0q", "-1.5", # Reduce boxiness
            "equalizer", "250", "1.8q", "-2.0", # Cut muddiness
            "equalizer", "400", "1.2q", "-1.0", # Smooth low-mids
            "equalizer", "800", "0.8q", "0.8",  # Add body
            "equalizer", "1800", "1.5q", "1.2", # Presence boost
            "equalizer", "3200", "1.8q", "2.0", # Clarity
            "equalizer", "5500", "2.2q", "1.5", # Air and openness
            "equalizer", "8000", "1.5q", "0.8", # Subtle sparkle
        ],
        
        # STAGE 2: Professional Multi-Band Dynamics
        "mcompand_string": "0.003,0.05 -50,-45,-40,-38,-30,-28,-25,-23,-15,-12 150 0.002,0.03 -48,-43,-38,-36,-28,-26,-23,-21,-13,-10 2500 0.001,0.015 -46,-41,-36,-34,-26,-24,-21,-19,-11,-8 6000 0.0008,0.01 -44,-39,-34,-32,-24,-22,-19,-17,-9,-6",
        
        # STAGE 3: Harmonic Enhancement & Character
        "deess_freq": "6200",
        "saturation": "2.2",
        "harmonic_enhancement": True,
        
        # STAGE 4: Professional Features
        "stereo_width": 0.95,
        "transient_shaping": "gentle",
        "vintage_character": "tube_warmth"
    },
    
    "podcast_pro_female": {
        "lufs_target": -16.0,
        
        # Optimized for female vocal characteristics
        "character_eq": [
            "highpass", "85",
            "equalizer", "150", "2.0q", "-1.8",  # Reduce boominess
            "equalizer", "280", "1.6q", "-2.5",  # Cut harsh low-mids
            "equalizer", "450", "1.0q", "-0.8",
            "equalizer", "950", "0.9q", "1.0",   # Warmth
            "equalizer", "2200", "1.4q", "1.8",  # Presence
            "equalizer", "4200", "1.6q", "2.5",  # Clarity and definition
            "equalizer", "6800", "2.0q", "1.8",  # Brightness
            "equalizer", "9500", "1.8q", "1.0",  # Air
        ],
        
        "mcompand_string": "0.002,0.04 -48,-43,-38,-36,-28,-26,-23,-21,-13,-10 200 0.0015,0.025 -46,-41,-36,-34,-26,-24,-21,-19,-11,-8 3000 0.001,0.012 -44,-39,-34,-32,-24,-22,-19,-17,-9,-6 7000 0.0006,0.008 -42,-37,-32,-30,-22,-20,-17,-15,-7,-4",
        
        "deess_freq": "6800",
        "saturation": "1.8",
        "harmonic_enhancement": True,
        "stereo_width": 0.92,
        "transient_shaping": "crisp",
        "vintage_character": "silk_presence"
    },
    
    # ===============================================================
    # PREMIUM AUDIOBOOK PRESETS
    # ===============================================================
    "audiobook_male_premium": {
        "lufs_target": -18.0,
        
        "character_eq": [
            "highpass", "70",
            "equalizer", "100", "1.5q", "-1.2",  # Remove floor noise
            "equalizer", "200", "2.0q", "-1.8",  # Reduce boxiness
            "equalizer", "350", "1.3q", "-1.0",
            "equalizer", "700", "0.8q", "0.5",   # Gentle warmth
            "equalizer", "1400", "1.2q", "1.0",  # Intelligibility
            "equalizer", "2800", "1.6q", "1.5",  # Clarity
            "equalizer", "5000", "2.0q", "1.2",  # Presence
            "equalizer", "7500", "1.8q", "0.6",  # Subtle air
        ],
        
        # Gentler compression for long-form listening
        "mcompand_string": "0.008,0.15 -55,-50,-45,-43,-35,-33,-30,-28,-20,-17 180 0.004,0.08 -53,-48,-43,-41,-33,-31,-28,-26,-18,-15 3000 0.002,0.04 -51,-46,-41,-39,-31,-29,-26,-24,-16,-13 5500 0.001,0.02 -49,-44,-39,-37,-29,-27,-24,-22,-14,-11",
        
        "deess_freq": "5800",
        "saturation": "1.2",
        "harmonic_enhancement": False,
        "stereo_width": 0.88,
        "listening_fatigue_reduction": True
    },
    
    "audiobook_female_premium": {
        "lufs_target": -18.0,
        
        "character_eq": [
            "highpass", "80",
            "equalizer", "120", "1.8q", "-1.5",
            "equalizer", "250", "2.2q", "-2.0",  # Critical for female voice clarity
            "equalizer", "400", "1.1q", "-0.8",
            "equalizer", "800", "0.9q", "0.8",
            "equalizer", "1600", "1.3q", "1.2",
            "equalizer", "3200", "1.5q", "1.8",
            "equalizer", "5800", "2.0q", "1.5",
            "equalizer", "8500", "1.6q", "0.8",
        ],
        
        "mcompand_string": "0.006,0.12 -53,-48,-43,-41,-33,-31,-28,-26,-18,-15 200 0.003,0.06 -51,-46,-41,-39,-31,-29,-26,-24,-16,-13 3500 0.0015,0.03 -49,-44,-39,-37,-29,-27,-24,-22,-14,-11 6500 0.0008,0.015 -47,-42,-37,-35,-27,-25,-22,-20,-12,-9",
        
        "deess_freq": "7200",
        "saturation": "1.0",
        "harmonic_enhancement": False,
        "stereo_width": 0.85,
        "listening_fatigue_reduction": True
    },
    
    # ===============================================================
    # BROADCAST & COMMERCIAL GRADE
    # ===============================================================
    "broadcast_radio_premium": {
        "lufs_target": -14.0,
        
        "character_eq": [
            "highpass", "95",
            "equalizer", "120", "2.5q", "1.5",   # Punchy low end
            "equalizer", "200", "1.8q", "-1.0",
            "equalizer", "400", "1.0q", "-0.5",
            "equalizer", "800", "0.8q", "1.2",   # Body and power
            "equalizer", "1600", "1.2q", "1.8",  # Cut-through
            "equalizer", "3200", "1.6q", "2.5",  # Presence
            "equalizer", "6400", "2.0q", "2.0",  # Broadcast brightness
            "equalizer", "10000", "1.5q", "1.2", # Air
        ],
        
        # Aggressive compression for broadcast
        "mcompand_string": "0.001,0.02 -65,-60,-20,-18,-15,-13,-12,-10,-8,-6 250 0.0008,0.015 -63,-58,-18,-16,-13,-11,-10,-8,-6,-4 4000 0.0005,0.01 -61,-56,-16,-14,-11,-9,-8,-6,-4,-2 8000 0.0003,0.005 -59,-54,-14,-12,-9,-7,-6,-4,-2,0",
        
        "deess_freq": "7000",
        "saturation": "3.5",
        "harmonic_enhancement": True,
        "stereo_width": 1.0,
        "transient_shaping": "aggressive",
        "broadcast_processing": True
    },
    
    # ===============================================================
    # GAMING & CHARACTER VOICES
    # ===============================================================
    "gaming_character_premium": {
        "lufs_target": -14.0,
        
        "character_eq": [
            "highpass", "50",                    # Keep low rumble for character
            "equalizer", "80", "1.5q", "2.0",   # Powerful low end
            "equalizer", "150", "2.0q", "3.0",  # Chest resonance
            "equalizer", "300", "1.2q", "-1.5", # Control muddiness
            "equalizer", "600", "0.9q", "1.5",  # Body
            "equalizer", "1200", "1.1q", "0.8",
            "equalizer", "2400", "1.4q", "2.2", # Aggression
            "equalizer", "4800", "1.8q", "2.8", # Bite and clarity
            "equalizer", "8000", "2.2q", "3.2", # Presence and cut
            "equalizer", "12000", "1.6q", "1.5", # Sparkle
        ],
        
        # Character-focused compression
        "mcompand_string": "0.001,0.03 -60,-55,-25,-23,-18,-16,-15,-13,-10,-8 300 0.0008,0.02 -58,-53,-23,-21,-16,-14,-13,-11,-8,-6 5000 0.0005,0.01 -56,-51,-21,-19,-14,-12,-11,-9,-6,-4 9000 0.0003,0.005 -54,-49,-19,-17,-12,-10,-9,-7,-4,-2",
        
        "deess_freq": "7500",
        "saturation": "4.0",
        "harmonic_enhancement": True,
        "stereo_width": 1.05,
        "character_enhancement": True,
        "gaming_optimized": True
    },
    
    # ===============================================================
    # EDUCATIONAL & CORPORATE
    # ===============================================================
    "educator_crystal_clear": {
        "lufs_target": -16.0,
        
        "character_eq": [
            "highpass", "90",
            "equalizer", "150", "2.0q", "-1.8",  # Remove muddiness
            "equalizer", "300", "1.5q", "-2.2",  # Critical for clarity
            "equalizer", "500", "1.0q", "-0.8",
            "equalizer", "1000", "0.8q", "0.5",
            "equalizer", "2000", "1.2q", "2.0",  # Speech intelligibility
            "equalizer", "4000", "1.6q", "2.8",  # Maximum clarity
            "equalizer", "6000", "2.0q", "2.2",  # Presence
            "equalizer", "8500", "1.5q", "1.2",  # Air without harshness
        ],
        
        "mcompand_string": "0.004,0.08 -52,-47,-42,-40,-32,-30,-27,-25,-17,-14 220 0.002,0.04 -50,-45,-40,-38,-30,-28,-25,-23,-15,-12 3500 0.001,0.02 -48,-43,-38,-36,-28,-26,-23,-21,-13,-10 6500 0.0008,0.01 -46,-41,-36,-34,-26,-24,-21,-19,-11,-8",
        
        "deess_freq": "6000",
        "saturation": "1.0",
        "harmonic_enhancement": False,
        "intelligibility_optimization": True,
        "fatigue_reduction": True
    },
    
    # ===============================================================
    # EXPERIMENTAL & SPECIALTY
    # ===============================================================
    "vintage_radio_show": {
        "lufs_target": -16.0,
        
        "character_eq": [
            "highpass", "120",                   # Vintage rolloff
            "equalizer", "200", "1.0q", "1.0",
            "equalizer", "400", "0.8q", "1.2",
            "equalizer", "800", "0.9q", "1.5",  # Vintage warmth
            "equalizer", "1600", "1.2q", "2.0", # Presence
            "equalizer", "3200", "1.8q", "1.5",
            "lowpass", "8000"                   # Vintage rolloff
        ],
        
        "mcompand_string": "0.01,0.2 -60,-55,-50,-48,-40,-38,-35,-33,-25,-22 200 0.005,0.1 -58,-53,-48,-46,-38,-36,-33,-31,-23,-20",
        
        "deess_freq": "5500",
        "saturation": "2.8",
        "vintage_character": "classic_radio",
        "tape_saturation": True
    },
    
    # ===============================================================
    # UTILITY & TESTING
    # ===============================================================
    "reference_mastered": {
        "lufs_target": -23.0,
        "character_eq": ["highpass", "20"],
        "mcompand_string": None,
        "deess_freq": None,
        "saturation": "0",
        "reference_grade": True
    },
    
    "diagnostic_transparent": {
        "lufs_target": -16.0,
        "character_eq": None,
        "mcompand_string": None,
        "deess_freq": None,
        "saturation": "0",
        "diagnostic_mode": True
    }
}

# Voice catalog for Text-to-Audio (PRO_COOKBOOK_V1 compatibility)
PRO_COOKBOOK_V1 = {
    "podcast_pro_male": {
    "voice": "en-US-DavisNeural",
    "lufs_target": -16.0,
    "initial_sox_eq": ["highpass", "80", "equalizer", "3200", "1.5q", "1.0"],
    "mcompand_params": "0.005,0.1 -47,-40,-35,-35,-25,-25 200 0.003,0.05 -47,-40,-35,-35,-25,-25 4000 0.001,0.02 -47,-40,-35,-35,-25,-25",
    "deess_freq": "6200",
    "saturation": "1.5",
    "ssml_mode": "prosody",
    "prosody_rate": "-8%",  # NEW: Slightly slower for authority
    "prosody_pitch": "-2%"  # NEW: Slightly lower for warmth
    },
    
    "podcast_pro_female": {
        "voice": "en-US-JennyMultilingualNeural",
        "lufs_target": -16.0,
        "initial_sox_eq": ["highpass", "90", "equalizer", "4200", "1.5q", "1.5"],
        "mcompand_params": "0.005,0.1 -45,-38,-33,-33,-23,-23 250 0.003,0.05 -45,-38,-33,-33,-23,-23 4500 0.001,0.02 -45,-38,-33,-33,-23,-23",
        "deess_freq": "6800",
        "saturation": "1.2",
        "ssml_mode": "prosody"
    }
}