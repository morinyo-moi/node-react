def comprehensive_cover(model, age, ins_type, body_type, owner_type, usage, sum_assured):
    
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
        excess_protector = max(5000, (0.0025*sum_assured))
        pvt = max(2500, (0.0025*sum_assured))
        
        if sum_assured <= 2000000:            
            premium = max(50000, 0.06* sum_assured) * mark_up         
            return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif 2000000 < sum_assured <= 3000000:           
            premium = max(50000, 0.0425 * sum_assured)*mark_up              
            return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif sum_assured > 3000000:           
           premium = max(50000, 0.03* sum_assured)*mark_up         
           return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
       
    elif ins_type == "commercial" and usage in ["own_goods", "general_cartage"]:
        excess_protector = max(10000, (0.005*sum_assured))
        pvt = max(3000, (0.0035*sum_assured))
        
        if sum_assured < 3000000:            
            premium = max(75000, 0.045* sum_assured) * mark_up         
            return round(premium + excess_protector + pvt), "Ksh {:6,.0f} per year Inclusive of excess protector and PVT".format(premium + excess_protector + pvt)
        
        elif sum_assured >= 3000000:           
            premium = max(75000, 0.035 * sum_assured)*mark_up              
            return round(premium + excess_protector + pvt), "Ksh {:6,.0f} per year Inclusive of excess protector and PVT".format(premium + excess_protector + pvt)


#Third party cover premium computations (TPO)
def tpo_cover(duration, ins_type, tonnage, body_type, usage):
    
    mark_up = 1.01
    
    if duration == "annual":
        if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
            premium = 10000
            return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)
        
        elif ins_type == "commercial" and usage in ["own_goods", "general_cartage"]:
            if tonnage <= 8:
              premium = 25000 * mark_up
            else:
              premium = (25000 + ((tonnage-8)*2000)) * mark_up
              return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)
