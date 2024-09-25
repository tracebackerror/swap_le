from django.urls import path
from .views import (
    GoogleIndexViewVerification, TableForKidsView, PeriodicTableForKidsView,
    PeriodicTableForKidsAdvView, ScientificCalcView, GlobeExplorer,
    DNAViewer, SolarViewer, SolarSysViewer, AdsTextView, HomePageView
)

app_name = 'home'

urlpatterns = [
    path('google0f6eb0891016c158.html', GoogleIndexViewVerification.as_view(), name='googleindexview'),
    path('tables', TableForKidsView.as_view(), name='school_kids_tables'),
    path('periodic-tables', PeriodicTableForKidsView.as_view(), name='periodic_tables'),
    path('periodic-tables-adv', PeriodicTableForKidsAdvView.as_view(), name='periodic_tables_adv'),
    path('scientific-calculator', ScientificCalcView.as_view(), name='scientific_calculator'),
    path('globe-explorer', GlobeExplorer.as_view(), name='globe_explorer'),
    path('dna-viewer', DNAViewer.as_view(), name='dna_viewer'),
    path('solar-viewer', SolarViewer.as_view(), name='solar_viewer'),
    path('solar-system-viewer', SolarSysViewer.as_view(), name='solar_sys_viewer'),
    path('ads.txt', AdsTextView.as_view(), name='ads_txt'),

    # Uncomment if needed
    # path('sw.js', PropellerAds.as_view(), name='propellerads'),
    
    path('', HomePageView.as_view(), name='homeview'),
]
