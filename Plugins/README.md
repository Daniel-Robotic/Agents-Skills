# Плагины Trilium ETAPI

В репозитории есть два подключения к Trilium: нативный плагин для Hermes Agent и локальный плагин для Codex Desktop. Оба работают с официальным REST ETAPI. Для настройки нужен адрес вашего Trilium и ETAPI-ключ из **Trilium → Options → ETAPI**.

| Платформа | Папка плагина | Где указать адрес и ключ |
| --- | --- | --- |
| Hermes Agent | [`HermesAgent/trilium-etapi/`](HermesAgent/trilium-etapi/) | В настройках плагина Hermes |
| Codex Desktop | [`ChatGPT/trilium-etapi/`](ChatGPT/trilium-etapi/) | В переменных окружения компьютера |

## Hermes Agent

1. Скопируйте папку `Plugins/HermesAgent/trilium-etapi` в `~/.hermes/plugins/trilium-etapi`.
2. Выполните `hermes plugins enable trilium-etapi`.
3. В настройках плагина укажите адрес Trilium без `/etapi` и ETAPI-ключ.
4. Начните новую сессию Hermes.

Команды копирования для Windows, Linux и macOS, а также настройка без Desktop приведены в [инструкции Hermes](HermesAgent/trilium-etapi/README.md).

## Codex Desktop

1. Добавьте репозиторий как источник плагинов: `codex plugin marketplace add Daniel-Robotic/Agents-Skills`.
2. Перезапустите Codex Desktop и установите **trilium-etapi** из источника **Agents Skills** в каталоге Plugins.
3. На компьютере задайте `TRILIUM_BASE_URL` (адрес без `/etapi`) и `TRILIUM_ETAPI_TOKEN`, затем перезапустите Codex Desktop.
4. Начните новый чат и попросите Codex использовать Trilium.

Подробности настройки переменных окружения и примеры запросов находятся в [инструкции Codex](ChatGPT/trilium-etapi/README.md). Для этого варианта требуется локальный запуск Python 3.

ETAPI-ключ не нужно записывать в файлы репозитория или отправлять в чат.
