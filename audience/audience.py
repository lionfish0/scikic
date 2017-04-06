""" Simple insight generation

The main scikic was developed to perform bayesian inference over a bayesian
network to generate insights. This API is far more simple. The classes in /simple
each handle one of the basic insights, originally developed for the Energy
insight selection.
"""

import numpy as np
 
class Simple(object):
    """ Base class to create basic insights
        call insight, values = getInsight(data)
        
        parameters:
            data = dictionary (e.g. results of a survey, packaged and sent from the device)
        returns
            insight = string (simple insight message)
            values = dictionary (of values we'll provide back to the device)
    """

    def getInsight(self, data):
        return None, None
