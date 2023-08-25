from django.shortcuts import render
from .models import Profile, Board, Sticky
from django.contrib import messages
from django.shortcuts import redirect
from .forms import BoardForm, StickyForm


def home(request):
    if request.user.is_authenticated:
        board_form = BoardForm(request.POST or None)
        sticky_form = StickyForm(request.POST or None)
        if request.method == "POST":
            action = request.POST.get('action')
            if action == 'new_sticky':
                if sticky_form.is_valid():
                    sticky = sticky_form.save(commit=False)
                    sticky.user = request.user
                    sticky.save()
                    messages.success(request, "Sticky created successfully!")
                    return redirect('home')
            elif action == 'new_board':
                if board_form.is_valid():
                    board = board_form.save(commit=False)
                    board.user = request.user
                    board.save()
                    messages.success(request, "Board created successfully!")
                    return redirect('home')
            
        boards = Board.objects.all().order_by('-date_modified')
        stickys = Sticky.objects.all()
        return render(request, 'home.html', {"boards":boards, "board_form":board_form, "sticky_form":sticky_form, "stickys":stickys})

    else:
        boards = Board.objects.all().order_by('-date_modified')
        stickys = Sticky.objects.all()
        return render(request, 'home.html', {"boards":boards, "board_form":board_form, "sticky_form":sticky_form, "stickys":stickys})

def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.all()
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, "You must be logged in to view profiles.")
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        boards = Board.objects.filter(user_id=pk).order_by('-date_modified')

        #post form logic
        if request.method == "POST":
            #Get current user
            current_user_profile = request.user.profile
            #Get form data
            action = request.POST['follow']

            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            else:
                current_user_profile.follows.add(profile)
        
        return render(request, 'profile.html', {"profile": profile, "boards": boards})
   

    else:
        messages.success(request, "You must be logged in to view profiles.")
        return redirect('home')
    
def board(request, pk):
    if request.user.is_authenticated:
        board = Board.objects.get(user_id=pk)
        return render(request, 'board.html', {"board": board})
    else:
        messages.success(request, "You must be logged in to view boards.")
        return redirect('home')
    
def sticky(request, pk):
    if request.user.is_authenticated:
        sticky = Sticky.objects.get(user_id=pk)
        return render(request, 'sticky.html', {"sticky": sticky})
    else:
        messages.success(request, "You must be logged in to view stickies.")
        return redirect('home')