#!/bin/bash


if ! command -v docker &> /dev/null; then
    echo "Docker не найден, устанавливаем..."
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
fi


if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose не найден, устанавливаем..."
    curl -L "https://github.com/docker/compose/releases/download/v2.27.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi


if [ ! -d "X-ui-cleaner" ]; then
    git clone https://github.com/polozhnyack/X-ui-cleaner.git
fi

cd X-ui-cleaner || exit


sudo docker build -t xui-cleaner .


sudo docker run -d \
  --name xui-cleaner \
  -p 8000:8000 \
  -v /etc/x-ui:/etc/x-ui \
  --restart=unless-stopped \
  xui-cleaner