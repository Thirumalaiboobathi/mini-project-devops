pipeline {
    agent any

    environment {
        IMAGE_NAME = "weatherservice"
    }

    stages {
        stage('Clone Repo') {
            steps {
                git url: 'https://github.com/Thirumalaiboobathi/mini-project-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'eval $(minikube docker-env)'
                    sh "docker build -t ${IMAGE_NAME}:latest ./weatherservice"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f weather.yml'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 10'
                sh 'curl -f http://weatherservice:5000/health || echo "Weather service health check failed"'
            }
        }
    }
}
