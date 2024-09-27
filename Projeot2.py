import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Importar a base de dados
Tabela_Excel = pd.read_excel('Vendas.xlsx')

# Visualizar a base de dados, Faturamento das lojas e quantidade de produtos vendidos por cada loja
a = Tabela_Excel[['ID Loja', 'Quantidade', 'Valor Final']].groupby('ID Loja').sum()

# Ticket médio por produto em cada loja
b = a['Valor Final'] / a['Quantidade']
a['Ticket Médio'] = b

# Converter a tabela em formato HTML
tabela_html = a.to_html()

# Configurações do e-mail
gmail_user = 'pedrolucasgraciano.py@gmail.com'
gmail_password = 'ogpo nasq tqur fnfm'
destinatario = 'predograciano@gmail.com'
assunto = 'Faturamento de Setembro'

# Corpo do e-mail com a tabela em HTML
corpo = f'''
<html>
  <body>
    <p>Prezados,</p>
    <p>Segue relatório do mês de agosto do faturamento das lojas:</p>
    {a.to_html(formatters={"Valor Final": 'R${:,.2f}'.format,"Ticket Médio": 'R${:,.2f}'.format})}
    <p>Atenciosamente,<br>Pedro Lucas Graciano</p>
  </body>
</html>
'''

# Criando a mensagem
msg = MIMEMultipart('alternative')
msg['From'] = gmail_user
msg['To'] = destinatario
msg['Subject'] = assunto

# Anexando o corpo HTML ao e-mail
msg.attach(MIMEText(corpo, 'html'))

try:
    # Conectando ao servidor SMTP do Gmail
    servidor = smtplib.SMTP('smtp.gmail.com', 587)
    servidor.starttls()  # Iniciando a conexão criptografada
    servidor.login(gmail_user, gmail_password)  # Fazendo login

    # Enviando o e-mail
    servidor.sendmail(gmail_user, destinatario, msg.as_string())
    print('E-mail enviado com sucesso!')

    servidor.quit()  # Fechando a conexão

except Exception as e:
    print(f'Erro ao enviar e-mail: {e}')


