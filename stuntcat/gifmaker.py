import pygame as pg
import os
import subprocess
import time


# TODO: don't rely on imagemagik for saving.
# TODO: make it work on windows.
# TODO: Pillow support if imagemagik is not installed.
# TODO: a backend for windows? Pure python gif saving?
# TODO: ffmpeg backend? http://blog.pkh.me/p/21-high-quality-gif-with-ffmpeg.html
# https://stackoverflow.com/questions/3688870/create-animated-gif-from-a-set-of-jpeg-images
# ffmpeg -i bla%d.png -framerate 30 -filter_complex "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse" anim.gif
#


def which(cmd):
    """ find an executable cmd.
    """
    import shutil
    if hasattr(shutil, 'which'):
        return shutil.which(cmd)
    import distutils.spawn
    return distutils.spawn.find_executable(cmd)


class GifMaker:
    """ For making gif animation of a pygame.

    >>> gifmaker = Gif()
    >>> gifmaker.update(events, screen)

    Press K_g to start recording,
          K_g again to finish recording.

    Uses imagemagik 'convert' or ffmpeg tool for making the gif.

        brew install imagemagick ffmpeg
        apt-get install imagemagick ffmpeg

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

    def convert(self, convert_path, image_paths, output_path):

        convert_path = which('convert')
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

    def ffmpeg(self, output_path):
        ffmpeg_path = which('ffmpeg')
        if ffmpeg_path is None:
            return False

        cmd = [
            ffmpeg_path,
            "-i",
            os.path.join(self.path, "bla_%05d.png"),
            "-framerate",
            str(self.fps),
            "-filter_complex",
            "[0:v] split [a][b];[a] palettegen [p];[b][p] paletteuse",
            output_path,
        ]
        print(cmd)
        subprocess.call(cmd)
        return True

    def finish(self):
        print("saving images for gif")
        output_path = "%s/anim.gif" % self.path
        image_paths = []
        for frame_idx, surf in enumerate(self.surfs):
            image_path = "%s/bla_%05d.png" % (self.path, frame_idx)
            image_paths.append(image_path)
            pg.image.save(surf, image_path)

        if not self.ffmpeg(output_path):
            if not self.convert(image_paths, image_paths, output_path):
                raise ValueError('could not find convert or ffmpeg')

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
