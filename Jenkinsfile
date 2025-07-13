pipeline {
    agent any

    environment {
        IMAGE_NAME = "gatewayservice"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '5')) // keep last 5 builds
    }

    stages {
        stage('Checkout') {
            steps {
                // Get code from repository
                checkout scm
                
            }
        }

        stage('Start Minikube') {
            steps {
                script {
                    echo "🚀 Starting Minikube..."
                    sh '''
                        minikube status || minikube start --driver=docker --force
                    '''
                }
            }
        }

        stage('Set Minikube Docker Env') {
            steps {
                script {
                    echo "🔧 Setting Docker env from Minikube..."
                    def envOutput = sh(script: "minikube docker-env --shell bash", returnStdout: true).trim()
                    def envLines = envOutput.split("\n")
                    def dockerEnvVars = envLines.findAll { it.startsWith("export") }
                                                .collect { it.replace("export ", "").split("=", 2) }
                                                .collectEntries { [(it[0]): it[1].replaceAll('"', '')] }
                    withEnv(dockerEnvVars.collect { "${it.key}=${it.value}" }) {
                        sh "docker info"
                        sh "docker version"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "📦 Building Docker image: ${IMAGE_NAME}"
                    def envOutput = sh(script: "minikube docker-env --shell bash", returnStdout: true).trim()
                    def envLines = envOutput.split("\n")
                    def dockerEnvVars = envLines.findAll { it.startsWith("export") }
                                                .collect { it.replace("export ", "").split("=", 2) }
                                                .collectEntries { [(it[0]): it[1].replaceAll('"', '')] }

                    withEnv(dockerEnvVars.collect { "${it.key}=${it.value}" }) {
                        sh "docker build -t ${IMAGE_NAME}:latest ./getwayservice"
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    echo "🛠️ Applying Kubernetes configuration..."
                    try {
                        sh 'kubectl apply -f gateway.yml'
                        echo "✅ Deployment successful"
                    } catch (err) {
                        echo "❌ Deployment failed: ${err}"
                        currentBuild.result = 'FAILURE'
                        error("Stopping pipeline")
                    }
                }
            }
        }

        stage('Generate Timestamp File') {
            steps {
                script {
                    def timestamp = new Date().format("yyyy-MM-dd_HH-mm-ss")
                    writeFile file: "timestamp.txt", text: "Build timestamp: ${timestamp}\n"
                    echo "🕒 Timestamp: ${timestamp}"
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
                    sh "sleep 10"
                    def serviceUrl = sh(script: "minikube service ${IMAGE_NAME} --url", returnStdout: true).trim()
                    echo "🔍 Checking health at: ${serviceUrl}/health"

                    try {
                        def response = sh(script: "curl -s -f ${serviceUrl}/health", returnStdout: true).trim()
                        echo "✅ Health check OK: ${response}"
                    } catch (e) {
                        echo "❌ Health check failed"
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
        always {
            echo '🧹 Pipeline completed.'
        }
    }
}
