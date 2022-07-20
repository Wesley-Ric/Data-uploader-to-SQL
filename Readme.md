# Uploader
## Feito para pegar arquivo .txt formatados no computador e os subir para o banco de dados.

O código feito tem como objetivo:
* Abrir o explorer, pegar o caminho do arquivo e armazenar em uma variavél.
* Testar diversos tipos de erros com if, elif e else.
* Ler o arquivo e indicar ',' como separação e a linguagem para 'latin-1' usando o pandas
* Cria um dataframe com pandas indicando quais são as colinas da 'variavél1' no caso 'cod, qtd, tipo, dt, hr'
* Converte cod, qtd, tipo, dt, hr em string, dt e hr em datetime formatando ht com o dia primeiro e hr em hora, minutos e segundos
* faz a conexão com o servidor e sobe os dados do arquivo para a tabela do banco

### Ifs, elif e else.

Para que o programa rode sem erros temos que testar:
1. Conexão com internet.
~~~python
if aberto == 0:     #testa se está vazio pelo getsize
    tkinter.messagebox.showinfo('Erro!' , 'O arquivo enviado está vazio')
else:
~~~
2. Se a variavél camarq (caminho do arquivo) está vazia

~~~python
if txtCaminho['text'] == '':        #se estiver sem caminho do arquivo não roda
    tkinter.messagebox.showinfo('Erro!' , 'Nenhum arquivo foi selecionado')
~~~

3. Se a extenção é aceita.

~~~python
elif camarq.endswith('.wes') == False:  #testa se a extensão é compatível
    tkinter.messagebox.showinfo('Erro!' , 'A extensão do arquivo não é aceita!\n'
                                        'apenas arquivos ".wes" são aceitos!') 
else:
~~~

4. Se o arquivo está vazio usando getsize

~~~python
aberto = os.path.getsize(camarq)    #atribui o tamanho do arquivo a variável
if aberto == 0:     #testa se está vazio pelo getsize
    tkinter.messagebox.showinfo('Erro!' , 'O arquivo enviado está vazio')
else:
~~~

5. Se existe o cabeçalho (header) no arquivo

~~~python
if header in line:  #se tiver 'cod,qtd,tipo,ht,hr' na linha
    variavel1 = pandas.read_csv(camarq, sep=',', encoding='latin-1')    #usa pandas para ser o arquivo csv na variável camarq, indicando que está separado por ',' e escrito em latin-1
    df = pandas.DataFrame(variavel1, columns=['cod', 'qtd', 'tipo', 'dt', 'hr'])    #cria um quadro de dados(dataframe) que pega a variavel1 e indicas as colunas que são o header
    df = df.astype({
        #converte os valores das colunas em strings respectivamente
        "cod": str,
        "qtd": str,
        "tipo": str,
    })
    df['dt']= pandas.to_datetime(df['dt'],dayfirst=True)    #converte os valores da coluna em datetime (apenas data) com dias primeiro
    df['hr'] = pandas.to_datetime(df['hr'], format='%H:%M:%S').dt.time  #converte os valores da coluna em horario no formato hora, minutos e segundos
    conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' #abre conexão com o banco de dados
                            'Server=tcp:myserver.database.windows.net;'
                            'Database=restaurante;'
                            'UID=myusername;'
                            'PWD=mypassword;'
                            )
    cursor = conn.cursor()
    for row in df.itertuples(): #para cada fileira na tubla do df
        cursor.execute('''INSERT INTO base_refeicao (cod, qtd, tipo, dt, hr) VALUES (?,?,?,?,?)''', #executa o comando sql para inserir os valores nas culunas do banco de dados
                        row[1],
                        row[2],
                        row[3],
                        row[4],
                        row[5]
                        )
        cursor.commit() #fecha a conexão
    for x in range(10):
        progressBr['value'] +=10
        tela.update_idletasks()
        time.sleep(0.1) #carrega a barra de progresso
    tkinter.messagebox.showinfo('Sucesso!' ,'A conexão com o banco foi bem sucedida!\n'
                                            'Os valores foram adicionados ao banco de dados')
    break   #fecha o for quando os dados do txt terminam de ser adicionados no banco de dados
else:
    tkinter.messagebox.showinfo('Erro!' , 'O arquivo não apresenta os dados corretos!') #tratamento de erro caso não tenha header
    break
~~~

### Proximos passos

Após testar se existe header no arquivo o script define ',' como a separação das colunas usando a biblioteca pandas `variavel1 = pandas.read_csv(camarq, sep=',', encoding='latin-1')`

depois cria um dataframe representado por df puxando a variavel1 para indicar a separação das colunas e nomeando as colunas através do pandas com o metodo DataFrame `df = pandas.DataFrame(variavel1, columns=['cod', 'qtd', 'tipo', 'dt', 'hr'])`

Subsequente converte as colunas em Strings:

~~~python
df = df.astype({
    #converte os valores das colunas em strings respectivamente
    "cod": str,
    "qtd": str,
    "tipo": str,
})
~~~

Então transforma dt e hr em datetime e indica o seu formato em dia primeiro e horas, minutos e segundos:

~~~python
df['dt']= pandas.to_datetime(df['dt'],dayfirst=True)    #converte os valores da coluna em datetime (apenas data) com dias primeiro
df['hr'] = pandas.to_datetime(df['hr'], format='%H:%M:%S').dt.time
~~~

#### Data.
Logo após isso o script pega a data do pc por meio da biblioteca datetime e a converte em string para ser gravada no arquivo .txt com os comandos:
~~~python
from datetime import date
data = str(date.today())
~~~

Abre a conexão com o servidor SQL:

~~~python
conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};' #abre conexão com o banco de dados
                        'Server=tcp:myserver.database.windows.net;'
                        'Database=restaurante;'
                        'UID=myusername;'
                        'PWD=mypassword;'
                        )
~~~
Cria o cursor para executar os comandos so SQL e insere nas colunas do banco de dados os valores dos arquivos .txt e fecha a conexão:

~~~python
for row in df.itertuples(): #para cada fileira na tubla do df
    cursor.execute('''INSERT INTO base_refeicao (cod, qtd, tipo, dt, hr) VALUES (?,?,?,?,?)''', #executa o comando sql para inserir os valores nas culunas do banco de dados
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5]
                    )
    cursor.commit() #fecha a conexão
~~~


# em suma é isso, obrigado por ler sobre meu código, se possivel me siga e favorite meus commits <3