from PyQt5.QtWidgets import QMenu


class UIUtil:
    @staticmethod
    def get_action(menu: QMenu, action_name: str):
        for action in menu.actions():
            if action.objectName() == action_name:
                return action
        return None  # This never occurs in this program context
