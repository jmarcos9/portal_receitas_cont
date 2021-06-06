from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import auth, messages
from receitas.models import Receita


def cadastro(request):

    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        print(nome, email, senha, senha2)

        if not nome.strip():
            messages.error(request, 'Nome não pode ficar em branco')
            return redirect('cadastro')

        if not email.strip():
            messages.error(request, 'Email não pode ficar em branco')
            return redirect('cadastro')

        if senha != senha2:
            messages.error(request, 'As senhas não são iguais!')
            return redirect('cadastro')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado!')
            return redirect('cadastro')
        #atribui nome, email e senha a user
        user = User.objects.create_user(username=nome, email=email, password=senha)
        # salva no bd
        user.save()
        messages.success(request, 'Cadastro efetuado com sucesso!')
        return redirect('login')
    else:
        return render(request, 'usuarios/cadastro.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['senha']

        if email == "" or senha == "":
            messages.error(request, 'Email ou Senha não informado(s)!')
            return redirect('login')
        #Atribui email a variavel nome para poder fazer login... django autentica com username
        if User.objects.filter(email=email).exists():
            nome = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=nome, password=senha)
            #faz o login no bd
            if user is not None:
                auth.login(request, user)
                return redirect('dashboard')
    return render(request, 'usuarios/login.html')


def dashboard(request):
    #checa se usuario está autenticado e so vai para dashboard caso True
    if request.user.is_authenticated:
        #identifica o criado da receita
        id = request.user.id
        #armazena e lista por ordem de data as resceitas
        receitas = Receita.objects.order_by('-data_receita').filter(pessoa=id)

        #passar as informaçoes para template
        dados = {
            'receitas': receitas
        }


        return render(request, 'usuarios/dashboard.html', dados)
    else:
        return redirect('index')


def logout(request):
    auth.logout(request)
    return redirect('index')


def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        imagem_receita = request.FILES['imagem_receita']

        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa=user,
                                         nome_receita=nome_receita,
                                         ingredientes=ingredientes,
                                         modo_preparo=modo_preparo,
                                         tempo_preparo=tempo_preparo,
                                         rendimento=rendimento,
                                         categoria=categoria,
                                         imagem_receita=imagem_receita)

        receita.save()

        return redirect('dashboard')
    else:
        return render(request, 'usuarios/cria_receita.html')
