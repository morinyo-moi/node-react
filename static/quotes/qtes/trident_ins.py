#Comprehensive cover premium computations
def comprehensive_cover(age, ins_type, owner_type, body_type, usage, tonnage, seating_cap, sum_assured):

    if age > 20:
      return None

    mark_up = 1.01

    if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":

      excess_protector = 0
      pvt = 0

      if age <= 15:
        if sum_assured < 1000000:
          premium = max(15000, 0.04  * sum_assured) * mark_up          
        elif sum_assured >= 1000000:
          premium = max(15000, 0.035 * sum_assured) * mark_up          
        return " {:6,.0f} ".format(premium + excess_protector)

      elif 15 < age <= 20:
        if sum_assured < 1000000:
          premium = max(20000, 0.048* sum_assured) * mark_up         
        elif sum_assured > 1000000:
          premium = max(20000, 0.04* sum_assured) * mark_up         
        return " {:6,.0f} ".format(premium + excess_protector)
        
    elif ins_type == "commercial" and body_type == "pickup" and usage != "private":
      excess_protector = 0
      pvt = 0
      if age <= 15:
        if sum_assured < 1000000:
          premium = max(15000, 0.045 * sum_assured)  * mark_up          
        elif sum_assured >= 1000000:
          premium = max(15000, 0.04 * sum_assured) * mark_up          
        return " {:6,.0f} ".format(premium + excess_protector)
      
      elif 15 < age <= 20:
        if sum_assured < 1000000:
          premium = max(20000, 0.05* sum_assured) * mark_up          
        elif sum_assured > 1000000:
          premium = max(20000, 0.045* sum_assured) * mark_up         
        return " {:6,.0f}".format(premium + excess_protector)
    
    elif ins_type == "commercial" and usage in ["own_goods", "general_cartage"] and body_type not in ["pickup", "motor_cycle", "tuktuk", "heavy_equipment"]:
      excess_protector = 0
      pvt = 0
      if age <= 15:
        if sum_assured < 1000000:
            premium = max(20000, 0.0525 * sum_assured) * mark_up  
            return " {:6,.0f}".format(premium + excess_protector)
        elif sum_assured >= 1000000:
            premium = max(20000, 0.045 * sum_assured) * mark_up          
            return " {:6,.0f}".format(premium + excess_protector)
      
      elif 15 < age <= 20:
        if sum_assured < 1000000:
            premium = max(15000, 0.0575* sum_assured) * mark_up  
            return " {:6,.0f}".format(premium + excess_protector)
        elif sum_assured > 1000000:
            premium = max(20000, 0.0525* sum_assured) * mark_up          
            return " {:6,.0f}".format(premium + excess_protector)

      elif body_type == "primemover":
        if age <= 15:
          if sum_assured < 1000000:
              premium = max(20000, 0.0475 * sum_assured) * mark_up   
              return " {:6,.0f}".format(premium + excess_protector)
          elif sum_assured > 1000000:
              premium = max(20000, 0.045 * sum_assured) * mark_up  
              return " {:6,.0f}".format(premium + excess_protector)

            
    elif ins_type == "motor_trade" and owner_type in ["yard", "showroom"]:

      excess_protector = 0
      pvt = 0

      if age <= 8:
        premium = max(20000, 0.04 * sum_assured) * mark_up  
        return " {:6,.0f}".format(premium + excess_protector)
        
    elif usage in ["school_bus", "staff_bus", "institutional"]:
      excess_protector = 0
      pvt = 0
      premium = max(15000, 0.045 * sum_assured) * mark_up  
      return " {:6,.0f}".format(premium + excess_protector)
    
    elif body_type == "motor_cycle":
      excess_protector = 0
      pvt = 0
      if ins_type == "psv": 
        premium = max(6500, 0.035 * sum_assured) * mark_up  
      else:
        premium = max(4500, 0.03 * sum_assured) * mark_up  
      return " {:6,.0f}".format(premium + excess_protector)

    elif body_type == "tuktuk":
      excess_protector = 0
      pvt = 0
      if ins_type == "psv": 
        pll = 250
        premium = max(12500, 0.035 * sum_assured) * mark_up + (pll*seating_cap) 
        return " {:6,.0f}".format(premium + excess_protector)
      else:
        premium = max(7500, 0.03 * sum_assured) * mark_up  
        return " {:6,.0f} ".format(premium + excess_protector)
        
    elif usage == "tanker":
      excess_protector = 0
      pvt = 0
      if age <= 15:
        premium = max(30000, 0.0675 * sum_assured) * mark_up  
        return " {:6,.0f} ".format(premium + excess_protector)
      else:
        pass

    
    elif usage in ["chauffeur_cab", "app_hailing"] and ins_type == "psv":
      pll = 500
      excess_protector = 0
      pvt = 0
      if age <= 15:
        if sum_assured < 1000000:
          premium = max(20000, 0.0475 * sum_assured) * mark_up + (pll*seating_cap) 
        elif sum_assured >= 1000000:
          premium = max(20000, 0.045 * sum_assured) * mark_up + (pll*seating_cap) 
        return " {:6,.0f}".format(premium + excess_protector)
    
    elif usage == "driving_school":
      pll = 500
      excess_protector = 0
      pvt = 0
      if sum_assured < 1000000:
        premium = max(20000, 0.045 * sum_assured) * mark_up + (pll*seating_cap) 
      elif sum_assured >= 1000000:
        premium = max(20000, 0.0425 * sum_assured) * mark_up + (pll*seating_cap) 
      return " {:6,.0f}".format(premium + excess_protector)
    
    elif usage == "agriculture" and body_type == ["heavy_equipment", "primemover"]:
      excess_protector = 0
      pvt = 0
      premium = max(5000, 0.02 * sum_assured) * mark_up  
      return " {:6,.0f} ".format(premium + excess_protector)
    
    elif usage == "ambulance":
      pll=500
      excess_protector = 0
      pvt = 0
      premium = max(15000, 0.045 * sum_assured) * mark_up + (pll*seating_cap)  
      return " {:6,.0f}".format(premium + excess_protector)
    
    elif usage == "personal_taxi" and body_type == "personalcar":
      pll=500
      excess_protector = 0
      pvt = 0
      premium = max(15000, 0.05 * sum_assured) * mark_up + (pll*seating_cap)  
      return  " {:6,.0f}".format(premium + excess_protector)
    
    
