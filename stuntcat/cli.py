""" Command line interface.
"""
import os
import sys
import traceback

LOCAL_PATH = os.path.abspath(os.path.dirname(__file__))

# What was this trying to do?
# try:
#     # import stuntcat
#
#     # if isinstance(stuntcat.__path__, list):
#     #     LOCAL_PATH = os.path.abspath(stuntcat.__path__[0])
#     # else:
#     #     LOCAL_PATH = os.path.abspath(stuntcat.__path__._path[0])
# except ImportError:
#     LOCAL_PATH = os.path.split(os.path.abspath(sys.argv[0]))[0]

try:
    import pygame as pg
except ImportError:
    pg = None
    raise ImportError( # pylint:disable=raise-missing-from
        "Cannot import pygame, install version 1.9.4 or higher"
    )


try:
    from .main import main
except ImportError:
    from stuntcat.main import main


class Cli:
    """
    Cli Class.
    """

    def __init__(self):
        # these directories will be used if stuntcat cannot find
        # the directories in the location of the main program
        if sys.platform == "win32":
            self.data_dir = "C:\\Program Files\\stuntcat"
            self.code_dir = "C:\\Program Files\\stuntcat\\code"
        else:
            self.data_dir = "/usr/share/games/stuntcat"
            self.code_dir = "/usr/lib/games/stuntcat"

        self.handlers = (self.__pgbox, self.__tkinterbox, self.__windowsbox)

    def cli_main(self):
        """
        Main function
        """
        # figure out our directories
        # first try to get the path from the stuntcat package.
        testdata = LOCAL_PATH
        testcode = os.path.join(LOCAL_PATH, ".")

        if os.path.isdir(os.path.join(testdata, "data")):
            self.data_dir = testdata
        if os.path.isdir(testcode):
            self.code_dir = testcode

        # pyinstaller uses this variable to store the path
        #   where it extracts data to.
        pyinstaller_path = getattr(sys, "_MEIPASS", None)
        if pyinstaller_path:
            self.data_dir = os.path.join(pyinstaller_path, "data")
        else:
            # apply our directories and test environment
            os.chdir(self.data_dir)
            sys.path.insert(0, self.code_dir)
            self.check_dependencies()

        # run game and protect from exceptions
        try:
            # import pdb;pdb.set_trace()
            main()
        except KeyboardInterrupt:
            print("Keyboard Interrupt (Control-C)...")
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

    def check_dependencies(self):
        """
        Only returns if everything looks ok
        """
        msgs = []

        # make sure this looks like the right directory
        if not os.path.isdir(self.code_dir):
            msgs.append("Cannot locate stuntcat modules")
        if not os.path.isdir("data"):
            msgs.append("Cannot locate stuntcat data files")

        # first, we need python >= 2.7
        if sys.hexversion < 0x2070000:
            self.errorbox("Requires Python-2.7 or Greater")

        # is correct pg found?
        if pg.ver < "1.9.4":
            msgs.append("Requires pygame 1.9.4 or Greater, You Have " + pg.ver)

        # check that we have FONT and IMAGE
        if pg:
            if not pg.font:
                msgs.append("pg requires the SDL_ttf library, not available")
            if not (pg.image and pg.image.get_extended()):
                msgs.append("pg requires the SDL_image library, not available")

        if msgs:
            msg = "\n".join(msgs)
            self.errorbox(msg)

    # Pretty Error Handling Code...
    @staticmethod
    def __windowsbox(title, message):
        raise ImportError  # the MessageBox command is crashing!
        # import win32ui, win32con
        # win32ui.MessageBox(message, title, win32con.MB_ICONERROR)

    # def __wxpythonbox(self, title, message):
    #     import wxPython.wx as wx
    #
    #     class LameApp(wx.wxApp):
    #         def OnInit(self): return 1
    #
    #     app = LameApp()
    #     dlg = wx.wxMessageDialog(None, message, title, wx.wxOK | wx.wxICON_EXCLAMATION)
    #     dlg.ShowModal()
    #     dlg.Destroy()

    @staticmethod
    def __tkinterbox(title, message):
        #pylint: disable=import-outside-toplevel, import-error
        if sys.version_info[0] >= 3:
            import tkinter as tk
            from tkinter.messagebox import showerror
        else:
            import Tkinter as tk
            from tkMessageBox import showerror

        tk.Tk().wm_withdraw()
        showerror(title, message)

    @staticmethod
    def __pgbox(title, message):
        try:
            pg.quit()  # clean out anything running
            pg.display.init()
            pg.font.init()
            screen = pg.display.set_mode((460, 140))
            pg.display.set_caption(title)
            font = pg.font.Font(None, 18)
            foreg, backg, liteg = (0, 0, 0), (180, 180, 180), (210, 210, 210)
            ok_surf = font.render("Ok", True, foreg, liteg)
            ok_rect = ok_surf.get_rect().inflate(200, 10)
            ok_rect.centerx = screen.get_rect().centerx
            ok_rect.bottom = screen.get_rect().bottom - 10
            screen.fill(backg)
            screen.fill(liteg, ok_rect)
            screen.blit(ok_surf, ok_rect.inflate(-200, -10))
            pos = [10, 10]
            for text in message.split("\n"):
                if text:
                    msg = font.render(text, True, foreg, backg)
                    screen.blit(msg, pos)
                pos[1] += font.get_height()
            pg.display.flip()
            stopkeys = pg.K_ESCAPE, pg.K_SPACE, pg.K_RETURN, pg.K_KP_ENTER
            while True:
                event = pg.event.wait()
                if (
                    event.type == pg.QUIT
                    or (event.type == pg.KEYDOWN and event.key in stopkeys)
                    or (
                        event.type == pg.MOUSEBUTTONDOWN
                        and ok_rect.collidepoint(event.pos)
                    )
                ):
                    break
            pg.quit()
        except pg.error:
            raise ImportError  # pylint:disable=raise-missing-from

    def __showerrorbox(self, message):
        title = os.path.splitext(os.path.split(sys.argv[0])[1])[0]
        title = title.capitalize() + " Error"
        for handler in self.handlers:
            try:
                handler(title, message)
                break
            except (ImportError, NameError, AttributeError):
                pass

    def errorbox(self, message):
        """
        Displays an error box and write the error to stderr.

        :param message: The error message to show and write.
        """
        message = str(message)
        if not message:
            message = "Error"
        self.__showerrorbox(message)
        sys.stderr.write("ERROR: " + message + "\n")
        raise SystemExit

    def exception_handler(self):
        """
        Exception handler function.
        """
        exception_type, info, trace = sys.exc_info()
        tracetop = traceback.extract_tb(trace)[-1]
        tracetext = "File %s, Line %d" % tracetop[:2]
        if tracetop[2] != "?":
            tracetext += ", Function %s" % tracetop[2]
        exception_message = '%s:\n%s\n\n%s\n"%s"'
        message = exception_message % (
            str(exception_type),
            str(info),
            tracetext,
            tracetop[3],
        )
        if exception_type not in (KeyboardInterrupt, SystemExit):
            self.__showerrorbox(message)


if __name__ == "__main__":
    cli = Cli()
    cli.cli_main()
