def comprehensive_cover(model, age, ins_type, body_type, usage, sum_assured, tonnage, seat_cap):
    
    problem_models = []
    special_models = []
    

    if sum_assured < 500000:
      return None

    if age > 15:
      return None  
         
    mark_up = 1.01
      
    if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":

        excess_protector = max(5000, (0.0025*sum_assured)) 
        pvt = max(2500, (0.0025*sum_assured))
        
        if 500000 <= sum_assured < 1500000:
          premium = max(37500, 0.06 * sum_assured) * mark_up 
          return " {:6,.0f}".format(premium + excess_protector)
        elif 1500000 <= sum_assured < 2500000:
          premium = max(37500, 0.04 * sum_assured) * mark_up 
          return " {:6,.0f}".format(premium + excess_protector)
        elif 2500000 <= sum_assured < 4000000:
          premium = max(37500, 0.03 * sum_assured) * mark_up 
          return " {:6,.0f}".format(premium + excess_protector)
        if sum_assured > 4000000:
          premium = max(37500, 0.03 * sum_assured) * mark_up 
          return " {:6,.0f}".format(premium + excess_protector)
        
    elif ins_type in ["psv", "commercial"] and usage == "own_goods" and body_type not in ["motor_cycle", "tuktuk", "heavy_equipment"]:

        excess_protector = max(5000, (0.005*sum_assured)) 
        pvt = max(2500, (0.0025*sum_assured))

        if tonnage <= 3: 
          if 500000 <= sum_assured < 2000000:      
              premium = max(37500, 0.06* sum_assured) * mark_up         
              return " {:6,.0f}".format(premium + excess_protector)
          
          elif sum_assured >= 2000000:            
              premium = max(37500, 0.04 * sum_assured) * mark_up            
              return " {:6,.0f}".format(premium + excess_protector)

        elif tonnage > 3: 
          if 500000 <= sum_assured < 2000000:      
              premium = max(50000, 0.07 * sum_assured) * mark_up          
              return " {:6,.0f}".format(premium + excess_protector)
          
          elif sum_assured >= 2000000:            
              premium = max(50000, 0.05 * sum_assured) * mark_up            
              return " {:6,.0f}".format(premium + excess_protector)
              
    elif ins_type in ["psv", "commercial"] and usage == "general_cartage" and body_type not in ["motor_cycle", "tuktuk", "heavy_equipment"]:

        excess_protector = max(5000, (0.005*sum_assured)) 
        pvt = max(2500, (0.0025*sum_assured))

        if tonnage <= 3: 
          if 500000 <= sum_assured < 2000000:      
              premium = max(37500, 0.06 * sum_assured) * mark_up         
              return " {:6,.0f} ".format(premium + excess_protector)
          
          elif sum_assured >= 2000000:            
              premium = max(37500, 0.04 * sum_assured) * mark_up            
              return " {:6,.0f}".format(premium + excess_protector)

        elif tonnage > 3: 
          if 500000 <= sum_assured < 2000000:      
              premium = max(50000, 0.07 * sum_assured) * mark_up          
              return " {:6,.0f}".format(premium + excess_protector)
          
          elif sum_assured >= 2000000:            
              premium = max(50000, 0.055 * sum_assured) * mark_up            
              return " {:6,.0f}".format(premium + excess_protector)

    elif ins_type in ["psv", "commercial"] and usage in ["chauffeur_cab", "app_hailing"]:

        excess_protector = 0
        pvt = max(2500, (0.0025*sum_assured))
        pll = 500

        if 500000 <= sum_assured < 4000000:     
            premium = max(40000, 0.06 * sum_assured) * mark_up + pll*seat_cap         
            return " {:6,.0f}".format(premium + excess_protector)
        elif sum_assured >= 4000000:      
            premium = max(40000, 0.06 * sum_assured) * mark_up + pll*seat_cap           
            return " {:6,.0f} ".format(premium + excess_protector)

#Third party cover premium computations (TPO)
def tpo_cover(duration, ins_type, body_type, usage, tonnage, seat_cap):
      
    mark_up = 1.01
    
    if duration == "annual":
        
        if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
          premium = 7500
          return  " {:6,.0f}".format(premium * mark_up)

        elif ins_type in ["psv", "commercial"] and usage == "own_goods" and body_type not in ["motor_cycle", "tuktuk", "heavy_equipment"]:
          if tonnage <= 3:
            premium = 7500
          elif 3 < tonnage <= 8:
            premium = 10000
          elif 8 < tonnage <= 15:
            premium = 12500
          elif tonnage > 15:
            premium = 20000
          return  " {:6,.0f} ".format(premium * mark_up)

        elif ins_type in ["psv", "commercial"] and usage == "general_cartage" and body_type not in ["motor_cycle", "tuktuk", "heavy_equipment"]:
          if tonnage <= 3:
            premium = 7500
          elif 3 < tonnage <= 8:
            premium = 10000
          elif 8 < tonnage <= 15:
            premium = 15000
          elif tonnage > 15:
            premium = 20000
          return round(premium * mark_up), " {:6,.0f}".format(premium * mark_up)
