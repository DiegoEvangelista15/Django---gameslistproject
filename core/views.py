from django.shortcuts import render
from django.contrib import messages  # adicionar mensagens no Django
from .forms import ContatoForm, ProdutoModelForms
from .models import Produto
from django.shortcuts import redirect


# Create your views here.

def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            # nome = form.cleaned_data['nome']
            # email = form.cleaned_data['email']
            # assunto = form.cleaned_data['assunto']
            # mensagem = form.cleaned_data['mensagem']

            # print('Mensagem enviada!')
            # print(f'Nome: {nome}')
            # print(f'Email: {email}')
            # print(f'Assunto: {assunto}')
            # print(f'Mensagem: {mensagem}')

            form.send_mail()

            messages.success(request, 'Email enviado com sucesso!!!)')
            form = ContatoForm()
    context = {
        'form': form
    }

    return render(request, 'contato.html', context)


def produto(request):
    if str(request.user) != 'AnonymousUser':
        if request.method == 'POST':
            form = ProdutoModelForms(request.POST, request.FILES)  # tem que usar o files porque tem imagem
            if form.is_valid():
                # prod = form.save(commit=False)  # para nao mandar para o banco de dados, so conferir
                #
                # print(f'nome: {prod.nome}')
                # print(f'preco: {prod.preco}')
                # print(f'estoque: {prod.estoque}')
                # print(f'imagem: {prod.imagem}')

                form.save()

                messages.success(request, 'Produto salvo com sucesso!!!')
                form = ProdutoModelForms()  # para limpar o formulario
            else:
                messages.error(request, 'Erro ao salvar!!!')
        else:
            form = ProdutoModelForms()
        context = {
            'form': form
        }
        return render(request, 'produto.html', context)
    else:
        return redirect('index')
