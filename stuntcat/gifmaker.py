import pygame as pg
import os
import subprocess
import time


# TODO: don't rely on imagemagik for saving.
# TODO: make it work on windows.
# TODO: Pillow support if imagemagik is not installed.
# TODO: a backend for windows? Pure python gif saving?
# TODO: ffmpeg backend? http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html

class GifMaker:
    """ For making gif animation of a pygame.

    >>> gifmaker = Gif()
    >>> gifmaker.update(events, screen)

    Press K_g to start recording,
          K_g again to finish recording.

    Uses imagemagik 'convert' tool for making the gif.

        brew install imagemagik
        apt-get install imagemagick

    ::Example::

    Press the K_g key to record 2 second gif.

    >>> gifmaker = Gif(seconds=2)
    >>> gifmaker.update(events, screen)
    """

    def __init__(self, path="/tmp/", fps=30, seconds=None):
        self.path = path
        self.start_saving = False
        self.finished_saving = False
        self.surfs = []
        self.fps = fps
        self.seconds = seconds

    def finish(self):
        print("saving images for gif")
        output_path = "%s/anim.gif" % self.path
        image_paths = []
        for frame_idx, surf in enumerate(self.surfs):
            image_path = "%s/bla_%05d.png" % (self.path, frame_idx)
            image_paths.append(image_path)
            pg.image.save(surf, image_path)

        convertpath = "convert"
        cmd = [
            convertpath,
            "-delay",
            "%s,1000" % (1000 // self.fps),
            "-size",
            "%sx%s" % (self.surfs[0].get_width(), self.surfs[0].get_height()),
        ]
        cmd += image_paths
        cmd += [output_path]
        print(cmd)
        subprocess.call(cmd)

        for image_path in image_paths:
            os.remove(image_path)

        print("%s saved" % output_path)

        self.image_path = []
        self.finished_saving = False
        self.start_saving = False

    def update(self, events, screen):
        for e in events:
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_g and not self.start_saving:
                    self.start_saving = time.time()
                    self.finished_saving = False
                    print("recording surfs, press g")
                elif e.key == pg.K_g and self.start_saving:
                    self.start_saving = False
                    self.finished_saving = True


        if self.finished_saving:
            self.finish()
        if self.start_saving:
            self.surfs.append(screen.copy())
            if self.seconds is not None:
                if time.time() - self.start_saving > self.seconds:
                    self.finish()
