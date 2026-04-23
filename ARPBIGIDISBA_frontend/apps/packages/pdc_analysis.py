"""
Adapted PDC analysis module for use within automatizacion_rp.py.
Original script: PDC_run.py (CC BY-NC 4.0)

Detects PDC beta-lactamase variant in a de novo assembly (FASTA) via BLAST.
Returns a dict with the detected PDC type and differences vs PDC-1.
"""

import os
import re
import logging
import tempfile
import shutil
from typing import List, Optional, Tuple

from modules.blast_functions import analize_sample, run_blast, get_differences
from modules.general_functions import execute_command

logger = logging.getLogger(__name__)

# ── Deletion merge helpers (unchanged from PDC_run.py) ────────────────────────

def _parse_del(token: str) -> Optional[Tuple[int, int, str, str]]:
    s = token.strip()
    m1 = re.fullmatch(r'([A-Z])(\d+)-', s)
    if m1:
        aa, p = m1.group(1), int(m1.group(2))
        return (p, p, aa, aa)
    m2 = re.fullmatch(r'([A-Z])(\d+)-([A-Z])(\d+)del', s)
    if m2:
        aa1, p1, aa2, p2 = m2.group(1), int(m2.group(2)), m2.group(3), int(m2.group(4))
        if p2 < p1:
            p1, p2, aa1, aa2 = p2, p1, aa2, aa1
        return (p1, p2, aa1, aa2)
    return None

def _fmt_del(p1: int, p2: int, aa1: str, aa2: str) -> str:
    return f"{aa1}{p1}del" if p1 == p2 else f"{aa1}{p1}-{aa2}{p2}del"

def _merge_deletions(items: List[str]) -> List[str]:
    out = items[:]
    run_active = False
    run_start_idx = run_p1 = run_p2 = None
    run_aa1 = run_aa2 = None
    for i, tok in enumerate(items):
        parsed = _parse_del(tok)
        if parsed:
            p1, p2, aa1, aa2 = parsed
            if not run_active:
                run_active, run_start_idx = True, i
                run_p1, run_p2, run_aa1, run_aa2 = p1, p2, aa1, aa2
            else:
                if p1 <= run_p2 + 1:
                    if p2 > run_p2:
                        run_p2, run_aa2 = p2, aa2
                    out[i] = None
                else:
                    out[run_start_idx] = _fmt_del(run_p1, run_p2, run_aa1, run_aa2)
                    run_start_idx, run_p1, run_p2, run_aa1, run_aa2 = i, p1, p2, aa1, aa2
        else:
            if run_active:
                out[run_start_idx] = _fmt_del(run_p1, run_p2, run_aa1, run_aa2)
                run_active = False
    if run_active:
        out[run_start_idx] = _fmt_del(run_p1, run_p2, run_aa1, run_aa2)
    return [t for t in out if t not in (None, "")]


# ── Main function ──────────────────────────────────────────────────────────────

