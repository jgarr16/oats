# -*- coding: <encoding name> -*-
# Public Contract: given the ticket ID and URL-type requested as an argument, this module will return the URL for the specific CAPRS Incident (IM) or VersionOne Story/Defect in question

# TO-DO: set this up so that it automatically defaults to type1 (short CAPRS) or type3 (V1 - if id starts with S- or D-), and type2 has to be called out specifically


import settings


def url_make(id, url_type):
    if url_type == '1':  # gives user a quick view of CAPRS status
        settings.newURL = "http://dnnsoprod2.ba.ad.ssa.gov/ticketstatus/default.aspx?PMNum=" + \
            str(id)
    elif url_type == '2':   # takes user to CAPRS application
        settings.newURL = "https://sso.ba.ssa.gov/sm/index.do?ctx=docEngine&file=probsummary&query=number=%22" + \
            str(id) + "%22"
    elif url_type == '3':   # takes user to VersionOne for Stories and Defects
        # settings.newURL = "https://dcpsv1.ba.ssa.gov/VersionOne/assetdetail.v1?Number=" + str(id)
        V1_URL = ("https://dcpsv1.ba.ssa.gov/VersionOne/assetdetail.v1?Number=%s" % (id))
        settings.newURL = V1_URL
