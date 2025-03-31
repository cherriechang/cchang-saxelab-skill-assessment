# Imports
from random import choices
import numpy as np
from collections import Counter, defaultdict

factorA = [1, 2, 3, 4]  # 4 levels (between-subject factor)
factorB = ['X', 'Y']    # 2 levels (within-subject factor)
factorC = ['L', 'R']    # 2 levels (within-subject factor)

# Make array of the 4 possible combinations of Factor B and Factor C
factorBC_combos = [[b, c] for b in factorB for c in factorC]
# Total number of subjects
total_subjects = 79
# Generates stub subject IDs for the "bank" subject ID-condition map initialized in the server
stub_subjectIds = np.arange(0, 79) 
# Initialize an empty dictionary that will hold the actual subject ID-condition mappings assigned in real time as the experiment is run on recruited subjects
real_subjectId_condition_map = {} 

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

print("Randomizing trials for server's stub subject IDs...")
server_subjectId_condition_map = randomize_trials(stub_subjectIds)

def assign_conditions_to_subject(subjectId):
    """
    Assigns the conditions to a new subject and updates the server's condition map.

    Parameters:
    - subjectId: ID of the new subject to assign conditions to

    Returns:
    - Dictionary mapping the subject ID to their assigned conditions
    """
    # Check if the subjectId already exists in the server's condition map
    if subjectId not in real_subjectId_condition_map:
        real_subjectId_condition_map[subjectId] = server_subjectId_condition_map.pop(np.random.choice(list(server_subjectId_condition_map.keys()))) # Pops a random subjectId-condition mapping from the starting dictionary in the server and updates a global dictionary to hold the pairing between the actual subject ID and condition
    print(f"{subjectId}:\n")
    for condition in real_subjectId_condition_map[subjectId]:
        print(f"    {condition}")
    print(f"Number of entires in real_subjectId_condition_map:{len(real_subjectId_condition_map)}\n")
    return real_subjectId_condition_map[subjectId]

if __name__ == "__main__":
    # Example subject IDs
    example_subjectIds = ["S" + str(i) for i in np.arange(1,200)]
    np.random.shuffle(example_subjectIds)
    # Call the assign_conditions_to_subject function for up to 79 subjects
    for i in range(79):
        assign_conditions_to_subject(example_subjectIds[i])