Postmon-python
==============

Python wrapper to Postmon API

Utilização
-----------

* Instalação:

        pip install postmon

* Uso:

        from postmon import buscar_cep
 
        cep = buscar_cep('01419101')

        cidade = cep.cidade
        estado = cep.estado
        logradouro = cep.logradouro
        bairro = cep.bairro

        print logradouro + ', ' + bairro + ' - ' + cidade + '/' + estado
