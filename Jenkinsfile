pipeline {
    agent any

    environment {
        IMAGE_NAME = "alertservice"
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
                    sh "docker build -t ${IMAGE_NAME}:latest ./alertservice"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh 'kubectl apply -f ./alertservice/alert.yml'
            }
        }

        stage('Health Check') {
            steps {
                sh 'sleep 10'
                sh 'curl -f http://alertservice:6000/health || echo "Alert service health check failed"'
            }
        }
    }
}
