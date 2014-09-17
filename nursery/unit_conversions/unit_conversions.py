"""
Unit conversions, brought in from general.utils
"""
    
def miles_to_meters(miles):
    if miles is None:
        return 0
    return int(float(miles) * 1609.344)
    
def meters_to_miles(meters):
    if meters is None:
        return 0
    return float(meters) * 0.000621371192
    
def feet_to_meters(feet, precision=0):
    if feet is None:
        return 0
    return format(float(feet) * .3048, precision)
    
def meters_to_feet(meters, precision=0):
    if meters is None:
        return 0
    return format(float(meters) * 3.2808399, precision)
    
def sq_meters_to_sq_miles(sq_meters):
    if sq_meters is None:
        return 0
    return float(sq_meters) * .000000386102159
    
def sq_meters_to_acres(sq_meters):
    if sq_meters is None:
        return 0
    return float(sq_meters) * .000247104393
    
def mps_to_mph(mps):
    if mps is None:
        return 0
    return float(mps) * 2.23693629
    
def mph_to_mps(mph):
    if mph is None:
        return 0
    return float(mph) * 0.44704

