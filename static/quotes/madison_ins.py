def comprehensive_cover(age, ins_type, owner_type, body_type, usage, tonnage, seating_cap, sum_assured):
    
    mark_up = 1.01

    if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":

      excess_protector = max(5000, (0.005*sum_assured))
      pvt = max(2500, (0.0025*sum_assured))

      if sum_assured <= 1000000:
        premium = max(35000, 0.075  * sum_assured) * mark_up  
        return round(premium * mark_up), "Ksh {:6,.0f} per year Excluding excess protector".format(premium * mark_up)     
      
      elif 1000000 < sum_assured <= 2000000:
        premium = max(35000, 0.05* sum_assured) * mark_up        
      if 2000000 < sum_assured <= 3000000:
        premium = max(35000, 0.04* sum_assured) * mark_up 
      elif sum_assured > 3000000:
        premium = max(35000, 0.035* sum_assured) * mark_up        
        return round(premium + excess_protector), "Ksh {:6,.0f} per year Including excess protector".format(premium + excess_protector)
    
    elif ins_type == "commercial":
      excess_protector = max(5000, (0.005*sum_assured))
      pvt = max(5000, (0.005*sum_assured))

      if usage in ["own_goods", "general_cartage"] and body_type not in ["motor_cycle", "tuktuk"]:
        premium = max(50000, 0.045 * sum_assured) * mark_up     
        return round(premium + excess_protector), "Ksh {:6,.0f} per year Including excess protector".format(premium + excess_protector)   

      elif usage == "institutional"  and body_type not in ["motor_cycle", "tuktuk"]:
        premium = max(50000, 0.0375 * sum_assured) * mark_up
        return round(premium + excess_protector), "Ksh {:6,.0f} per year Including excess protector".format(premium + excess_protector)
    

def tpo_cover(duration, ins_type, owner_type, body_type, usage, tonnage, seating_cap):

  mark_up = 1.01
  if duration == "annual":
    if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
      premium = 7500       
      return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)
    elif ins_type == "commercial" and usage in ["own_goods", "general_cartage"] and body_type not in ["motor_cycle", "tuktuk"]:
      if tonnage <= 3:
        premium = 10000
        return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)
      elif 3 < tonnage <= 8:
        premium = 15000 
        return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)
      elif 8 < tonnage <= 20:
        premium = 20000
        return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)
      elif 20 < tonnage <= 30:
        premium = 25000        
        return round(premium * mark_up), "Ksh {:6,.0f} per year".format(premium * mark_up)
