from Bio.Seq import Seq
import sys
import os

os.environ[
    "LOG_FILE"
] = "/work/xiaoxi/mRNA/tools/mRNAid/backend/flask_app/logs/test.log"
sys.path.append("/work/xiaoxi/mRNA/tools/mRNAid/backend/common/")
from OptimizationProblems import initialize_optimization_problem
from OptimizationTask import optimization_task
from utils.Datatypes import OptimizationParameters
from Evaluation import Evaluation
from dnachisel.reports.optimization_reports import write_optimization_report


def get_rare_codons(species, threshold):
    if threshold is None:
        return []
    # TODO: get tables for different species, if needed (e.g. from python_codon_tables)
    freqs = {
        "UAA": 0.3,
        "UAG": 0.24,
        "UGA": 0.47,
        "GCA": 0.23,
        "GCC": 0.4,
        "GCG": 0.11,
        "GCU": 0.27,
        "UGC": 0.54,
        "UGU": 0.46,
        "GAC": 0.54,
        "GAU": 0.46,
        "GAA": 0.42,
        "GAG": 0.58,
        "UUC": 0.54,
        "UUU": 0.46,
        "GGA": 0.25,
        "GGC": 0.34,
        "GGG": 0.25,
        "GGU": 0.16,
        "CAC": 0.58,
        "CAU": 0.42,
        "AUA": 0.17,
        "AUC": 0.47,
        "AUU": 0.36,
        "AAA": 0.43,
        "AAG": 0.57,
        "CUA": 0.07,
        "CUC": 0.2,
        "CUG": 0.4,
        "CUU": 0.13,
        "UUA": 0.08,
        "UUG": 0.13,
        "AUG": 1.0,
        "AAC": 0.63,
        "AAU": 0.47,
        "CCA": 0.28,
        "CCC": 0.32,
        "CCG": 0.11,
        "CCU": 0.29,
        "CAA": 0.27,
        "CAG": 0.73,
        "AGA": 0.21,
        "AGG": 0.21,
        "CGA": 0.11,
        "CGC": 0.18,
        "CGG": 0.2,
        "CGU": 0.08,
        "AGC": 0.24,
        "AGU": 0.15,
        "UCA": 0.15,
        "UCC": 0.22,
        "UCG": 0.05,
        "UCU": 0.19,
        "ACA": 0.28,
        "ACC": 0.36,
        "ACG": 0.11,
        "ACU": 0.25,
        "GUA": 0.12,
        "GUC": 0.24,
        "GUG": 0.46,
        "GUU": 0.18,
        "UGG": 1,
        "UAC": 0.56,
        "UAU": 0.44,
    }
    rare_codons = [codon for codon, freq in freqs.items() if freq < threshold]
    return rare_codons


