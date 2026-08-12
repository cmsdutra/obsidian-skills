# Obsidian Skills

Skills para agentes compatíveis com o padrão [Agent Skills](https://agentskills.io/specification), focadas em criação, edição, manutenção e automação de vaults do Obsidian.

Este repositório é um fork de [`kepano/obsidian-skills`](https://github.com/kepano/obsidian-skills.git), com otimização do workflow das skills de bases, canvas, fravored markdown e cli, e ampliado com workflows para snippets, temas, plugins e saneamento de vault.

## Composição

```text
.
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── .codex-plugin/plugin.json
├── LICENSE
├── README.md
└── skills/
    ├── defuddle/
    ├── obsidian-bases/
    ├── obsidian-canvas/
    ├── obsidian-cli/
    ├── obsidian-markdown/
    ├── obsidian-plugin-creator/
    ├── obsidian-snippet-creator/
    ├── obsidian-theme-creator/
    └── obsidian-vault-sanitizer/
```

## Instalação

### Codex

Opção 1: usar como plugin local.

1. Clone este repositório:

```sh
git clone https://github.com/cmsdutra/obsidian-skills.git
```

2. Instale ou aponte o Codex para este repositório como plugin local. O manifesto está em:

```text
.codex-plugin/plugin.json
```

O manifesto expõe todas as skills por meio de:

```json
"skills": "./skills/"
```

Opção 2: copiar as skills diretamente.

```sh
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

Reinicie o Codex depois de instalar ou atualizar as skills.

### npx skills

Via SSH:

```sh
npx skills add git@github.com:cmsdutra/obsidian-skills.git
```

Via HTTPS:

```sh
npx skills add https://github.com/cmsdutra/obsidian-skills
```

### Claude Code

Este repositório também é um marketplace de plugins no formato usado pelo Claude Code, através dos manifestos em:

```text
.claude-plugin/plugin.json
.claude-plugin/marketplace.json
```

O manifesto do plugin expõe todas as skills por meio de:

```json
"skills": "./skills/"
```

Instale via marketplace apontando para o repositório remoto:

```text
/plugin marketplace add cmsdutra/obsidian-skills
/plugin install obsidian-skills@obsidian-skills
```

Ou clone localmente e aponte para o caminho:

```sh
git clone https://github.com/cmsdutra/obsidian-skills.git
```

```text
/plugin marketplace add ./obsidian-skills
/plugin install obsidian-skills@obsidian-skills
```

Alternativa manual: copie o conteúdo deste repositório para a pasta de skills usada pelo Claude Code no seu projeto ou vault. Consulte a documentação oficial do Claude Skills para o local exato esperado pela sua instalação.

### Cowork

No [Cowork](https://support.claude.com/en/articles/13345190-get-started-with-claude-cowork), plugins são instalados pela interface, não por comandos:

1. Abra a aba **Cowork** e depois **Customize**, na barra lateral.
2. Vá na aba **Plugins**.
3. No bloco "Personal plugins", clique em **+** → **Add marketplace**.
4. Escolha adicionar por repositório GitHub / URL git e informe `cmsdutra/obsidian-skills` (ou a URL `https://github.com/cmsdutra/obsidian-skills`).
5. Com o marketplace adicionado, clique em **Browse plugins** e instale o plugin `obsidian-skills`.

O fluxo de "Add marketplace" via repositório GitHub/URL git usa o mesmo `.claude-plugin/marketplace.json` deste repositório, então nenhum arquivo adicional é necessário. Veja mais detalhes em [Use plugins in Cowork](https://support.claude.com/en/articles/13837440-use-plugins-in-cowork).

### OpenCode

Clone o repositório completo dentro do diretório de skills do OpenCode:

```sh
git clone https://github.com/cmsdutra/obsidian-skills.git ~/.opencode/skills/obsidian-skills
```

Não copie apenas a pasta interna `skills/`. A estrutura esperada fica assim:

```text
~/.opencode/skills/obsidian-skills/skills/<skill-name>/SKILL.md
```

Reinicie o OpenCode depois da instalação.

### Marketplace original

O upstream original pode ser instalado pelo marketplace do pacote de Kepano:

```text
/plugin marketplace add kepano/obsidian-skills
/plugin install obsidian@obsidian-skills
```

⚠️ **Esses comandos se referem ao pacote original, não a este fork.**

## Skills incluídas

| Skill | Resumo |
|-------|--------|
| [defuddle](skills/defuddle) | Extrai Markdown limpo de páginas web com o Defuddle CLI, removendo navegação, anúncios e ruído para reduzir tokens ao analisar URLs. |
| [obsidian-bases](skills/obsidian-bases) | Cria, edita e valida Obsidian Bases em arquivos `.base` ou blocos Markdown `base`, com views, filtros, fórmulas e summaries. |
| [obsidian-canvas](skills/obsidian-canvas) | Cria e edita arquivos `.canvas` no formato JSON Canvas usado pelo Obsidian, incluindo nodes, edges, grupos, cards de texto, links e arquivos. |
| [obsidian-cli](skills/obsidian-cli) | Usa a Obsidian CLI para ler, buscar, criar, mover e gerenciar notas, tarefas, propriedades, backlinks e operações link-safe em vaults. |
| [obsidian-markdown](skills/obsidian-markdown) | Cria e edita Obsidian Flavored Markdown com wikilinks, embeds, callouts, frontmatter, tags, comentários, blocos e propriedades. |
| [obsidian-plugin-creator](skills/obsidian-plugin-creator) | Ajuda a criar, modificar, depurar e validar plugins locais ou comunitários do Obsidian, incluindo `manifest.json`, TypeScript, build e testes. |
| [obsidian-snippet-creator](skills/obsidian-snippet-creator) | Cria e salva snippets CSS em `.obsidian/snippets`, usando variáveis e padrões de estilo do Obsidian. |
| [obsidian-theme-creator](skills/obsidian-theme-creator) | Cria, refatora, depura e valida temas completos do Obsidian com `theme.css`, `manifest.json`, modos claro/escuro e critérios de publicação. |
| [obsidian-vault-sanitizer](skills/obsidian-vault-sanitizer) | Audita e corrige problemas de saneamento do vault, como links quebrados, anexos órfãos, nomes genéricos tipo `Sem título 1.md`, duplicatas e frontmatter inválido. |

## Como usar

Depois de instalada, invoque a skill explicitamente quando quiser forçar um workflow:

```text
Use $obsidian-vault-sanitizer para auditar este vault e propor correções.
Use $obsidian-markdown para criar uma nota com callouts e propriedades.
Use $obsidian-plugin-creator para criar um plugin local do Obsidian.
```

Agentes que suportam invocação implícita também podem carregar a skill automaticamente quando o pedido mencionar arquivos, tarefas ou conceitos cobertos pela descrição da skill.

## Dependências úteis

Algumas skills funcionam melhor com ferramentas externas instaladas:

| Ferramenta | Usada por | Observação |
|------------|-----------|------------|
| `obsidian` CLI | `obsidian-cli`, operações link-safe e validações em runtime | Necessária quando o agente precisa consultar o índice vivo do Obsidian ou mover/renomear preservando links. |
| `defuddle` CLI | `defuddle` | Instale com `npm install -g defuddle` se ainda não estiver disponível. |
| Python 3 | scripts de validação e saneamento | Usado por scripts como `obsidian-vault-sanitizer/scripts/audit_vault.py`. |
| Node.js/npm | criação de plugins, temas e snippets | Necessário para builds, linters e ferramentas do ecossistema Obsidian quando presentes. |

## Manutenção

- Cada skill deve manter seu próprio `SKILL.md` enxuto e colocar detalhes adicionais em `references/`.
- Scripts reutilizáveis devem ficar em `scripts/` e ser validados após alterações.
- Mudanças em instruções, scripts, referências ou política de validação devem ser registradas no `docs/changelog.md` da respectiva skill quando esse arquivo existir.
- Evite editar diretamente vaults Obsidian quando a operação afetar links, backlinks, aliases, anexos ou headings; prefira workflows link-safe via Obsidian CLI quando disponíveis.

## Licença

Este projeto segue a licença em [LICENSE](LICENSE).
