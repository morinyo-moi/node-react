def comprehensive_cover(model, age, ins_type, body_type, usage, sum_assured, seat_cap):
    
    problem_models = ['subaru', 'probox', 'succeed', 'sienta', 'noah', 'voxy']
    special_models = ['acura', 'cadillac', 'citroen', 'ferrari', 'lamborghini', 'bentley', 'maserati', 'MG', 'dodge']
    

    if age > 15:
        return None

    if model in special_models:
        return f"Please call us on +254739881818 for a special quotation for {model}"

    
    if model in problem_models:
        if age > 10:
            return None 
         
    mark_up = 1.01
      
    if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
        if sum_assured < 500000:
          return None
        
        excess_protector = max(3000, (0.0025*sum_assured)) 
        pvt = max(3000, (0.0025*sum_assured))
        
        if 500000 <= sum_assured <= 1000000:
            if model in problem_models:
                premium = max(37500, 0.075 * sum_assured) * mark_up
            else:
                premium = max(37500, 0.06 * sum_assured) * mark_up    
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif 1000000 < sum_assured <= 1500000: 
            if model in problem_models:
                premium = max(60000, 0.0725 * sum_assured) * mark_up 
            else:           
                premium = max(60000, 0.05 * sum_assured) * mark_up           
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif 1500000 < sum_assured <= 2500000:  
            if model in problem_models:
                premium = max(75000, 0.07 * sum_assured) * mark_up 
            else:          
                premium = max(75000, 0.04 * sum_assured) * mark_up           
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif 2500000 < sum_assured <= 5000000:            
            premium = max(100000, 0.035 * sum_assured) * mark_up          
            return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)

        elif sum_assured > 5000000:            
            premium = max(175000, 0.03 * sum_assured) * mark_up           
            return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
    elif ins_type in ["psv", "commercial"] and body_type not in ["motor_cycle", "tuktuk"]:
        if sum_assured < 500000:
          return None
        
        excess_protector = max(5000, (0.005*sum_assured)) 
        pvt = max(3000, (0.0045*sum_assured))
        
        if  usage == "own_goods":
            if age <= 10:
                premium = max(50000, 0.05 * sum_assured) * mark_up 
            else:          
                premium = max(50000, 0.0525 * sum_assured) * mark_up           
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif  usage == "general_cartage":
            if age <= 10:
                premium = max(100000, 0.07 * sum_assured) * mark_up 
            else:          
                premium = max(100000, 0.0725 * sum_assured) * mark_up           
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif  usage in ["chauffeur_cab", "app_hailing"]:
            pll = 500
            if age <= 10:
                premium = max(50000, 0.05 * sum_assured) * mark_up + pll*seat_cap 
            else:          
                premium = max(50000, 0.055 * sum_assured) * mark_up + pll*seat_cap          
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector and PLL".format(premium + excess_protector)
        
        elif  usage == "tanker":
            if age <= 10:
                premium = max(50000, 0.07 * sum_assured) * mark_up 
            else:          
                premium = max(50000, 0.075 * sum_assured) * mark_up      
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif  usage == "driving_school":
            if age <= 10:
                premium = max(50000, 0.05 * sum_assured) * mark_up 
            else:          
                premium = max(50000, 0.055 * sum_assured) * mark_up       
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif  usage in ["school_bus", "institutional" ]:
            pll = 250
            if age <= 10:
                premium = max(50000, 0.04 * sum_assured) * mark_up + pll*seat_cap  
            else:          
                premium = max(50000, 0.045 * sum_assured) * mark_up + pll*seat_cap        
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector and PLL".format(premium + excess_protector)
        
        elif  usage == "ambulance":
            if age <= 10:
                premium = max(50000, 0.06 * sum_assured) * mark_up 
            else:          
                premium = max(50000, 0.065 * sum_assured) * mark_up       
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif  body_type == "heavy_equipment" and usage == "agriculture":
            if age <= 10:
                premium = max(50000, 0.03 * sum_assured) * mark_up 
            else:          
                premium = max(50000, 0.035 * sum_assured) * mark_up       
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)
        
        elif  body_type == "heavy_equipment" and usage != "agriculture":
            if age <= 10:
                premium = max(100000, 0.03 * sum_assured) * mark_up 
            else:          
                premium = max(100000, 0.035 * sum_assured) * mark_up       
                return round(premium + excess_protector), "Ksh {:6,.0f} per year Inclusive of excess protector".format(premium + excess_protector)

#Third party cover premium computations (TPO)
def tpo_cover(duration, ins_type, body_type, usage, tonage, seat_cap):
    
    mark_up = 1.01
    
    if duration == "annual":
        
        if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
            premium = 7500
            return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium* mark_up)

        elif ins_type in ["psv", "commercial"] and body_type not in ["motor_cycle", "tuktuk"]:
            
            if  usage == "own_goods" and body_type != "primemover":
                if tonage <= 3:
                    premium = 7500
                elif 3 < tonage <= 8:
                    premium = 12000
                elif 8 < tonage <= 10:
                    premium = 18000
                    return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium* mark_up)
               
            if  usage == "general_cartage" and body_type != "primemover":
                if tonage <= 3:
                    premium = 7500
                elif 3 < tonage <= 8:
                    premium = 12000
                elif 8 < tonage <= 20:
                    premium = 20000
                elif 20 < tonage <= 30:
                    premium = 25000
                elif tonage > 30:
                    premium = 25000 + (tonage-30)*500
                    return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium* mark_up)
            
            if  body_type == "primemover":
                premium = 20000
                return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium* mark_up)
            
            if  usage in ["chauffeur_cab", "app_hailing"]:
                pll = 500
                if seat_cap <= 9:
                    premium = 7500 * mark_up + pll*seat_cap
                elif 9 < seat_cap <= 25:
                    premium = 12500 * mark_up + pll*seat_cap
                elif seat_cap > 25:
                    premium = 15000 * mark_up + pll*seat_cap    
                    return round(premium), "Ksh {:6,.0f} per year Inclusive of PLL".format(premium)
            
            if  usage == "driving_school":
                if body_type == "personalcar":
                  premium = 7500 
                else:
                  premium = 10000   
                  return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium* mark_up)
            
            if  usage in ["school_bus", "staff_bus", "institutional"]:
                pll = 250
                if seat_cap <= 9:
                    premium = 7500 + pll*seat_cap
                elif 9 < seat_cap <= 25:
                    premium = 15000 + pll*seat_cap
                elif seat_cap > 25:
                    premium = 20000 + pll*seat_cap    
                    return round(premium), "Ksh {:6,.0f} per year Inclusive of PLL".format(premium)
            
            if  body_type == "heavy_equipment" and usage == "agriculture":
                premium = 5000  
                return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium* mark_up)
            
            if  body_type == "heavy_equipment" and usage == "other_equipment":
                return "Please call +254739881818 for a speciallized quotation for this equipment"   
