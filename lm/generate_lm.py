import os
import subprocess
import time
from argparse import ArgumentParser
from create_vocab_lexicon_file import convert_and_filter_topk

def build_lm(args, data, vocab):
    print("\nCreating ARPA file ...")
    lm_path = os.path.join(args.output_dir, "lm.arpa")
    subargs = [
            os.path.join(args.kenlm_bins, "lmplz"),
            "--order",
            str(args.arpa_order),
            "--temp_prefix",
            args.output_dir,
            "--memory",
            args.max_arpa_memory,
            "--text",
            data,
            "--arpa",
            lm_path,
            "--prune",
            *args.arpa_prune.split("|"),
        ]
    if args.discount_fallback:
        subargs += ["--discount_fallback"]
    subprocess.check_call(subargs)

    # read vocab file into space separated strng
    with open(vocab, 'r') as file:
        vocab_str = "\n".join([word for word in file.readlines()])
    
    # Filter LM using vocabulary of top-k words
    print("\nFiltering ARPA file using vocabulary of top-k words ...")
    filtered_path = os.path.join(args.output_dir, "lm_filtered.arpa")
    subprocess.run(
        [
            os.path.join(args.kenlm_bins, "filter"),
            "single",
            "model:{}".format(lm_path),
            filtered_path,
        ],
        input=vocab_str.encode("utf-8"),
        check=True,
    )

    # Quantize and produce trie binary.
    print("\nBuilding lm.binary ...")
    binary_path = os.path.join(args.output_dir, "lm.binary")
    subprocess.check_call(
        [
            os.path.join(args.kenlm_bins, "build_binary"),
            "-a",
            str(args.binary_a_bits),
            "-q",
            str(args.binary_q_bits),
            "-v",
            args.binary_type,
            filtered_path,
            binary_path,
        ]
    )

def get_parser():
    parser = ArgumentParser(
        description="Generate lm.binary and top-k vocab for DeepSpeech."
    )
    parser.add_argument(
        "--data",
        help="Path to a file.txt or file.txt.gz with sample sentences",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output_dir", help="Directory path for the output", type=str, required=True
    )
    parser.add_argument(
        "--kenlm_bins",
        help="File path to the KENLM binaries lmplz, filter and build_binary",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--top_k",
        help="Use top_k most frequent words for the vocab.txt file. These will be used to filter the ARPA file.",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--arpa_order",
        help="Order of k-grams in ARPA-file generation",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--max_arpa_memory",
        help="Maximum allowed memory usage for ARPA-file generation",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--arpa_prune",
        help="ARPA pruning parameters. Separate values with '|'",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--binary_a_bits",
        help="Build binary quantization value a in bits",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--binary_q_bits",
        help="Build binary quantization value q in bits",
        type=int,
        required=True,
    )
    parser.add_argument(
        "--binary_type",
        help="Build binary data structure type",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--discount_fallback",
        help="To try when such message is returned by kenlm: 'Could not calculate Kneser-Ney discounts [...] rerun with --discount_fallback'",
        action="store_true",
    )

    return parser

if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()

    start_time = time.time()
    convert_and_filter_topk(args.data, args.output_dir, args.top_k)
    vocab = os.path.join(args.output_dir, 'vocab-{}.txt'.format(args.top_k))
    build_lm(args, args.data, vocab)
    total_time = time.time() - start_time 
    print(f"Total time taken {total_time} sec")