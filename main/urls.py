from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('table/', mainTable, name='table'),
    path('next/', mainNext, name='next'),
    path('leagues/', mainListLeagues, name='leagues'),
    path('ajax/table_matches', ajaxTableMatches, name='tablematches'),
    path('ajax/stat_match', ajaxStatMatch, name='statmatch'),
    path('ajax/<int:old>/next_matches', ajaxNextMatches, name='nextmatches'),
]