FROM jenkins/jenkins:lts

# Открытые порты для Jenkins
EXPOSE 8080 50000

# Устанавливаем рабочую директорию
WORKDIR /var/jenkins_home

# Команда для запуска Jenkins
CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war"]
