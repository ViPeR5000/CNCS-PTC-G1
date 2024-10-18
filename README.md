# CNCS-PTC-G1
 
# Servidor de Tarefas com Criptografia

Este repositório contém um servidor de tarefas simples que armazena as tarefas de forma criptografada usando a biblioteca Fernet.

## Descrição

O servidor permite que os clientes se conectem e executem as seguintes operações:

* Adicionar uma nova tarefa
* Listar as tarefas existentes
* Marcar uma tarefa como concluída

As tarefas são armazenadas em um arquivo chamado `todo_list.fernet` de forma criptografada. A chave de criptografia é armazenada no arquivo `key.fernet`.

## Como executar

1. Certifique-se de ter Python 3 instalado.
2. Instale a biblioteca Fernet:
pip install cryptography

3. Gere uma chave de criptografia:
python -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); print(key.decode())" > key.fernet

4. Execute o servidor:
python server_todo_fernet.py

5. Liga-se ao servidor usando um cliente TCP (por exemplo, netcat) na porta 8888.

## Formato dos comandos

Os comandos enviados ao servidor devem seguir o seguinte formato:

<opção>-<dados>


Onde:

* `<opção>` é um número que indica a operação desejada:
    * `1`: Adicionar tarefa (`<dados>` deve ser `título,descrição`)
    * `2`: Listar tarefas
    * `3`: Concluir tarefa (`<dados>` deve ser o índice da tarefa)
* `<dados>` são os dados necessários para a operação.

## Exemplos de comandos

* Adicionar uma tarefa: `1`
* Listar as tarefas: `2`
* Concluir a tarefa com índice 0: `3`

## Observações

* O servidor foi projetado para fins educacionais e demonstrativos.
* A segurança da criptografia depende da segurança da chave armazenada no arquivo `key.fernet`.
* O código pode ser modificado e melhorado para atender a necessidades específicas.