import subprocess
import re

def pdffonts(infile):
    """
    Wraps command line utility pdffonts
    """
    import os.path as osp

    cmd = 'C:\\tools\\xpdf\\pdffonts.exe'
    if not osp.exists(cmd):
        raise RuntimeError('System command not found: %s' % cmd)

    if not osp.exists(infile):
        raise RuntimeError('Provided input file not found: %s' % infile)

    def _extract(row):
        """Extracts the right hand value from a : delimited row"""
        return row.split(':', 1)[1].strip()

    def findspaceposition(cmd_out_list):
        spaceposition = []
        if len(cmd_out_list) > 2:
            if cmd_out_list[1][:3] == b'---':
                spaceposition = [m.start() for m in re.finditer(b' ', cmd_out_list[1])]
                spaceposition.insert(0,0) #add 0 as beginning of a string
                spaceposition.append(len(cmd_out_list[1])) # add end string position
        return spaceposition

    def extractrow (row, spaceposition):
        resultline = []
        if len(spaceposition) > 1:
            resultline = [(row[spaceposition[i]:spaceposition[i + 1]]).rstrip() for i in range(0, len(spaceposition) - 1)]
        return resultline

    p = subprocess.run([cmd, infile], shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    cmd_output = p.stdout
    result = []
    cmd_out_list = cmd_output.splitlines()
    [print(line) for line in cmd_out_list] #pretty printing

    if len(cmd_out_list) > 2:
        spaceposition = findspaceposition(cmd_out_list)
        if len(spaceposition) > 2:
            for row in cmd_out_list:
                result.append(extractrow(row,spaceposition))
        del result[1] #delete  line with "---- " part
    return result

#code testing
#print(pdffonts("C:\\temp2\\Certificate.pdf"))


