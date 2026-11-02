# Trilium ETAPI для Hermes Agent

Плагин подключает Hermes Agent к вашему Trilium через официальный REST API. Адрес сервера задаётся в настройках плагина, ETAPI-ключ хранится как секрет Hermes. Отдельный сервер или посредник не требуется.

## Что понадобится

- Установленный Hermes Agent и Python из его окружения.
- Адрес Trilium: например, `https://notes.example.com`.
- ETAPI-ключ, созданный в **Trilium → Options → ETAPI**.

Для удалённого сервера используйте HTTPS. В адресе указывайте корень Trilium, без `/etapi`.

## Установка

Склонируйте репозиторий и перейдите в него:

```bash
git clone https://github.com/Daniel-Robotic/Agents-Skills.git
cd Agents-Skills
```

Скопируйте **всю папку** плагина в каталог пользовательских плагинов Hermes.

**Windows PowerShell:**

```powershell
New-Item -ItemType Directory -Force "$HOME\.hermes\plugins" | Out-Null
Copy-Item -Recurse -Force "Plugins\HermesAgent\trilium-etapi" "$HOME\.hermes\plugins\trilium-etapi"
```

**Linux и macOS:**

```bash
mkdir -p ~/.hermes/plugins
cp -R Plugins/HermesAgent/trilium-etapi ~/.hermes/plugins/trilium-etapi
```

Включите плагин:

```bash
hermes plugins enable trilium-etapi
```

После установки папка `~/.hermes/plugins/trilium-etapi/` должна содержать `plugin.yaml`, `__init__.py`, `etapi_ops.json` и `SKILL.md`.

## Настройка

В Hermes Desktop откройте **Settings → Plugins → trilium-etapi** и заполните два поля:

| Поле | Значение |
| --- | --- |
| **Trilium base URL** | Адрес сервера, например `https://notes.example.com` |
| **ETAPI token** | Ключ из **Trilium → Options → ETAPI** |

Если используете Hermes без Desktop, задайте адрес в `~/.hermes/config.yaml`, а ключ передайте через переменную окружения `TRILIUM_ETAPI_TOKEN` перед запуском Hermes:

```yaml
plugins:
  entries:
    trilium-etapi:
      settings:
        base_url: https://notes.example.com
```

Ключ в `config.yaml` записывать не нужно. После настройки начните новую сессию Hermes.

## Использование

Пишите обычными словами, например: «Найди заметки о проекте и кратко перескажи их» или «Создай заметку “План” внутри заметки “Проект”». Плагин предоставляет Hermes инструмент `trilium_etapi` для операций официального ETAPI: поиск и содержимое заметок, ветки дерева, вложения, атрибуты, история, календарь, импорт и экспорт, резервные копии.

Если Hermes сообщает об отсутствии настроек, проверьте адрес и наличие ключа в секретах или окружении. При ошибке соединения проверьте, что адрес Trilium доступен с компьютера, где запущен Hermes.

[Документация Hermes по плагинам](https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins) · [Документация Trilium ETAPI](https://docs.triliumnotes.org/user-guide/advanced-usage/etapi)
