from django.shortcuts import render, HttpResponse


# Create your views here.

def cliente(request):
    context ={
        
    }
    return render(request, 'clientes.html', context)