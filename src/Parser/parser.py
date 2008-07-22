import getopt
import sys

def parse(argv):
    '''
    It is the function of the application that parses the arguments and flags passed 
    through command line.
    
    @param arg: the arguments in command line
    @return: the file or directory path, the flag to do on a dir or on a file, the bibtex flag, the url flag
    '''
    
    content = ''
    flag= 'None'
    url = False
    bibtex = False
    downloadPdf = False
    
    try:
        opts, args = getopt.getopt(argv[1:], "hf:d:ubp", ["help","file=","dir=","url","bibtex","pdf"])
    except getopt.GetoptError, err:
         return (content,flag,url,bibtex)

    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-f", "--file"):
            content = a
            flag = "file"
        elif o in ("-d", "--dir"):
            content = a
            flag = "dir"
        elif o in ("-u", "--url"):
            url=True
        elif o in ("-b", "--bibtex"):
            bibtex=True
            url=True
        elif o in ("-p", "--pdf"):
            downloadPdf=True
            url=True
        else:
            continue
    
    return (content,flag,url,bibtex,downloadPdf)

def usage():
    print "     Usage: \n\n \
    -h            --help              This help Command \n \
    -f filepath   --file=filepath     Run on a file \n \
    -d directory  --dir=directory     Run into a directory \n \
    -u            --url               Get the title url \n \
    -b            --bibtex            Get the bibtex article \n \n \
    -p            --pdf               Download the article cited in the references as pdf \n \n \
    Examples:\n\n \
    pdftoref -b -u -f ~/file.pdf\n \
    pdftoref --url --bibtex --file=~/file.pdf\n \
    pdftoref -d /home/user/articles "
    
def listPdfFiles(dir):
    '''
    It is the function of the application that get all pdf files in a directory
    simple seeing if at the end of the files there is .pdf.
    
    @param dir: the dir in which search pdf files
    @return: a list of pdf files
    '''
    import os
    files = os.listdir(dir)
    pdfFiles = []
    for each in files:
        if each[len(each)-4:] == ".pdf":
            pdfFiles.append(each)
    return pdfFiles
        
