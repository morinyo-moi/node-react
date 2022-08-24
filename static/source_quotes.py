from django.http import HttpResponse
from static.quotes import trident_ins
from static.quotes import jubilee_ins
from static.quotes import corporate_ins
from static.quotes import pioneer_ins
from static.quotes import madison_ins
from static.quotes import directline
from static.quotes import britam_ins
from static.quotes import uap_ins
from static.quotes import sanlam_ins


def quotations(model, cover_type, duration, age, ins_type, owner_type, body_type, usage, tonnage, seat_cap,
               sum_assured):

    best_deals = {}
    if cover_type == "third_party":
        jubilee = jubilee_ins.tpo_cover(duration=duration, ins_type=ins_type, body_type=body_type, usage=usage,
                                        tonage=tonnage, seat_cap=seat_cap)
        if jubilee is not None:
            best_deals['JUBILEE ALLIANZ'] = {'amount': jubilee, 'img': 'insurance-1.png', 'name': 'JUBILEE ALLIANZ'}

        britam = britam_ins.tpo_cover(duration=duration, ins_type=ins_type, tonnage=tonnage, body_type=body_type,
                                      usage=usage)
        if britam is not None:

            best_deals['BRITAM INSURANCE'] = {'amount': britam, 'img': 'insurance-2.png', 'name': 'BRITAM INSURANCE'}

        uap = uap_ins.tpo_cover(duration=duration, ins_type=ins_type, tonnage=tonnage, body_type=body_type, usage=usage)
        if uap is not None:
            best_deals['UAP OLD MUTUAL'] = {'amount': uap, 'img': 'insurance-10.png', 'name': 'UAP OLD MUTUAL'}

        madison = madison_ins.tpo_cover(duration=duration, ins_type=ins_type, owner_type=owner_type,
                                        body_type=body_type, usage=usage, tonnage=tonnage, seating_cap=seat_cap)
        if madison is not None:
            best_deals['MADISON INSURANCE'] = {'amount': madison, 'img': 'insurance-7.png', 'name': 'MADISON INSURANCE'}

        #         ga = ga_ins.tpo_cover(duration=duration, ins_type=ins_type, tonnage=tonnage, body_type=body_type, usage=usage)
        #         if ga is not None:
        #             best_deals['GA INSURANCE'] = ga

        corporate = corporate_ins.tpo_cover(duration=duration, ins_type=ins_type, body_type=body_type, usage=usage)
        if corporate is not None:
            best_deals['CORPORATE INSURANCE'] = {'amount': corporate, 'img': 'insurance-9.png',
                                                 'name': 'CORPORATE INSURANCE'}

        sanlam = sanlam_ins.tpo_cover(duration=duration, ins_type=ins_type, body_type=body_type, usage=usage,
                                      tonnage=tonnage)
        if sanlam is not None:
            best_deals['SANLAM INSURANCE'] = {'amount': sanlam, 'img': 'insurance-2.png', 'name': 'SANLAM INSURANCE'}

        pioneer = pioneer_ins.tpo_cover(duration=duration, ins_type=ins_type, body_type=body_type, usage=usage,
                                        tonnage=tonnage, seat_cap=seat_cap)
        if pioneer is not None:
            best_deals['PIONEER INSURANCE'] = {'amount': pioneer, 'img': 'insurance-6.png', 'name': 'PIONEER INSURANCE'}

        direct_ln = directline.tpo_cover(duration=duration, ins_type=ins_type, body_type=body_type, usage=usage,
                                         tonnage=tonnage, seating_cap=seat_cap)
        if direct_ln is not None:
            best_deals['DIRECTLINE ASSURANCE'] = {'amount': direct_ln, 'img': 'insurance-8.png',
                                                  'name': 'DIRECTLINE ASSURANCE'}

        trident = trident_ins.tpo_cover(duration=duration, ins_type=ins_type, owner_type=owner_type,
                                        body_type=body_type, usage=usage, tonnage=tonnage, seat_cap=seat_cap)
        if trident is not None:
            best_deals['TRIDENT INSURANCE'] = {'amount': trident, 'img': 'insurance-5.png', 'name': 'TRIDENT INSURANCE'}

    elif cover_type == "comprehensive":
        jubilee = jubilee_ins.comprehensive_cover(model=model, age=age, ins_type=ins_type, body_type=body_type,
                                                  usage=usage, sum_assured=sum_assured, seat_cap=seat_cap)
        if jubilee is not None:
            best_deals['JUBILEE ALLIANZ'] = {'amount': jubilee, 'img': 'insurance-1.png', 'name': 'JUBILEE ALLIANZ'}

        britam = britam_ins.comprehensive_cover(model=model, age=age, ins_type=ins_type, body_type=body_type,
                                                owner_type=owner_type, usage=usage, sum_assured=sum_assured)
        if britam is not None:

            print(britam)
            best_deals['BRITAM INSURANCE'] = {'amount': britam, 'img': 'insurance-3.png', 'name': 'BRITAM INSURANCE'}

        uap = uap_ins.comprehensive_cover(model=model, age=age, ins_type=ins_type, body_type=body_type, usage=usage,
                                          sum_assured=sum_assured)
        if uap is not None:
            best_deals['UAP OLD MUTUAL'] = {'amount': uap, 'img': 'insurance-10.png', 'name': 'UAP OLD MUTUAL'}

        sanlam = sanlam_ins.comprehensive_cover(model=model, age=age, ins_type=ins_type, body_type=body_type,
                                                usage=usage, seat_cap=seat_cap, sum_assured=sum_assured)
        if sanlam is not None:
            best_deals['SANLAM INSURANCE'] = {'amount': sanlam, 'img': 'insurance-2.png', 'name': 'SANLAM INSURANCE'}

        madison = madison_ins.comprehensive_cover(age=age, ins_type=ins_type, owner_type=owner_type,
                                                  body_type=body_type, usage=usage, tonnage=tonnage,
                                                  seating_cap=seat_cap, sum_assured=sum_assured)
        if madison is not None:
            best_deals['MADISON INSURANCE'] = {'amount': madison, 'img': 'insurance-7.png', 'name': 'MADISON INSURANCE'}

        #         ga = ga_ins.comprehensive_cover(model=model, age=age, ins_type=ins_type, body_type=body_type, owner_type=owner_type, usage=usage, sum_assured=sum_assured)
        #         if ga is not None:
        #             best_deals['GA INSURANCE'] = ga

        corporate = corporate_ins.comprehensive_cover(model=model, age=age, ins_type=ins_type, body_type=body_type,
                                                      usage=usage, sum_assured=sum_assured)
        if corporate is not None:
            best_deals['CORPORATE INSURANCE'] = {'amount': corporate, 'img': 'insurance-9.png',
                                                 'name': 'CORPORATE INSURANCE'}

        pioneer = pioneer_ins.comprehensive_cover(age=age, model=model, ins_type=ins_type, body_type=body_type,
                                                  usage=usage, tonnage=tonnage, seat_cap=seat_cap,
                                                  sum_assured=sum_assured)
        if pioneer is not None:
            best_deals['PIONEER INSURANCE'] = {'amount': pioneer, 'img': 'insurance-6.png', 'name': 'PIONEER INSURANCE'}

        direct_ln = directline.comprehensive_cover(age=age, ins_type=ins_type, owner_type=owner_type,
                                                   body_type=body_type, usage=usage, tonnage=tonnage,
                                                   seating_cap=seat_cap, sum_assured=sum_assured)
        if direct_ln is not None:
            best_deals['DIRECTLINE ASSURANCE'] = {'amount': direct_ln, 'img': 'insurance-8.png',
                                                  'name': 'DIRECTLINE ASSURANCE'}

        trident = trident_ins.comprehensive_cover(age=age, ins_type=ins_type, owner_type=owner_type,
                                                  body_type=body_type, usage=usage, tonnage=tonnage,
                                                  seating_cap=seat_cap, sum_assured=sum_assured)
        if trident is not None:
            best_deals['TRIDENT INSURANCE'] = {'amount': trident, 'img': 'insurance-5.png', 'name': 'TRIDENT INSURANCE'}

    return best_deals
