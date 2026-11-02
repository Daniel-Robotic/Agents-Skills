# Плагины

В этом каталоге лежат версии плагинов для Hermes Agent и Codex. Устанавливайте пакет из папки своей платформы; инструкции и настройки конкретного плагина находятся в его `README.md`.

| Плагин | Hermes Agent | Codex |
| --- | --- | --- |
| Trilium ETAPI — работа с заметками через REST | [Установка](HermesAgent/trilium-etapi/README.md) | [Установка](ChatGPT/trilium-etapi/README.md) |
| Lesson Studio — планы и подробные занятия по AI и ML | [Установка](HermesAgent/lesson-studio/README.md) | [Установка](ChatGPT/lesson-studio/README.md) |

Для Hermes пакет копируется в `~/.hermes/plugins/` и включается командой `hermes plugins enable <имя>`. Для Codex добавьте репозиторий как источник командой `codex plugin marketplace add Daniel-Robotic/Agents-Skills`, затем установите нужный плагин из каталога **Plugins**. Дополнительные требования зависят от конкретного пакета и указаны по ссылкам выше.
