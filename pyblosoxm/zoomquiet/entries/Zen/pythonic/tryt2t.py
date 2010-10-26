PREFORMATTER_ID = 'txt2tags'
#tags Zen,pythonic
FILE_EXT = 't2t'
__version__ = '$Id$'
__author__ = 'Zoom.Quiet <Zoom dot Quiet  at gmail.com>'
#T2T = "/usr/local/bin/txt2tags"
T2T = "t2t"


def cb_entryparser(args):
    args['t2t'] = parse
    #args[FILE_EXT] = readfile
    return args


"""
def parse(filename):
    #html = publish_string(story, writer_name='html')
    import os
    act = T2T+" -t html -H --toc %s"%filename
    html = act
    html += os.popen(act).read().strip()
    #return html[html.find('<body>') + 6:html.find('</body>')]
    return html
"""
#def parse(filename, request):
def parse(filename):
    import os, sys
    from StringIO import StringIO
    # open own source
    #config = request.getConfiguration()
    act = T2T+" -t html -H --toc -o - %s"%filename
    #source = open(filename).read()
    #out = StringIO()
    
    #html = os.popen(act).read().strip()
    print act
    #print os.popen(act).read().strip()
    # write colorized version to "python.html"
    #Parser(source, out).format(None, None)
    
    #print out.getvalue()
    """
    entryData = {'body' : out.getvalue(),
                 'title' : filename.replace(config['datadir'], '')}
    return entryData
    """


parse("py-code-rule.t2t")
