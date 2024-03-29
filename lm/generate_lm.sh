while getopts i:o:k: flag
do
    case "${flag}" in
        i) inp_text=${OPTARG};;
        o) out_dir=${OPTARG};;
        k) kenlm_bin=${OPTARG};;
    esac
done
python generate_lm.py \
		--data $inp_text \
        --output_dir $out_dir \
		--kenlm_bins $kenlm_bin \
		--top_k 500000 \
		--arpa_order 5 \
		--max_arpa_memory "85%" \
		--arpa_prune "0|0|1" \
		--binary_a_bits 255 \
		--binary_q_bits 8 \
		--binary_type trie \
#		--discount_fallback
