"""recommender.py

Stuff for talking to the recommender
"""

from py4j.java_gateway import JavaGateway

class Recommender(object):
    
    def __init__(self):
        self.gateway = JavaGateway()
        self.mahout_recommender = self.gateway.entry_point.getRecommender()
        
        
   
def to_base36(value):
    """Convert a value to base36 representation"""
    
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    
    if not isinstance(value, (int, long)):
        raise TypeError

    if value == 0:
        return '0'
    
    sign = ''

    if value < 0:
        sign = '-'
     
    if 0 <= value < len(alphabet):
        return sign + alphabet[value] 
        
    result = []
 
    while value != 0:
        value, i = divmod(value, len(alphabet))
        result.append(alphabet[i])
        
    result.reverse()
 
    return sign + ''.join(result)