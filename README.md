

# 🐱‍🏍 — the first pygame 2 community game. Starting now! Are you in?


"My first cat was named Speedy. Because when he went into one of those crazy dashes across the house, he'd run all along the backrest of the couch, like one of those motorcycle stuntperson.
On a near-vertical surface."

* repo: [https://github.com/pygame/stuntcat](https://github.com/pygame/stuntcat)
* [discord web chat](https://discordapp.com/invite/r8yreB6) #communitygame channel.


To help drive pygame 2 development, we are making a game with pygame 2.

The whole pygame community is invited to take part. In making this one game. In 4 days.

[More info here](https://renesd.blogspot.com/2018/11/first-pygame-2-community-game-starting.html)



## Get started.

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.dev.txt
python run_game.py
```


## The team.

* bitcraft - "I hope I can contribute, but my work schedule is awful". pyscroll, pytmx libraries.

* blubberquark - "Anyway, I would love to work on some kind of async networking or server features
Twitch/IRC integration, leaderboards, Discord...""

* Bottersnake - snäke library. "In fact, I have a a load of frees today so I'll probably whip up all the boilerplate needed to make everything else quicker to write."

* claudeb - "My first cat was named Speedy. Because when he went into one of those crazy dashes across the house"

* dirk0 - "Unfortunately I am terribly busy right now, but I could contribute music and Mac OSX compilation/testing, if needed."

* illume - fixes to pygame 2, any general thing that needs doing.

* Kuba | ThePolish - "pm me if you need sfx and/or music"

* TJWhale - "Hey, I'm interested in helping with this community game if I can :) I've got some experience with pygame, I actually lanched a game on steam with it"

* *** - writing

* hfoxp - "Im interested in helping. Im still learning pygame but I would still love to be involved. Will be fun and a good learning experience"

* xeno - I tried drawing a cat, it looks weird.




## Awesome libraries

Apart from pygame 2 we are going to try using some awesome libraries.

* [pyscroll](https://github.com/bitcraft/pyscroll) - scrolling map
* [pytmx](https://github.com/bitcraft/pytmx) - tilemap
* [thorpy](http://www.thorpy.org/) - gui
* [pymunk](http://www.pymunk.org/en/latest/) - physics
* [snäke](https://pypi.org/project/pygame.snake/) - cleaner api
* [pyinstaller](https://www.pyinstaller.org/)
* [pytest](https://docs.pytest.org/en/latest/) - our game will have some tests.
* ... other?


## pygame 2 compilation

The game should also work with pygame 1.9.4+, but this game is about using pygame 2.

So...

For now compiling pygame 2 from source is needed (hopefully not by the end of things).

- [Ubuntu](http://www.pygame.org/wiki/CompileUbuntu#pygame%20with%20sdl2%20(alpha))
- [Mac](https://www.pygame.org/wiki/MacCompile#pygame%20with%20sdl2)
- [Windows](https://www.pygame.org/wiki/CompileWindows) (incomplete instructions)


### Running tests.

Tests can be found in the tests/ folder.

Type `pytest`.
Or run `python -m tox`

Tests are run on mac, linux, windows when there is a pull request made.

### releasing

Releasing is tested with python3.7(not python2 or any other version).

To the python package index (pypi).
```
rm -rf dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```

On windows:
```
python setup.py bdist_msi
dir build/*.msi
```

On mac:
```
python setup.py bdist_dmg
ls build/*.dmg
```

### Making gif.

Uncomment the game.py line. Then press g to start recording, g to stop.
```python
        # self.gifmaker = GifMaker()
```

Requires imagemagic tested on OSX, probably works on linux.


## Licenses

#### Code license

License for code will be the same as the pygame license (LGPL, but you can keep your parts of course!)


#### Art assets

https://creativecommons.org/licenses/by-sa/4.0/
https://creativecommons.org/2015/10/08/cc-by-sa-4-0-now-one-way-compatible-with-gplv3/

- @AokiAhishatsu stuntcat/data/images/
- @dirkk0 stuntcat/data/sounds/ict_0026.ogg
- M. other stuntcat/data/sounds/

So technically anyone should be able to distribute the game following those licenses (and even sell it).