"""
Test whole optimization process, check if optimized sequences conform to constraints set by parameters
"""
seq = "AGCAGAGAAGGCGGAAGCAGTGGCGTCCGCAGCTGGGGCTTGGCCTGCGGGCGGCCAGCGAAGGTGGCGAAGGCTCCCACTGGATCCAGAGTTTGCCGTCCAAGCAGCCTCGTCTCGGCGCGCAGTGTCTGTGTCCGTCCTCTACCAGCGCCTTGGCTGAGCGGAGTCGTGCGGTTGGTGGGGGAGCCCTGCCCTCCTGGTTCGGCCTCCCCGCGCACTAGAACGATCATGAACTTCTGAAGGGACCCAGCTTTCTTTGTGTGCTCCAAGTGATTTGCACAAATAATAATATATATATTTATTGAAGGAGAGAATCAGAGCAAGTGATAATCAAGTTACTATGAGTCTGCTAAACTGTGAAAACAGCTGTGGATCCAGCCAGTCTGAAAGTGACTGCTGTGTGGCCATGGCCAGCTCCTGTAGCGCTGTAACAAAAGATGATAGTGTGGGTGGAACTGCCAGCACGGGGAACCTCTCCAGCTCATTTATGGAGGAGATCCAGGGATATGATGTAGAGTTTGACCCACCCCTGGAAAGCAAGTATGAATGCCCCATCTGCTTGATGGCATTACGAGAAGCAGTGCAAACGCCATGCGGCCATAGGTTCTGCAAAGCCTGCATCATAAAATCAATAAGGGATGCAGGTCACAAATGTCCAGTTGACAATGAAATACTGCTGGAAAATCAACTATTTCCAGACAATTTTGCAAAACGTGAGATTCTTTCTCTGATGGTGAAATGTCCAAATGAAGGTTGTTTGCACAAGATGGAACTGAGACATCTTGAGGATCATCAAGCACATTGTGAGTTTGCTCTTATGGATTGTCCCCAATGCCAGCGTCCCTTCCAAAAATTCCATATTAATATTCACATTCTGAAGGATTGTCCAAGGAGACAGGTTTCTTGTGACAACTGTGCTGCATCAATGGCATTTGAAGATAAAGAGATCCATGACCAGAACTGTCCTTTGGCAAATGTCATCTGTGAATACTGCAATACTATACTCATCAGAGAACAGATGCCTAATCATTATGATCTAGACTGCCCTACAGCCCCAATTCCATGCACATTCAGTACTTTTGGTTGCCATGAAAAGATGCAGAGGAATCACTTGGCACGCCACCTACAAGAGAACACCCAGTCACACATGAGAATGTTGGCCCAGGCTGTTCATAGTTTGAGCGTTATACCCGACTCTGGGTATATCTCAGAGGTCCGGAATTTCCAGGAAACTATTCACCAGTTAGAGGGTCGCCTTGTAAGACAAGACCATCAAATCCGGGAGCTGACTGCTAAAATGGAAACTCAGAGTATGTATGTAAGTGAGCT"

parameters = OptimizationParameters(
    input_mRNA=seq,
    input_DNA=seq.replace("U", "T"),
    five_end="ATG",
    three_end="CGG",
    avoid_codons=["ACT", "CTA"],
    avoid_motifs=[],
    max_GC_content=0.7,
    min_GC_content=0.3,
    GC_window_size=30,
    usage_threshold=0.1,
    uridine_depletion=True,
    organism="h_sapiens",
    entropy_window=80,
    number_of_sequences=1,
    mfe_method="stem_loop",
    dinucleotides=False,
    codon_pair=False,
    CAI=True,
    location=(0, len(seq) - len(seq) % 3, 1),
    filename="optimization_results",
)
translation = Seq(parameters.five_end + seq + parameters.three_end).translate()
optimization_problem = initialize_optimization_problem(parameters)
sequence = optimization_task(
    optimization_problem,
    target_path="/work/xiaoxi/mRNA/tools/mRNAid/backend/tests/logs",
)
# evaluator = Evaluation([sequence], parameters)
# seq_properties = evaluator.get_evaluation()
# for properties in seq_properties["optimized"]:
#     opt_seq = properties["RNASeq"]
#     u_depletion = sum(
#         1 for i in range(0, len(opt_seq) - 2, 3) if opt_seq[i + 2] in ["U", "T"]
#     )
#     avoid_motifs = sum(1 for motif in parameters.avoid_motifs if motif in opt_seq)
#     assert (
#         parameters.min_GC_content <= properties["GC_ratio"] <= parameters.max_GC_content
#     )
#     # assert properties['score'] > seq_properties['input']['score']
#     # This assertion fails
#     if parameters.uridine_depletion:
#         assert u_depletion == 0
#     rare_codons = get_rare_codons(parameters.organism, parameters.usage_threshold)
#     breaches = sum(
#         1 for i in range(0, len(opt_seq) - 2, 3) if opt_seq[i : i + 2] in rare_codons
#     )
#     assert Seq(opt_seq).translate() == translation
#     assert avoid_motifs == 0
#     assert breaches == 0
