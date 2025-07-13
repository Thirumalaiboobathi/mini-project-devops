pipeline {
    agent any

    environment {
        IMAGE_NAME = "weatherservice"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Thirumalaiboobathi/mini-project-devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'eval $(minikube docker-env) && docker build -t ${IMAGE_NAME}:latest ./weatherservice'
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
                script {
                    sh 'sleep 10'
                    def healthCheck = sh(script: 'curl -sf http://weatherservice:5001/health', returnStatus: true)
                    if (healthCheck != 0) {
                        error("❌ Weather service health check failed.")
                    } else {
                        echo "✅ Weather service is healthy."
                    }
                }
            }
        }
    }

    post {
        success {
            echo "✅ Pipeline completed successfully!"
        }
        failure {
            echo "❌ Pipeline failed. Please check the logs."
        }
    }
}
