import sys
import argparse
import tempfile
import time
import secrets
from os import remove
from os.path import join

sys.path.append("/home/llawrence/misc-python-utils/")
sys.path.append("/home/lclawrence_umass_edu/misc-python-utils/")
from write_str_to_fpath import write_str_to_fpath
from fpath_to_str import fpath_to_str
from query_gpt import get_chat_completion
from submit_cmd import submit_cmd
from write_str_to_fpath_w_diff import write_str_to_fpath_w_diff

# 
update_cache = False

def spellcheck_default(fpath: str) -> str:
    global update_cache

    fstr      = fpath_to_str(fpath)
    num_lines = len(fstr.split('\n'))
    fstr      = '\n'.join([f"{i}: {line}" for i, line in enumerate(fstr.split('\n')) if i != num_lines - 1 or line != ''])
    user_prompt = f'''You are document reviewer looking for the following types of mistakes:

Misspellings
Lack of punctuation, eg. missing periods and commas
Incorrect tenses of verbs
Lack of capitalization, eg. not capitalizing the first letter of a sentence

Here is a text file containing some text. Propose spellchecks and grammar edits to this file. 

{fstr}

For each proposed edit indicate the line number and the correction you wish to make. Do include lines which don't need correction. The line number is already indicated within the file. Do not include a correction with an empty line which is the last line of the file, namely don't include "{{\'line_number\': {num_lines - 1}, \'correction\': \'\'}}. PLEASE DO NOT INCLUDE LINES WITH NO CORRECTION, JUST LEAVE ABSENT FROM THE RESPONSE. DO NOT INCLUDE EXPLANATIONS, JUST UT THE REWRITE".
    '''
    json_schema = {
      "name"  : "response",
      "strict": True,
      "schema": {
        "type": "object",
        "properties": {
          "edits": {
            "type" : "array",
            "items": {
              "type"        : "object",
              "properties"  : {
                "line_number": {
                  "type": "number"
                },
                "correction": {
                  "type": "string"
                }
              },
              "required"            : ["line_number", "correction"],
              "additionalProperties": False
            }
          }
        },
        "required"            : ["edits"],
        "additionalProperties": False
      }
    }

    # 
    output = get_chat_completion(user_prompt=user_prompt, json_schema=json_schema, update_cache=update_cache)
    return output

def fpath_to_corrections(fpath: str) -> str:
    
    # 
    if fpath.endswith('.md'):
        return spellcheck_default(fpath)

    raise NotImplementedError()

def fpath_to_spellcheck_diff(fpath: str) -> None:
    # 
    fstr      = fpath_to_str(fpath)
    fstr_list = fstr.split('\n')

    # 
    correction_list    = fpath_to_corrections(fpath)['edits']
    for v in correction_list:
        fstr_list[v['line_number']] = v['correction']
    fstr = '\n'.join(fstr_list)
    
    #
    write_str_to_fpath_w_diff(fstr, fpath, diff_name='gpt-rewrite')

    # 
#     tmp_fname = join('/tmp', f"spellcheck-{secrets.token_hex(8)}.txt")
#     write_str_to_fpath(fstr, tmp_fname)
#     
#     # 
#     cmd = f"touch /tmp/empty && git merge-file -L {fpath} -L B -L {tmp_fname} -p {fpath} /tmp/empty {tmp_fname}"
#     out = submit_cmd(cmd, return_output=True)
#     out = '\n'.join(out)
#     out = out.replace(tmp_fname, 'gpt rewrite')
#     
#     # 
#     remove(tmp_fname)
# 
#     #
#     write_str_to_fpath(out, fpath)

def parse_args():
    parser = argparse.ArgumentParser()

    #
    parser.add_argument('--file_path', required=True, type=str)

    #
    args, _ = parser.parse_known_args()
    return vars(args)

def test():
    fpath = '/home/llawrence/.config/nvim/python/spellcheck_test.md'
    print(fpath_to_corrections(fpath))

if __name__ == "__main__":

    #
    args = parse_args()
    fpath_to_spellcheck_diff(args['file_path'])
