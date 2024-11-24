FROM jenkins/jenkins:lts

# Устанавливаем дополнительные плагины Jenkins (при необходимости)
RUN jenkins-plugin-cli --plugins "pipeline-multibranch-step git"

# Открытые порты для Jenkins
EXPOSE 8080 50000

# Устанавливаем рабочую директорию
WORKDIR /var/jenkins_home

# Команда для запуска Jenkins
CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]
