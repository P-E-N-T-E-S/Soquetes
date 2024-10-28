<p align="center">
  <img
    src="https://img.shields.io/badge/Status-Em%20desenvolvimento-green?style=flat-square"
    alt="Status"
  />
</p>

<p align="center">
  <img
    src="https://img.shields.io/github/repo-size/P-E-N-T-E-S/Soquetes?style=flat"
    alt="Repository Size"
  />
  <img
    src="https://img.shields.io/github/languages/count/P-E-N-T-E-S/Soquetes?style=flat&logo=python"
    alt="Language Count"
  />
  <img
    src="https://img.shields.io/github/commit-activity/t/P-E-N-T-E-S/Soquetes?style=flat&logo=github"
    alt="Commit Activity"
  />
  <a href="LICENSE.md"
    ><img
      src="https://img.shields.io/github/license/P-E-N-T-E-S/Soquetes"
      alt="License"
  /></a>
</p>

## 📄 Descrição do Projeto

<p float="left">

<img align="right" width="150" src="https://png.pngtree.com/png-vector/20220903/ourmid/pngtree-ethernet-port-png-image_6135720.png" />

Esta aplicação cliente-servidor foi desenvolvida para fornecer um transporte confiável de dados em um ambiente onde ocorrem perdas de pacotes e erros simulados. O projeto utiliza sockets para comunicação entre cliente e servidor e implementa mecanismos de controle de fluxo e controle de congestionamento, garantindo a integridade e a entrega dos dados.

## 🔧 Funcionalidades
### 🖥️ Cliente
- **Conexão com o Servidor**: Permite conexão ao servidor via **localhost** ou **IP**.
- **Envio de Pacotes**: Capacidade de enviar pacotes individuais ou em grupos (rajadas).
- **Simulação de Erros**: Possibilidade de inserir erros de integridade em pacotes específicos.
- **Atualização Dinâmica**: A janela de recepção do servidor é atualizada em tempo real, considerando as confirmações recebidas e perdas de pacotes.

### 🌐 Servidor
- **Gerenciamento de Pacotes**: O servidor pode marcar pacotes que não serão confirmados e incluir erros de integridade nas confirmações.
- **Confirmações Negativas**: Capacidade de sinalizar ao cliente sobre confirmações negativas.
- **Negociação de Protocolo**: O cliente e o servidor podem negociar se utilizarão repetição seletiva ou o protocolo Go-Back-N.
- **Janela de Recepção**: A janela de recepção é informada e atualizada dinamicamente para o cliente.

## 📪 Protocolo de Aplicação
Um protocolo de aplicação foi desenvolvido e documentado, incluindo regras para:
- Requisições e respostas
- Soma de verificação
- Número de sequência
- Reconhecimento e reconhecimento negativo
- Controle de janela e paralelismo

## ♟️ Simulação de Falhas
A aplicação permite a simulação de falhas de integridade e perdas de mensagens, possibilitando a inserção de 'erros' que podem ser verificados pelo servidor.

## 📎 Requisitos
- **Ambiente**: A aplicação requer um ambiente que suporte sockets para a comunicação entre cliente e servidor.
- **Linguagem**: O projeto foi desenvolvido em [especificar a linguagem de programação, por exemplo, Python, Java, etc.].

## 👩‍💻 Membros de CC

<ul>
  <li>
    <a href="https://github.com/Thomazrlima">Thomaz Lima</a> - trl@cesar.school 📩
  </li>
  <li>
    <a href="https://github.com/hsspedro">Pedro Henrique Silva</a> - phss@cesar.school 📩
  </li>
  <li>
    <a href="https://github.com/Sofia-Saraiva">Sofia Saraiva</a> - spscl@cesar.school 📩
  </li>
  <li>
    <a href="https://github.com/Nerebo">André Goes</a> - algcf@cesar.school 📩
  </li>
  <li>
    <a href="https://github.com/evaldocunhaf">Evaldo Galdino</a> - egcf@cesar.school 📩
  </li>
</ul>

<br>

<a href="https://github.com/P-E-N-T-E-S/Soquetes/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=P-E-N-T-E-S/Soquetes" />
</a>
