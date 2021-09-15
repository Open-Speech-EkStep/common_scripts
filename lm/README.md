## To prepare the data
### Edit the parameters on congif.yaml

```
Params:
  Lang: 'en' # lang code
  File: 'toy.txt' # input file name
  Loc: '' # path to directory containing text and dict file
  Dict: 'dict.ltr.txt' # dict file containing charcter set of your language
```
Run prepare_data.py for transforming raw text data
```
$ python prepare_data.py
```
The final file will be created as {file-name}*.unique.txt

## To build lm.binary, lexicon.lst and vocab-500000.txt file from final cleaned text file

Every other parameters are set as default to make change go on file generate_lm.sh

```
$ bash generate_lm.sh -i /path/to/final/txt/file -o /folder/path/to/save/binary -k /path/to/kenlm/build/bin
```