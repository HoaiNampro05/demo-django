from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Post
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'blog/home.html')

def startRegister(request):
    return render(request,'blog/register.html')

def startLogin(request):
    return render(request,'blog/login.html')

def startAddPost(request):
   # print("da vao startaddpost")
    if request.method == 'POST':
        context = {'username': request.session.get('user_name'),'user_id': request.session.get('user_id')}
        return render(request,'blog/addpost.html',context)

def processRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
       
        # Kiểm tra mật khẩu có trùng khớp không
        if password == password2:
            # Kiểm tra xem username có tồn tại hay không
            if User.objects.filter(username=username).exists():
                print("ok1")
                messages.error(request, 'Tên đăng nhập đã tồn tại.')
            # Kiểm tra xem email đã được sử dụng hay chưa
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email đã được sử dụng.')
            else:
                # Tạo user mới
                user = User(username=username, email=email, password=password)
                #user=User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Tài khoản đã được tạo thành công!')
                return render(request,'blog/home.html')
        else:
            messages.error(request, 'Mật khẩu không trùng khớp.')
    
    return render(request, 'blog/register.html')

def processLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,password,"dâdsada")
        # Xác thực người dùng
        #user = authenticate(request, username=username, password=password)
        user=None
        try:
            user = User.objects.get(username=username)
            if user != None and user.password==password:
                request.session['user_id'] = user.id  # Lưu user_id vào session
                request.session['user_name'] = user.username
                posts = Post.objects.filter(user_id=user.id)
                print(len(posts))
                context={'username':request.session.get('user_name'),'user_id':request.session.get('user_id'),"posts":posts}
                return render(request,'blog/userhome.html',context)
            return render(request, 'blog/login.html')
        except:
            return render(request, 'blog/login.html') 
    else:
        return render(request, 'blog/login.html')




def addPost(request):
    if request.method =='POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        user = User.objects.get(id=request.session.get('user_id'))
        post = Post.objects.create(user=user, title=title, content=content)
        post.save()
        posts = Post.objects.filter(user_id=request.session.get('user_id'))
        context={'username':request.session.get('user_name'),'user_id':request.session.get('user_id'),"posts":posts}
        return render(request,'blog/userhome.html',context)