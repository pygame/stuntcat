""" gifmaker is for making gifs with pygame.

It relies on ffmpeg, or convert(from imagemagick being available):

    brew install imagemagick ffmpeg
    apt-get install imagemagick ffmpeg

::Example::

    >>> from gifmaker import GifMaker
    >>> gifmaker = GifMaker(seconds=2)
    >>> gifmaker.update(events, screen)

"""

import os
import subprocess
import time
import shutil
import distutils.spawn
import pygame as pg


# TODO: make it work on windows (tmp path handling fixes)
# TODO: try to use Pillow if imagemagik/ffmpeg is not installed?
# TODO: a backend for windows? Pure python gif saving? windows built in gif saving?
# TODO: ffmpeg backend to pipe data into ffmpeg rather than use tmp files.
# TODO: async operation for saving.
# TODO: scaling image to a smaller size.


def which(cmd):
    """find an executable cmd."""
    if hasattr(shutil, "which"):
        return shutil.which(cmd)

    return distutils.spawn.find_executable(cmd)


class GifMaker:
    """For making gif animation of a pygame.

    >>> gifmaker = GifMaker()
    >>> gifmaker.update(events, screen)

    Press K_g to start recording,
          K_g again to finish recording.

    Uses imagemagik 'convert' or ffmpeg tool for making the gif.

        brew install imagemagick ffmpeg
        apt-get install imagemagick ffmpeg

    ::Example::

    Press the K_g key to record 2 second gif.

    >>> gifmaker = GifMaker(seconds=2)
    >>> gifmaker.update(events, screen)
    """

    def __init__(self, path="/tmp/", fps=30, seconds=None):
        self.path = path
        self.start_saving = False
        self.finished_saving = False
        self.surfs = []
        self.fps = fps
        self.seconds = seconds

    def _convert(self, image_paths, output_path):

        convert_path = which("convert")
        if convert_path is None:
            return False

        cmd = [
            convert_path,
            "-delay",
            "%s,1000" % (1000 // self.fps),
            "-size",
            "%sx%s" % (self.surfs[0].get_width(), self.surfs[0].get_height()),
        ]
        cmd += image_paths
        cmd += [output_path]
        print(cmd)
        subprocess.call(cmd)
        return True

    def _ffmpeg(self, output_path):
        # https://stackoverflow.com/questions/3688870/create-animated-gif-from-a-set-of-jpeg-images

        ffmpeg_path = which("ffmpeg")
        if ffmpeg_path is None:
            return False

        cmd = [
            ffmpeg_path,
            "-i",
            os.path.join(self.path, "bla_%05d.png"),
            "-y",  # overwrite output file without asking.
            "-framerate",
            str(self.fps),
            "-filter_complex",  # use a pallet for the gif for nicer image.
            "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse",
            output_path,
        ]
        print(cmd)
        subprocess.call(cmd)
        return True

    def finish(self):
        """Called when finished with making the gifs."""
        print("saving images for gif")
        output_path = "%s/anim.gif" % self.path
        image_paths = []
        for frame_idx, surf in enumerate(self.surfs):
            image_path = "%s/bla_%05d.png" % (self.path, frame_idx)
            image_paths.append(image_path)
            pg.image.save(surf, image_path)

        if not (self._ffmpeg(output_path) or self._convert(image_paths, output_path)):
            raise ValueError("could not find convert or ffmpeg")

        for image_path in image_paths:
            os.remove(image_path)

        print("%s saved" % output_path)

        self.finished_saving = False
        self.start_saving = False

    def update(self, events, screen):
        """To integrate with the main program.

        Call it once per frame after drawing is done.
        """
        for event in events:
            if event.type == pg.KEYDOWN and event.key == pg.K_g:
                if not self.start_saving:
                    self.start_saving = time.time()
                    self.finished_saving = False
                    print("recording surfs, press g")
                else:
                    self.start_saving = False
                    self.finished_saving = True

        if self.finished_saving:
            self.finish()
        if self.start_saving:
            self.surfs.append(screen.copy())
            if (
                self.seconds is not None
                and time.time() - self.start_saving > self.seconds
            ):
                self.finish()
