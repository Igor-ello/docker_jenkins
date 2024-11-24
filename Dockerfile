FROM jenkins/jenkins:lts

# Указываем переменную окружения PORT
ENV PORT=8080

# Экспортируем порты
EXPOSE 8080 50000

# Команда запуска Jenkins
CMD ["java", "-jar", "/usr/share/jenkins/jenkins.war", "--httpPort=${PORT}"]
