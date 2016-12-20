import os, ftfy, subprocess
from glob import glob
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from cStringIO import StringIO

files = []
start_dir = os.getcwd()
pattern   = "*.pdf"
output = ""
    

def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    currpage = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
        currpage +=1

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

for dir,_,_ in os.walk(start_dir):
    files.extend(glob(os.path.join(dir,pattern))) 

print "{} files found, extraction will start".format(len(files))
print "Please note, this process may take several minutes"

for path in files:
	print 'parsing {}'.format(path)
	input_ = convert_pdf_to_txt(path).decode('utf-8')
	output = output + ftfy.fix_text(input_)
	print 'converted the file in {}'.format(path)

print 'done processing pdf files, writing output text file.'

with open('output.txt', 'w') as file_:
    file_.write(output.encode('utf-8'))

print 'translating pdf into h5 and json file'
command = 'python preprocess.py'
return_v = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
print return_v
print "done"