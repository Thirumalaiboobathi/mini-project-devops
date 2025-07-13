pipeline {
    agent any

    environment {
        IMAGE_NAME = "alertservice"
    }

    triggers {
        pollSCM('H/5 * * * *') // Poll Git every 5 minutes
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'eval $(minikube docker-env)'
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "Starting deployment to Kubernetes..."
                    try {
                        sh 'ls -l alert.yaml'
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
                    sh 'sleep 10'
                    try {
                        sh 'curl -f http://localhost:5000/health'
                        echo "✅ Health check passed."
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
            echo '✅ Build succeeded!'
        }
        failure {
            echo '❌ Build failed!'
        }
    }
}
