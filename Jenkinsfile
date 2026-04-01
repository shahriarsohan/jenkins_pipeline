pipeline {
    agent any

    environment {
        IMAGE = "sohan0077/jenbackend:v1"
    }

    stages {
        stage('Clone') {
            steps {
                git 'https://github.com/shahriarsohan/jenkins_pipeline.git'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t $IMAGE ./app'
            }
        }

        stage('Push') {
            steps {
                sh 'docker push $IMAGE'
            }
        }

        stage('Deploy') {
            steps {
                sh 'kubectl apply -f k8s/backend.yaml'
            }
        }
    }
}