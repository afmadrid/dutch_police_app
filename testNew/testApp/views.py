from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from .forms import SignUpForm , UpdateUserForm, UpdateProfileForm, CaseForm, ContactForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from .models import Case

#from django.contrib.auth.decorators import login_required
# Create your views here.
#Signup
def sign_up(request):
    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():

            fm.save()
            messages.success(request,'Account Created Successfully!!!')
            return HttpResponseRedirect('/')
    else:
        fm = SignUpForm()
    return render(request,'signup.html',{'form':fm})
    #return HttpResponseRedirect('/profile/')
#Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully!!!')
                    return HttpResponseRedirect('/')
        else:
            fm = AuthenticationForm()
        return render(request,'login.html',{'form':fm})
    else:
        return HttpResponseRedirect('/show/')

#Profile
#from django.contrib.auth.decorators import permission_required
#@permission_required('testApp.add_vote')
def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=request.user)
            profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile is updated successfully')
                return redirect(to='/logout/')
        else:
            user_form = UpdateUserForm(instance=request.user)
            profile_form = UpdateProfileForm(instance=request.user.profile)

        #return render(request,'profile.html',{'name':request.user})
        return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})
    else:
        return HttpResponseRedirect('/login/')
#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'

#from django.contrib.auth.decorators import user_passes_test
#from django.contrib.auth.models import Group
#@user_passes_test(lambda u: Group.objects.get(name='Police') in u.groups.all())
#def dashboard(request):
    # Logic for dashboard

'''def create_case(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    form = CaseForm(request.POST or None)
    if form.is_valid():
        form.save()

    context['form'] = form
    return render(request, "create_case.html", context)'''


def create(request):
    if request.user.is_authenticated and request.user.has_perm('testApp.add_case'): #and request.user.groups.filter(name='police'):
        if request.method == "POST":
            form = CaseForm(request.POST)
            if form.is_valid():
                try:

                    link = form.save(commit=False)
                    link.user = request.user
                    link.save()
                    return redirect('/show')
                except:
                    pass
        else:
            form = CaseForm()
        return render(request, 'create.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def show(request):
    if request.user.is_authenticated:
        cases = Case.objects.all()
        return render(request,"show.html",{'cases':cases})
    else:
        return HttpResponseRedirect('/login/')

'''def list_case(request):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["dataset"] = Case.objects.all()

    return render(request, "list_case.html", context)'''

def edit(request, id):
    if request.user.is_authenticated and request.user.has_perm('testApp.change_case'):
        case = Case.objects.get(id=id)
        return render(request,'edit.html', {'case':case})
    else:
        return HttpResponseRedirect('/login/')


# pass id attribute from urls
'''def detail_case(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["data"] = Case.objects.get(id=id)

    return render(request, "detail_case.html", context)'''



# after updating it will redirect to detail_View
'''def detail_case(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # add the dictionary during initialization
    context["data"] = Case.objects.get(id=id)

    return render(request, "detail_case.html", context)'''

def update(request, id):
    if request.user.is_authenticated and request.user.has_perm('testApp.change_case'):
        case = Case.objects.get(id=id)
        form = CaseForm(request.POST, instance = case)
        if form.is_valid():
            form.save()
            return redirect("/show")
        return render(request, 'edit.html', {'case': case})
    else:
        return HttpResponseRedirect('/login/')

# update view for details
'''def update_case(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Case, id=id)

    # pass the object as instance in form
    form = CaseForm(request.POST or None, instance=obj)

    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/" + id)

    # add form dictionary to context
    context["form"] = form

    return render(request, "update_case.html", context)'''

def destroy(request, id):
    if request.user.is_authenticated and request.user.has_perm('testApp.change_case'):
        case = Case.objects.get(id=id)
        if request.method == 'POST':
            case.delete()
            return redirect("/show")
        return render(request, 'delete.html', {'case': case})
    else:
        return HttpResponseRedirect('/login/')


# delete view for details
'''def delete_case(request, id):
    # dictionary for initial data with
    # field names as keys
    context = {}

    # fetch the object related to passed id
    obj = get_object_or_404(Case, id=id)

    if request.method == "POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return HttpResponseRedirect("/")

    return render(request, "delete_case.html", context)'''





