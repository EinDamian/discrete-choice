"""
This is a utility class. Here are functions, which are frequently used in the View
(See FileMenu and EditMenu)
"""

from PyQt5.QtWidgets import QMenu, QMessageBox


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

    def wrapper(*args, **kwargs):
        widget = args[0]  # the ColumnWidget/ModelWidget
        try:
            if kwargs:
                result = function(*args, **kwargs)
            elif len(args) > 1 and args[1]:
                result = function(*args)
            else:
                result = function(args[0])
            return result
        except OSError as error:
            # here the Error handling for the class ColumnWidget takes place
            error_message_box = QMessageBox(parent=widget)
            error_message_box.setText(str(error))
            error_message_box.exec()
            widget.update()

    return wrapper
