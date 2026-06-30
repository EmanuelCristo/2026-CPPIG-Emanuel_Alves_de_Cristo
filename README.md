# Projeto Integrador: Gestão de Chaves

Um sistema web desenvolvido para automatizar, organizar e monitorar o fluxo de reservas e empréstimos de chaves do Centro de Tecnologia da Universidade Federal de Santa Maria (UFSM). O foco do projeto é garantir o rastreio do inventário de cópias, automatizar o controle de prazos e facilitar a rotina de atendimento nas portarias.

## Resumo do Sistema

O sistema simula o controle de chaves por um fluxo digital. Ele permite que usuários solicitem chaves antecipadamente e que os porteiros registrem as entregas e devoluções.

## Principais Funcionalidades

* **Rastreio Físico Individualizado:** Cadastro de salas categorizadas por Anexos (CT, Anexos A, B e C), com monitoramento exato do status de cada cópia física de uma chave (Disponível ou Quebrada).
* **Controle de Acesso por Perfil:** Interfaces e permissões dinâmicas adaptadas para o dia a dia de Administradores, Porteiros, Servidores e Alunos.
* **Regras de Negócio e Restrições:** O sistema trava tentativas inválidas automaticamente; Servidores podem reservar chaves de uso restrito ou comunitário, enquanto Alunos só possuem permissão para reservar salas do tipo comunitária.
* **Rotinas de Automação de Tempo:** Cancelamento automático de reservas caso o usuário não compareça no horário estipulado e disparo automático de alertas via e-mail para atrasos de devolução superiores a 24 horas.
* **Auditoria e Bloqueios:** Registro do porteiro responsável pela entrega/devolução e sistema de advertência que bloqueia automaticamente usuários que devolvam chaves danificadas repetidas vezes.
