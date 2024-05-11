{
  "cells": [
    {
      "cell_type": "markdown",
      "metadata": {
        "colab_type": "text",
        "id": "view-in-github"
      },
      "source": [
        "<a href=\"https://colab.research.google.com/github/Cavafa27/FEC-Free_Essay_Corrector/blob/main/FEC_Free_Essay_Corrector.ipynb\" target=\"_parent\"><img src=\"https://colab.research.google.com/assets/colab-badge.svg\" alt=\"Open In Colab\"/></a>"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "OcNj_nXnYKp5"
      },
      "source": [
        "**Instalação de Pacotes**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 1,
      "metadata": {
        "id": "u6XpJ-Ugq0ig"
      },
      "outputs": [],
      "source": [
        "!pip install -U -q google-generativeai"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "GJA_LlwVYTWP"
      },
      "source": [
        "**Configuração de API e Importação de Ferramentas**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 2,
      "metadata": {
        "id": "3Huow5AcYZBq"
      },
      "outputs": [],
      "source": [
        "import google.generativeai as genai\n",
        "\n",
        "from google.colab import userdata\n",
        "\n",
        "GOOGLE_API_KEY= userdata.get('API_FEC')\n",
        "genai.configure(api_key=GOOGLE_API_KEY)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "t9QUEDRbhy46"
      },
      "source": [
        "**Configurando os parâmentros do modelo**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 3,
      "metadata": {
        "id": "Yr2AX9qah1oy"
      },
      "outputs": [],
      "source": [
        "# Parâmetros em default pela impossibilidade de mudança na versão atual.\n",
        "generation_config = {\n",
        "  \"temperature\": 1,\n",
        "  \"top_p\": 0.95,\n",
        "  \"top_k\": 0,\n",
        "  \"max_output_tokens\": 8192,\n",
        "}\n",
        "\n",
        "# Define o nível de exigência que será considerado pelo modelo. Podem ser atribuídos valores como: moderado, exigente, leniente, ultra-rigoroso, etc.\n",
        "nivelexigencia = \"rigoroso\"\n",
        "system_instruction =f\"Você é um {nivelexigencia} professor de língua portuguesa especializado em produção de texto\"\n",
        "\n",
        "# Define os filtros de segurança como \"Block low\" para que o modelo saiba lidar com temas sensíveis que podem ocorrer nos temas das redações.\n",
        "safety_settings = [\n",
        "  {\n",
        "    \"category\": \"HARM_CATEGORY_HARASSMENT\",\n",
        "    \"threshold\": \"BLOCK_ONLY_HIGH\"\n",
        "  },\n",
        "  {\n",
        "    \"category\": \"HARM_CATEGORY_HATE_SPEECH\",\n",
        "    \"threshold\": \"BLOCK_ONLY_HIGH\"\n",
        "  },\n",
        "  {\n",
        "    \"category\": \"HARM_CATEGORY_SEXUALLY_EXPLICIT\",\n",
        "    \"threshold\": \"BLOCK_ONLY_HIGH\"\n",
        "  },\n",
        "  {\n",
        "    \"category\": \"HARM_CATEGORY_DANGEROUS_CONTENT\",\n",
        "    \"threshold\": \"BLOCK_ONLY_HIGH\"\n",
        "  },\n",
        "]\n",
        "\n",
        "# Define o modelo a ser utilizado e seus parâmetros\n",
        "model = genai.GenerativeModel(model_name=\"gemini-1.5-pro-latest\",\n",
        "                              generation_config=generation_config,\n",
        "                              system_instruction=system_instruction,\n",
        "                              safety_settings=safety_settings)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "_Gup8IfOAlOJ"
      },
      "source": [
        "**Entrada de informações de referência**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 4,
      "metadata": {
        "id": "bG_99clgAklV"
      },
      "outputs": [],
      "source": [
        "chat = model.start_chat(history=[\n",
        "# Entrada das orientações para correções de redações do ENEM feitas pelo MEC.\n",
        "  {\n",
        "    \"role\": \"user\",\n",
        "    \"parts\": [\"Armazene\\nas informações abaixo no contexto para referência futura\\n\\n\\n\\nCritério\\n01 - Domínio da escrita formal da língua portuguesa\\n\\nInstrução\\nsobre o critério: É avaliado se a redação do participante está adequada às\\nregras de ortografia, como acentuação, ortografia, uso de hífen, emprego de\\nletras maiúsculas e minúsculas e separação silábica. Ainda são analisadas a\\nregência verbal e nominal, concordância verbal e nominal, pontuação,\\nparalelismo, emprego de pronomes e crase.\\n\\nPontuação – Descrição\\n\\n200 pontos – Demonstra excelente domínio da modalidade escrita formal da\\nlíngua portuguesa e de escolha de registro. Desvios gramaticais ou de\\nconvenções da escrita serão aceitos somente como excepcionalidade e quando não\\ncaracterizarem reincidência.\\n\\n160 pontos – Demonstra bom domínio da modalidade escrita formal da língua\\nportuguesa e de escolha de registro, com poucos desvios gramaticais e de\\nconvenções da escrita.\\n\\n120 pontos – Demonstra domínio mediano da modalidade escrita formal da\\nlíngua portuguesa e de escolha de registro, com alguns desvios gramaticais e de\\nconvenções da escrita.\\n\\n80 pontos – Demonstra domínio insuficiente da modalidade escrita formal\\nda língua portuguesa, com muitos desvios gramaticais, de escolha de registro e\\nde convenções da escrita.\\n\\n40 pontos – Demonstra domínio precário da modalidade escrita formal da\\nlíngua portuguesa, de forma sistemática, com diversificados e frequentes\\ndesvios gramaticais, de escolha de registro e de convenções da escrita.\\n\\n0 ponto – Demonstra desconhecimento da modalidade escrita formal da\\nlíngua portuguesa.\\n\\n\\n\\nCritério\\n02 - Compreender o tema e não fugir do que é proposto\\n\\nInstrução\\nsobre o critério: Avalia as habilidades integradas de leitura e de escrita do\\ncandidato. O tema constitui o núcleo das ideias sobre as quais a redação deve\\nser organizada e é caracterizado por ser uma delimitação de um assunto mais\\nabrangente.\\n\\nPontuação\\n– Descrição\\n\\n200 pontos\\n– Desenvolve o tema por meio de argumentação consistente, a partir de um\\nrepertório sociocultural produtivo e apresenta excelente domínio do texto\\ndissertativo-argumentativo.\\n\\n160 pontos\\n– Desenvolve o tema por meio de argumentação consistente e apresenta bom\\ndomínio do texto dissertativo-argumentativo, com proposição, argumentação e\\nconclusão.\\n\\n120 pontos\\n- Desenvolve o tema por meio de argumentação previsível e apresenta domínio\\nmediano do texto dissertativo-argumentativo, com proposição, argumentação e\\nconclusão.\\n\\n80 pontos\\n– Desenvolve o tema recorrendo à cópia de trechos dos textos motivadores ou\\napresenta domínio insuficiente do texto dissertativo-argumentativo, não\\natendendo à estrutura com proposição, argumentação e conclusão.\\n\\n40 pontos\\n– Apresenta o assunto, tangenciando o tema, ou demonstra domínio precário do\\ntexto dissertativo-argumentativo, com traços constantes de outros tipos\\ntextuais.\\n\\n0 ponto\\n– Fuga ao tema/não atendimento à estrutura dissertativo-argumentativa. Nestes\\ncasos a redação recebe nota zero e é anulada.\\n\\n\\n\\nCritério\\n03 - Selecionar, relacionar, organizar e interpretar informações, fatos,\\nopiniões e argumentos em defesa de um ponto de vista\\n\\nInstrução\\nsobre o critério: O candidato precisa elaborar um texto que apresente,\\nclaramente, uma ideia a ser defendida e os argumentos que justifiquem a posição\\nassumida em relação à temática da proposta da redação. Trata da coerência e da\\nplausibilidade entre as ideias apresentadas no texto, o que é garantido pelo\\nplanejamento prévio à escrita, ou seja, pela elaboração de um projeto de texto.\\n\\nPontuação       Descrição\\n\\n200 pontos\\n– Apresenta informações, fatos e opiniões relacionados ao tema proposto, de\\nforma consistente e organizada, configurando autoria, em defesa de um ponto de\\nvista.\\n\\n160 pontos\\n– Apresenta informações, fatos e opiniões relacionados ao tema, de forma\\norganizada, com indícios de autoria, em defesa de um ponto de vista.\\n\\n120 pontos\\n– Apresenta informações, fatos e opiniões relacionados ao tema, limitados aos\\nargumentos dos textos motivadores e pouco organizados, em defesa de um ponto de\\nvista.\\n\\n80 pontos\\n– Apresenta informações, fatos e opiniões relacionados ao tema, mas\\ndesorganizados ou contraditórios e limitados aos argumentos dos textos\\nmotivadores, em defesa de um ponto de vista.\\n\\n40 pontos\\n– Apresenta informações, fatos e opiniões pouco relacionados ao tema ou\\nincoerentes e sem defesa de um ponto de vista.\\n\\n0 ponto  - Apresenta informações, fatos e opiniões não\\nrelacionados ao tema e sem defesa de um ponto de vista.\\n\\n\\n\\n\\n\\nCritério\\n04 – Conhecimento dos mecanismos linguísticos necessários para a construção da\\nargumentação\\n\\nInstrução\\nsobre o critério: São avaliados itens relacionados à estruturação lógica e\\nformal entre as partes da redação. A organização textual exige que as frases e\\nos parágrafos estabeleçam entre si uma relação que garanta uma sequência\\ncoerente do texto e a interdependência entre as ideias.\\n\\n\\n\\nPreposições,\\nconjunções, advérbios e locuções adverbiais são responsáveis pela coesão do\\ntexto porque estabelecem uma inter-relação entre orações, frases e parágrafos.\\nCada parágrafo será composto por um ou mais períodos também articulados. Cada\\nideia nova precisa estabelecer relação com as anteriores.\\n\\nPontuação\\n- Descrição\\n\\n200 pontos\\n– Articula bem as partes do texto e apresenta repertório diversificado de\\nrecursos coesivos.\\n\\n160 pontos\\n– Articula as partes do texto, com poucas inadequações, e apresenta repertório\\ndiversificado de recursos coesivos.\\n\\n120 pontos\\n– Articula as partes do texto, de forma mediana, com inadequações, e apresenta\\nrepertório pouco diversificado de recursos coesivos.\\n\\n80 pontos\\n– Articula as partes do texto, de forma insuficiente, com muitas inadequações e\\napresenta repertório limitado de recursos coesivos.\\n\\n40 pontos\\n– Articula as partes do texto de forma precária.\\n\\n0 ponto\\n– Não articula as informações.\\n\\n\\n\\nCritério\\n05 - Respeito aos direitos humanos\\n\\nInstrução\\nsobre o critério: Apresentar uma proposta de intervenção para o problema\\nabordado que respeite os direitos humanos. Propor uma intervenção para o\\nproblema apresentado pelo tema significa sugerir uma iniciativa que busque,\\nmesmo que minimamente, enfrentá-lo. A elaboração de uma proposta de intervenção\\nna prova de redação do Enem representa uma ocasião para que o candidato\\ndemonstre o preparo para o exercício da cidadania, para atuar na realidade em\\nconsonância com os direitos humanos.\\n\\nPontuação - Descrição\\n\\n200 pontos – Elabora muito bem proposta de\\nintervenção, detalhada, relacionada ao tema e articulada à discussão\\ndesenvolvida no texto.\\n\\n160 pontos – Elabora bem proposta de\\nintervenção relacionada ao tema e articulada à discussão desenvolvida no texto.\\n\\n120 pontos – Elabora, de forma mediana,\\nproposta de intervenção relacionada ao tema e articulada à discussão\\ndesenvolvida no texto.\\n\\n80 pontos – Elabora, de forma insuficiente,\\nproposta de intervenção relacionada ao tema, ou não articulada com a discussão\\ndesenvolvida no texto.\\n\\n40 pontos – Apresenta proposta de intervenção\\nvaga, precária ou relacionada apenas ao assunto.\\n\\n0 ponto – Não apresenta proposta de intervenção ou apresenta\\nproposta não relacionada ao tema ou ao assunto.\"]\n",
        "  },\n",
        "# Entrada dos parâmetros do relatório final.\n",
        "  {\n",
        "    \"role\": \"user\",\n",
        "    \"parts\": [\"Siga os seguintes passos:\\n\\n\\n\\n2 - Faça uma análise criteriosa e cuidadosa do texto que será inserido a\\nseguir de acordo com os critérios armazenados no contexto\\n\\n3 - Determine uma nota de 0 a 200 para cada critério de avaliação, de\\nacordo com as informações armazenadas no contexto\\n\\n4 - Dê um feedback separado pelos critérios. O feedback tem que conter as\\nseguintes informações\\n\\nNota atribuída para cada critério\\n\\nPartes boas do texto de acordo com os critérios\\n\\nRelatório detalhado das partes que diminuíram a pontuação de acordo com\\ncada critério\\n\\n5 - Caso o tema da redação não seja avaliável pelo critério 5, substituir\\no feedback deste critério pela mensagem: O tema desta redação não é avaliável\\npelo critério Respeito aos direitos humanos\\n\\n6 - Ao final do relatório deve vir a nota geral do texto (soma da\\npontuação de cada critério) e as considerações gerais.\\n\\n7 – Pule duas linhas entre cada critério no relatório\\n\\n8 - O relatório deve vir completo\"]\n",
        "  },\n",
        "])"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "oIZe5462BC16"
      },
      "source": [
        "**Input do texto e Análise dos Dados**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 5,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 55
        },
        "id": "cvnSQHQtpKdI",
        "outputId": "01a02819-4041-437c-d473-5895dd88c38d"
      },
      "outputs": [
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "O Modernismo, escola literária surgida na primeira metade do século XX, representou um período de ruptura e de transição nas diversas manifestações artísticas ao buscar as raízes da sociedade brasileira por meio do princípio nacionalista. Nesse contexto, a  linguagem composta por arcaísmos cedeu lugar aos dialetos presentes no território nacional e os quadros passaram a representar  elementos constituintes da cultura do país. Entretanto, apesar dessa conquista histórica, ainda há a falta de compreensão e de  valorização da identidade do Brasil, visto que muitas instituições educacionais carecem do ensino desse assunto, provocando um  sentimento de inferioridade, sendo urgente a solução do impasse. Em primeira análise, o antropólogo Darcy Ribeiro, em sua obra “O Povo Brasileiro”, defende que as matrizes culturais indígenas  e africanas foram apagadas e marginalizadas ao longo da formação do país. Nessa perspectiva, o processo de colonização e a herança  etnocêntrica que colocava a Europa como continente superior e, dessa forma, possibilitava a “civilização” de outros povos, causaram  a subvalorização de outras identidades, especialmente da população autóctone, que foi submetida ao abandono de certos hábitos e crenças  para atender a vontade do colonizador europeu. Isso possibilitou o desenvolvimento da sensação de subalternidade da cultura nacional por  ter sido negligenciada durante a construção da pátria, impedindo a prática de costumes brasileiros. Outrosim, a realidade educacional demonstra a ausência de discussão sobre a identidade brasileira. Sob esse viés, a ideia defendida  pelo filósofo Immanuel Kant de que o homem é aquilo que a educação faz dele é concretizada nesse cenário, visto que o fato de as escolas  não trabalharem matérias, de modo efetivo, ligadas ao multiculturalismo, contribui para a formação de cidadãos desprovidos da capacidade  de compreender e de valorizar suas nacionalidades. Portanto, para concretizar a valorização da sociedade brasileira, as escolas devem proporcionar aulas que discutam sobre esse quesito,  através da interligação das disciplinas de História e Sociologia, que abordem o assunto apontando, principalmente, para as origens da  composição da identidade nacional, com o objetivo de construir um sentimento de identificação com a matriz cultural do país. Assim, haverá  a formação de indivíduos que se sintam pertencentes aos costumes brasileiros e reconhecidos por outras nações ao enalteceram suas  histórias, como ocorreu no Movimento Modernista de 1920.\n"
          ]
        }
      ],
      "source": [
        "# Input do texto a ser analisado e corrigido.\n",
        "prompt = input()\n",
        "\n",
        "# Provoca a geração do relatório.\n",
        "response = chat.send_message(prompt)"
      ]
    },
    {
      "cell_type": "markdown",
      "metadata": {
        "id": "98mx8CsQv5eq"
      },
      "source": [
        "**Configuração do Relatório e Geração**"
      ]
    },
    {
      "cell_type": "code",
      "execution_count": 6,
      "metadata": {
        "colab": {
          "base_uri": "https://localhost:8080/",
          "height": 1000
        },
        "id": "XpCRf0gywYZW",
        "outputId": "b21fa347-40a7-4702-c053-b631325e971d"
      },
      "outputs": [
        {
          "data": {
            "text/markdown": [
              "> ATENÇÃO! Esta aplicação não substitui a necessidade de avaliações feitas por professores.\n",
              "> * ## Análise da Redação\n",
              "> \n",
              "> **Critério 01 - Domínio da escrita formal da língua portuguesa**\n",
              "> \n",
              "> **Nota: 160**\n",
              "> \n",
              "> **Pontos Positivos:** O texto demonstra um bom domínio da norma culta da língua portuguesa. A estrutura gramatical está sólida, com frases bem construídas e uso correto da pontuação na maior parte do texto. \n",
              "> \n",
              "> **Relatório Detalhado:** \n",
              "> * Há algumas repetições de palavras como `identidade` e `cultura`, o que poderia ser evitado com o uso de sinônimos e pronomes para um vocabulário mais rico e variado. \n",
              "> * A expressão `sendo urgente a solução do impasse` soa um pouco coloquial e poderia ser reformulada de forma mais sofisticada. \n",
              "> \n",
              "> ---\n",
              "> \n",
              "> **Critério 02 - Compreender o tema e não fugir do que é proposto**\n",
              "> \n",
              "> **Nota: 200**\n",
              "> \n",
              "> **Pontos Positivos:**  A redação aborda o tema da valorização da identidade brasileira de forma completa e consistente. O texto apresenta uma argumentação coesa, explorando o legado do Modernismo e os desafios contemporâneos relacionados à compreensão e valorização da cultura nacional.\n",
              "> \n",
              "> **Relatório Detalhado:** Nenhum problema encontrado.\n",
              "> \n",
              "> ---\n",
              "> \n",
              "> **Critério 03 - Selecionar, relacionar, organizar e interpretar informações, fatos, opiniões e argumentos em defesa de um ponto de vista**\n",
              "> \n",
              "> **Nota: 160**\n",
              "> \n",
              "> **Pontos Positivos:** O texto apresenta informações relevantes, como a referência a Darcy Ribeiro e Immanuel Kant, para sustentar a argumentação. A organização das ideias é clara, com um parágrafo introdutório, desenvolvimento em dois parágrafos argumentativos e conclusão.\n",
              "> \n",
              "> **Relatório Detalhado:** A argumentação sobre a falta de compreensão e valorização da identidade brasileira poderia ser enriquecida com exemplos mais concretos e específicos. A menção a instituições educacionais que carecem do ensino sobre a identidade brasileira, por exemplo,  poderia ser complementada com dados, pesquisas ou exemplos de como essa lacuna se manifesta na prática.\n",
              "> \n",
              "> ---\n",
              "> \n",
              "> **Critério 04 – Conhecimento dos mecanismos linguísticos necessários para a construção da argumentação**\n",
              "> \n",
              "> **Nota: 160**\n",
              "> \n",
              "> **Pontos Positivos:** O texto demonstra bom uso de conectivos e elementos coesivos, como `Nesse contexto`, `Entretanto`, `Em primeira análise`, `Outrosim` e `Portanto`.  A progressão temática é fluida, com as ideias se conectando de forma lógica.\n",
              "> \n",
              "> **Relatório Detalhado:** Há alguns momentos em que a coesão poderia ser aprimorada. Por exemplo, a transição entre o primeiro e o segundo parágrafo poderia ser mais suave, com o uso de um conectivo que estabeleça uma relação mais explícita entre a conquista histórica do Modernismo e os desafios contemporâneos. \n",
              "> \n",
              "> ---\n",
              "> \n",
              "> **Critério 05 - Respeito aos direitos humanos**\n",
              "> \n",
              "> **Nota: O tema desta redação não é avaliável pelo critério Respeito aos direitos humanos**\n",
              "> \n",
              "> ---\n",
              "> \n",
              "> ## Nota Geral: 880\n",
              "> \n",
              "> ## Considerações Gerais\n",
              "> \n",
              "> A redação apresenta boa qualidade textual e argumentativa, demonstrando bom domínio da norma culta e capacidade de desenvolver ideias de forma organizada e coerente. A argumentação sobre a valorização da identidade brasileira é pertinente e bem fundamentada, com a utilização de autores relevantes para a discussão. Para alcançar uma nota ainda melhor, seria interessante enriquecer a argumentação com exemplos mais específicos e aprimorar a coesão em alguns pontos do texto. No geral, a redação demonstra um bom desempenho em relação aos critérios avaliados. \n",
              ">  \n",
              "> \n",
              "> Bons estudos e continue praticando! :) \n",
              "> * Os resultados são gerados por IA e podem sofrer pequenas alterações se gerados mais de uma vez"
            ],
            "text/plain": [
              "<IPython.core.display.Markdown object>"
            ]
          },
          "metadata": {},
          "output_type": "display_data"
        },
        {
          "name": "stdout",
          "output_type": "stream",
          "text": [
            "\n"
          ]
        }
      ],
      "source": [
        "# Configuração da função Display e Markdown.\n",
        "import textwrap\n",
        "from IPython.display import display\n",
        "from IPython.display import Markdown\n",
        "\n",
        "def to_markdown(text):\n",
        "  text = text.replace('\"', '`')\n",
        "  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))\n",
        "\n",
        "# Definição do que será gerado no relatório final de acordo com a última resposta armazenada no contexto.\n",
        "last_message = next((message for message in reversed(chat.history) if message.role == 'model'), None)\n",
        "if last_message:\n",
        "  display(to_markdown(f'ATENÇÃO! Esta aplicação não substitui a necessidade de avaliações feitas por professores.\\n* {last_message.parts[0].text} \\n\\nBons estudos e continue praticando! :) \\n* Os resultados são gerados por IA e podem sofrer pequenas alterações se gerados mais de uma vez'))\n",
        "\n",
        "# Geração do relatório final.\n",
        "  print('')"
      ]
    }
  ],
  "metadata": {
    "colab": {
      "authorship_tag": "ABX9TyNCLSHdi7AExkdHLL23MtMC",
      "include_colab_link": true,
      "provenance": []
    },
    "kernelspec": {
      "display_name": "Python 3",
      "name": "python3"
    },
    "language_info": {
      "name": "python"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 0
}
