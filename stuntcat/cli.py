""" Command line interface.
"""
import os
import sys
import traceback

# these directories will be used if stuntcat cannot find
# the directories in the location of the main program
if sys.platform == "win32":
    DATADIR = "C:\\Program Files\\stuntcat"
    CODEDIR = "C:\\Program Files\\stuntcat\\code"
else:
    DATADIR = "/usr/share/games/stuntcat"
    CODEDIR = "/usr/lib/games/stuntcat"


def cli_main():
    """
    Main function
    """
    # figure out our directories
    global DATADIR, CODEDIR

    # first try to get the path from the stuntcat package.
    try:
        import stuntcat
        if isinstance(stuntcat.__path__, list):
            localpath = os.path.abspath(stuntcat.__path__[0])
        else:
            localpath = os.path.abspath(stuntcat.__path__._path[0])
    except ImportError:
        localpath = os.path.split(os.path.abspath(sys.argv[0]))[0]

    testdata = localpath
    testcode = os.path.join(localpath, '.')

    if os.path.isdir(os.path.join(testdata, 'data')):
        DATADIR = testdata
    if os.path.isdir(testcode):
        CODEDIR = testcode

    # pyinstaller uses this variable to store the path
    #   where it extracts data to.
    pyinstaller_path = getattr(sys, '_MEIPASS', None)
    if pyinstaller_path:
        DATADIR = os.path.join(pyinstaller_path, 'data')
    else:
        # apply our directories and test environment
        os.chdir(DATADIR)
        sys.path.insert(0, CODEDIR)
        checkdependencies()

    # run game and protect from exceptions
    try:
        # import pdb;pdb.set_trace()
        try:
            from .main import main
        except ImportError:
            from stuntcat.main import main
        import pygame as pg
        main()
    except KeyboardInterrupt:
        print('Keyboard Interrupt (Control-C)...')
    except Exception as err:
        # must wait on any threading
        # if game.thread:
        #     game.threadstop = 1
        #     while game.thread:
        #         pg.time.wait(10)
        #         print('waiting on thread...')

        # we need to enable a debug handler for release.
        # exception_handler()
        # if game.DEBUG:
        #     raise
        raise err


def checkdependencies():
    """
    Only returns if everything looks ok
    """
    msgs = []

    # make sure this looks like the right directory
    if not os.path.isdir(CODEDIR):
        msgs.append('Cannot locate stuntcat modules')
    if not os.path.isdir('data'):
        msgs.append('Cannot locate stuntcat data files')

    # first, we need python >= 2.7
    if sys.hexversion < 0x2070000:
        errorbox('Requires Python-2.7 or Greater')

    # is correct pg found?
    try:
        import pygame as pg
        if pg.ver < '1.9.4':
            msgs.append('Requires pygame 1.9.4 or Greater, You Have ' + pg.ver)
    except ImportError:
        msgs.append("Cannot import pygame, install version 1.9.4 or higher")
        pg = None

    # check that we have FONT and IMAGE
    if pg:
        if not pg.font:
            msgs.append('pg requires the SDL_ttf library, not available')
        if not (pg.image and pg.image.get_extended()):
            msgs.append('pg requires the SDL_image library, not available')

    if msgs:
        msg = '\n'.join(msgs)
        errorbox(msg)


# Pretty Error Handling Code...

def __windowsbox(title, message):
    raise ImportError  # the MessageBox command is crashing!
    # import win32ui, win32con
    # win32ui.MessageBox(message, title, win32con.MB_ICONERROR)


# def __wxpythonbox(title, message):
#     import wxPython.wx as wx
#
#     class LameApp(wx.wxApp):
#         def OnInit(self): return 1
#
#     app = LameApp()
#     dlg = wx.wxMessageDialog(None, message, title, wx.wxOK | wx.wxICON_EXCLAMATION)
#     dlg.ShowModal()
#     dlg.Destroy()


def __tkinterbox(title, message):
    import tkinter.messagebox
    tkinter.Tk().wm_withdraw()
    tkinter.messagebox.showerror(title, message)


def __pgbox(title, message):
    import pygame as pg
    try:
        pg.quit()  # clean out anything running
        pg.display.init()
        pg.font.init()
        screen = pg.display.set_mode((460, 140))
        pg.display.set_caption(title)
        font = pg.font.Font(None, 18)
        foreg, backg, liteg = (0, 0, 0), (180, 180, 180), (210, 210, 210)
        ok_surf = font.render('Ok', True, foreg, liteg)
        ok_rect = ok_surf.get_rect().inflate(200, 10)
        ok_rect.centerx = screen.get_rect().centerx
        ok_rect.bottom = screen.get_rect().bottom - 10
        screen.fill(backg)
        screen.fill(liteg, ok_rect)
        screen.blit(ok_surf, ok_rect.inflate(-200, -10))
        pos = [10, 10]
        for text in message.split('\n'):
            if text:
                msg = font.render(text, True, foreg, backg)
                screen.blit(msg, pos)
            pos[1] += font.get_height()
        pg.display.flip()
        stopkeys = pg.K_ESCAPE, pg.K_SPACE, pg.K_RETURN, pg.K_KP_ENTER
        while True:
            event = pg.event.wait()
            if event.type == pg.QUIT or \
                    (event.type == pg.KEYDOWN and event.key in stopkeys) or \
                    (event.type == pg.MOUSEBUTTONDOWN and ok_rect.collidepoint(event.pos)):
                break
        pg.quit()
    except pg.error:
        raise ImportError


HANDLERS = __pgbox, __tkinterbox, __windowsbox  # , __wxpythonbox


def __showerrorbox(message):
    title = os.path.splitext(os.path.split(sys.argv[0])[1])[0]
    title = title.capitalize() + ' Error'
    for handler in HANDLERS:
        try:
            handler(title, message)
            break
        except (ImportError, NameError, AttributeError):
            pass


def errorbox(message):
    """
    Displays an error box and write the error to stderr.

    :param message: The error message to show and write.
    """
    message = str(message)
    if not message:
        message = 'Error'
    __showerrorbox(message)
    sys.stderr.write('ERROR: ' + message + '\n')
    raise SystemExit


def exception_handler():
    """
    Exception handler function.
    """
    exception_type, info, trace = sys.exc_info()
    tracetop = traceback.extract_tb(trace)[-1]
    tracetext = 'File %s, Line %d' % tracetop[:2]
    if tracetop[2] != '?':
        tracetext += ', Function %s' % tracetop[2]
    exception_message = '%s:\n%s\n\n%s\n"%s"'
    message = exception_message % (str(exception_type), str(info), tracetext, tracetop[3])
    if exception_type not in (KeyboardInterrupt, SystemExit):
        __showerrorbox(message)


if __name__ == '__main__':
    cli_main()
