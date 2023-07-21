"""
This is a utility class. Here are functions, which are frequently used in the View
(See FileMenu and EditMenu)
"""

import traceback
from PyQt5.QtWidgets import QMenu, QMessageBox, QErrorMessage

from src.model.SnapshotError import SnapshotError


def get_action(menu: QMenu, action_name: str):
    """
    This function finds buttons of a menu, so the button
    can be connected to a specific function in the code.
    @param menu: The menu, where the button should be found
    @type menu: QMenu
    @param action_name: The name  of the button
    @type action_name: str
    @return: The button (action)
    @rtype: QAction
    """
    for action in menu.actions():
        if action.objectName() == action_name:
            return action
    return None  # This never occurs in this program context


def display_exceptions(function):
    """Wrapper function with try block used to displaying occurring errors to the user.
    Intended to be used on the public functions of class ColumnWidget and ModelWidget.
    Widget needs function update().

    Args:
        function (function): function to be wrapped in this try block.
    """

    def __wrapper(*args, **kwargs):
        widget = args[0]

        def __show_error(error):
            # here the Error handling takes place
            error_message_box = QMessageBox(parent=widget)
            error_message_box.setIcon(QMessageBox.Critical)
            error_message_box.setWindowTitle(type(error).__name__)
            error_message_box.setText(str(error))
            error_message_box.exec()
            widget.update()
            traceback.print_exception(error)  # show error in konsole additionally

        try:
            if kwargs:
                result = function(*args, **kwargs)
            elif len(args) > 1 and args[1]:
                result = function(*args)
            else:
                result = function(args[0])
            return result
        except SnapshotError as e:
            __show_error(e.parent)
        except Exception as e:
            __show_error(e)

    return __wrapper
