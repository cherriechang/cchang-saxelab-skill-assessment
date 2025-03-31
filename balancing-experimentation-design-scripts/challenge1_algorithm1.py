# Imports
from random import choices
import numpy as np
from collections import Counter, defaultdict

factorA = [1, 2, 3, 4]  # 4 levels (between-subject factor)
factorB = ['X', 'Y']    # 2 levels (within-subject factor)
factorC = ['L', 'R']    # 2 levels (within-subject factor)
# Make array of the 4 possible combinations of Factor B and Factor C
factorBC_combos = [[b, c] for b in factorB for c in factorC]

def randomize_trials(subjectIds):
    """
    Implements a mixed design randomization system with:
    - Factor A as between-subject (each subject gets one level)
    - Factors B and C as within-subject (each subject gets all combinations)

    Parameters:
    - subjectIds: array-like, IDs of subjects to assign conditions to

    Returns:
    - Dictionary mapping each subject ID to their condition sequence
    """
    # Step 1: Create balanced assignment of Factor A across all subjects
    # Maximize distribution equality of Factor A levels by dividing length of subjectIds by length of factorA, then tiling factorA by the quotient, finally filling in the remainder factorA-level-to-subjectId assignments by randomly sampling without replacement from factorA.
    facA_quotient, facA_remainder = divmod(len(subjectIds), len(factorA))
    # Create base array with equal distribution
    factorA_expanded = np.tile(factorA, facA_quotient)
    # Randomly assign remaining Factor A levels for perfect equal distribution
    factorA_expanded = np.append(factorA_expanded, np.random.choice(factorA, size=facA_remainder, replace=False))
    # Shuffle to randomize which subject gets which Factor A level
    np.random.shuffle(factorA_expanded)

    # Print distribution of Factor A levels to verify equal distribution
    print("Frequency of each factorA level:")
    print({key: Counter(factorA_expanded)[key] for key in factorA})

    # Step 2: Create condition sequences for each subject
    # For each subject, assign one Factor A level and all Factor B-C combinations
    subjectId_condition_map = defaultdict(list)
    for sid, a in list(zip(subjectIds, factorA_expanded)):
        # Make a copy to prevent modifying the original combinations
        factorBC_copy = np.copy(factorBC_combos)
        # Shuffle Factor B-C combinations to create a unique presentation order for this subject ID (sid)
        np.random.shuffle(factorBC_copy)
        # Assign each B-C combination to this subject while keeping their Factor A level constant
        for b, c in factorBC_copy:
            subjectId_condition_map[sid].append({'factorA': a, 'factorB': b, 'factorC': c})

    return subjectId_condition_map

if __name__ == "__main__":
    # Example subject IDs
    subjectIds = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']
    # Call the randomize_trials function
    subject_conditions = randomize_trials(subjectIds)
    # Print the resulting condition assignments
    for subject, conditions in subject_conditions.items():
        print(f"Subject {subject}:")
        for condition in conditions:
            print(f"  {condition}")