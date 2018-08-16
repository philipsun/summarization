#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      sunxp
#
# Created:     31/03/2016
# Copyright:   (c) sunxp 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import re
import codecs
import sxpReadFileMan
def ProduceTuples(system_dir,model_dir):
    filelist,subdir = sxpReadFileMan.GetDir(system_dir)

def ComposeConfXML(config_file_path,system_dir,model_dir):
        system_models_tuples = ProduceTuples(system_dir,model_dir)
        with codecs.open(config_file_path, 'w', encoding='utf-8') as f:
            f.write('<ROUGE-EVAL version="1.55">')
            for task_id, (system_filename, model_filenames) in enumerate(
                    system_models_tuples, start=1):

                eval_string = get_eval_string(
                    task_id, system_id,
                    system_dir, system_filename,
                    model_dir, model_filenames)
                f.write(eval_string)
            f.write("</ROUGE-EVAL>")

def get_eval_string(
            task_id, system_id,
            system_dir, system_filename,
            model_dir, model_filenames):
        """
        ROUGE can evaluate several system summaries for a given text
        against several model summaries, i.e. there is an m-to-n
        relation between system and model summaries. The system
        summaries are listed in the <PEERS> tag and the model summaries
        in the <MODELS> tag. pyrouge currently only supports one system
        summary per text, i.e. it assumes a 1-to-n relation between
        system and model summaries.

        """
        peer_elems = "<P ID=\"{id}\">{name}</P>".format(
            id=system_id, name=system_filename)
##        peer_elems = ''
##        if system_id[0] != 'None':
##            system_filename1 = system_filename.split('.')[:-1]
##            s1 = '.'.join(system_filename1)
##        else:
##            s1 = system_filename
##
##        for eachid in system_id:
##            peer_elems += "<P ID=\"{id}\">{name}.{id1}</P>\n".format(
##                id=eachid, id1=eachid,name=s1)

        model_elems = ["<M ID=\"{id}\">{name}</M>".format(
            id=chr(65 + i), name=name)
            for i, name in enumerate(model_filenames)]

        model_elems = "\n\t\t\t".join(model_elems)
        eval_string = """
    <EVAL ID="{task_id}">
        <MODEL-ROOT>{model_root}</MODEL-ROOT>
        <PEER-ROOT>{peer_root}</PEER-ROOT>
        <INPUT-FORMAT TYPE="SEE">
        </INPUT-FORMAT>
        <PEERS>
            {peer_elems}
        </PEERS>
        <MODELS>
            {model_elems}
        </MODELS>
    </EVAL>
""".format(
            task_id=task_id,
            model_root=model_dir, model_elems=model_elems,
            peer_root=system_dir, peer_elems=peer_elems)
        return eval_string

def main():
    pass

if __name__ == '__main__':
    main()
