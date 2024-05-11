# FEC-Free_Essay_Corrector
## Projeto Imersão IA Alura + Google - Corretor de Redações para ENEM automatizado

![fec.png]([URL da imagem](https://github.com/Cavafa27/FEC-Free_Essay_Corrector/blob/main/FEC.png))


**INSTRUÇÕES:** Será solicitado ao usuário que dê entrada de um texto para a correção. Isso pode ser feito com qualquer texto desejado. No arquivo "Redações para teste da aplicação" há dois textos disponíveis para teste. 

**OBJETIVO:** Universalizar o acesso à correção de redações para vestibulares.

**PÚBLICO ALVO:** Estudantes carentes candidatos ao Ensino Superior.

**DESCRIÇÃO:** A preparação para o ENEM e vestibulares é uma etapa fundamental na vida de todos. Devido à profunda desigualdade social, estudantes que não podem pagar um curso pré-vestibular ou professor acabam por não ter acesso à ferramentas que lhes permitam competir em pé de igualdade com os demais candidatos. O **FEC** foi desenvolvido para que qualquer pessoa que possua um celular possa treinar sua escrita recebendo um feedback detalhado sobre sua produção, assim como uma estimativa de nota simulando os critérios do ENEM.

**ALIMENTAÇÃO DO MODELO:** O Modelo foi alimentado utilizando as orientações e critérios utilizados para correção de redações do ENEM definidos pelo ministério da cultura (MEC)
Os dados utilizados podem ser encontrados em: http://portal.mec.gov.br/ultimas-noticias/418-enem-946573306/81381-conheca-as-cinco-competencias-cobradas-na-redacao-do-enem

**OBSERVAÇÕES:** O projeto original partia da premissa que seria possível selecionar um arquivo a partir do Google Drive para ser processado pela Gemini e posteriormente avaliado e corrigido. Após a constatação que para isso seria necessário ativar a Google Cloud Vision API, e por não ter certeza se isso seria permitido no concurso, o projeto foi adaptado para a entrada manual de texto.

**ESCOLHA DA VERSÃO DO GEMINI:** A versão escolhida foi a gemini-1.5-pro-latest devido aos seguintes fatores:
- Ser a atual versão estável (10/05/2024).
- Ter sido a versão utilizada na interface do Google IA Studio para aprendizado e teste das hipóteses para este projeto.

Devido ao fato desta versão ainda estar como "Preview", não foi possível configurar os parâmetros para consulta e geração. Caso fosse possível a configuração utilizada seria (resumo):

generation_config: (não utilizado devido à versão)
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

**LEGAL:** Os textos disponíveis para teste ou foram cedidos pessoalmente para o projeto, ou estão disponíveis gratuitamente na internet como modelos de redação.
