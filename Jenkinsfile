pipeline {
    agent any

    environment {
        IMAGE_NAME = "gatewayservice"
    }

    stages {
        

        stage('Build Docker Image') {
            steps {
                script {
                    sh 'eval $(minikube docker-env)'  // Use Minikube Docker daemon
                    sh "docker build -t ${IMAGE_NAME}:latest ./getwayservice"
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "🛠️ Applying Kubernetes configuration..."
                    sh 'kubectl apply -f gateway.yml'
                }
            }
        }

        stage('Health Check') {
            steps {
                script {
                    sh 'sleep 10' // Give time for pod to become ready
                    def serviceUrl = sh(script: "minikube service gatewayservice --url", returnStdout: true).trim()
                    echo "🔎 Gateway service URL: ${serviceUrl}"

                    try {
                        sh "curl -f ${serviceUrl}/health"
                        echo "✅ Health check passed."
                    } catch (err) {
                        echo "❌ Gateway health check failed!"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Gateway pipeline completed successfully!'
        }
        failure {
            echo '❌ Gateway pipeline failed!'
        }
    }
}
