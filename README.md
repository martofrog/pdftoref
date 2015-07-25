# pdftoref

This project aims to develop an efficient rule based extractor of entries of references, located in scientific articles in English language. The application takes a pdf file or a directory of pdf and then returns an html file, containing the list of all entries with their respective title. Moreover the title of the article cited is searched through Google Web Service to get the URL that identifying the article on the web. If the URL provides on the page a Bibtex entry, this will appear in the html output under the relative entries, stolen from some typical site like citeseer, ieeexlpore etc. The application does not make search over pdf file based on images.

