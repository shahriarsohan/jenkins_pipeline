pipeline {
    agent any

    environment {
        IMAGE = "sohan0077/jenbackend:v${BUILD_NUMBER}"
    }

    stages {
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
                sh """
                sed 's|image:.*|image: $IMAGE|' k8s/backend.yaml | kubectl apply -f - --validate=false
                """
            }
        }
    }
}