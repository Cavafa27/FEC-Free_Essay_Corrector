# FEC-Free_Essay_Corrector
Projeto da imersão IA da Alura - Corretor de Redações para ENEM Automatizado


**ESCOLHA DA VERSÃO DO GEMINI**

A versão escolhida foi a gemini-1.5-pro-latest devido aos seguintes fatores:
- Ser a atual versão estável (10/05/2024).
- Ter sido a versão utilizada na interface do Google IA Studio para aprendizado e teste das hipóteses para este projeto.
- Permitir a manipulação de arquivos e imagens (Vision).

Devido ao fato desta versão ainda estar como "Preview", não foi possível configurar os parâmetros para consulta e geração. Caso fosse possível a configuração utilizada seria (resumo):

generation_config:
- "temperature": 0.5
- "top_p": 1,
- "top_k": 5,

**Comentário:**
Visto que o projeto visa a correção de redações para vestibulares, é importante que o resultado seja aproximado da realidade e do vocabulário utilizado neste contexto.
A temperatura em 0.5 e o Top K em 5 irão funcionar como um filtro de controle para a diversidade de palavras.
O Top P em 1 visa balancear as restrições impostas acima permitindo que vocabulários mais refinados possam ser utilizados.

safety_settings:
- "category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_ONLY_HIGH"
- "category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_ONLY_HIGH"
- "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_ONLY_HIGH"
- "category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_ONLY_HIGH"

**Comentário:**
Os filtros estão em "Block Few" pois como o projeto irá trabalhar com redações, ele precisará estar apto à trabalhar com os temas a serem dissertados nas propostas de redações, quem podem incluir assuntos sensíveis e que possívelmente entrariam em conflito com um filtro mais rigoroso. Foi mantido um mínimo de rigorosidade no filtro para evitar resultados efetivamente ofensivos.

