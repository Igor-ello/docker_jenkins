import os
import subprocess
import git
import requests

# Константы
REPO_NAME = "docker_jenkins"
GITHUB_USERNAME = "your_github_username"
GITHUB_TOKEN = "your_github_token"  # Создайте personal access token в GitHub
RENDER_API_TOKEN = "your_render_api_token"  # Получите API-токен Render
RENDER_SERVICE_NAME = "jenkins_service"

# Шаг 1: Подготовка проекта
def prepare_project():
    if not os.path.exists(REPO_NAME):
        os.makedirs(REPO_NAME)
    docker_compose_content = """
version: '3.8'
services:
  jenkins:
    image: jenkins/jenkins:lts
    container_name: docker_jenkins
    ports:
      - "8080:8080"
      - "50000:50000"
    volumes:
      - jenkins_home:/var/jenkins_home
volumes:
  jenkins_home:
"""
    with open(f"{REPO_NAME}/docker-compose.yml", "w") as f:
        f.write(docker_compose_content)
    print(f"Проект {REPO_NAME} подготовлен.")

# Шаг 2: Загрузка в GitHub
def upload_to_github():
    repo_path = os.path.abspath(REPO_NAME)
    if not os.path.exists(os.path.join(repo_path, ".git")):
        repo = git.Repo.init(repo_path)
        origin = repo.create_remote("origin", f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git")
        print("Репозиторий создан.")
    else:
        repo = git.Repo(repo_path)

    repo.git.add(all=True)
    repo.index.commit("Initial commit")
    origin = repo.remotes.origin
    origin.push(refspec="master:master")
    print("Код отправлен в GitHub.")

# Шаг 3: Деплой в Render
def deploy_to_render():
    url = "https://api.render.com/v1/services"
    headers = {
        "Authorization": f"Bearer {RENDER_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "serviceName": RENDER_SERVICE_NAME,
        "env": "docker",
        "repo": f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}",
        "branch": "master",
        "rootDirectory": "/",
        "dockerfilePath": "Dockerfile",
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print("Jenkins успешно развернут в Render!")
    else:
        print(f"Ошибка: {response.text}")

# Основной процесс
if __name__ == "__main__":
    prepare_project()
    upload_to_github()
    deploy_to_render()
