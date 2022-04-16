from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from .forms import SignUpForm, UpdateUserForm, UpdateProfileForm, CaseForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .models import Case
from django.views.generic import TemplateView
from django.db.models import Q  # this is for search reason to allow the user to search about the case title or number


def sign_up(request):
    """Signup function to allow users to create their account."""
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():

            fm.save()
            messages.success(request, 'Account Created Successfully!!!')
            return HttpResponseRedirect('/')
    else:
        fm = SignUpForm()
    return render(request, 'signup.html', {'form': fm})


def user_login(request):
    """Login function to authenticate the users by using django authentication model."""
    if not request.user.is_authenticated:  # check if the user is not authenticated
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']  # assign user name from web page to variable
                upass = fm.cleaned_data['password']  # assign password from web page to variable
                user = authenticate(request, username=uname, password=upass)  # check the user name and password
                if user is not None:
                    login(request, user)  # if correct login and redirect him to home page
                    messages.success(request, 'Logged in successfully!!!')
                    return HttpResponseRedirect('/')
        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form':fm})
    else:
        # if he is already logged in show message and redirect him to home page
        messages.error(request, 'You are already logged in!!!')
        return HttpResponseRedirect('/')


def user_profile(request):
    """Profile function to update user profile which is related to the correct user."""
    if request.user.is_authenticated:  # check if the user is authenticated
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile is updated successfully')
                return redirect(to='/')
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)
        return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        # if the user does not have authentication show error message and redirct him to login page
        messages.error(request, 'Your are not logged in')
        return HttpResponseRedirect('/login/')


def user_logout(request):
    """Logout function to allow the user to logout and redirect him to home page."""
    logout(request)
    return HttpResponseRedirect('/')


class Home(TemplateView):
    """This is the Home page view"""
    template_name = 'home.html'


def create(request):
    """Create Case function starts to check if the user is authenticated and authorized to create cases.
        Authorization/permission is compared to the groups permissions which are configured at the beginning 
        by superuser or admin"""
    if request.user.is_authenticated and request.user.has_perm('testApp.add_case'):
        if request.method == "POST":
            form = CaseForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    titl = form.cleaned_data.get('title')  # get fields from web page to variables
                    no = form.cleaned_data.get('number')
                    dat = form.cleaned_data.get('date')
                    img = form.cleaned_data.get('evidence')
                    usr = request.user
                    reg = Case(title=titl, number=no, date=dat, evidence=img, user=usr)
                    reg.save()  # save data to database
                    messages.success(request, 'Case Created Successfully.')
                    return redirect('/show')
                except:
                    pass
        else:
            form = CaseForm()
        return render(request, 'create.html', {'form': form})
    else:
        # if the user is not authorized show error message
        messages.error(request, 'Your do not have permission to Add')
        return HttpResponseRedirect('/show/')
    

def show(request):
    """Show view to list all cases in the database in nice table on web page"""
    if request.user.is_authenticated:
        search_case = request.GET.get('search')
        if search_case:
            # retrieve all case which contain text in search field ordered with creation date
            cases = Case.objects.filter(Q(title__icontains=search_case) | Q(number__icontains=search_case))
        else:
            # retrieve all case ordered with creation date
            cases = Case.objects.all().order_by("-date")

        return render(request, "show.html", {'cases':cases})
    else:
        return HttpResponseRedirect('/login/')


def edit(request, id):
    """Edit Case function it starts to check if the user is authenticated and authorized to edit cases.
        Authorization/permission is compared to the groups permission which are configured at the beginning 
        by superuser or admin."""
    if request.user.is_authenticated and request.user.has_perm('testApp.change_case'):
        case = Case.objects.get(id=id)

        return render(request, 'edit.html', {'case': case})
    else:
        messages.error(request, 'Your do not have permission to edit')
        return HttpResponseRedirect('/show/')


def details(request, id):
    """Details function to show case details in separate web page."""
    if request.user.is_authenticated:
        context = {}
        context["case"] = Case.objects.get(id=id)
        return render(request, "details.html", context)
    else:
        return HttpResponseRedirect('/login/')


def update(request, id):
    """Update Case function it starts to check if the user is authenticated and authorized to update cases.
        Authorization/permission is compared to the groups permission which are configured at the beginning 
        by superuser or admin."""
    if request.user.is_authenticated and request.user.has_perm('testApp.change_case'):
        case = Case.objects.get(id=id)
        form = CaseForm(request.POST, instance = case)
        if form.is_valid():
            form.save()
            messages.success(request, 'Case Updated Successfully.')
            return redirect("/show")
        return render(request, 'edit.html', {'case': case})
    else:
        return HttpResponseRedirect('/login/')


def destroy(request, id):
    """Destroy Case function it starts to check if the user is authenticated and authorized to delete cases.
        Authorization/permission is compared to the groups permission which are configured at the beginning 
        by superuser or admin."""
    if request.user.is_authenticated and request.user.has_perm('testApp.change_case'):
        case = Case.objects.get(id=id)
        if request.method == 'POST':
            case.delete()  # if the user login and have permission to delete cases then the case will be deleted
            messages.success(request, 'Case Deleted Successfully.')
            return redirect("/show")
        return render(request, 'delete.html', {'case': case})
    else:
        # if user does not have permission show error message
        messages.error(request, 'Your do not have permission to delete')
        return HttpResponseRedirect('/show/')

