# Сервис XUI Cleaner

Сервис для удаления забаганных пользователей в панели **3x-ui**.
Правит базу данных **локально на хосте** через SQLite.

### Запуск через Docker

### 1. Собрать Docker-образ:

```bash
docker build -t xui-cleaner .
```
### 2. Запустить контейнер:
```bash
docker run -d \
  --name xui-cleaner \
  --env-file .env \
  -p 8000:8000 \
  -v /etc/x-ui:/etc/x-ui \
  --restart=unless-stopped \
  xui-cleaner
```

* `--env-file .env` — содержит переменные окружения:

  ```env
  DB_PATH=/etc/x-ui/x-ui.db
  API_KEY=super-secret-key
  ```
* `-v /etc/x-ui:/etc/x-ui` — монтируем папку с базой внутрь контейнера.
* `--restart=unless-stopped` — контейнер автоматически перезапускается после сбоя или перезагрузки хоста.

### Эндпоинт для удаления клиента

```http
DELETE /deleteclient
```

**Заголовки:**

* `Content-Type: application/json`
* `X-API-Key: <ваш API_KEY из .env>`

**Тело запроса:**

```json
{
  "identifier": "6641696567"   // email или UUID
}
```

**Пример с `curl`:**

```bash
curl -X DELETE http://127.0.0.1:8000/delete-client \
  -H "Content-Type: application/json" \
  -H "X-API-Key: super-secret-key" \
  -d '{"identifier": "6641696567"}'
```

**Ответ:**

* `200 OK` — если клиент удалён успешно.
* `404 Not Found` — если клиент не найден.
* `401 Unauthorized` — если неверный API ключ.

### Просмотр логов

```bash
docker logs -f xui-cleaner
```

* `-f` — режим онлайн, новые строки отображаются автоматически.

### Обновление сервиса

1. Остановить старый контейнер:

```bash
docker stop xui-cleaner
docker rm xui-cleaner
```

2. Собрать новый образ:

```bash
docker build -t xui-cleaner .
```

3. Запустить заново (как выше).
