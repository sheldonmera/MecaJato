function add_carro(){

    container = document.getElementById("form-carro")

    html = "<br><div class='row'> <div class='col-md'> <input type='text' placeholder='carro' class='form-control' name='carro'></div> <div class='col-md'><input type='text' placeholder='Placa' class='form-control' name='placa'> </div> <div class='col-md'><input type='number' placeholder='Ano' class='form-control' name='ano'> </div></div>"

    container.innerHTML += html
}

function exibir_form(tipo){
    
    adiciona_cliente = document.getElementById('adicionar-cliente');
    atualiza_cliente = document.getElementById('busca_cliente');
    dados_atualiza_cliente = document.getElementById('form-att-cliente')

    if (tipo == "1") {
        atualiza_cliente.style.display = "none";
        adiciona_cliente.style.display = "block";
        document.getElementById("form_cadastrar_cliente").reset();

    }else if(tipo == "2") {
        atualiza_cliente.style.display = "block";
        adiciona_cliente.style.display = "none";
        document.getElementById("form_alterar_cliente").reset();
        
    }
}

function dados_cliente() {
    cliente = document.getElementById('cliente-select');
    
    csrf_token = document.querySelector('[name=csrfmiddlewaretoken]').value;
    cpf_cliente = cliente.value;

    data = new FormData();
    data.append('cpf_cliente', cpf_cliente);
    fetch("/cliente/busca_cliente/", {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: data 
    }).then(function(result) {
        return result.json();
    }).then(function(data) {
        document.getElementById('form-att-cliente').style.display = 'block';

        id = document.getElementById('id');
        id.value = data['cliente_id'];

        nome = document.getElementById('nome');
        nome.value = data['cliente']['nome'];

        sobrenome = document.getElementById('sobrenome');
        sobrenome.value = data['cliente']['sobrenome'];

        cpf = document.getElementById('cpf');
        cpf.value = data['cliente']['cpf'];

        email = document.getElementById('email');
        email.value = data['cliente']['email'];

        div_carros =document.getElementById('carros')
        div_carros.innerHTML = ""
        for(i=0; i<data['carros'].length; i++){
            div_carros.innerHTML+= "<form  action = '/cliente/update_carro/"+ data['carros'][i]['id'] +"' method = 'POST'>\
            <div class= 'row'>\
                <div class= 'col-md'>\
                    <input class='form-control' type='text' name = 'modelo' value = '"+ data['carros'][i]['fields']['modelo'] +"'>\
                </div>\
                <div class= 'col-md'>\
                    <input class='form-control' type='text' name = 'placa' value = '"+ data['carros'][i]['fields']['placa'] +"'>\
                </div>\
                <div class= 'col-md'>\
                    <input class='form-control' type='text' name = 'ano' value = '"+ data['carros'][i]['fields']['ano'] +"'>\
                </div>\
                <div class= 'col-md'>\
                    <input class='btn btn-primary' type='submit' name = 'Salvar' value='Salvar''>\
                </div>\
                <div class= 'col-md'>\
                    <a class='btn btn-danger' href='/cliente/delete_carro/"+data['carros'][i]['id']+"'>Excluir</a>\
                </div>\
            </div>\
        </form>\
            <br>"

        }

        
    });
}


function update_cliente(){

    nome = document.getElementById('nome').value
    sobrenome = document.getElementById('sobrenome').value
    email = document.getElementById('email').value
    cpf = document.getElementById('cpf').value
    id = document.getElementById('id').value
    

    fetch("/cliente/update_cliente/"+ id, {
        method: "POST",
        headers: {
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify({

            nome: nome,
            sobrenome: sobrenome,
            email: email,
            cpf: cpf,

        })
    
    }).then(function(result){
        return result.json()
    }).then(function(data){
        if (data['status']=='200'){
            nome = data['nome'];
            sobrenome = data['sobrenome'];
            email = data['email'];
            cpf = data['cpf'];
        }else{
            $('.alert-primary').alert()
        }
    })

}