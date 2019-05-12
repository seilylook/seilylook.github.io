from django.shortcuts import render,redirect
from .models import Blog
from .models import BlogData

def home(request):
    return render(request,'home.html')

def recom_food(request):
    return render(request,'recom_food.html')

def new(request):
    return render(request, 'new.html')

def president(request):
    blog = Blog.objects
    return render(request,'president.html', {'blog': blog})

def challenge(request):
    return render(request,'challenge.html')

def honbob(request):
    return render(request, 'honbob.html')

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
            request.POST['username'], password=request.POST['password1'])
            auth.login(request, user)
            return redirect('blog')
    return render(request, 'accounts/signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'accounts/login.html')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('blog')
    return render(request, 'accounts/signup.html')  

def write(request):
    return render(request, 'write.html')

def create(request):   
    blog = Blog()
    blog.storename = request.GET['storename']  
    blog.price =  request.GET['price']
    blog.content = request.GET['content']    
    blog.mainmenuname = request.GET['mainmenuname']
    blog.foodimage = request.GET['foodimage']
    blog.save()    
    return redirect('/president/'+str(blog.id))

def recommend(request):
    return render(request, 'recommend.html')