def tpo_cover(duration, ins_type, owner_type, body_type, usage, tonnage, seat_cap):
    
    mark_up = 1.2

    if duration == "annual":
        if ins_type == "private" and body_type in ["personalcar", "pickup"] and usage == "private":
            premium = 4200
            return " {:6,.0f}".format(premium *mark_up)

        elif ins_type == "motor_trade" and owner_type in ["yard", "showroom"]:
            premium = 7500
            return " {:6,.0f}".format(premium *mark_up)

        elif ins_type in ["commercial", "psv"] and usage in ["school_bus", "staff_bus", "institutional"]:
          pll = 250
          premium = (7500*mark_up) + (pll*seat_cap)
          return " {:6,.0f}".format(premium)

        elif body_type == "motor_cycle":
          if ins_type == "psv": 
            premium = 3500
          else:
            premium = 2050
          return " {:6,.0f}".format(premium *mark_up)

        elif body_type == "tuktuk":
          pll = 750
          if ins_type == "psv": 
            premium = (4000*mark_up) + (pll * seat_cap)
            return " {:6,.0f}".format(premium)
          else:
            premium = 3000
            return " {:6,.0f}".format(premium *mark_up)

        elif ins_type in ["commercial", "psv"] and usage in ["chauffeur_cab", "app_hailing"]:
            pll = 500
            if seat_cap <= 4:
                premium = 4200*mark_up + (pll * seat_cap)
            if 4 < seat_cap <=9:
                premium = 7500*mark_up + (pll * seat_cap)
            elif seat_cap > 9:
                premium = 10000*mark_up + (pll * seat_cap)
            return " {:6,.0f}".format(premium)

        elif body_type == "heavy_equipment" and usage in ["agriculture", "other_equipment"]:
            premium = 3000
            return " {:6,.0f}".format(premium *mark_up)

        elif ins_type in ["commercial", "psv"] and usage == "ambulance":
          pll = 500
          premium = (7500*mark_up) + (pll*seat_cap)
          return " {:6,.0f}".format(premium)

        elif usage == "personal_taxi" and body_type == "personalcar":
          pll = 500
          premium = (5500*mark_up) + (pll*seat_cap)
          return " {:6,.0f}".format(premium)

        elif ins_type == "commercial" and usage in ["own_goods", "general_cartage"]:
          if tonnage <= 3:
              premium = 4500
          elif 3 < tonnage <= 8:
              premium = 5500
          elif 8 < tonnage <= 12:
              premium = 6500
          elif 12 < tonnage <= 15:
              premium = 7500
          elif 15 < tonnage <= 20:
              premium = 10000
          elif tonnage > 20:
              premium = 15000 
          elif body_type == "primemover":
              premium =  10000 
          return " {:6,.0f}".format(premium *mark_up)

        elif ins_type == "commercial" and usage == "tanker":
          if tonnage <= 10:
              premium = 17500
          elif 10 < tonnage <= 20:
              premium = 25000
          elif 20 < tonnage <= 30:
              premium = 30000
          elif tonnage > 30:
              premium = 45000
          elif body_type == "primemover":
              premium =  25000
          return " {:6,.0f}".format(premium *mark_up)

        elif ins_type in ["commercial", "psv"] and usage == "driving_school":
            if tonnage <= 7:
                premium = 10000
            elif tonnage > 7:
                premium = 15000
            elif body_type == "personalcar":
                  premium = 5000
            return " {:6,.0f}".format(premium *mark_up)
    
    #TOR premium computations        
    elif duration == "tor_cover":
        if ins_type == "private" and body_type in ["personalcar", "pickup"]:
          premium = 1200 * mark_up
          return " {:6,.0f}".format(premium)

        elif ins_type == "commercial" and usage in ["own_goods", "general_cartage"]:
          if tonnage <= 3:
              premium = 2000
          elif 3 < tonnage <= 8:
              premium = 2500 
          elif 8 < tonnage <= 12:
              premium = 2500 
          elif 12 < tonnage <= 15:
              premium = 3000
          elif 15 < tonnage <= 20:
              premium = 3000
          elif tonnage > 20:
              premium = 5500
          return " {:6,.0f}".format(premium *mark_up)
        
        elif body_type == "motor_cycle":
            if ins_type == "psv": 
                premium = 1800 * mark_up
                return " {:6,.0f}".format(premium)

        elif body_type == "tuktuk":
          if ins_type == "psv": 
            pll = 750
            premium = 1800 * mark_up
            return " {:6,.0f}".format(premium)
          else:
              premium = 1500
              return " {:6,.0f}".format(premium *mark_up)
