#bibliotecas gui
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox

#biblioteca para pegar o tempo
import time

#bibliotecas de banco de dados
import pyodbc
import pandas

#biblioteca de O.S e teste de internet
import os
import urllib.request
def teste_conexao():    #testa a internet usando o google
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

if teste_conexao() == False:    #se estiver sem conexão o programa não roda
    tkinter.messagebox.showinfo('Erro!' , 'O computador está sem internet!\n'
                                              'Conecte-se a internet ou entre em contato com um técnico para resolver.')
else:
    tela = Tk() #gui com tkinter
    tela.title('Leitor de pontos')
    tela.geometry('1082x620+500+200')
    tela['bg'] = "#d9d9d9"
    tela.resizable(width=False, height=False)
    icone=PhotoImage(file='venv/imgs/icon.png')
    tela.iconphoto(False, icone)

    def abrirarq():
        if teste_conexao() == False :   #testa a conexão quando invoca a função
            tkinter.messagebox.showinfo('Erro!' , 'O computador está sem internet!\n'
                                                  'Conecte-se a internet ou entre em contato com um técnico para resolver.')
        else :
            txtCaminho['text'] = '' #seta o label como vazio, para apagar o texto ao clicar (caso a pessoa escolha mais de um arquivo)
            global camarq   #variável global para usar em outras funções
            camarq = askopenfilename()  #abre o explorer pra pessoa escolher o arquivo
            txtCaminho['text'] = camarq #mostra o caminho do arquivo no lbl

    def jogasql():
        if teste_conexao() == False :
            tkinter.messagebox.showinfo('Erro!' , 'O computador está sem internet!\n'
                                                  'Conecte-se a internet ou entre em contato com um técnico para resolver.')
        else :
            #tratamento de erros
            if txtCaminho['text'] == '':        #se estiver sem caminho do arquivo não roda
                tkinter.messagebox.showinfo('Erro!' , 'Nenhum arquivo foi selecionado')
            elif camarq.endswith('.wes') == False:  #testa se a extensão é compatível
                tkinter.messagebox.showinfo('Erro!' , 'A extensão do arquivo não é aceita!\n'
                                                      'apenas arquivos ".wes" são aceitos!')
            else:
                progressBr['value'] = 0 #seta a barra de progresso em 0
                tela.update_idletasks()

                aberto = os.path.getsize(camarq)    #atribui o tamanho do arquivo a variável
                if aberto == 0:     #testa se está vazio pelo getsize
                    tkinter.messagebox.showinfo('Erro!' , 'O arquivo enviado está vazio')
                else:
                    header = "cod,qtd,tipo,dt,hr"
                    abrido = open(camarq, 'r')  #'abrido' foi de propósito (muito melhor que aberto)
                    for line in abrido: #para cada linha no arquivo
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



    #GUI
    ftitulo = Frame(tela, bg='red')
    ftitulo.pack(side=TOP, fill=X)
    fcorpo = Frame(tela, bg='#d9dee8')
    fcorpo.pack(fill=BOTH, expand=True)

    #titulo
    lblTitulo = Label(ftitulo, text='Upload de arquivos', width=100, height=3)
    lblTitulo ['bg'] = '#00a0f5'
    lblTitulo ['font'] = 'Calibri 20 bold'
    lblTitulo ['fg'] = '#ffffff'
    lblTitulo.pack(side=TOP, fill=X, ipady=10)

    #Sustenido + lbl de texto
    lblsustenido1 = Label(fcorpo, text='*')
    lblsustenido1['bg']='#d9dee8'
    lblsustenido1['font']='Calibri 20'
    lblsustenido1['fg']='red'
    lblsustenido1.place(x=80,y=75)

    lblTitCam = Label(fcorpo, text='Código do crachá:')
    lblTitCam['bg']='#d9dee8'
    lblTitCam['font']='Calibri 20'
    lblTitCam['fg']='#0055be'
    lblTitCam.place(x=100,y=75)

    #caminho de texto como txtbox para que possa digitar o ditetorio
    txtCaminho= Label(fcorpo, width=70, relief='flat', highlightthickness=2, anchor='w', justify='left')
    txtCaminho.config(highlightbackground='#78879b', highlightcolor='#d9dee8')
    txtCaminho['font']='Calibri 18'
    txtCaminho['fg']='black'
    txtCaminho.focus_set()
    txtCaminho.place(x=78,y=135, height=40)

    btnCaminho = Button(fcorpo, width=10, text='. . .', command=abrirarq)
    btnCaminho.place(x=928,y=135, height=40)

    imgbtnLerArq = PhotoImage(file='imgs/button_ler-arquivouni.png')
    imgbtnSair = PhotoImage(file='imgs/button_sairuni.png')

    btnLerArq = Button(fcorpo, image=imgbtnLerArq, borderwidth=0, bg='#d9dee8', activebackground='#d9dee8', command=jogasql)
    btnLerArq.place(x=170,y=250)

    btnSair = Button(fcorpo, image=imgbtnSair, borderwidth=0, bg='#d9dee8', activebackground='#d9dee8', command=tela.destroy)
    btnSair.place(x=550,y=250)


    #barra de progresso
    progressBr = ttk.Progressbar(tela, orient=HORIZONTAL, length=980)
    progressBr.place(x=50,y=525, height=50)



    tela.mainloop()