from PyQt5.QtWidgets import QMenu


class UIUtil:

    def getAction(menu : QMenu, actionName : str):
        for action in menu.actions():
            if action.objectName() == actionName:
                return action
        return None #This never occurs in this program context