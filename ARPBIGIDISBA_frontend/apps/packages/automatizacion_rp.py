import csv
import json


def effect_multiplier(effect):
    """Converts the effect sign to a multiplier (+ -> 1, - -> -1)."""
    return 1 if effect == "+" else -1


def evaluate_LOF(record):
    """
    For LOF conditions:
    Checks whether the string 'stop' appears in column 5 (index 4)
    (lowercased for comparison).
    """
    if "stop" in record[4].lower() or "indel" in record[4].lower():
        return 'LOF'
####
## Missing: conditionals for INDELs — these only handle SNPs ******************************************************************************************
####

    elif 'missense_variant' in record[4].lower():
        return 'SNP'
    else:
        return 'NLOF'


def evaluate_GOF(record, alleles):
    """
    For GOF/GOFO conditions:
    - Checks that 'missense_variant' appears in column 5 (index 4).
    - Extracts the numeric value from column 13 (index 12) and compares it against the keys
      in 'alleles' (converted to int).
    - If a match is found, compares the expected value (3-character string) against the
      last 3 letters of the protein annotation (assumed to be in column 10, index 9).
    Returns:
      - "double" if the allele match condition is met.
      - "simple" if a missense variant is found but the allele does not match.
      - None if no condition is met.
    """
    if "missense_variant" not in record[4].lower():
        return None
    try:
        allele_num = int(record[12])
    except ValueError:
        return None

    # Handles the case where no specific amino acids are required and the mutation is neither an indel nor a STOP codon
    if not bool(alleles) and "stop" not in record[4].lower() and "indel" not in record[4].lower():
        return "double"  # Match: any mutation is accepted

    # Iterate over keys (as strings) and compare as integers; if alleles is empty, the loop is skipped
    for key, aa in alleles.items():
        try:
            ####
            ## If the JSON key is an amino acid range, e.g. "80-93" : "Xxx", check whether the mutated amino acid falls within that range; Xxx is unused but kept to preserve JSON format
            ####
            if '-' in key:
                keys = key.split('-')
                if int(keys[0]) <= allele_num <= int(keys[1]):
                    return "double"  # Match: the double value will be used
            elif int(key) == allele_num:
                values = aa if isinstance(aa, list) else [aa]
                for value in values:
                ####
                ## Check whether the following conditional reads the correct columns and is sufficient to
                ## correctly identify the cases that appear in the Scores conditions ******************************************************************************************
                ####
                    # Compare the expected allele against the last 3 letters of the protein annotation
                    if value == 'Xxx' and "stop" not in record[4].lower() and "indel" not in record[4].lower():
                        return "double"  # Match: any mutation is accepted
                    elif record[9][-3:] == value:
                        return "double"  # Match: the double value will be used

                return "simple"
        except ValueError:
            continue

    ####
    ## Duplicate with the previous return "simple"? If one is reached, could the other also be reached?
    ####
    # return "simple"


def evaluate_condition(record, condition):
    """
    Evaluates the condition (without considering regulators) for a given record.
    Returns the score (with sign) to add for that record according to the condition.
    Returns 0 if the condition is not met.
    """
    mut_type = condition["mutation_type"]
    eff = effect_multiplier(condition["effect"])
    reg_result = {'reg_eval' : 0, 'value' : 0}

    if mut_type == "LOF":
        if evaluate_LOF == 'LOF':
            reg_result['reg_eval'] = 1
            reg_result['value'] = eff * condition["doble_value"]
        elif evaluate_LOF == 'SNP':
            reg_result['reg_eval'] = 1
            reg_result['value'] = eff * condition["simple_value"]
        else:
            reg_result['reg_eval'] = 0
            reg_result['value'] = 0

    elif mut_type == "LOFN":
        if evaluate_LOF == 'LOF':
            reg_result['reg_eval'] = 0
            reg_result['value'] = 0
        ## If it is a SNP in the mex_s pump genes, can it be directly considered active? Or does something else need to be evaluated? ******************************************************************************************
        elif evaluate_LOF == 'SNP':
            reg_result['reg_eval'] = 1
            reg_result['value'] = eff * condition["simple_value"]
        else:
            reg_result['reg_eval'] = 1
            reg_result['value'] = eff * condition["doble_value"]

    elif mut_type in ("GOF", "GOFO"):
        result = evaluate_GOF(record, condition["alleles"])
        if result is None:
            reg_result['reg_eval'] = 0
            reg_result['value'] = 0
        if result == "double":
            reg_result['reg_eval'] = 1
            reg_result['value'] = eff * condition["doble_value"]
        else:
            # For GOF, simple_value is added if the allele does not match;
            # for GOFO, nothing is added if there is no match.
            if mut_type == "GOF":
                reg_result['reg_eval'] = 1
                reg_result['value'] = eff * condition["simple_value"]
            else:
                reg_result['reg_eval'] = 0
                reg_result['value'] = 0
    else:
        print(f'Error in mut_type value for {record[7]} it is none of LOF, GOF or GOFO')

    return reg_result


