import json
import numpy as np

from sklearn.externals import joblib
from TextProcessing import TextProcessing
from collections import OrderedDict

import os
import sys

fullList = ['ope','con','ext','agr','neu'] 
class jsonExtractor(object):
    """ Json object related processes 
    
     Attributes:
         self.typeList: contains the big5 trait list which need to be returned
                   default: return all big5 traits
                   full list: ['ope','con','ext','agr','neu']
    
    """
    

    
    
    def getJsonStr(self, text, typeList=['ope','con','ext','agr','neu']):
        """ get the Json String according to the predicted data (predict model is determined by the typeList)
        Args: 
            text: a string of text used to predict big5 trait   
            typeList: contains the big5 trait list which need to be returned  
        Returns:
            jsonStr: a Json String, e.g., {"ope": 4.2, "neu": 2.31, "con": 3.09, "ext": 3.69, "agr": 3.08}  
        """

        sys.path.insert(1,os.path.dirname(__file__))
        
        model_path =  os.path.join(os.path.dirname(__file__), """./model/""")

        data = OrderedDict()
        
        tp = TextProcessing()
        X = tp.extractFeature(text)
        X = np.array(X)
            
        for t in typeList:
            if t not in fullList:
                continue
            else:
                model_name = """Predictor_"""+t+""".pkl"""
                print model_path+model_name
                model = joblib.load(model_path+model_name)
                y_pred = model.test(X)  
                data[t] = y_pred[0]
        
        jsonStr = json.dumps(data)       
        return jsonStr
                
