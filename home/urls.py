from django.conf.urls import url
from .views import *


app_name='home'

urlpatterns = [
   
    url(r'^google0f6eb0891016c158\.html$', GoogleIndexViewVerification.as_view(), name="googleindexview"),
    url(r'^tables$', TableForKidsView.as_view(), name="school_kids_tables"),
    url(r'^periodic-tables$', PeriodicTableForKidsView.as_view(), name="periodic_tables"),
    url(r'^periodic-tables-adv$', PeriodicTableForKidsAdvView.as_view(), name="periodic_tables_adv"),
    url(r'^scientific-calculator$', ScientificCalcView.as_view(), name="scientific_calculator"),
    url(r'^globe-explorer$', GlobeExplorer.as_view(), name="globe_explorer"),
    url(r'^dna-viewer$', DNAViewer.as_view(), name="dna_viewer"),
    url(r'^solar-viewer$', SolarViewer.as_view(), name="solar_viewer"),
    url(r'^solar-system-viewer$', SolarSysViewer.as_view(), name="solar_sys_viewer"),
    url(r'^ads\.txt$', AdsTextView.as_view(), name="ads_txt"),
    
    #url(r'^sw.js', PropellerAds.as_view(), name="propellerads"),
    
    url(r'^', HomePageView.as_view(), name="homeview"),
    
    ]