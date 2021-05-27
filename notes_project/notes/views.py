import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework import routers, serializers, viewsets
from .models import Note
from .serializer import NoteSerializer
from django.http import JsonResponse, response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
import json


def home(request):
    if request.method == 'GET':
        return render(request, 'notes/home.html')
    if request.method == 'POST':
        important_checked = None
        if request.POST.get('importantInput') == 'True':
            important_checked = True
        else:
            important_checked = False

        new_note = Note(title=request.POST['titleInput'], description=request.POST['descInput'], 
                        important=important_checked, user=request.user)
        new_note.save()
        print(new_note, new_note.description, new_note.important)
        return render(request, 'notes/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'notes/signupuser.html', )
    else:
        # validate inputs
        SpecialSym =['$', '@', '#', '%']
        user_password = request.POST['signuppassword1']
        user_username = request.POST['signupusername']
        validation_error_password = 'Password should be at least 3 and maximum 20 character. The password should have at least one numeral letter, \
            one uppercase letter, one lowercase letter and one symbol ( $ @ # % )'
        validation_error_username = 'Username should be at least 3 and maximum 20 character'

        if (len(user_password) < 3 or len(user_password) > 20 or not any(char.isdigit() for char in user_password) or 
            not any(char.isupper() for char in user_password) or not any(char.islower() for char in user_password) or 
            not any(char in SpecialSym for char in user_password)):
            return render(request, 'notes/signupuser.html', {'error': validation_error_password})

        if len(user_username) < 3 or len(user_username) > 20:
            return render(request, 'notes/signupuser.html', {'error': validation_error_username})

        try:
            # check if username exists
            check_user = User.objects.get(username=request.POST['signupusername'])
            return render(request, 'notes/signupuser.html', {'error': f'Username ({check_user}) already taken.'})
        except User.DoesNotExist:
            # check passwords if match
            if request.POST['signuppassword1'] == request.POST['signuppassword2']:
                try:
                    user = User.objects.create_user(username=request.POST['signupusername'], password=request.POST['signuppassword1'])
                    user.save()
                    login(request, user)
                    return redirect('home')
                except:
                    return render(request, 'notes/signupuser.html', {'error': 'Something went wrong. Please try it again.'})
            else:
                return render(request, 'notes/signupuser.html', {'error': "Password's don't match"})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'notes/loginuser.html', )
    else:
        user = authenticate(request, username = request.POST['loginusername'], password = request.POST['loginpassword'])
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'notes/loginuser.html', {'error': 'Wrong username or password'})


def logoutuser(request):
    logout(request)
    return redirect('home')


@login_required
@csrf_exempt
def note_list(request):
    if request.method == 'GET':
        notes = Note.objects.all().filter(user_id=request.user.id)
        serializer = NoteSerializer(notes, many=True)
        return JsonResponse(serializer.data, safe=False)
    # elif request.method == 'POST':
    #     data = JSONParser().parse(request)
    #     print(data)
    #     print(data[0])
    #     serializer = NoteSerializer(data=data)
    #     print(serializer)
    #     if serializer.is_valid():
    #         print('VALID')
    #         serializer.save()
    #         return redirect('home')
    #     # Ez így nem jó. Törlést egyből be kell küldeni
    #     print('NEM VALID')
    #     return redirect('home')


@login_required
@csrf_exempt
def delete_note(request):
    if request.method == 'POST':
        del_data = JSONParser().parse(request)
        p_key = del_data['del_id']
        del_note = Note.objects.filter(pk=p_key)
        del_note.delete()
        return render(request, 'notes/home.html')
