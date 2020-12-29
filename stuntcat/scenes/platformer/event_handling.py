"""
Event Handling Module
"""

from collections import defaultdict

import pygame as pg

from . import actions


class EventQueueHandler:
    """
    Event Queue Handler class.
    """

    def __init__(self):
        self._inputs = defaultdict(list)
        self._inputs[0].append(KeyboardInput())
        self._inputs[0].append(GamepadInput())

    def process_event(self, event):
        """
        Process pygame events.

        :param event: The event to process.
        """
        for _, inputs in self._inputs.items():
            for player_input in inputs:
                player_input.process_event(event)

        for _, inputs in self._inputs.items():
            for player_input in inputs:
                for game_event in player_input.get_events():
                    yield game_event

    def print_controls(self):
        """
        Print the controls to the console.
        """
        print("Keyboard controls:", self._inputs[0][0], "\n")
        print("Gamepad controls:", self._inputs[0][0], "\n")


class PlayerInput:
    """
    Player input class.
    """

    __slots__ = ["button", "value", "hold_time", "triggered"]

    def __init__(self, button, value=0, hold_time=0):
        self.button = button
        self.value = value
        self.hold_time = hold_time
        self.triggered = False

    @property
    def pressed(self):
        """
        Pressed property.

        :return: True if pressed.
        """
        return bool(self.value) and self.hold_time == 1

    @property
    def held(self):
        """
        Held property.

        :return: True if held.
        """
        return bool(self.value)


class EventHandler:
    """
    Event handler class.
    """

    default_input_map = None

    def __init__(self, event_map=None):
        if event_map is None:
            event_map = self.default_input_map.copy()
        self.buttons = {}
        self.event_map = event_map
        for button in event_map.values():
            self.buttons[button] = PlayerInput(button)

    def __repr__(self):
        print(self.event_map)

    def process_event(self, event):
        """
        Process pygame events.

        :param event: The event to process.
        """
        raise NotImplementedError

    def get_events(self):
        """
        Get events.
        """
        for inp in self.buttons.values():
            if inp.held:
                yield inp
                inp.hold_time += 1
            elif inp.triggered:
                yield inp
                inp.triggered = False

    def press(self, button, value=1):
        """
        Press a button.

        :param button: Button to press.
        :param value: Value to press it with.
        """
        inp = self.buttons[button]
        inp.value = value
        if not inp.hold_time:
            inp.hold_time = 1

    def release(self, button):
        """
        Release a button.

        :param button: Button to release.
        """
        inp = self.buttons[button]
        inp.value = 0
        inp.hold_time = 0
        inp.triggered = True


class GamepadInput(EventHandler):
    """
    Gamepad input class.
    """

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

    def __init__(self, event_map=None, deadzone=0.25):
        EventHandler.__init__(self, event_map)

        self.deadzone = deadzone
        self.init_all_joysticks()

    def __repr__(self):
        print(GamepadInput.default_input_map)

    @staticmethod
    def init_all_joysticks():
        """
        Initialise all joysticks.
        """
        pg.joystick.init()
        for index in range(pg.joystick.get_count()):
            pg.joystick.Joystick(index).init()

    def process_event(self, event):
        """
        Process a joystick/game controller event.

        :param event: The event to process.
        """
        self.check_button(event)
        self.check_hat(event)
        self.check_axis(event)

    def check_button(self, event):
        """
        Check joystick button event.

        :param event: The event to check.
        """
        try:
            button = self.event_map[event.button]
            if event.type == pg.JOYBUTTONDOWN:
                self.press(button)
            elif event.type == pg.JOYBUTTONUP:
                self.release(button)
        except (KeyError, AttributeError):
            pass

    def check_hat(self, event):
        """
        Check joystick hat event.

        :param event: The event to check.
        """
        if event.type != pg.JOYHATMOTION:
            return
        hat_x, hat_y = event.value
        if hat_x == -1:
            self.press(actions.LEFT, value=hat_x * -1)
        elif hat_x == 0:
            self.release(actions.LEFT)
            self.release(actions.RIGHT)
        elif hat_x == 1:
            self.press(actions.RIGHT)

        if hat_y == -1:
            self.press(actions.DOWN, value=hat_y * -1)
        elif hat_y == 0:
            self.release(actions.DOWN)
            self.release(actions.UP)
        elif hat_y == 1:
            self.press(actions.UP)

    def check_axis(self, event):
        """
        Check joystick axis motion event.

        :param event: The event to check.
        """
        if event.type != pg.JOYAXISMOTION:
            return
        value = event.value

        if event.axis == 0:
            if abs(value) >= self.deadzone:
                if value < 0:
                    self.press(actions.LEFT, value * -1)
                else:
                    self.press(actions.RIGHT, value)
            else:
                self.release(actions.LEFT)
                self.release(actions.RIGHT)

        elif event.axis == 1:
            if abs(value) >= self.deadzone:
                if value < 0:
                    self.press(actions.UP, value * -1)
                else:
                    self.press(actions.DOWN, value)
            else:
                self.release(actions.UP)
                self.release(actions.DOWN)


class KeyboardInput(EventHandler):
    """
    Keyboard Input class.
    """

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

    def process_event(self, event):
        """
        Translate a pg event to an internal game event

        :type event: pg.event.Event
        """
        pressed = event.type == pg.KEYDOWN
        released = event.type == pg.KEYUP

        if pressed or released:
            # try to get game-specific action for the key
            try:
                button = self.event_map[event.key]
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
                self.release(actions.UNICODE)
                if pressed:
                    self.press(actions.UNICODE, event.unicode)
            except AttributeError:
                pass