def run_pdc(spades_fasta: str, databases_path: str, tblastn_options: list = None) -> dict:
    """
    Detect PDC beta-lactamase variant in a de novo assembly.

    Parameters
    ----------
    spades_fasta : str
        Path to the SPAdes de novo assembly FASTA file.
    databases_path : str
        Path to the databases directory. Expected layout:
            <databases_path>/PDC/PDC-1nt.fasta
            <databases_path>/PDC/PDCs_seq/*.fasta   (protein sequences)
    tblastn_options : list, optional
        Extra BLAST options (e.g. ["-evalue", "1e-6"]). Defaults to ["-evalue", "1e-10"].

    Returns
    -------
    dict with keys:
        pdc         : str   – PDC variant name, e.g. "PDC-35", "new type",
                              "Non-Functional(...)", "deleted", or "unknown"
        reference   : str   – full reference string, e.g. "PDC-35 (WP_063864573.1)"
        differences : list  – amino-acid differences vs PDC-1, e.g. ["G27D", "A97V"]
        bit_score   : float
        gaps        : int
        identity    : float
        error       : str   – non-empty string if something went wrong
    """

    if tblastn_options is None:
        tblastn_options = ["-evalue", "1e-10"]

    result = {
        "pdc": "unknown", "reference": "", "differences": [],
        "bit_score": -1, "gaps": -1, "identity": -1, "error": ""
    }

    if not os.path.exists(spades_fasta):
        result["error"] = f"FASTA file not found: {spades_fasta}"
        logger.error(result["error"])
        return result

    PDC_DATABASE_PATH = os.path.join(databases_path, "PDC", "PDCs_seq")
    PDC1NT_PATH       = os.path.join(databases_path, "PDC", "PDC-1nt.fasta")

    if not os.path.isdir(PDC_DATABASE_PATH):
        result["error"] = f"PDC database directory not found: {PDC_DATABASE_PATH}"
        logger.error(result["error"])
        return result
    if not os.path.exists(PDC1NT_PATH):
        result["error"] = f"PDC-1 nucleotide reference not found: {PDC1NT_PATH}"
        logger.error(result["error"])
        return result

    # Build sorted list of protein FASTA files
    pattern = r"(PDC-\d+)"
    files_protein = sorted(
        [f for f in os.listdir(PDC_DATABASE_PATH) if f.endswith(".fasta")],
        key=lambda f: int(re.search(pattern, f).group(1).split("-")[1])
                      if re.search(pattern, f) else 0
    )
    files = []
    for fname in files_protein:
        m = re.search(pattern, fname)
        if m:
            files.append((fname, m.group(0)))

    sample_name = os.path.basename(spades_fasta).replace(".fasta", "")

    # Use a temporary directory for BLAST outputs
    tmp_dir = tempfile.mkdtemp(prefix="pdc_blast_")
    try:
        # ── Step 1: nucleotide pre-filter (frameshift detection) ──────────
        nt_output = os.path.join(tmp_dir, f"{sample_name}_PDC-1nt.json")
        cmd_nt = ["blastn", "-query", PDC1NT_PATH, "-subject", spades_fasta,
                  "-out", nt_output, "-outfmt", "15", "-evalue", "10"]
        nt_ok = execute_command(cmd_nt)

        if nt_ok and os.path.exists(nt_output):
            nt_results = analize_sample(nt_output, "PDC-1nt", "nucleotide", cover_limit=0)
            differences_nt = nt_results.get("differences", [])
            if isinstance(differences_nt, str):
                differences_nt = [differences_nt]

            non_functional = False
            for diff in differences_nt:
                if "ins" in diff:
                    m = re.search(r'ins(\d+)', diff)
                    if m and int(m.group(1)) % 3 != 0:
                        non_functional = True
                        break
                elif "del" in diff:
                    m = re.search(r'del(\d+)', diff)
                    if m and int(m.group(1)) % 3 != 0:
                        non_functional = True
                        break

            if non_functional:
                logger.info("PDC Non-Functional detected in sample %s", sample_name)
                result.update({
                    "pdc": f"Non-Functional({','.join(differences_nt)})",
                    "reference": "Non-Functional",
                    "differences": differences_nt,
                    "bit_score": nt_results.get("bit_score", -1),
                    "gaps": nt_results.get("gaps", -1),
                    "identity": nt_results.get("identity", -1),
                })
                return result

        # ── Step 2: protein BLAST against all PDC variants ────────────────
        PDC1 = {}
        max_bitscore = {"name": "deleted", "value": -1, "gaps": -1,
                        "identity": -1, "differences": [], "path": ""}

        for index, (fname, pdc_name) in enumerate(files):
            fpath = os.path.join(PDC_DATABASE_PATH, fname)
            out_file = os.path.join(tmp_dir, f"{sample_name}_{pdc_name}.json")

            cmd_prot = (["tblastn", "-query", fpath, "-subject", spades_fasta,
                         "-out", out_file, "-outfmt", "15"] + tblastn_options)
            ok = execute_command(cmd_prot)
            if not ok:
                logger.error("BLAST failed for %s vs %s", sample_name, pdc_name)
                continue

            res = analize_sample(out_file, pdc_name, "protein")
            bit_score = res.get("bit_score", -1)
            gaps      = res.get("gaps", -1)
            identity  = res.get("identity", -1)

            logger.debug("(%s/%s) %s – gaps:%s identity:%.2f bitscore:%.3f",
                         index + 1, len(files), pdc_name, gaps, identity, bit_score)

            # Track PDC-1 specifically for difference reporting
            if pdc_name == "PDC-1":
                PDC1 = {"differences": res.get("differences", []),
                        "bit_score": bit_score, "gaps": gaps, "identity": identity}

            if bit_score >= max_bitscore["value"]:
                with open(fpath) as fh:
                    header = fh.readline()
                full_name = "{} ({})".format(pdc_name, header.split(" ")[0][1:])
                max_bitscore.update({"name": full_name, "path": fpath,
                                     "value": bit_score, "gaps": gaps,
                                     "identity": identity,
                                     "differences": res.get("differences", [])})

            if gaps == 0 and identity == 100:
                logger.info("Exact PDC match: %s for sample %s", pdc_name, sample_name)
                break

        # ── Step 3: interpret result ───────────────────────────────────────
        pdc1_diffs  = _merge_deletions(PDC1.get("differences", []))
        pdc1_merged = ",".join(pdc1_diffs)

        if max_bitscore["value"] == -1:
            result.update({"pdc": "unknown", "reference": "unknown",
                           "error": "No BLAST result obtained"})

        elif max_bitscore["gaps"] == 0 and max_bitscore["identity"] == 100:
            pdc_name = "deleted" if pdc1_merged == "deleted" else max_bitscore["name"]
            result.update({"pdc": pdc_name, "reference": max_bitscore["name"],
                           "differences": pdc1_diffs,
                           "bit_score": max_bitscore["value"],
                           "gaps": max_bitscore["gaps"],
                           "identity": max_bitscore["identity"]})

        else:
            if pdc1_merged == "deleted":
                result.update({"pdc": "deleted", "reference": "deleted",
                               "differences": pdc1_diffs,
                               "bit_score": max_bitscore["value"],
                               "gaps": max_bitscore["gaps"],
                               "identity": max_bitscore["identity"]})
            else:
                # Check for stop codon → Non-Functional
                added = False
                for diff in pdc1_diffs:
                    if diff.endswith("X"):
                        result.update({
                            "pdc": f"Non-Functional({pdc1_merged})",
                            "reference": "Non-Functional",
                            "differences": pdc1_diffs,
                            "bit_score": max_bitscore["value"],
                            "gaps": max_bitscore["gaps"],
                            "identity": max_bitscore["identity"]})
                        added = True
                        break
                if not added:
                    result.update({"pdc": "new type",
                                   "reference": "new type",
                                   "differences": pdc1_diffs,
                                   "bit_score": max_bitscore["value"],
                                   "gaps": max_bitscore["gaps"],
                                   "identity": max_bitscore["identity"]})

    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    logger.info("PDC result for %s: %s", sample_name, result["pdc"])
    return result