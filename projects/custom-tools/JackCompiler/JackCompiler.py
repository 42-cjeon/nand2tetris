import sys
import os
import re

from lib.Errors import ParseError
from lib.CompileEngine import CompileEngine

if len(sys.argv) != 2:
    print('[Invalid args] usage: python JackCompiler.py <input file/folder path>')
    exit(1)

input_path = sys.argv[1]

if os.path.isfile(input_path):
    input_files = [input_path]

elif os.path.isdir(input_path):
    input_files = [os.path.join(input_path, jack_file) for jack_file in os.listdir(input_path) if re.match(r".*[.]jack$", jack_file)]
else:
    print('[!] file or folder not found')
    exit(1)

for input_file_path in input_files:
    compile_engine = CompileEngine(input_file_path)
    try:
        compile_engine.compile_class()
    except ParseError as e:
        print(f"File {e.file_name}, LINE {e.line}\n{e.message}")
    finally:
        compile_engine.close()