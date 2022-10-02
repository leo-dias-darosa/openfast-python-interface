import sys
sys.setrecursionlimit(1000000)

from fast_nrel import wind

######################################## Customized  ########################################

import fast_nrel.Customized
from fast_nrel.Customized import FAST
from fast_nrel.Customized import fast_report

######################################## IEC61400-12 ########################################

import fast_nrel.IEC6140012
from fast_nrel.IEC6140012 import FAST
from fast_nrel.IEC6140012 import fast_report

######################################## IEC61400-13 ########################################

import fast_nrel.IEC6140013
from fast_nrel.IEC6140013 import FAST
from fast_nrel.IEC6140013 import fast_report


#### Get names ###
__all__=['wind','IEC6140012','IEC6140013','Customized']
