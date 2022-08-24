def comprehensive_cover(model, age, ins_type, body_type, usage, sum_assured):
    
    problem_models = []
    special_models = []
    
    if age > 12:
        return None
    
    if model in problem_models:
        if age > 12:
            return None
    
    if model in special_models:
        return f"Please call +254739881818 for a specialized quotation for a {model}"
    
    mark_up = 1.01
    
    if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
        if sum_assured < 750000:
            return None
        
        excess_protector = max(5000, (0.0025*sum_assured))
        pvt = max(5000, (0.0025*sum_assured))
        
        if 750000 <= sum_assured < 1000000:            
            premium = max(37500, 0.06 * sum_assured) * mark_up
            excess_protector = 0              
            return " {:6,.0f}".format(premium + excess_protector)
        
        elif 1000000 <= sum_assured < 1500000:            
            premium = max(37500, 0.05 * sum_assured) * mark_up              
            return " {:6,.0f}".format(premium + excess_protector)
        
        elif 1500000 <= sum_assured < 2500000:            
            premium = max(37500, 0.04 * sum_assured) * mark_up          
            return " {:6,.0f}".format(premium + excess_protector)
        
        elif 2500000 <= sum_assured <= 5000000:            
            premium = max(37500, 0.03 * sum_assured) * mark_up           
            return " {:6,.0f}".format(premium + excess_protector)
        
    elif ins_type in ["psv", "commercial"] and body_type not in ["motor_cycle", "tuktuk"] and usage == "own_goods":
        if sum_assured < 1000000:
            return None

        excess_protector = max(7500, (0.005*sum_assured)) 
        pvt = max(7500, (0.005*sum_assured))
         
        if 1000000 <= sum_assured < 2500000:      
            premium = max(50000, 0.05 * sum_assured) * mark_up         
            return " {:6,.0f}".format(premium + excess_protector)
        
        elif sum_assured >= 2500000:            
            premium = max(50000, 0.045 * sum_assured) * mark_up            
            return " {:6,.0f}".format(premium + excess_protector)


#Third party cover premium computations (TPO)
def tpo_cover(duration, ins_type, body_type, usage):
    
    mark_up = 1.01
    
    if duration == "annual":
        if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
            premium = 10000
            return " {:6,.0f}".format(premium * mark_up)
        
        elif ins_type == "commercial" and usage == "own_goods":
            premium = 15000
            return " {:6,.0f} per year".format(premium * mark_up)
