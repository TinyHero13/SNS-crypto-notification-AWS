# Notificador de Crypto na AWS

Este projeto implementa um **notificador de criptomoedas** utilizando diversos serviços da AWS, com foco em automação e escalabilidade. O fluxo principal consiste em uma função Lambda que, a cada 2 horas, realiza uma requisição à API CoinGecko para obter dados sobre criptomoedas e, em seguida, envia esses dados por e-mail utilizando o Amazon SNS.

## Arquitetura do Projeto
![Arquitetura do Projeto](/imgs/arq.png)

A arquitetura é composta por:
- **AWS Lambda**: para executar o código.
- **Amazon EventBridge**: para agendar e disparar a execução da função Lambda a cada 2 horas.
- **CoinGecko API**: para obter os dados das criptomoedas.
- **Amazon SNS**: para enviar as notificações via e-mail.

## Funcionalidades
- **Conexão com a API CoinGecko**: A função Lambda faz requisições à API CoinGecko para obter informações de criptomoedas.
- **Agendamento com Amazon EventBridge**: A função Lambda é executada automaticamente a cada 2 horas.
- **Envio de e-mails via Amazon SNS**: Após a execução da função Lambda, as informações sobre as criptomoedas são enviadas por e-mail.

## Tecnologias Utilizadas
- **AWS Lambda**: Serviço de computação sem servidor que permite executar código em resposta a eventos.
- **Python**: Linguagem utilizada para escrever a função Lambda que interage com a CoinGecko API e envia dados via SNS.
- **Amazon EventBridge**: Serviço de barramento de eventos que permite agendar e disparar eventos, como a execução da função Lambda.
- **Amazon SNS**: Serviço de notificação que envia mensagens (como e-mails) em resposta a eventos.
- **IAM**: Serviço de gerenciamento de identidade e acesso, usado para conceder permissões à função Lambda.

## Como Montar o Projeto

### 1. Criar uma Conta na AWS
Primeiro, você precisará criar uma conta na AWS para acessar e utilizar os serviços da plataforma. Caso já tenha uma conta, basta fazer login.

### 2. Criar um Tópico no SNS
1. Acesse o serviço **SNS** na AWS e crie um novo tópico do tipo "Standard", que permite o envio de notificações por SMS, e-mail ou HTTP.
2. Dê um nome ao seu tópico e, em seguida, crie uma **subscrição** para esse tópico, colocando um e-mail de sua escolha.
3. Após a criação do tópico e a inscrição, o sistema enviará um e-mail para o endereço informado. Você precisará confirmar a subscrição.

### 3. Criar Role e Policy no IAM
Para que o AWS Lambda possa publicar mensagens no SNS, você precisará criar uma **policy** que permita esse acesso.

1. Crie uma policy no IAM com o seguinte conteúdo, substituindo `SEU_ARN_SNS` pelo ARN do seu tópico SNS:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "sns:Publish",
            "Resource": "SEU_ARN_SNS"
        }
    ]
}
```

Depois, crie uma role para o Lambda e anexe a policy criada, além da AWSLambdaBasicExecutionRole, que é necessária para dar permissão de execução da função Lambda.

### 4. Criar o Lambda
Acesse o serviço Lambda e crie uma nova função.
Durante a configuração, na opção "Mudar cargo de execução padrão", escolha a role que você criou anteriormente.
Utilize um código em Python ou outra linguagem para extrair os dados desejados da CoinGecko API (veja o exemplo de código abaixo para referência).
Teste a função para garantir que ela está funcionando corretamente.

### 5. Configurar o Amazon EventBridge
No Amazon EventBridge, crie uma nova regra com a cron expression 0 */2 * * ? *, que agendará a execução da função Lambda a cada 2 horas.

Para entender melhor sobre as cron expressions, indico o site [CronTabGuru](https://crontab.guru).

Escolha AWS Lambda como o target da regra e selecione a função Lambda criada.
Após a configuração, a função Lambda será executada automaticamente a cada 2 horas.


Com esses passos, o notificador de criptomoedas estará pronto para funcionar automaticamente a cada 2 horas, enviando informações sobre o mercado de criptomoedas para o seu e-mail via SNS.