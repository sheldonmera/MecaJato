from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import constants
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import Cliente,Carro
from utils.cpf_validador import validador_cpf
import json
import re


# Create your views here.

def cliente(request):
    
    if request.method == "GET":
        clientes = Cliente.objects.all()
        return render(request, 'clientes.html',{"clientes":clientes})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        cpf = request.POST.get('cpf')
        email = request.POST.get('email')
        carros = request.POST.getlist('carro')
        anos = request.POST.getlist('ano')
        placas = request.POST.getlist('placa')
        
        cliente_novo = Cliente(
            nome = nome,
            sobrenome = sobrenome,
            cpf = cpf,
            email = email,
        )
        verifica_cliente = Cliente.objects.filter(cpf=cpf)
        
        if verifica_cliente.exists():
            messages.add_message(request, constants.WARNING, 'CPF já cadastrado ! ')
            return render(request,'clientes.html', {'nome':nome, 'sobrenome':sobrenome, 'email':email,'carros': zip(carros, placas, anos)})
        
        if not re.fullmatch(r'^[a-z0-9.]+@[a-z0-9]+\.[a-z]+(\.[a-z]+)?$', email, re.IGNORECASE):
            messages.add_message(request, constants.WARNING, 'Email incorreto !')
            return render(request, 'clientes.html', {'nome':nome, 'sobrenome':sobrenome, 'cpf':cpf, 'carros': zip(carros, placas, anos)})
        
        if validador_cpf(cpf) is False:
            messages.add_message(request, constants.WARNING, 'CPF Inválido !')
            return render(request, 'clientes.html', {'nome':nome, 'sobrenome':sobrenome,  'email':email})
        
        cliente_novo.save()
        
        for modelo, ano, placa in zip(carros, anos, placas):
            carro_novo = Carro(
                modelo = modelo,
                ano = ano,
                placa = placa,
                cliente = cliente_novo,
            )
            
            #TODO fazer verificacao de placa
            carro_novo.save()
        messages.add_message(request, constants.SUCCESS, 'Carro(s) e Cliente Cadastrados !')
        return render(request, 'clientes.html')
    
def atualiza_cliente(request):
    #TODO arrumar para fazer a busca por cpf
    cpf_cliente = request.POST.get('cpf_cliente')
    cliente = Cliente.objects.filter(cpf=cpf_cliente)
    carros = Carro.objects.filter(cliente=cliente[0])
    cliente_json = json.loads(serializers.serialize('json', cliente))[0]['fields']
    cliente_id = json.loads(serializers.serialize('json', cliente))[0]['pk']
    carros_json = json.loads(serializers.serialize('json', carros))
    carros_json = [{'fields': i['fields'], 'id': i['pk']} for i in carros_json]
    data = {'cliente': cliente_json, 'carros': carros_json, 'cliente_id': cliente_id}
    print(data)
    return JsonResponse(data)
    

@csrf_exempt
def update_carro(request,id):
    modelo = request.POST.get('modelo')
    placa = request.POST.get('placa')
    ano = request.POST.get('ano')
    
    carro = Carro.objects.get(id=id)
    id_verifica = Carro.objects.filter(placa=placa).exclude(id=id)
    
    if id_verifica.exists():
        messages.add_message(request, constants.WARNING, 'Placa já cadastrada no sistema ! ')
        return render(request, 'clientes.html')
    
    carro.modelo = modelo
    carro.placa = placa
    carro.ano = ano
    carro.save()
    messages.add_message(request, constants.INFO, 'Carro alterado com sucesso !')
    return render(request, 'clientes.html')


def delete_carro(request,id):
    #carro = Carro.objects.get(id=id)
    try:
        id_verifica = Carro.objects.get(id=id)
        id_verifica.delete()
        messages.add_message(request, constants.INFO, 'Carro deletado com sucesso !')
        return redirect(reverse('cliente'))
        
    except:
        messages.add_message(request, constants.WARNING, 'Algo de eraado aconteceu, redirecionando... !')
        return redirect(reverse('cliente'))
    

# def atualiza_cliente(request):
    
#     if request.method == "POST":
#         cpf = request.POST.get('cpf_busca')
#         if validador_cpf(cpf) is False:
#             messages.add_message(request, constants.WARNING, 'CPF Inválido !')
            
#         dados_cliente = Cliente.objects.filter(cpf=cpf)
#         id_cliente = dados_cliente.values_list('id', flat=True).first()
#         carros_cliente = Carro.objects.filter(cliente__id=id_cliente)
        
#         #carros_json =json.loads(serializers.serialize('json',carros_cliente))
#         #cliente_json = json.loads(serializers.serialize('json',dados_cliente))[0]['fields']
        
#         return render(request, 'clientes.html',{"dados_cliente":dados_cliente, "carros_cliente":carros_cliente})