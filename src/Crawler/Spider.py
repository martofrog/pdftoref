from SOAPpy import SOAPProxy
from SOAPpy import Types
import urllib2
import urllib
import socket
import re

# CONSTANTS
_url = 'http://api.google.com/search/beta2'
_namespace = 'urn:GoogleSearch'


# need to marshall into SOAP types
SOAP_FALSE = Types.booleanType(0)
SOAP_TRUE = Types.booleanType(1)

# Google search options
_license_key = 'Cu7YX75QFHLS3WD/7/4CO+GsI/jC69eb' 
_query = ""
_start = 0
_maxResults = 3
_filter = SOAP_FALSE
_restrict = ''
_safeSearch = SOAP_FALSE
_lang_restrict = ''

def googleSearch(title):
    '''
    It is the function of the application that make the request at google WS using
    getting the first url of response.
    
    @param title: the title of the article to serach for
    @return: the first url
    '''
    
     
    # create SOAP proxy object
    google = SOAPProxy(_url, _namespace)
    
    _query= google.doSpellingSuggestion( _license_key, title )
    
    if _query == None:
        _query=title
    
    # call search method over SOAP proxy
    results = google.doGoogleSearch( _license_key, _query, 
                                     _start, _maxResults, 
                                     _filter, _restrict,
                                     _safeSearch, _lang_restrict, '', '' )
               
    # display results
#    print 'google search for  " ' + _query + ' "\n'
#    print 'estimated result count: ' + str(results.estimatedTotalResultsCount)
#    print '           search time: ' + str(results.searchTime) + '\n'
#    print 'results ' + str(_start + 1) + ' - ' + str(_start + _maxResults) +':\n'
                                                           
    numresults = len(results.resultElements)
    if numresults:
        for i in range(numresults):
            url = results.resultElements[i].URL
            r = re.compile("http://(.*)\.pdf",re.IGNORECASE)
            if (r.match(url)):
                url = r.match(url).group()
                type = "pdf"
                return (url,type,_query)
            else:
                r = re.compile("http://citeseer.ist.psu.edu/")
                if(r.match(url)):
                    type = "citeseer"
                    return (url,type,_query)
                else:
                    r = re.compile("http://portal.acm.org/")
                    if(r.match(url)):
                        type = "acm"
                        return (url,type,_query)
                    else:
                        r = re.compile("http://doi.ieeecomputersociety/")
                        if(r.match(url)):
                            type = "doi"
                            return (url,type,_query)
                        else: 
                            pass
        type = "default"
        return  (url,type,_query)                          
    else:
        url= "#"
        type = None
        return (url,type,_query)
    

    
#    for i in range(numresults):
#        title = results.resultElements[i].title
#        noh_title = title.replace('<b>', '').replace('</b>', '')
#        print 'title: ' + noh_title
#        print '  url: ' + results.resultElements[i].URL + '\n'


def getBibTex(url,type):
    '''
    It is the function of the application that serach the bibxtex entry in the url 
    provided by Google WS. 
    The function switch on each site and for each site it makes a particular search.
    
    @param url: the url where start to serach
    @return: the string with the bibtex entry
    '''
       
    # timeout in seconds
    timeout = 20
    socket.setdefaulttimeout(timeout)
    html = openUrl(url)
    if html:
        #FIXME: finish the retreival
        #FIXME: Insert the timeout
        if url <> "#":
            if type == "citeseer":
                bibtex = "BibTeX"
                index = html.find(bibtex)
                if index <> -1:
                    html = html[index:]
                    index = html.find("@")
                    html = html[index:]
                    index = html.find("}</pre>")
                    html = html[:index+1]
                    return html
                else:
                     return None
            elif type == "doi":
                #Il pdf non si puo' scaricare e' a pagamento
                index = html.find("Popup.document.write(\'@")
                if index <> -1:
                    html = html[index+len("Popup.document.write(\'"):]
                    index = html.find("}')")
                    html = html[:index+1]
                    return html.replace("&nbsp;"," ").replace("<xsl:text>","").replace("<br/>","\n")
                else:
                    return None
            elif type == "acm":
                index = html.find("window.open('popBibTex")
                if index <> -1:
                    html = html[index+len("window.open('"):]
                    index = html.find(",'BibTex',")
                    subUrl = html[:index]
                    html = openUrl("http://portal.acm.org/"+subUrl)
                    if html:
                        index = html.find('@')
                        if index <> -1:
                            html = html[index - 1:]
                            html = html[:html.find('}\r\n</pre>')-1:]
                            return html
                        else:
                            return None
                    else:
                        return None
  
            
            
            
    return None


def openUrl(url):
    '''
    It is the function that get the html from the specific url 
    using urllib2 python library.
    
    @param url: the url to connect to
    @return: the html of the page in the url
    '''
    
    html=''
    try:
            if url <> "#":
                website = urllib2.urlopen(url)
                html = website.read()
                return html
            else:
                return None
    except (urllib2.URLError, socket.timeout):
        print "\n\n\t~ The url "+url+" is in timeout. Skipping it.\n"
        return None
  

def getOfflinePdf(url,type,filename,dir,i):
    
    #timeout = 10
    #socket.setdefaulttimeout(timeout)
    
    filename = filename[:len(filename)- 4]
    pathToSave= dir+"/"+filename+"_ref_"+str(i)+".pdf"
    
    html = openUrl(url)
    if html:
        
        if type == "citeseer":
            index = html.find("PDF</a>")
            if index <> -1:   
                html = html[:index]
                index = html.rfind(".pdf';")
                html = html[:index+4]
                index = html.rfind("self.status='")
                html = html[index+len("self.status='"):]
                downloadPdf(html,pathToSave)
                return pathToSave
        
        if type == "acm":
            index = html.find("<A NAME=\"FullText\" HREF=\"")
            if index <> -1:
                html = html[index:]
                index = html.find("\"")
                html = html[:index]
                downloadPdf("http://portal.acm.org/"+html,pathToSave)
                return pathToSave
        
        if type == "pdf":
            downloadPdf(url,pathToSave)
            return pathToSave
    
    return None
        
        
        

    

def downloadPdf(url,pathToSave):
    """Copy the contents of a file from a given URL
    to a local file.
    """
 
    try:  
        webFile = urllib.urlopen(url)
        localFile = open(pathToSave, 'w')
        localFile.write(webFile.read())
        webFile.close()
        localFile.close()
    except IOError:
        print url
    except socket.timeout:
        pass
    
    
