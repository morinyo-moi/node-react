def comprehensive_cover(age, ins_type, owner_type, body_type, usage, tonnage, seating_cap, sum_assured):
      
      mark_up = 1.01

      if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
        excess_protector = 0
        pvt = max(5000, (0.005*sum_assured))
        
        if sum_assured >= 750000:
          if age <= 15:
            premium = max(30000, 0.0375 * sum_assured) * mark_up          
            return  " {:6,.0f}".format(premium + excess_protector + pvt)
      
      elif body_type == "motor_cycle":
          excess_protector = max(5000, (0.005*sum_assured))
          pvt = max(5000, (0.005*sum_assured))
          if age <= 3:
            if ins_type == "psv": 
              if sum_assured >= 110000:
                premium = max(5000, 0.05 * sum_assured) * mark_up  + 1000    
                return " {:6,.0f}".format(premium + excess_protector)
            elif ins_type == "private": 
              if sum_assured >= 100000:
                premium = max(5000, 0.05 * sum_assured) * mark_up + 1000
                return  " {:6,.0f}".format(premium + excess_protector)
      
      elif ins_type == "commercial":
            
            excess_protector = max(5000, (0.005*sum_assured))
            pvt = max(5000, (0.005*sum_assured))
              
            if sum_assured >= 750000:
                if age <= 15:
                    if usage in ["own_goods", "general_cartage"] and body_type not in ["motor_cycle", "tuktuk", "primemover"]:
                        premium = max(40000, 0.04 * sum_assured) * mark_up           
                        return " {:6,.0f}".format(premium + excess_protector)
      
                    elif usage in ["school_bus", "staff_bus", "institutional"]:
                        pll = 500
                        premium = max(40000, 0.04 * sum_assured) * mark_up + pll*seating_cap          
                        return " {:6,.0f}".format(premium + excess_protector)
                    
                    elif body_type in ["heavy_equipment", "primemover"] and usage == "agriculture":
                        premium = max(20000, 0.03 * sum_assured) * mark_up           
                        return " {:6,.0f}".format(premium + excess_protector)
                      
                    elif body_type == "primemover":
                        premium = max(50000, 0.04 * sum_assured) * mark_up           
                        return " {:6,.0f}".format(premium + excess_protector)
                   
      elif ins_type == "psv":
          excess_protector = max(5000, (0.005*sum_assured))
          pvt = max(5000, (0.005*sum_assured))
                      
          if sum_assured >= 750000:
              if age <= 15:
                  if body_type == "bus" and usage == "matatu":
                        if 6 <= seating_cap <= 35:
                            premium = 0.05 * mark_up * sum_assured   
                        elif seating_cap > 35:
                            premium = 0.06 * mark_up * sum_assured          
                        return " {:6,.0f}".format(premium + excess_protector)
                  elif usage in ["personal_taxi", "app_hailing", "chauffeur_cab"]:
                      pll = 500
                      premium = max(30000, 0.055 * sum_assured) * mark_up + pll*seating_cap          
                      return " {:6,.0f}".format(premium + excess_protector)
                  elif usage == "car_hire":
                      pll = 500
                      premium = max(30000, 0.06 * sum_assured) * mark_up + pll*seating_cap          
                      return  " {:6,.0f}".format(premium + excess_protector)
                          
            
def tpo_cover(duration, ins_type, body_type, usage, tonnage, seating_cap):
      mark_up = 1.2
      
      if duration == "annual":
        if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
          premium = 4580     
          return " {:6,.0f}".format(premium * mark_up)
        
        elif body_type == "motor_cycle":
          if ins_type == "psv": 
            premium = 3651  
          elif ins_type == "private": 
            premium = 3194      
            return " {:6,.0f} ".format(premium * mark_up)
        
        elif ins_type == "commercial":
            if usage in ["own_goods", "general_cartage"] and body_type not in ["motor_cycle", "tuktuk"]:
                if tonnage <= 3:
                  premium = 5665
                elif 3 < tonnage <= 8:
                    premium = 8176 
                elif 8 < tonnage <= 10:
                    premium = 12195 
                elif 10 < tonnage <= 15:
                    premium = 15208 
                elif 15 < tonnage <= 20:
                    premium = 20231
                elif tonnage > 20:
                    premium = 25354 
                return  " {:6,.0f}".format(premium * mark_up)
            elif body_type in ["heavy_equipment", "primemover"] and usage == "agriculture":
                premium = 4190
                return " {:6,.0f}".format(premium * mark_up)
            elif body_type == "primemover":
                premium = 15190
                return " {:6,.0f}".format(premium * mark_up)
              
        elif ins_type == "psv": 
            if usage == "car_hire":
                pll = 500
                if 4 <= seating_cap <= 9: 
                    premium = 7500* mark_up + seating_cap*pll  
                elif 9 < seating_cap <= 25: 
                    premium = 12500* mark_up + seating_cap*pll    
                elif seating_cap > 25: 
                    premium = 15000* mark_up + seating_cap*pll   
                return  " {:6,.0f}".format(premium)
            elif usage in ["school_bus", "staff_bus", "institutional"]:
                pll = 500
                if 7 <= seating_cap <= 25:
                    premium = 8500 * mark_up + seating_cap*pll  
                elif 25 < seating_cap <= 105:
                    premium = 15000 * mark_up + seating_cap*pll        
                return " {:6,.0f}".format(premium)
            elif usage in ["personal_taxi", "app_hailing", "chauffeur_cab"]:
                    pll = 500
                    premium = 5042 * mark_up + seating_cap*pll
                    return " {:6,.0f}".format(premium)
