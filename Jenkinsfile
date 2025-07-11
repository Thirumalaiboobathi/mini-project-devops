pipeline {
    agent any

    environment {
        IMAGE_NAME = "gatewayservice"
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
                    sh "docker build -t ${IMAGE_NAME}:latest ./getwayservice"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f gateway.yml'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 10'
                sh 'curl -f http://localhost:31000/ || echo "Gateway health check failed"' // 31000 is example NodePort
            }
        }
    }
}
