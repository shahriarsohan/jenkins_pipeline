pipeline {
    agent any

    environment {
        IMAGE = "sohan0077/jenbackend:v${BUILD_NUMBER}"
        APP = "jenkins-proj-101-backend"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 10, unit: 'MINUTES')
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
                export KUBECONFIG=/home/sohan/.kube/config
                sed 's|image:.*|image: $IMAGE|' k8s/backend.yaml > k8s/backend-${BUILD_NUMBER}.yaml
                kubectl apply -f k8s/backend-${BUILD_NUMBER}.yaml --validate=false
                """
            }
        }
        stage('Verify') {
            steps {
                sh """
                export KUBECONFIG=/home/sohan/.kube/kubeadm-config.yaml
                kubectl rollout status deployment/$APP
                """
            }
        }
    }
}