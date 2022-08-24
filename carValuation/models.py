from django.db import models
from sqlalchemy import true


#Define a table to record successful user queries

class CustomerRating(models.Model):
    rating = models.CharField(max_length=20, null=False)
    name = models.CharField(max_length=20, null=True)
    comment = models.CharField(max_length=200, null=False)


class valuation_userdata_mysql(models.Model):
    make = models.CharField(max_length=30,null=False)
    model = models.CharField(max_length=302,null=False)
    trim = models.CharField(max_length=30,null=False,default='standard')
    fuel_type =models.CharField(max_length=30,null=False) 
    transmission = models.CharField(max_length=30,null=False) 
    how_used = models.CharField(max_length=30,null=False) 
    body_type = models.CharField(max_length=30,null=False) 
    region = models.CharField(max_length=30,null=False) 
    origin =models.CharField(max_length=30,null=False) 
    descriptn = models.CharField(max_length=30,null=False) 
    eng_capacity = models.CharField(max_length=30,null=False) 
    year_man = models.CharField(max_length=30,null=False) 
    mileage =models.CharField(max_length=30,null=False) 
    estm_value = models.CharField(max_length=30,null=False) 
    date = models.DateField(auto_now_add=True, null=True, blank=True)

#Define a table to record user orders
class insurance_client_table(models.Model):
    cover_type = models.CharField(max_length=30,null=False) 
    insurance_type = models.CharField(max_length=30,null=False) 
    insurance_period = models.CharField(max_length=30,null=False) 
    make = models.CharField(max_length=30,null=False) 
    model = models.CharField(max_length=30,null=False) 
    year_man = models.CharField(max_length=30,null=False) 
    body_type = models.CharField(max_length=30,null=False) 
    owner_type = models.CharField(max_length=30,null=False) 
    use_case = models.CharField(max_length=30,null=False) 
    tonage =models.CharField(max_length=30,null=False) 
    eng_capacity = models.CharField(max_length=30,null=False) 
    seating_capacity =models.CharField(max_length=30,null=False) 
    owner_names = models.CharField(max_length=30,null=False) 
    email_address = models.CharField(max_length=30,null=False) 
    owner_contacts = models.CharField(max_length=30,null=False) 
    reg_number = models.CharField(max_length=30,null=False) 
    pin_number = models.CharField(max_length=30,null=False) 
    valuation = models.CharField(max_length=30,null=False) 
    preferred_insurer = models.CharField(max_length=30,null=False) 
    start_date = models.DateField(null=False)
    premium = models.CharField(max_length=30,null=False) 
    amount_paid = models.CharField(max_length=30,null=False) 
    payment_ref = models.CharField(max_length=30,null=False) 
    logbook_url = models.CharField(max_length=225,null=False)
    natid_url = models.CharField(max_length=225,null=False)
    date = models.DateField( auto_now_add=True, null=True, blank=True)

    class client_payments_table(models.Model):
        transLoID = models.CharField(max_length=225, null=False,  primary_key=True)
        TransactionType = models.CharField(max_length=225, null=False)
        TransID = models.CharField(max_length=225, null=False)
        TransTime = models.CharField(max_length=225, null=False)
        TransAmount = models.CharField(max_length=225, null=False)
        BusinessShortCode = models.CharField(max_length=225, null=False)
        BillRefNumber = models.CharField(max_length=225, null=False)
        InvoiceNumber = models.CharField(max_length=225, null=True)
        OrgAccountBalance = models.CharField(max_length=225, null=False)
        ThirdPartyTransID = models.CharField(max_length=225, null=True)
        MSISDN = models.CharField(max_length=225, null=False)
        FirstName = models.CharField(max_length=225, null=False)
        MiddleName = models.CharField(max_length=225, null=True)
        LastName = models.CharField(max_length=225, null=False, default='NaN')



