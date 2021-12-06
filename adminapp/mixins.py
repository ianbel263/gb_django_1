from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeletionMixin


class ProtectDispatchMixin(View):
    @method_decorator(user_passes_test(lambda user: user.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProtectDispatchMixin, self).dispatch(request, *args, **kwargs)


class AdminDeleteMixin(DeletionMixin, SingleObjectMixin):
    success_messages = {
        'delete': 'Данные успешно удалены',
        'restore': 'Данные успешно восстановлены'
    }

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = not self.object.is_active
        self.object.save()
        success_message = self.success_messages['restore'] if self.object.is_active else self.success_messages['delete']
        messages.success(request, success_message)
        return HttpResponseRedirect(self.get_success_url())
