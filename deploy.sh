#!/bin/bash

if [ "$EUID" -ne 0 ]; then
    echo "Рекомендуется запускать скрипт с sudo или от root"
fi

if ! command -v docker &> /dev/null; then
    echo "Docker не найден, устанавливаем..."
    curl -fsSL https://get.docker.com | sh
    sudo systemctl enable docker
    sudo systemctl start docker
fi

if ! groups $USER | grep -q "\bdocker\b"; then
    echo "Добавляем пользователя $USER в группу docker..."
    sudo usermod -aG docker $USER
    echo "Выйдите и войдите заново, чтобы изменения вступили в силу"
fi

if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose не найден, устанавливаем..."
    sudo curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi


if [ ! -d "X-ui-cleaner" ]; then
    git clone https://github.com/polozhnyack/X-ui-cleaner.git
fi

cd X-ui-cleaner || exit


docker build -t xui-cleaner .


docker run -d \
  --name xui-cleaner \
  -p 8000:8000 \
  -v /etc/x-ui:/etc/x-ui \
  --restart=unless-stopped \
  xui-cleaner

echo "Done!"
