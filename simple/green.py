""" Green Question

Generates an insight reporting on the green credentials of the citizen.
"""

import numpy as np
from simple import Simple
 
class Green(Simple):
    """ Base class to create basic insights
        call insight, values = getInsight(data)
        
        parameters:
            data = dictionary (e.g. results of a survey, packaged and sent from the device)
        returns
            insight = string (simple insight message)
            values = dictionary (of values we'll provide back to the device)
    """

    categories = [{'name':'Green Daily Behaviour','weight':0.4}, {'name':'Green Home','weight':0.3}, {'name':'Green in Shopping Behaviour','weight':0.2}, {'name':'Transport','weight':0.1}]
    
    final_insights = [{'range_min':80,'range_max':101,'label':'Always green'},{'range_min':60,'range_max':80,'label':'Mostly green'},{'range_min':40,'range_max':60,'label':'Occasionally green'},{'range_min':20,'range_max':40,'label':'Rarely green'},{'range_min':-1,'range_max':20,'label':'Never green'}]

    #it wasn't necessary to actually describe the question specifically here, the answer_score lists would have done, but I think this might help with debugging etc later.
    #Green Daily Behaviour
    heating = {'name':'heating','text':'When at home during the winter, how warm do you keep your house?','weight':20,'answer_scores':[20,40,60,80,100,60,20]}
    aircon = {'name':'aircon','text':'Similarly when at home during the summer, to what temperature do you set your digital air conditioner to?','weight': 15,'answer_scores': [100,80,60,40,20,100,60]} 
    lights={'name':'lights','text':'Do you instantly turn the lights off when you don\'t need them anymore e.g. when you switch over to another room?', 'weight': 15, 'answer_scores':[100,80,60,40,0]}
    tumble={'name':'tumble','text':'How regularly, if at all, do you tumble dry your clothes?','weight': 10, 'answer_scores':[0,40,60,100,100]}
    bike={'name':'bike','text':'Do you walk or bike short distances e.g. when you pop-over to the local shop or for running quick errands?', 'weight': 15, 'answer_scores':[0,40,80,100]}
    recycle={'name':'recycle','text':'How much do you recycle at home?','weight': 15, 'answer_scores':[0,40,80,100]}
    bags={'name':'bags','text':'How often do you use the plastic bags provided at supermarkets and shops at checkout?','weight': 10, 'answer_scores':[100,80,40,0]}
    #Green Home
    energy={'name':'energy','text':'Thinking about your home energy (gas & electricity), are you on a green tariff?','weight': 40, 'answer_scores':[0,0,80,80,100]}
    glazing={'name':'glazing','text':'Do your windows have double-glazing','weight':10, 'answer_scores':[100,0,20]}
    insulation={'name':'insulation','text':'How good would you consider your wall and floor insulation to be?','weight': 20, 'answer_scores':[100,80,60,20,50,50]}
    systems={'name':'systems','text':'Which, if any, of these green energy systems do you have in your home?','weight': 30, 'answer_scores':[80,60,60,60,40,0], 'max_score':100}
    #Shopping behaviour
    energyrating={'name':'energyrating','text':'Is a home appliance\'s energy rating an important consideration at time of purchase?','weight': 30, 'answer_scores':[40,40,60,100,0]}
    ecofriendly={'name':'ecofriendly','text':'When out grocery shopping, is a product\'s eco-friendliness an important consideration at time of purchase?','weight': 40, 'answer_scores':[40,60,80,100,0]}
    packaging={'name':'packaging','text':'Do you choose products with minimal/re-usable packaging whenever possible?','weight': 30, 'answer_scores':[40,60,80,100,0]}
    #Trasport
    car={'name':'car','text':'When you last bought a car, if ever, how important was its carbon emissions in your decision making process?','weight': 50, 'answer_scores':[0,20,40,80,100,50]}
    publictransport={'name':'publictrasport','text':'Is public transport a preferred means of transport for you?','weight': 50, 'answer_scores':[0,60,80,100]}
    
    
    green_daily_questions = [heating,aircon,lights,tumble,bike,recycle,bags]
    green_home = [energy,glazing,insulation,systems]
    shopping = [energyrating, ecofriendly,packaging]
    transport = [car,publictransport]
    questions = [green_daily_questions, green_home, shopping, transport]
    
    def getInsight(self, data):
        all_scores = [] #raw scores (unweighted)
        category_scores = [] #the weighted scores combined into each category
        
        values = {'debug':[]}
        insight_messages = []
        
        debug_question_list = [] #temporary to help with debugging
        
        if 'answers' in data:
            for data_category,question_category in zip(data['answers'],self.questions):
                question_scores = []
                category_score = 0
                for responses, question in zip(data_category, question_category):
                    try:
                        score = 0
                        for response in responses:
                            score += question['answer_scores'][response] #todo, add exception handling?
                        debug_question_list.append([question['name'],question['text'],responses])
                    except (IndexError, TypeError):
                        score = 0 #not sure what to do here...
                        values['debug'].append('Error while handling question response value')
                        values['debug'].append(responses)
                    if 'max_score' in question:
                        if score>question['max_score']:
                            score = question['max_score']
                    category_score += score * question['weight']/100.0
                    question_scores.append(score)
                all_scores.append(question_scores)
                category_scores.append(category_score)
                
        overall_score = 0
        for cat,cat_score in zip(self.categories,category_scores):
            overall_score += cat_score*cat['weight']
            
        values['overall_score'] = overall_score                
        values['category_scores'] = category_scores
        values['all_scores'] = all_scores
        
        values['debug'].append(debug_question_list)
        print overall_score
        for insight_range in self.final_insights:
            print insight_range['range_min'], insight_range['range_max']
            if (overall_score>=insight_range['range_min']) and (overall_score<insight_range['range_max']):
                insight_messages.append(insight_range['label'])
        
        return insight_messages, values

