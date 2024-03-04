from os import listdir
from pathlib import Path
import subprocess
import pypandoc 
import shutil
import re
import traceback

{'pdf', 'docx', 'doc', 'txt', 'rtf'}

def join_paragraphs_and_clean(lines):
    return re.sub(r'\\', '', re.sub(r"(?<!\n)\n(?!\n)", " ", lines))

if __name__ == "__main__":
    # filetypes = set([listdir(f"./files/{i}")[0].split('.')[-1] for i in listdir("./files")])

    
    for i in [i for i in listdir("./rp files")]:
        print(i)
        
        if len(listdir(f"./rp files/{i}")) == 0:
            print(i, "no such file")
            continue
        
        filename = "./rp files/" + str(i) + '/' + listdir(f"./rp files/{i}")[0] 
        
        filetype = filename.split('.')[-1]
        
        path = Path('./txt/' + filetype)
        path.mkdir(parents=True, exist_ok=True)
        
        try:
            # output = pypandoc.convert_file(filename, 'markdown', outputfile="./txt/" + filetype + '/' + ''.join(listdir(f"./files/{i}")[0].split('.')[:-1]) + ".txt")
            path = Path('./tmp')
            path.mkdir(parents=True, exist_ok=True)
            # output = pypandoc.convert_file(filename, 'markdown', outputfile="./txt/" + filetype + '/' + f'{i}_'.join(listdir(f"./files/{i}")[0].split('.')[:-1]) + ".txt")
            output = pypandoc.convert_file(filename, 'markdown', outputfile="./tmp/tmp.txt")
            
            with open("./tmp/tmp.txt", 'r') as r:
                with open("./txt/" + filetype + '/' + f'{i}_' + ''.join(listdir(f"./rp files/{i}")[0].split('.')[:-1]) + ".txt", 'w') as w:
                    w.write(join_paragraphs_and_clean(r.read()))
        
        
        
        except RuntimeError as er:
            if filetype == 'doc':
                path = Path('./tmp')
                path.mkdir(parents=True, exist_ok=True)
                subprocess.call(['soffice', '--headless', '--convert-to', 'docx', '--outdir', './tmp', filename])
                # output = pypandoc.convert_file("./tmp/" + listdir(f"./tmp")[0], 'markdown', outputfile="./txt/" + filetype + '/' + f'{i}_' + ''.join(listdir(f"./files/{i}")[0].split('.')[:-1]) + ".txt")
                output = pypandoc.convert_file("./tmp/" + listdir(f"./tmp")[0], 'markdown', outputfile="./tmp/tmp.txt")
                with open("./tmp/tmp.txt", 'r') as r:
                    with open("./txt/" + filetype + '/' + f'{i}_' + ''.join(listdir(f"./rp files/{i}")[0].split('.')[:-1]) + ".txt", 'w') as w:
                        w.write(join_paragraphs_and_clean(r.read()))
            elif filetype == 'txt':
                shutil.copyfile(filename, "./txt/txt/" + str(i) + '_' + filename.split('/')[-1])
            elif filetype == 'pdf':
                shutil.copyfile(filename, "./txt/pdf/" + str(i) + '_' + filename.split('/')[-1])
            else:
                print(f"You forgot this filetype, dummy: {filetype}")
        except IndexError as er:
            print(f"IndexError: list index out of range for file '{filename}'")
            traceback.print_exc()
        finally:
            shutil.rmtree('./tmp')
        