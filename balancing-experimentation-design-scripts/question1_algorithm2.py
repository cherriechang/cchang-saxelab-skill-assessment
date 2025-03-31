# Imports
from random import choices
import numpy as np
from collections import Counter

factorA = [1, 2, 3, 4]  # 4 levels (between-subject factor)
factorB = ['X', 'Y']    # 2 levels (within-subject factor)
factorC = ['L', 'R']    # 2 levels (within-subject factor)

# Make array of the 4 possible combinations of Factor B and Factor C
factorBC_combos = [[b, c] for b in factorB for c in factorC]
# Index tracking which level in the factorA array to assign to the next subject
factorA_index = 0
# Dictionary keeping track of the condition sequences each subject was assigned
subjectId_condition_map = {}

def modified_randomize_trials(subjectId):
    """
    Implements a mixed design randomization system that outputs a dictionary containing the 4 trial conditions for each subject with the following assignment rules for factors A, B and C:
    - Factor A as between-subject (each subject gets one level)
    - Factors B and C as within-subject (each subject experiences all combinations)

    Parameters:
    - subjectId: ID of the subject to assign conditions to

    Returns:
    - Dictionary mapping each subject ID to their 4 conditions
    """
    if subjectId not in subjectId_condition_map:
        factorBC_copy = np.copy(factorBC_combos)
        np.random.shuffle(factorBC_copy)
        subjectId_condition_map[subjectId] = [{'factorA': factorA[factorA_index], 'factorB': b, 'factorC': c} for b, c in factorBC_copy]
        global factorA_index
        factorA_index += 1
        factorA_index %= len(factorA)

    return subjectId_condition_map[subjectId]

if __name__ == "__main__":
    # Example subject IDs
    subjectIds = ['S1', 'S2', 'S3', 'S4', 'S5', 'S6', 'S7', 'S8']
    # Call the modified_randomize_trials function for each subject ID
    for subjectId in subjectIds:
        conditions = modified_randomize_trials(subjectId)
        print(f"Subject {subjectId}:")
        for condition in conditions:
            print(condition)
    