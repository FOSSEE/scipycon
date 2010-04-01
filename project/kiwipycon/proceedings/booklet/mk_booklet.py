# encoding: utf-8

import os
import sys
import codecs
import re

try:
    from sanum import model
except:
    root_dir = os.path.abspath(os.getcwd() + '/../../')
    os.chdir(root_dir)
    sys.path.append(root_dir)
    from sanum import model

import sanum

import turbogears
turbogears.update_config(configfile="dev.cfg",
                         modulename="sanum.config")


from mk_scipy_paper import tex2pdf, current_dir , copy_files, preamble, \
        render_abstract, addfile, sourcedir, outdir, outfilename


def hack_include_graphics(latex_text, attach_dir):
    """ Replaces all the \includegraphics call with call that impose the
        width to be 0.9\linewidth.
    """
    latex_text = re.sub(r'\\includegraphics(\[.*\])?\{',
                        r'\includegraphics\1{' + attach_dir,
                        latex_text)
    return latex_text


class MyStringIO(object):
    """ An unicode-friendly stringIO-like object.
    """

    def __init__(self):
        self.lines = []

    def write(self, line):
        self.lines.append(line)

    def getvalue(self):
        return u''.join(self.lines)

def mk_booklet_tex(outfilename):
    """ Generate the entire booklet latex file.
    """
    outfile = codecs.open(outfilename, 'w', 'utf-8')
    preamble(outfile)
    copy_files()
    #addfile(outfile, sourcedir + os.sep + 'title.tex')
    addfile(outfile, sourcedir + os.sep + 'introduction.tex')

    #outfile.write(ur'\setcounter{page}{0}' + '\n')

    #from sanum.controllers import Root as Controller
    abstracts = model.Abstract.select()
    for abstract in abstracts:
        if not abstract.approved:
            continue
        print abstract.title
        # Hack: I don't use a stringIO, because it is not unicode-safe.
        tmpout = MyStringIO()
        # Hack: I don't wont to be bound to the controller, to be
        # abstractle to run without cherrypy.
        #attach_dir = Controller._paper_attach_dir(abstract.id)
        attach_dir = os.path.abspath(os.sep.join(
                    (os.path.dirname(sanum.__file__), 'static', 
                    'papers', '%i' % abstract.id))) + os.sep
        render_abstract(tmpout, abstract)
        outstring = hack_include_graphics(tmpout.getvalue(),
                            attach_dir)
        outfile.write(outstring)
        #outfile.write(ur'\fillbreak' + '\n')

    outfile.write(ur'\end{document}' + '\n')




def mk_booklet(outfilename=outfilename):
    """ Generate the entire booklet pdf file.
    """
    name, ext = os.path.splitext(outfilename)
    mk_booklet_tex(name + '.tex')
    return tex2pdf(name, remove_tex=False, timeout=60)

if __name__ == '__main__':
    mk_booklet(outfilename)
