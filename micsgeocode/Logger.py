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


class Logger():
    """ Manager for logging inside the plugin
                Acts asa static class, with callable method.
        Basically, it behaves as a QGsMessageLog wrapper.
        It is helpful to encapsulate the handling Category field (==> tab in qgis)
    """
    CATEGORY = "MICS Geocode"
    widget = None

    @staticmethod
    def logInfo(message: str) -> None:
        QgsMessageLog.logMessage(message, Logger.CATEGORY, Qgis.Info)

    @staticmethod
    def logWarning(message: str) -> None:
        QgsMessageLog.logMessage(message, Logger.CATEGORY, Qgis.Warning)
        if Logger.widget:
            Logger.widget.setText("WARNING\n" + message)

    @staticmethod
    def logException(message: str, e: BaseException) -> None:
        messageException = "Error: {0}. Arguments: {1!r}".format(type(e).__name__, e.args)
        QgsMessageLog.logMessage(message + '\n' + messageException, Logger.CATEGORY, Qgis.Warning)
        if Logger.widget:
            Logger.widget.setText("ERROR\n" + message + '\n' + messageException)

    @staticmethod
    def logError(message: str) -> None:
        QgsMessageLog.logMessage(message, Logger.CATEGORY, Qgis.Critical)
        if Logger.widget:
            Logger.widget.setText("ERROR\n" + message)

    @staticmethod
    def logSuccess(message: str) -> None:
        QgsMessageLog.logMessage(message, Logger.CATEGORY, Qgis.Success)
        if Logger.widget:
            Logger.widget.setText(message)
