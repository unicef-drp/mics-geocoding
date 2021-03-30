## ###########################################################################
##
# CovariatesInputs.py
##
# Author: Etienne Delclaux
# Created: 17/03/2021 11:15:56 2016 (+0200)
##
# Description:
##
## ###########################################################################

import os

class CovariatesInputs():
    """ class that handle covariates inputs.
    """
    def __init__(self):
        self.input_csv = r'C:\Users\Janek\Documents\____UNICEF_GIS_STRATEGY\Projects\2020\MICS geocoding\Sample data\NorthMacedonia\covariates\mkd_input_covariates.txt'
        self.input_field_filename = 'FileName'
        self.input_field_fileformat = 'FileFormat'
        self.input_field_sumstat = 'SummaryStatistic'
        self.input_field_columnname = 'ColumnName'

        self.basefolder = Path(self.input_csv).parent
        self.out_file_name = os.path.join(self.basefolder, "output_covariates.csv")