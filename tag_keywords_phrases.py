import os
import pke
import argparse


def dir_map(dir_path, func):
    """ recursively maps func over a directory"""
    result = {}
    for directory_name, subdirectory_list, file_list in os.walk(dir_path):
        print(f'labeling keyphrases in {directory_name}:')
        for fname in file_list:
            print(f'   keyphrases in {fname}')
            full_file_path = f'{dir_path}/{fname}'
            if os.stat(full_file_path).st_size == 0:
                print(f'        file is empty')
            else:
                result[full_file_path] = func(full_file_path)
    return result


def keyphrases_from_file(filepath):
    """
    uses pke to extract the top words/phrases
    from a given file.

    TODO: read in an entire directory and extract the top phrases
    from the entire corpuse
    """

    extractor = pke.unsupervised.TopicRank()

    # we don't stem/lemma-ize since neither NValt or Roam
    # support that yet.
    try:
        extractor.load_document(input=filepath, language="en", normalization=None)
        extractor.candidate_selection()
        extractor.candidate_weighting()

        return {
            keyphrase: score
            for keyphrase, score
            in extractor.get_n_best(n=10, stemming="true")
        }

    except ValueError as error:
        print('        error: {error}')
        return {}


def inplace_change(filename, old_string, new_string):
    # Safely write the changed content, if found in the file
    with open(filename, 'r') as f:
        s = f.read()

    s = s.replace(old_string, new_string)

    # reopen with just 'w' (write), so f.write() overwrites the file contents
    with open(filename, 'w') as f:
        print(f'        "{old_string}" -> "{new_string}"')
        f.write(s)


def tag_keyphrases(filepath):
    keyphrases = keyphrases_from_file(filepath)
    for keyphrase in keyphrases:
        inplace_change(filepath, keyphrase, f'[[{keyphrase}]]')




parser = argparse.ArgumentParser()
parser.add_argument('directory', type=str, nargs='+', help='the root directory to start in')
args = parser.parse_args()
directory = args.directory[0]

dir_map('/Users/benmathes/Dropbox/notes/', directory)
