

# 🐱‍🏍 — the first pygame 2 community game. Starting now! Are you in?

<img src="docs/stuntcat.svg" style="zoom:200%;" />


![Alt text](docs/gameplay.gif?raw=true "Stuntcat")

"My first cat was named Speedy. Because when he went into one of those crazy dashes across the house, he'd run all along the backrest of the couch, like one of those motorcycle stuntperson.
On a near-vertical surface."

* github repo: [https://github.com/pygame/stuntcat](https://github.com/pygame/stuntcat)

This was originally an experiment in having the whole pygame community being invited to take part. In making this one game. In 4 days. [More info here](https://renesd.blogspot.com/2018/11/first-pygame-2-community-game-starting.html) It was meant to help drive pygame 2 development, making a game with pygame 2. Since then a few people have improved things. It's still meant to be used to develop pygame features and be an example game.

See the [stuntcat release notes](https://github.com/pygame/stuntcat/releases) for details on what has changed.


## Get started

For development you can start like this:

```
python3 -m venv venv
. ./venv/bin/activate
pip install -r requirements.dev.txt
python run_game.py
```

For playing you could install it with `python3 -m pip install stuntcat`, or download an executable from the [stuntcat releases](https://github.com/pygame/stuntcat/releases) page.



## The team:

* @illume - "fixes to pygame 2, any general thing that needs doing.""

* TJWhale - "Hey, I'm interested in helping with this community game if I can :) I've got some experience with pygame, I actually lanched a game on steam with it"

* @nachomonkey - "This update focuses primarily on fixing bugs and adding sounds."

* @MyreMylar - "Investigating this issue here, I thought I'd start by clearing the pylint output of as much as I could."

* bitcraft - "I hope I can contribute, but my work schedule is awful". pyscroll, pytmx libraries.

* Bottersnake - snäke library. "In fact, I have a a load of frees today so I'll probably whip up all the boilerplate needed to make everything else quicker to write."

* @dirk0 - "Unfortunately I am terribly busy right now, but I could contribute music and Mac OSX compilation/testing, if needed."

* M - "¡Gatito!" music, sound effects, game design, and graphics.

* @xeno - "I tried drawing a cat, it looks weird."

* @kleinesfilmroellchen




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

### pygame compatibility

This game works with pygame 1.9.4+ and pygame 2


### Running tests

Tests can be found in the tests/ folder.

Type `pytest`.
Or run `python -m tox`

Tests are run on Mac, Linux, Windows when there is a pull request made.

### Releasing

Releasing is tested with python3.7 (not python2 or any other version).

To the python package index (PyPI).
```
rm -rf dist/*
python setup.py sdist bdist_wheel
twine upload dist/*
```

On Windows:
```
python setup.py bdist_msi
dir build/*.msi
```

On Mac:
```
python setup.py bdist_dmg
ls build/*.dmg
```

### Recording gif animations

Run the game with the argument `-g`:

```bash
python run_game.py -g
```

Press G to start recording two seconds of footage.

Requires imagemagick. Tested on OSX and Linux.


## Licenses

#### Code license

License for code will be the same as the pygame license (LGPL, but you can keep your parts of course!)


#### Art assets

https://creativecommons.org/licenses/by-sa/4.0/legalcode
https://creativecommons.org/2015/10/08/cc-by-sa-4-0-now-one-way-compatible-with-gplv3/

- @AokiAhishatsu stuntcat/data/images/
- M. other stuntcat/data/sounds/

#### Other assets

- stuntcat/data/sound/boo.ogg: [Crowd booing sound](https://freesound.org/people/tim.kahn/sounds/336997/), licensed under [CC BY 3.0](https://creativecommons.org/licenses/by/3.0/legalcode)

So technically anyone should be able to distribute the game following those licenses (and even sell it).
