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

    @staticmethod
    def logInfo(message: str) -> None:
        QgsMessageLog.logMessage(message, Logger.CATEGORY, Qgis.Info)

    @staticmethod
    def logWarning(message: str) -> None:
        QgsMessageLog.logMessage(message, Logger.CATEGORY, Qgis.Warning)

    @staticmethod
    def logError(message: str) -> None:
        QgsMessageLog.logMessage(message, Logger.CATEGORY, Qgis.Critical)

    @staticmethod
    def logSuccess(message: str) -> None:
        QgsMessageLog.logMessage(message, Logger.CATEGORY, Qgis.Success)
