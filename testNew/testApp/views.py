from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib import messages
from .forms import SignUpForm , UpdateUserForm, UpdateProfileForm, CaseForm, CreateCaseForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from .models import Case
from django.contrib.auth.forms import PasswordChangeForm


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

#Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request,data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(request, username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request, 'Logged in successfully!!!')
                    return HttpResponseRedirect('/')

        else:
            fm = AuthenticationForm()
        return render(request,'login.html',{'form':fm})
    else:
        messages.error(request, 'You are already logged in!!!')
        return HttpResponseRedirect('/')


def user_profile(request):
    if request.user.is_authenticated:
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
        messages.error(request, 'Your are not logged in')
        return HttpResponseRedirect('/login/')
#Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


from django.shortcuts import render
from django.views.generic import TemplateView


class Home(TemplateView):
    template_name = 'home.html'



def create(request):
    if request.user.is_authenticated and request.user.has_perm('testApp.add_case'): #and request.user.groups.filter(name='police'):
        if request.method == "POST":
            form = CaseForm(request.POST, request.FILES)

            if form.is_valid():
                try:
                    titl = form.cleaned_data.get('title')
                    no = form.cleaned_data.get('number')
                    dat = form.cleaned_data.get('date')
                    img = form.cleaned_data.get('FIR')
                    usr = request.user
                    reg = Case(title=titl, number=no, date=dat, FIR=img, user=usr)
                    reg.save()

                    messages.success(request, 'Case Created Successfully.')
                    return redirect('/show')
                except:
                    pass
        else:
            form = CaseForm()
        return render(request, 'create.html', {'form': form})
            #return render(request, 'create.html',{})
    else:
        messages.error(request, 'Your do not have permission to Add')
        return HttpResponseRedirect('/show/')


from django.db.models import Q

def show(request):
    if request.user.is_authenticated:
        search_case = request.GET.get('search')
        if search_case:
            cases = Case.objects.filter(Q(title__icontains=search_case) | Q(number__icontains=search_case))
        else:
            # Query all cases
            cases = Case.objects.all().order_by("-date")

        return render(request,"show.html",{'cases':cases})
    else:
        return HttpResponseRedirect('/login/')


def edit(request, id):
    if request.user.is_authenticated and request.user.has_perm('testApp.change_case'):
        case = Case.objects.get(id=id)
        #return render(request,'edit.html', {'case':case})
        return render(request, 'edit.html', {'case': case})
    else:
        messages.error(request, 'Your do not have permission to edit')
        return HttpResponseRedirect('/show/')



def details(request, id):
    if request.user.is_authenticated:

        context = {}

    # add the dictionary during initialization
        context["case"] = Case.objects.get(id=id)

        return render(request, "details.html", context)
    else:

        return HttpResponseRedirect('/login/')

def update(request, id):
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
    if request.user.is_authenticated and request.user.has_perm('testApp.change_case'):
        case = Case.objects.get(id=id)
        if request.method == 'POST':
            case.delete()
            messages.success(request, 'Case Deleted Successfully.')
            return redirect("/show")
        return render(request, 'delete.html', {'case': case})
    else:
        messages.error(request, 'Your do not have permission to delete')
        return HttpResponseRedirect('/show/')

