from collections import defaultdict

import pygame as pg

from . import actions


class EventQueueHandler:
    def __init__(self):
        self._inputs = defaultdict(list)
        self._inputs[0].append(KeyboardInput())
        self._inputs[0].append(GamepadInput())

    def process_event(self, pg_event):
        for player, inputs in self._inputs.items():
            for player_input in inputs:
                player_input.process_event(pg_event)

        for player, inputs in self._inputs.items():
            for player_input in inputs:
                for game_event in player_input.get_events():
                    yield game_event


class PlayerInput:
    __slots__ = ["button", "value", "hold_time", "triggered"]

    def __init__(self, button, value=0, hold_time=0):
        self.button = button
        self.value = value
        self.hold_time = hold_time
        self.triggered = False

    @property
    def pressed(self):
        return bool(self.value) and self.hold_time == 1

    @property
    def held(self):
        return bool(self.value)


class EventHandler:
    default_input_map = None

    def __init__(self, event_map=None):
        if event_map is None:
            event_map = self.default_input_map.copy()
        self.buttons = dict()
        self.event_map = event_map
        for button in event_map.values():
            self.buttons[button] = PlayerInput(button)

    def process_event(self, pg_event):
        raise NotImplementedError

    def get_events(self):
        for inp in self.buttons.values():
            if inp.held:
                yield inp
                inp.hold_time += 1
            elif inp.triggered:
                yield inp
                inp.triggered = False

    def press(self, button, value=1):
        inp = self.buttons[button]
        inp.value = value
        if not inp.hold_time:
            inp.hold_time = 1

    def release(self, button):
        inp = self.buttons[button]
        inp.value = 0
        inp.hold_time = 0
        inp.triggered = True


class GamepadInput(EventHandler):
    default_input_map = {
        0: actions.JUMP,
        1: actions.INTERACT,
        6: actions.BACK,
        11: actions.LEFT,
        12: actions.RIGHT,
        13: actions.UP,
        14: actions.DOWN,
        7: actions.START,
    }

    def __init__(self, event_map=None, deadzone=.25):
        super(GamepadInput, self).__init__(event_map)
        self.deadzone = deadzone
        self.init_all_joysticks()

    def init_all_joysticks(self):
        pg.joystick.init()
        for index in range(pg.joystick.get_count()):
            pg.joystick.Joystick(index).init()

    def process_event(self, pg_event):
        self.check_button(pg_event)
        self.check_hat(pg_event)
        self.check_axis(pg_event)

    def check_button(self, pg_event):
        try:
            button = self.event_map[pg_event.button]
            if pg_event.type == pg.JOYBUTTONDOWN:
                self.press(button)
            elif pg_event.type == pg.JOYBUTTONUP:
                self.release(button)
        except (KeyError, AttributeError):
            pass

    def check_hat(self, pg_event):
        if pg_event.type == pg.JOYHATMOTION:
            x, y = pg_event.value
            if x == -1:
                self.press(actions.LEFT, value=x * -1)
            elif x == 0:
                self.release(actions.LEFT)
                self.release(actions.RIGHT)
            elif x == 1:
                self.press(actions.RIGHT)

            if y == -1:
                self.press(actions.DOWN, value=y * -1)
            elif y == 0:
                self.release(actions.DOWN)
                self.release(actions.UP)
            elif y == 1:
                self.press(actions.UP)

    def check_axis(self, pg_event):
        if pg_event.type == pg.JOYAXISMOTION:
            value = pg_event.value

            if pg_event.axis == 0:
                if abs(value) >= self.deadzone:
                    if value < 0:
                        self.press(actions.LEFT, value * -1)
                    else:
                        self.press(actions.RIGHT, value)
                else:
                    self.release(actions.LEFT)
                    self.release(actions.RIGHT)

            elif pg_event.axis == 1:
                if abs(value) >= self.deadzone:
                    if value < 0:
                        self.press(actions.UP, value * -1)
                    else:
                        self.press(actions.DOWN, value)
                else:
                    self.release(actions.UP)
                    self.release(actions.DOWN)


class KeyboardInput(EventHandler):
    default_input_map = {
        pg.K_UP: actions.UP,
        pg.K_DOWN: actions.DOWN,
        pg.K_LEFT: actions.LEFT,
        pg.K_RIGHT: actions.RIGHT,
        pg.K_RSHIFT: actions.RUN,
        pg.K_LSHIFT: actions.RUN,
        pg.K_ESCAPE: actions.BACK,
        pg.K_SPACE: actions.JUMP,
        None: actions.UNICODE,
    }

    def process_event(self, pg_event):
        """ Translate a pg event to an internal game event

        :type pg_event: pg.event.Event
        """
        pressed = pg_event.type == pg.KEYDOWN
        released = pg_event.type == pg.KEYUP

        if pressed or released:
            # try to get game-specific action for the key
            try:
                button = self.event_map[pg_event.key]
            except KeyError:
                pass
            else:
                if pressed:
                    self.press(button)
                else:
                    self.release(button)
                return

            # just get unicode value
            try:
                if pressed:
                    self.release(actions.UNICODE)
                    self.press(actions.UNICODE, pg_event.unicode)
                else:
                    self.release(actions.UNICODE)
            except AttributeError:
                pass
