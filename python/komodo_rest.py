""" function that can be used in Komodo to underline/overline current line"""

from xpcom import components

def underline_curline(with_char, up):
    viewSvc = components.classes["@activestate.com/koViewService;1"].getService(components.interfaces.koIViewService)
    view = viewSvc.currentView.queryInterface(components.interfaces.koIScintillaView)
    scimoz = view.scimoz
    scimoz.beginUndoAction()
    pos = scimoz.currentPos
    line = scimoz.lineFromPosition(pos)
    len = scimoz.lineLength(line)
    if up:
        scimoz.lineUp()
        scimoz.lineEnd()
        scimoz.newLine()
        scimoz.insertText(scimoz.currentPos, withChar*len)
        scimoz.lineDown()
    scimoz.lineEnd()
    scimoz.newLine()
    scimoz.insertText(scimoz.currentPos, withChar*len);
    scimoz.lineEnd()
    scimoz.newLine()
    scimoz.newLine()
    scimoz.endUndoAction()

