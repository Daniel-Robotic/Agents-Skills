# Навыки и плагины для AI-агентов

У каждого плагина своя папка и собственный `README.md` с настройками, которые нужны именно ему.

## Структура

```text
Agents-Skills/
├── Skills/
│   ├── HermesAgent/
│   └── ChatGPT/
├── Plugins/
│   ├── HermesAgent/
│   │   └── <имя-плагина>/
│   └── ChatGPT/
│       └── <имя-плагина>/
├── Prompts/
└── Guides/
```

`Skills/` содержит навыки, `Plugins/` — устанавливаемые плагины, `Prompts/` — текстовые промты, а `Guides/` — заметки о разработке. Плагины для разных платформ устанавливаются по-разному; инструкции ниже относятся к любому плагину в соответствующей папке.

## Скачать репозиторий

```bash
git clone https://github.com/Daniel-Robotic/Agents-Skills.git
cd Agents-Skills
```

Чтобы получить новые версии файлов позже, выполните `git pull` в папке репозитория.

## Установить плагин в Hermes Agent

Откройте `Plugins/HermesAgent/` и выберите папку нужного плагина. Скопируйте **папку целиком** в `~/.hermes/plugins/`, сохранив её имя. Например, для папки с именем `my-plugin` итоговый путь должен быть `~/.hermes/plugins/my-plugin/plugin.yaml`.

**Windows PowerShell** — замените `my-plugin` на имя нужной папки:

```powershell
$pluginName = 'my-plugin'
New-Item -ItemType Directory -Force "$HOME\.hermes\plugins\$pluginName" | Out-Null
Copy-Item -Recurse -Force "Plugins\HermesAgent\$pluginName\*" "$HOME\.hermes\plugins\$pluginName"
hermes plugins enable $pluginName
```

**Linux и macOS** — замените `my-plugin` на имя нужной папки:

```bash
plugin_name='my-plugin'
mkdir -p "$HOME/.hermes/plugins/$plugin_name"
cp -R "Plugins/HermesAgent/$plugin_name/." "$HOME/.hermes/plugins/$plugin_name/"
hermes plugins enable "$plugin_name"
```

После включения настройте плагин по его собственному `README.md` и начните новую сессию Hermes. Если у плагина есть ключи доступа, храните их в секретах или переменных окружения, как указано в его инструкции.

Когда обновите репозиторий, повторите копирование файлов нужного плагина. Поскольку плагины лежат во вложенных папках общего репозитория, команда `hermes plugins install Daniel-Robotic/Agents-Skills` не устанавливает их по отдельности.

## Установить плагин в Codex Desktop

Плагины Codex из этого репозитория перечислены в `.agents/plugins/marketplace.json`. Добавьте репозиторий как источник плагинов:

```bash
codex plugin marketplace add Daniel-Robotic/Agents-Skills
```

Перезапустите Codex Desktop, откройте каталог **Plugins** и выберите источник **Agents Skills**. Найдите нужный плагин и установите его. Затем откройте `Plugins/ChatGPT/<имя-плагина>/README.md`: там указаны необходимые программы, настройки и способ первого запуска.

Для плагинов из другого GitHub-репозитория используется та же команда с его адресом: `codex plugin marketplace add владелец/репозиторий`. В репозитории должен быть каталог плагинов, который понимает Codex.

Чтобы получить обновления источника, выполните `codex plugin marketplace upgrade`, затем обновите установленный плагин в Codex, если приложение предложит это сделать.

## Где искать настройки и помощь

Начните с `README.md` внутри папки выбранного плагина. Там описаны его зависимости, адреса сервисов, ключи доступа и примеры использования. Общие правила создания плагинов находятся в `Guides/`; краткий список доступных плагинов — в [Plugins/README.md](Plugins/README.md).
