# StuntCat Changelog

## 2020-07-21, Version 0.1.0, @nachomonkey

* Added three "boing" sounds that are played when the cat is hit by a NotFish or get bumped back onto the screen
* Added three "meow" sounds are played at random times
* Sound system now supports fadeout
* Added a splashing sound for when the cat falls into the water
* Added cat crashing sound
* Replaced shark attack and shark gone sounds
* Replaced "zirkus" sound with applause sound
* "shark_appears.ogg" sound is stopped when the shark goes underwater
* Replaced main menu song
* Changed jump physics so the cat doesn't lose all Y-velocity on jump button release
* Added SPACE as a jump key
* Improved jump sound
* Added a shark laser image
* When the cat gets hit by the laser, the crowd boos and throws more not-fish for a time
* The shark and elephant now leave when the cat dies
* The score text is now centered on a point, and no longer gets erased by objects
* Fixed libpng color profile errors
* Added more contrast to the fish images
* Shark now pauses a bit before firing in the 'aiming' state
* Replaced "cat_laser_2.ogg" with "cat_shot.ogg"
* Animated the cat's tail
* Removed old use of "cat\_wheel.ogg" and replaced it with a looping unicycle sound with velocity-dependent volume
* Version is now defined under stuntcat/\_\_init\_\_.py
* The resources.gfx function now accepts the convert and convert\_alpha arguments
* The window caption is now "Stunt Cat"
* Added some texture to the tent in "background.png"
* Modified "intro_screen.png" so that the polka dots are symmetrical
* The cat's rotation now affects his X-velocity (he a bit rolls in the direction he's facing)
* Added basic joystick control
* Updated the "gameplay.gif" animation
* README.md improvements
* Fixed most of the alerts raised by lgtm
* Added shebang (#!) to run_game.py for Linux
