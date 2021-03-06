from linkcheck import Linklist

from .models import PageTranslation, EventTranslation, POITranslation


class PageTranslationLinklist(Linklist):
    """
    Class for selecting the PageTranslation model for link checks
    """

    model = PageTranslation
    html_fields = ["text"]


class EventTranslationLinklist(Linklist):
    """
    Class for selecting the EventTranslation model for link checks
    """

    model = EventTranslation
    html_fields = ["description"]


class POITranslationLinklist(Linklist):
    """
    Class for selecting the POITranslation model for link checks
    """

    model = POITranslation
    html_fields = ["description"]


linklists = {
    "PageTranslations": PageTranslationLinklist,
    "EventTranslations": EventTranslationLinklist,
    "POITranslations": POITranslationLinklist,
}
