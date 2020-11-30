from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from ...decorators import staff_required
from ...models import Feedback


@method_decorator(login_required, name="dispatch")
@method_decorator(staff_required, name="dispatch")
class AdminDashboardView(TemplateView):
    """
    View for the admin dashboard
    """

    #: The template to render (see :class:`~django.views.generic.base.TemplateResponseMixin`)
    template_name = "dashboard/admin_dashboard.html"
    #: The context dict passed to the template (see :class:`~django.views.generic.base.ContextMixin`)
    base_context = {"current_menu_item": "admin_dashboard"}

    def get(self, request, *args, **kwargs):
        """
        Render admin dashboard

        :param request: Object representing the user call
        :type request: ~django.http.HttpRequest

        :param args: The supplied arguments
        :type args: list

        :param kwargs: The supplied keyword arguments
        :type kwargs: dict

        :return: The rendered template response
        :rtype: ~django.template.response.TemplateResponse
        """
        all_feedback = Feedback.objects.filter(is_technical=True)[:5]

        return render(
            request,
            self.template_name,
            {
                "current_menu_item": "admin_feedback",
                "all_feedback": all_feedback,
                **self.base_context,
            },
        )
