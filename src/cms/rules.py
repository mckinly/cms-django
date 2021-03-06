"""
We use `django-rules <https://pypi.org/project/rules/>`_ to add custom permissions for specific pages.

For a given user and page, the following permissions are added:

* ``cms.edit_page`` if one of the following predicates return true:

    * :func:`~cms.rules.can_edit_all_pages`
    * :func:`~cms.rules.is_page_editor`
    * :func:`~cms.rules.can_publish_all_pages`
    * :func:`~cms.rules.is_page_publisher`

* ``cms.publish_page`` if one of the following predicates return true:

    * :func:`~cms.rules.can_publish_all_pages`
    * :func:`~cms.rules.is_page_publisher`

See the project's `README <https://github.com/dfunckt/django-rules/blob/master/README.rst>`_ to learn more.
"""
from rules import add_perm, predicate


# Predicates


@predicate
def is_page_editor(user, page):
    """
    This predicate checks whether the given user is one of the editors of the given page.

    :param user: The user who's permission should be checked
    :type user: ~django.contrib.auth.models.User

    :param page: The requested page
    :type page: ~cms.models.pages.page.Page

    :return: Whether or not ``user`` is an editor of ``page``
    :rtype: bool
    """
    if not page:
        return False
    return user in page.editors.all()


@predicate
def is_page_publisher(user, page):
    """
    This predicate checks whether the given user is one of the publishers of the given page.

    :param user: The user who's permission should be checked
    :type user: ~django.contrib.auth.models.User

    :param page: The requested page
    :type page: ~cms.models.pages.page.Page

    :return: Whether or not ``user`` is a publisher of ``page``
    :rtype: bool
    """
    if not page:
        return False
    return user in page.publishers.all()


@predicate
def can_edit_all_pages(user, page):
    """
    This predicate checks whether the given user can edit all pages.

    :param user: The user who's permission should be checked
    :type user: ~django.contrib.auth.models.User

    :param page: The page parameter is used for the region check
    :type page: ~cms.models.pages.page.Page

    :return: Whether or not ``user`` can edit all pages
    :rtype: bool
    """
    if not (user.is_superuser or user.is_staff):
        if page and page.region not in user.profile.regions.all():
            return False
    return user.has_perm("cms.edit_pages")


@predicate
def can_publish_all_pages(user, page):
    """
    This predicate checks whether the given user can publish all pages.

    :param user: The user who's permission should be checked
    :type user: ~django.contrib.auth.models.User

    :param page: The page parameter is used for the region check
    :type page: ~cms.models.pages.page.Page

    :return: Whether or not ``user`` can publish all pages
    :rtype: bool
    """
    if not (user.is_superuser or user.is_staff):
        if page and page.region not in user.profile.regions.all():
            return False
    return user.has_perm("cms.publish_pages")


@predicate
def can_edit_or_publish_some_pages(user):
    """
    This predicate checks whether the given user can edit or publish at least some specific pages.

    :param user: The user who's permission should be checked
    :type user: ~django.contrib.auth.models.User

    :return: Whether or not ``user`` can edit or publish some pages
    :rtype: bool
    """
    if user.editable_pages.exists() or user.publishable_pages.exists():
        return True
    if user.profile.organization and user.profile.organization.pages.exists():
        return True
    return False


@predicate
def is_in_responsible_organization(user, page):
    """
    This predicate checks whether the given user is a member of the page's responsible organization.

    :param user: The user who's permission should be checked
    :type user: ~django.contrib.auth.models.User

    :param page: The requested page
    :type page: ~cms.models.pages.page.Page

    :return: Whether or not ``user`` is a member of ``page.organization``
    :rtype: bool
    """
    if not page or not page.organization:
        return False
    return user.profile in page.organization.members.all()


@predicate
def can_delete_chat_message(user, chat_message):
    """
    This predicate checks whether the given user can delete a given chat message

    :param user: The user who's permission should be checked
    :type user: ~django.contrib.auth.models.User

    :param chat_message: The requested chat message
    :type chat_message: ~cms.models.chat.chat_message.ChatMessage

    :return: Whether or not ``user`` is allowed to delete ``chat_message``
    :rtype: bool
    """
    # Superusers and staff can delete all messages
    if user.is_superuser or user.is_staff:
        return True
    # Normal users can only delete their own messages
    return user == chat_message.sender


# Permissions

add_perm(
    "cms.view_pages",
    can_edit_or_publish_some_pages | can_edit_all_pages | can_publish_all_pages,
)
add_perm(
    "cms.edit_page",
    can_edit_all_pages
    | is_page_editor
    | can_publish_all_pages
    | is_page_publisher
    | is_in_responsible_organization,
)
add_perm(
    "cms.publish_page",
    can_publish_all_pages | is_page_publisher | is_in_responsible_organization,
)
add_perm("cms.delete_chat_message", can_delete_chat_message)
