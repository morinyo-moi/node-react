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
        excess_protector = max(5000, (0.005*sum_assured))
        pvt = max(2500, (0.0025*sum_assured))
        
        if sum_assured <= 1000000:            
            premium = max(37500, 0.06*sum_assured)*mark_up        
            return " {:6,.0f}".format(premium + excess_protector)
        
        elif 1000000 < sum_assured <= 1500000:           
            premium = max(60000, 0.05*sum_assured)*mark_up               
            return " {:6,.0f}".format(premium + excess_protector)
        
        elif 1500000 < sum_assured <= 2500000:           
            premium = max(75000, 0.04*sum_assured)*mark_up          
            return " {:6,.0f}".format(premium + excess_protector)

        elif 2500000 < sum_assured <= 5000000:           
            premium = max(100000, 0.035*sum_assured)*mark_up          
            return " {:6,.0f}".format(premium + excess_protector)

        elif sum_assured > 5000000:           
            premium = max(175000, 0.03*sum_assured)*mark_up          
            return " {:6,.0f} ".format(premium + excess_protector)
        
       
    elif ins_type == "commercial" and body_type not in ["motor_cycle", "tuktuk", "heavy_equipment"]:
        excess_protector = max(5000, (0.005*sum_assured))
        pvt = max(2500, (0.0025*sum_assured))

        if usage == "general_cartage":           
            premium = max(100000, 0.07*sum_assured)*mark_up         
            return " {:6,.0f}".format(premium + excess_protector + pvt)
    
        elif usage == "own_goods":           
            premium = max(50000, 0.05*sum_assured)*mark_up         
            return " {:6,.0f}".format(premium + excess_protector + pvt)
    

#Third party cover premium computations (TPO)
def tpo_cover(duration, ins_type, tonnage, body_type, usage):
    
    mark_up = 1.01
    
    if duration == "annual":
        if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
            premium = 7500
            return " {:6,.0f}".format(premium * mark_up)
        
        elif ins_type == "commercial" and body_type not in ["motor_cycle", "tuktuk", "heavy_equipment"]:
            if usage == "own_goods":
                if tonnage <= 3:
                    premium = 7500
                elif 3 < tonnage <= 8:
                    premium = 12000
                elif tonnage > 8:
                    premium = 18000
                return " {:6,.0f}".format(premium * mark_up)
            elif usage == "general_cartage":
                if tonnage <= 3:
                    premium = 15000
                    return round(premium * mark_up), " {:6,.0f} per year".format(premium * mark_up)
                elif 3 < tonnage <= 20:
                    premium = 20000
                    return round(premium * mark_up), " {:6,.0f} per year".format(premium * mark_up)
                elif 20 < tonnage <= 30:
                    premium = 25000
                    return round(premium * mark_up), " {:6,.0f} per year".format(premium * mark_up)
                elif body_type == "primemover":
                    premium = 20000
                    return round(premium * mark_up), " {:6,.0f} per year".format(premium * mark_up)
