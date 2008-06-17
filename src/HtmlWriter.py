import Crawler.Spider as spider

_htmlHeader1 ="<html>\
<head>\
<title>"

_htmlHeader2 ="</title>\
<style type=\"text/css\">\
body{\
    font-family: sans-serif;   /*, Trebuchet MS, Lucida Sans Unicode, Arial;     Font to use */\
    font-size: 10pt;\
    font-weight: normal;\
}\
h1 {font: italic small-caps; color:#000085;}\
a{color: #000085;  text-decoration: none;}\
#content a{\
    text-decoration: none;\
    border-bottom: 1px  dotted;\
    font-variant: small-caps;\
    color: #000085;\
    font-size: 9pt;\
}\
#content ol \
{\
list-style: decimal inside url('arrow.gif')\
}\
#content li{\
padding-top: 10px;\
}\
#bibtex{ margin-left: 50%; background: #9BD1FA;}\
p{ padding-left: 2%;font-size: 8pt; white-space: pre; }\
b.rtop, b.rbottom{display:block;background: #FFF}\
b.rtop b, b.rbottom b{display:block;height: 1px;\
    overflow: hidden; background: #9BD1FA}\
b.r1{margin: 0 5px}\
b.r2{margin: 0 3px}\
b.r3{margin: 0 2px}\
b.rtop b.r4, b.rbottom b.r4{margin: 0 1px;height: 2px}\
}\
#footer{\
text-align:center;}\
#footer hr{\
border-top:1px dotted #CCCCCC;\
margin-left:10%;\
margin-right:10%;\
}\
#footer a{\
    text-decoration: underline;\
    color: #000085;\
}\
</style>\
</head>\
<body>"


_htmlPreBibtex= '<div id="bibtex">\
<b class="rtop">\
  <b class="r1"></b> <b class="r2"></b> <b class="r3"></b> <b class="r4"></b>\
</b>\
BibTex\
<p>'

_htmlPostBibtex='</p>\
<b class="rbottom">\
  <b class="r4"></b> <b class="r3"></b> <b class="r2"></b> <b class="r1"></b>\
</b>\
</div>'

_htmlFooter = '</div>\
<div id="footer">\
<hr/><p style="text-align:center">created with <a href="http://code.google.com/p/pdftoref/">PdfToRef</a></p>\
</div></body>\
</html>'

def write(entries,titles,path):
    output = open(path[:len(path)- 4]+".html","w")
    

    output.write(_htmlHeader1+"References for file: "+path + _htmlHeader2)
    
    #FIXME: Now we write in HTML ONLY the entries with a title but we must write all entries.
    dict = []
    for title in titles:
        for entry in entries:
            if entry.find(title) <> -1:
                url =  spider.googleSearch(title)
                bibtex = None #spider.getBibTex(url)
                dict.append(  (title,url,entry,bibtex) )
                break

                
                
                
    output.write("<h1>References of scientific article: <i><a href=\""+path+"\">"+path+"</a></i></h1>\n<div id=\"content\"><ol>")
    
    lenght =  len(titles)
    i=0
    while (i < lenght):
        title = dict[i][0]
        url   = dict[i][1]
        entry = dict[i][2]
        bibtex = dict[i][3]

        
        index = entry.find(title)
        printEntry = entry[:index]+ "<a href=\""+url+"\"><b>"+title+"</a></b>" + entry[index+len(title):]
        
        try:
            output.write("<li>"+printEntry + _htmlPreBibtex + bibtex+ _htmlPostBibtex +"</li>")
        except TypeError :
            output.write("<li>"+ printEntry + "</li>")
        #output.write("<b><p style=\"background-color:#ffff73\">" + dict[i][0]+  "</p></b>")
        i+=1
    output.write("</ol>")
    output.write(_htmlFooter)
    output.close()

        
