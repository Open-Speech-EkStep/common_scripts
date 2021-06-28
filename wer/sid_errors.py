from components import compute_wer
import argparse
import pandas as pd


def hypo_and_ref_text(hypo_path, ref_path):

    with open(hypo_path, encoding='utf-8') as f:
        hypo = f.read().splitlines()

    hypo_text = [' '.join(s.split(' ')[:-1]) for s in hypo]

    with open(ref_path, encoding='utf-8')as f:
        ref = f.read().splitlines()

    ref_text = [' '.join(s.split(' ')[:-1]) for s in ref]
    return hypo_text, ref_text


def wer_components(hypo_path, ref_path, save=False, csv_name=None):

    hypo, ref = hypo_and_ref_text(hypo_path, ref_path)

    substitutions = []
    insertions = []
    deletions = []

    for h, r in zip(hypo, ref):
        substitutions.append(compute_wer(predictions=[h], references=[r])['substitutions'])
        insertions.append(compute_wer(predictions=[h], references=[r])['insertions'])
        deletions.append(compute_wer(predictions=[h], references=[r])['deletions'])
    print(f'Number of substitutions: {sum(substitutions)}')
    print(f'Number of deletions: {sum(deletions)}')
    print(f'Number of insertions: {sum(insertions)}')

    if save:
        df = pd.DataFrame({'hypo': hypo, 'ref': ref, 'substitutions': substitutions, 'insertions': insertions,
                           'deletions': deletions})
        df.to_csv(csv_name, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get WER components')
    parser.add_argument('-o', '--ref', required=True, help='ref text')
    parser.add_argument('-p', '--hypo', required=True, help='hypo text')
    parser.add_argument('-s', '--save-output', help='save output file', type=bool)
    parser.add_argument('-n', '--name', help='save output file name', type=str)
    arguments = parser.parse_args()
    wer_components(arguments.hypo, arguments.ref, arguments.save_output, arguments.name)