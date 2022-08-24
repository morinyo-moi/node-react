def comprehensive_cover(model, age, ins_type, body_type, usage, seat_cap, sum_assured):
    
    problem_models = ["probox", "succeed", "sienta", "voxy", "noah"]
    special_models = []
    
    if sum_assured < 750000:
        return None
    
    if model in problem_models:
        return None
    
    if model in special_models:
        return f"Please call +254739881818 for a specialized quotation for a {model}"
    
    mark_up = 1.01
    
    if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
        if age > 15:
          return None

        excess_protector = max(5000, (0.005*sum_assured))
        pvt = max(3000, (0.0025*sum_assured))
        
        if sum_assured <= 1500000:            
            premium = max(37500, 0.06* sum_assured)*mark_up        
            return round(premium), "Ksh {:6,.0f} per year Excluding excess protector".format(premium)
        
        elif 1500000 < sum_assured <= 2500000:           
            premium = max(60000, 0.04* sum_assured)*mark_up               
            return round(premium + excess_protector), "Ksh {:6,.0f} per year Including excess protector".format(premium + excess_protector)
        
        elif sum_assured > 2500000:           
            premium = max(37500, 0.03* sum_assured)*mark_up          
            return round(premium + excess_protector), "Ksh {:6,.0f} per year Including excess protector".format(premium + excess_protector)
        
       
    elif ins_type == "commercial":
        if age > 12:
          return None

        excess_protector = max(5000, (0.005*sum_assured))
        pvt = max(3500, (0.0035*sum_assured))

        if usage == "general_cartage":           
            premium = max(100000, 0.07* sum_assured)*mark_up         
            return round(premium + excess_protector), "Ksh {:6,.0f} per year Including excess protector".format(premium + excess_protector)
    
        elif usage == "own_goods":           
            premium = max(50000, 0.05* sum_assured)*mark_up         
            return round(premium + excess_protector), "Ksh {:6,.0f} per year Including excess protector".format(premium + excess_protector)
   
    elif ins_type == "psv":
        if age > 12:
          return None
        if usage in ["chauffeur_cab", "app_hailing"]: 
            pll=500          
            premium = max(52000, 0.06* sum_assured)*mark_up  + pll*seat_cap       
            return round(premium), "Ksh {:6,.0f} per year Excluding excess protector".format(premium)
    

#Third party cover premium computations (TPO)
def tpo_cover(duration, ins_type, tonnage, body_type, usage):
    
    mark_up = 1.01
    
    if duration == "annual":
        if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
            premium = 7500
            return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)

        elif ins_type == "commercial":
          if usage == "own_goods":
            if tonnage <= 3:
              premium = 7500
            elif 3 < tonnage <= 8:
              premium = 11000
            elif tonnage > 8:
              premium = 15000
              return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)
          elif usage == "general_cartage":
            if tonnage <= 8:
              premium = 7500
            elif 8 < tonnage <= 20:
              premium = 12000
            elif 20 < tonnage <= 30:
              premium = 18000
            elif body_type == "primemover":
              premium = 15000
              return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)
