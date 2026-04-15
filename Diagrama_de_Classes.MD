---
config:
  layout: elk
  theme: neutral
  look: neo
---
classDiagram
    class Pessoa{
        String Nome
        String e-mail
        String foto
        bool permissão
        bool bloqueado
        int Quantidade de Danos
    }
    class Servidor{
        Int SIAPE
        String Função
    }
    class Aluno{
        Int Matrícula
    }
    class Salas{
        String Nome
        String Tipo
        String Anexo
    }
    class Chave{
        String Sala
    }
    class Emprestimo{
        date Data Retirada
        data Data Devolução
        String Status
    }
    class Reserva{
        date Inicio da Reserva
        date Fim da Reserva
        Strint Status
    }
    class Copia_Chave{
        int Numero da Copia
        int ID
        String Status
    }
    class Porteiro{
        String Nome
        String e-mail
    }

    Pessoa<|--Servidor
    Pessoa<|--Aluno

    Salas "1" *-- "1" Chave : Possui
    Reserva "1..n" o-- "1" Pessoa: Pede
    Reserva "1..n" -- "0..n" Emprestimo: Gera
    Emprestimo "1" --* "1..n" Copia_Chave: Empresta
    Pessoa "1" -- "1..n" Emprestimo: Realiza
    Reserva "1" --* "1" Chave: Reserva
    Chave "1" *-- "1..n" Copia_Chave
    Porteiro "1" -- "1..n" Emprestimo: Confirma Entrega
    Porteiro "1" -- "1..n" Emprestimo: Confirma Retirada
