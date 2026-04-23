## ###########################################################################
##
# Logger.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description: Manage logging
##
## ###########################################################################

from qgis.core import Qgis, QgsMessageLog
from PyQt5 import QtCore


class ProgressBar(QtCore.QObject):
    """ Manager for progress bar update inside the plugin
                Acts asa static class, with callable method.
    """
    
    # Signal emitted when progress updates
    progressChanged = QtCore.pyqtSignal(int)  # Emits percentage (0-100)
    widget = None

    def __init__(self, ui_progress_bar):
        super().__init__()
        self.widget = ui_progress_bar
        self.hide() # hide by default
        self.progressChanged.connect(self.widget.setValue)
        self.update(0)  # Initialize at 0%

    def update(self, progress: int):
        """Called by processing classes to update progress"""
        # print(f"UPDATE PROGRESS BAR: {progress}%")
        self.progressChanged.emit(progress)

    def hide(self) -> None:
        # print("HIDE PROGRESS BAR")
        if self.widget:
            self.widget.setVisible(False)

    def show(self) -> None:
        # print("SHOW PROGRESS BAR")
        if self.widget:
            self.widget.setVisible(True)