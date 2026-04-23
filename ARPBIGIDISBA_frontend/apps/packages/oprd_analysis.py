"""
Adapted OprD analysis module for use within automatizacion_rp.py.
Original script: oprD_run.py (CC BY-NC 4.0)

Detects OprD channel status (WT / mutated / deleted) in a de novo assembly
(FASTA) via sequential nucleotide + protein BLAST.
Returns a dict with the status and differences.
"""

import os
import logging
import tempfile
import shutil

from modules.blast_functions import get_differences, analize_sample
from modules.general_functions import execute_command

logger = logging.getLogger(__name__)


def run_oprd(spades_fasta: str, databases_path: str,
             blast_options: list = None,
             blastn_options: list = None) -> dict:
    """
    Detect OprD status in a de novo assembly.

    Parameters
    ----------
    spades_fasta : str
        Path to the SPAdes de novo assembly FASTA file.
    databases_path : str
        Path to the databases directory. Expected layout:
            <databases_path>/oprD/nucleotide/oprD_<name>_nucleotide.fasta
            <databases_path>/oprD/protein/oprD_<name>_protein.fasta
    blast_options : list, optional
        Options for nucleotide blastn. Defaults to ["-evalue", "1e-10"].
    blastn_options : list, optional
        Options for tblastn (protein). Defaults to ["-evalue", "1e-10"].

    Returns
    -------
    dict with keys:
        oprD        : str   – "WT", "deleted", a mutation string (e.g. "W65X,Q67X"),
                              or "unknown"
        reference   : str   – best-matching reference name (e.g. "PA14", "LESB58")
        bit_score   : float
        gaps        : int
        identity    : float
        error       : str   – non-empty if something went wrong
    """

    if blast_options is None:
        blast_options = ["-evalue", "1e-10"]
    if blastn_options is None:
        blastn_options = ["-evalue", "1e-10"]

    result = {
        "oprD": "unknown", "reference": "",
        "bit_score": -1, "gaps": -1, "identity": -1, "error": ""
    }

    if not os.path.exists(spades_fasta):
        result["error"] = f"FASTA file not found: {spades_fasta}"
        logger.error(result["error"])
        return result

    NUCLEOTIDE_PATH = os.path.join(databases_path, "oprD", "nucleotide")
    PROTEIN_PATH    = os.path.join(databases_path, "oprD", "protein")

    for path, label in [(NUCLEOTIDE_PATH, "nucleotide"), (PROTEIN_PATH, "protein")]:
        if not os.path.isdir(path):
            result["error"] = f"OprD {label} database directory not found: {path}"
            logger.error(result["error"])
            return result

    files_nucleotide = [f for f in os.listdir(NUCLEOTIDE_PATH) if f.endswith(".fasta")]
    if not files_nucleotide:
        result["error"] = "No nucleotide FASTA files found in OprD database"
        logger.error(result["error"])
        return result

    sample_name = os.path.basename(spades_fasta).replace(".fasta", "")

    max_bitscore = {"name": "deleted", "value": -1, "gaps": -1,
                    "identity": -1, "hsps": -1, "differences": []}

    tmp_dir = tempfile.mkdtemp(prefix="oprd_blast_")
    try:
        # ── Nucleotide BLAST against all OprD references ──────────────────
        for nuc_file in files_nucleotide:
            # Extract reference name: "oprD_PA14_nucleotide.fasta" → "PA14"
            suffix = nuc_file[:-len("_nucleotide.fasta")]
            name   = suffix.replace("oprD_", "")

            nuc_path   = os.path.join(NUCLEOTIDE_PATH, nuc_file)
            out_file   = os.path.join(tmp_dir, f"{sample_name}_{name}_nucleotide.json")

            cmd = (["blastn", "-query", nuc_path, "-subject", spades_fasta,
                    "-out", out_file, "-outfmt", "15"] + blast_options)
            ok = execute_command(cmd)

            if not ok:
                logger.error("blastn failed for sample %s vs %s", sample_name, name)
                continue

            res      = analize_sample(out_file, name, "nucleotide")
            bit_score = res.get("bit_score", -1)
            gaps      = res.get("gaps", -1)
            identity  = res.get("identity", -1)

            logger.debug("OprD nucleotide %s – bitscore:%.3f gaps:%s identity:%.2f",
                         name, bit_score, gaps, identity)

            if bit_score > max_bitscore["value"]:
                max_bitscore.update({"name": name, "value": bit_score,
                                     "gaps": gaps, "identity": identity,
                                     "hsps": res.get("hsps", -1),
                                     "differences": res.get("differences", [])})

        # ── Interpret nucleotide result ────────────────────────────────────
        if max_bitscore["value"] == -1:
            # No BLAST result at all
            result.update({"oprD": "unknown", "error": "No nucleotide BLAST result"})
            return result

        if max_bitscore["gaps"] == -1:
            # BLAST ran but assembly failed / no coverage
            logger.warning("OprD assembly failed on sample %s", sample_name)
            result.update({"oprD": ",".join(max_bitscore["differences"]) or "unknown",
                           "reference": max_bitscore["name"],
                           "bit_score": max_bitscore["value"],
                           "gaps": max_bitscore["gaps"],
                           "identity": max_bitscore["identity"]})
            return result

        if max_bitscore["gaps"] == 0 and max_bitscore["identity"] == 100:
            logger.info("OprD WT detected for sample %s (ref: %s)",
                        sample_name, max_bitscore["name"])
            result.update({"oprD": "WT",
                           "reference": max_bitscore["name"],
                           "bit_score": max_bitscore["value"],
                           "gaps": 0, "identity": 100.0})
            return result

        if max_bitscore["gaps"] == 0 and max_bitscore["identity"] < 100:
            # Nucleotide mismatch without gaps → go to protein level
            logger.info("OprD nucleotide mismatch for %s – running protein BLAST",
                        sample_name)
            best_ref  = max_bitscore["name"]
            prot_file = os.path.join(PROTEIN_PATH, f"oprD_{best_ref}_protein.fasta")

            if not os.path.exists(prot_file):
                logger.warning("Protein file not found for reference %s: %s",
                               best_ref, prot_file)
                # Fall through to gap-based difference detection below
            else:
                out_prot = os.path.join(tmp_dir, f"{sample_name}_{best_ref}_protein.json")
                cmd_prot = (["tblastn", "-query", prot_file, "-subject", spades_fasta,
                             "-out", out_prot, "-outfmt", "15"] + blastn_options)
                ok = execute_command(cmd_prot)

                if ok:
                    pres = analize_sample(out_prot, best_ref, "protein")
                    if pres.get("gaps") == 0 and pres.get("identity") == 100:
                        logger.info("OprD WT confirmed at protein level for %s", sample_name)
                        result.update({"oprD": "WT",
                                       "reference": pres.get("name", best_ref),
                                       "bit_score": pres.get("bit_score", -1),
                                       "gaps": 0, "identity": 100.0})
                    else:
                        diffs = pres.get("differences", [])
                        result.update({
                            "oprD": ",".join(diffs) if diffs else "mutated",
                            "reference": best_ref,
                            "bit_score": pres.get("bit_score", -1),
                            "gaps": pres.get("gaps", -1),
                            "identity": pres.get("identity", -1)})
                    return result

        # ── Gap-based differences (deletions in nucleotide) ───────────────
        diffs = get_differences(max_bitscore["hsps"], max_bitscore["name"],
                                max_bitscore["gaps"], "nucleotide")
        result.update({
            "oprD": ",".join(diffs) if diffs else "deleted",
            "reference": max_bitscore["name"],
            "bit_score": max_bitscore["value"],
            "gaps": max_bitscore["gaps"],
            "identity": max_bitscore["identity"]})

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    logger.info("OprD result for %s: %s", sample_name, result["oprD"])
    return result