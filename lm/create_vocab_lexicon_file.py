import argparse
import itertools
from collections import Counter
import os
from tqdm import tqdm
import time

def convert_and_filter_topk(fpath, dst, n) :
    print("\nReading input file...")
    with open(fpath, encoding="utf-8") as file_in:
        lines = file_in.readlines()
    print("\nCompleted reading")
    
    print(f"\nThere are {len(lines)} lines in input file.")

    print("\nCalculating number of words")
    words = list(itertools.chain(*[line.split() for line in tqdm(lines)]))
    

    print("\nCounting Word Frequencies ")
    counter = Counter(words)
    total_words = sum(counter.values())

    # Save top-k words
    print(f"\nSaving top {n} words ...")
    top_counter = counter.most_common(n)

    print(f"\nWriting vocab file...")
    vocab_str = "\n".join(word for word, count in top_counter)
    vocab_path = "vocab-{}.txt".format(n)
    vocab_path = os.path.join(dst, vocab_path)

    
    with open(vocab_path, "w+") as file:
        file.write(vocab_str)    
    print("\nCompleted writing")

    print(f"\nWriting lexicon file...")
    lexicon_path = os.path.join(dst, 'lexicon.lst')

    def help(word):
        return word + "\t" + " ".join(list(word.replace("/n", "").replace(" ", "|").strip())) + " |"

    lexicon_str = "\n".join(help(word) for word, count in top_counter)
    with open(lexicon_path, 'w+') as file:
        file.write(lexicon_str)
    print(f"\nCompleted writing")

    print(f"\nTotal words {total_words} \n Distinct words {len(counter)}")

    # print statistics
    top_words_sum = sum(count for word, count in top_counter)
    word_fraction = (top_words_sum / total_words) * 100
    print(
        "  Your top-{} words are {:.4f} percent of all words".format(
            n, word_fraction
        )
    )

    print('  Your most common word "{}" occurred {} times'.format(*top_counter[0]))

    last_word, last_count = top_counter[-1]

    print(
        '  The least common word in your top-k is "{}" with {} times'.format(
            last_word, last_count
        )
    )

    for i, (w, c) in enumerate(reversed(top_counter)):
        if c > last_count:
            print(
                '  The first word with {} occurrences is "{}" at place {}'.format(
                    c, w, len(top_counter) - 1 - i
                )
            )
            break

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(
        description="Generate vocab-{top-k}.txt using input text file"
    )
    parser.add_argument(
        "-i",
        "--input_txt",
        help="Path to a file.txt or file.txt.gz with sample sentences",
        type=str,
        required=True,
    )
    parser.add_argument(
        "-o",
        "--output_dir", 
        help="Directory path for the output", 
        type=str, 
        required=True
    )
    parser.add_argument(
        "-n",
        "--top_k",
        help="Use top_k most frequent words for the vocab.txt file. These will be used to filter the ARPA file.",
        type=int,
        required=True,
    )

    args = parser.parse_args()

    start_time = time.time()
    convert_and_filter_topk(args.input_txt, args.output_dir, args.top_k)
    total_time = time.time() - start_time
    print(f"Total time taken {total_time} sec")

    pass