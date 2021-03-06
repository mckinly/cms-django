"""
This is a collection of tags and filters for strings.
"""
from django import template

register = template.Library()


@register.filter(name="words")
def words(text):
    """
    Split the given text into a list of words, see :meth:`python:str.split`.

    :param text: The input string
    :type text: str

    :return: The list of words in the text
    :rtype: list
    """
    return text.split()


@register.filter(name="linkcheck_status_filter")
def linkcheck_status_filter(status_message):
    """
    Due to a long status entry for a single kind of faulty link,
    this filter reduced the output when display in list view

    :param status_message: error description
    :type status_message: str
    :return: a concise message
    :rtype: str
    """
    if status_message.startswith("Other Error:"):
        return "Other Error"
    return status_message
