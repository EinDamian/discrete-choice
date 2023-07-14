from PyQt5.QtWidgets import QMenu


class UIUtil:
    """
    This is a utility class. Here are functions, which are frequently used in the View
    (See FileMenu and EditMenu)
    """
    @staticmethod
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
