from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import login as auth_login
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm 
from django.core.mail import send_mail
from django.utils.html import mark_safe
from django.conf import settings
from django import template
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMessage
from .models import JobListing  # Import the JobListing model
from django.contrib.auth.models import User
from django.views import View
from .models import CustomUser
from django.core.paginator import Paginator
from django.db.models import Count

class Jobs(TemplateView):
    template_name = 'jobs.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_listings = JobListing.objects.all()

        # Category filtering
        category = self.request.GET.get('category')
        if category:
            job_listings = job_listings.filter(category=category)

        # Count jobs per category
        job_counts = job_listings.values('category').annotate(job_count=Count('category'))

        # Define predefined categories
        predefined_categories = [
            ('Content Writing & Strategy', 'Content Writing & Strategy'),
            ('Designing & Art', 'Designing & Art'),
            ('Data Analysis & Insights', 'Data Analysis & Insights'),
            ('Programming & Development', 'Programming & Development'),
        ]

        paginator = Paginator(job_listings, 10)  # Show 10 jobs per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        recent_job_listings = JobListing.objects.order_by('-date_added')[:3]

        context['page_obj'] = page_obj
        context['job_listings'] = page_obj.object_list
        context['categories'] = job_counts  # Use job_counts instead of JobListing categories
        context['selected_category'] = category  # Pass selected category to context
        context['recent_job_listings'] = recent_job_listings
        context['predefined_categories'] = predefined_categories

        return context


class JobDetail(TemplateView):
    template_name = 'jobs_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs['job_id']
        job = get_object_or_404(JobListing, id=job_id)

        responsibilities = [line.strip() for line in job.responsibilities.strip().split('\n') if line.strip()]
        requirements = [line.strip() for line in job.requirements.strip().split('\n') if line.strip()]
        skills_needed = [line.strip() for line in job.skills_needed.strip().split('\n') if line.strip()]

        context['job'] = job
        context['responsibilities'] = responsibilities
        context['requirements'] = requirements
        context['skills_needed'] = skills_needed

        return context





def apply_to_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if request.method == 'POST':
        # Process the form data
        name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        age = request.POST['age']
        gender = request.POST['gender']
        years_of_experience = request.POST['years_of_experience']
        cv = request.FILES['cv']
        why_apply = request.POST['why_apply']

        # Send an email to the hiring team with the CV attached
        hiring_team_subject = f'Job Application from {name}'
        hiring_team_message = f"""
        Name: {name}
        Email: {email}
        Phone Number: {phone_number}
        Age: {age}
        Gender: {gender}
        Years of Experience: {years_of_experience}
        Why Apply: {why_apply}
        """

        email_to_hiring_team = EmailMessage(
            hiring_team_subject,
            hiring_team_message,
            settings.DEFAULT_FROM_EMAIL,
            ['brijeshdahiya18@gmail.com']
        )

        if cv:
            email_to_hiring_team.attach(cv.name, cv.read(), cv.content_type)

        email_to_hiring_team.send(fail_silently=False)

        # Send a confirmation email to the applicant
        applicant_subject = 'Application Received'
        applicant_message = f"""Hi {name},

Thank you for applying for the position of {job.job_title} at {job.company_name}. 
We have received your application and will review it shortly.

Best regards,
The Hiring Team"""

        email_to_applicant = EmailMessage(
            applicant_subject,
            applicant_message,
            settings.DEFAULT_FROM_EMAIL,
            [email]
        )

        email_to_applicant.send(fail_silently=False)

        # Set a success message
        messages.success(request, 'You have applied for the job successfully!')

        # Redirect to the jobs page
        return redirect('jobs')  # Change 'jobs' to the name of your jobs listing URL

    return render(request, 'apply.html', {'job': job})
    
class HomePage(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_job_listings = JobListing.objects.order_by('-date_added')[:6]
        context['recent_job_listings'] = recent_job_listings
        return context

class AboutPage(TemplateView):
    template_name = 'about.html'

class ProfilePage(TemplateView):
    template_name = 'profile.html'







class SignupPage(View):
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, self.template_name)

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return render(request, self.template_name)

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return render(request, self.template_name)

        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.save()
        auth_login(request, user)
        return redirect('/jobs')



class LoginPage(View):
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('/jobs')  # Redirect to the jobs page after successful login
        else:
            messages.error(request, "Invalid email or password")
            return render(request, self.template_name)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        
        # Construct the email message
        email_subject = 'New Contact Form Submission'
        email_body = f"Hi Dipesh,\n\nYou have received a new contact form submission:\n\nName: {name}\nEmail: {email}\n\nMessage:\n{message}"
        recipient_email = 'brijeshdahiya18@gmail.com'  # Your email address here
        
        # Send email
        send_mail(
            email_subject,
            email_body,
            email,  # Sender's email address provided by the user
            [recipient_email],
            fail_silently=False
        )
        success_message = mark_safe('Thank you for contacting us. We will respond soon.<br>Feel free to check our job listings in the meantime.')
        messages.success(request, success_message)
        # Redirect to the jobs page
        return redirect('jobs')
    return render(request, 'contact.html')