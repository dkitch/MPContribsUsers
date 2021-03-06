"""This module provides the views for the MnO2_phase_selection explorer interface."""

import json
from bson import ObjectId
from django.shortcuts import render_to_response
from django.template import RequestContext
from mpcontribs.rest.views import get_endpoint
from mpcontribs.io.core.components import render_dataframe
from ..rest.rester import MnO2PhaseSelectionRester

def index(request):
    ctx = RequestContext(request)
    if request.user.is_authenticated():
        API_KEY = request.user.api_key
        ENDPOINT = request.build_absolute_uri(get_endpoint())
        with MnO2PhaseSelectionRester(API_KEY, endpoint=ENDPOINT) as mpr:
            #provenance = mpr.get_provenance()
            tables = {}
            for phase in mpr.get_phases():
                df = mpr.get_contributions(phase=phase)
                tables[phase] = render_dataframe(df, webapp=True)
    else:
        ctx.update({'alert': 'Please log in!'})
    return render_to_response("MnO2_phase_selection_explorer_index.html", locals(), ctx)
