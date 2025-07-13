pipeline {
    agent any

    environment {
        IMAGE_NAME = "alertservice"
    }

    triggers {
        pollSCM('H/5 * * * *') // Poll Git every 5 minutes
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5')) // Keep last 5 builds
    }

    stages {
        stage('Ensure Minikube Running') {
            steps {
                script {
                    sh 'minikube status || minikube start --driver=docker'
                }
            }
        }

        stage('Set Minikube Docker Env') {
            steps {
                script {
                    sh 'eval $(minikube docker-env)'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "📦 Building Docker image: ${IMAGE_NAME}"
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "🚀 Starting deployment to Kubernetes..."
                    try {
                        sh 'kubectl apply -f alert.yaml'
                    } catch (err) {
                        echo "❌ Deployment failed or file not found: ${err}"
                    }
                    echo "✅ Deployment stage completed (with or without errors)."
                }
            }
        }

        stage('Generate Timestamp File') {
            steps {
                script {
                    def timestamp = new Date().format("yyyy-MM-dd_HH-mm-ss")
                    writeFile file: "timestamp.txt", text: "Build timestamp: ${timestamp}\n"
                    echo "🕒 Timestamp file created: ${timestamp}"
                }
            }
        }

        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'timestamp.txt'
            }
        }

        stage('Health Check') {
            steps {
                script {
                    echo "⏳ Waiting for service to be ready..."
                    sh 'sleep 10'

                    def serviceUrl = sh(script: 'minikube service alertservice --url', returnStdout: true).trim()
                    echo "🔎 Checking service at: ${serviceUrl}/health"

                    try {
                        def response = sh(script: "curl -s -f ${serviceUrl}/health", returnStdout: true).trim()
                        echo "✅ Health check passed: ${response}"
                    } catch (e) {
                        echo "❌ Health check failed!"
                        currentBuild.result = 'UNSTABLE'
                    }
                }
            }
        }
    }

    post {
        success {
            echo '🎉 Build succeeded!'
        }
        failure {
            echo '💥 Build failed!'
        }
        always {
            echo '🧹 Cleaning up if needed (e.g., killing port-forwards)...'
            // sh 'pkill -f "kubectl port-forward" || true' // Uncomment if using port-forward
        }
    }
}
