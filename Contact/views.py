from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse_lazy


class CONTACT(FormView):
    form_class = ContactForm
    template_name = 'contact/contact.html'
    success_url = reverse_lazy('contact')
    def form_valid(self, form): 
        form.save()

        send_mail(
            subject='A new contact form has been submitted regarding the Tuition Project.',
            message=f"Message from {form.cleaned_data['name']}:\n {form.cleaned_data['Phone_number']}\n{form.cleaned_data['gmail']}\n{form.cleaned_data['text']}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )         
        messages.success(self.request, 'Message is successfully submitted')
        return super().form_valid(form)