def evaluate_regulators(gene, condition, records):
    """
    Evaluates the condition when 'regulators' is "YES".
    Two levels are considered:
      1. Regulator level (sub-loci): checks whether at least one record exists
         whose locus (column 8) matches a key in 'loci' and satisfies the sub-locus condition.
      2. Main level: evaluates the main condition on records where the locus (column 8)
         matches the gene.
    The combination of both levels is implemented (in a simplified form) as follows:
      - If a record in any sub-locus meets the condition (regulator_pass)
        and the main condition is also met (main_score ≠ 0), the following is added:
             main_score + (bonus from doble_value of the main condition)
      - If the first level is not met, main_score is added (or simple_value of the main condition).
      - If the regulator level is met but the main condition is not, simple_value is added.
    (The logic can be adjusted according to the interpretation of the requirements.)
    """
    # Records corresponding to the main gene
    main_records = [r for r in records if r[7] == gene]
    # Retrieve sub-loci keys
    subloci = condition.get("loci", {})
    # Collect all records belonging to any of the sub-loci
    sub_records = []
    for sub in subloci:
        sub_records.extend([r for r in records if r[7] == sub])

    # Evaluate sub-loci: check whether at least one record meets the sub-locus condition and add its value if conditions are met
    regulator_pass = False
    regulator_value = 0
    for sub in sub_records:
        if regulator_pass:
            break
    # for sub in subloci:
        sub_cond = subloci[sub[7]]
        sub_recs = [r for r in records if r[7] == sub[7]]
        for rec in sub_recs:
####
## The following condition only considers the first regulator whose effect is non-zero; if two have an effect, should both be summed? ************************************************************
####
            regulator_condition = evaluate_condition(rec, sub_cond)
            if regulator_condition['reg_eval'] != 0:
                regulator_pass = True
                regulator_value += regulator_condition['value']

                break

    # Evaluate the main condition on the gene's records
    main_score = 0

###
# If there is more than one mutation at a given locus, how should it be evaluated? There may be one with one effect and another with a different one — should both be summed? Or the strongest selected?
###
    for rec in main_records:
        main_score += evaluate_condition(rec, condition)['value']

    # Apply combined logic (as described)
    # if regulator_pass and main_score != 0:
    if regulator_pass:
        # Add both the main-level score and a "bonus" (using the double value)
        # return main_score + effect_multiplier(condition["effect"]) * condition["doble_value"]
        return main_score + regulator_value
    elif not regulator_pass:
        # If the regulator level is not met, add the main score
        # return main_score if main_score != 0 else effect_multiplier(condition["effect"]) * condition["simple_value"]
        return main_score

    ###
    # Is this case needed? *************************************************************************************************
    ###
    elif regulator_pass and main_score == 0:
        return effect_multiplier(condition["effect"]) * condition["simple_value"]
    # Caso por defecto
    return main_score


def main(scores_json, records):
    # # Load conditions from the JSON file
    # scores_json = load_scores("FuentesInformacion/SCORES_100WT.json")
    # # Load CSV records (the file is assumed to have 14 comma-separated columns)
    # records = load_csv("FuentesInformacion/PA001.snps.withoutcommon.curated")

    # Initialise score dictionary for each antibiotic
    antibiotics = ["CIP", "CAZ", "MER", "C/T", "TOB"]
    final_scores = {ab: 0 for ab in antibiotics}
    final_score_eval = {ab: [] for ab in antibiotics}

    gene_records = [r for r in records if r[7] in scores_json]
    gene_list = [r[7] for r in gene_records]

    # Iterate over each gene (locus) defined in the JSON
    for gene, conditions in scores_json.items():
        # Case where multiple main genes determine whether a score is added, not regulators
        if ',' in gene:
            genes = gene.split(',')
            gene_records_test = [r for r in records if r[7] in genes]
            gene_active = True
            score = 0

            # These will always have regulators
            for gene_record in gene_records_test:
                if evaluate_LOF(gene_record) == 'LOF':
                    gene_active = False
                    break

            if gene_active:
                for ab, cond in conditions.items():
                    for sub_gene in genes:
                        score = evaluate_regulators(sub_gene, cond, records)
                        final_scores[ab] += score
                        final_score_eval[ab].append({sub_gene: score})

        # For each antibiotic (condition) in the gene
        if gene in gene_list:
            mutations = [r for r in gene_records if r[7] == gene]
            for ab, cond in conditions.items():
                # Determine the evaluation type based on the "regulators" field
                if cond.get("regulators") == "NO":
                    # Filter records whose column 8 (index 7) matches the gene
                    for mutation in mutations:
                        score = evaluate_condition(mutation, cond)['value']
                        final_scores[ab] += score
                        final_score_eval[ab].append({gene: score})

                elif cond.get("regulators") == "YES":
                    # For conditions with regulators, evaluate using the specialised function
                    score = evaluate_regulators(gene, cond, records)
                    final_scores[ab] += score
                    final_score_eval[ab].append({gene: score})


    # Display the final score by antibiotic
    print("Total scores by ATB:")
    score_results = {}
    for ab, score in final_scores.items():
        if score <= 0.5:
            phenotype = 'S'
        elif score > 0.5 and score <= 1:
            phenotype = 'I'
        elif score > 1 :
            phenotype = 'R'
        else:
            phenotype = f'Scoring error for {ab}'
        score_results[ab] = [score, phenotype]
        print(f"{ab}: {score}")

    # Return the final score by antibiotic
    return score_results, final_score_eval