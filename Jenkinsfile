pipeline {
    agent any

    environment {
        IMAGE = "sohan0077/jenbackend:${env.GIT_COMMIT.take(7)}"
        APP = "jenkins-proj-101-backend"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timeout(time: 10, unit: 'MINUTES')
    }

    stages {
        stage('Initialize') {
            steps {
                sh 'rm -f .jenkins_deployed'
            }
        }

        stage('Test') {
            steps {
                dir('app') {
                    sh '''
                        set -euo pipefail
                        python3 -m venv .venv
                        source .venv/bin/activate
                        pip install -q -r requirements.txt
                        pytest -q
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                sh '''
                    set -euo pipefail
                    docker build -t "$IMAGE" ./app
                '''
            }
        }

        stage('Push') {
            steps {
                sh '''
                    set -euo pipefail
                    docker push "$IMAGE"
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -euo pipefail
                    export KUBECONFIG="${KUBECONFIG:-$HOME/.kube/config}"
                    sed "s|image: sohan0077/jenbackend:.*|image: $IMAGE|" k8s/backend.yaml > k8s/backend-${BUILD_NUMBER}.yaml
                    kubectl apply -f k8s/backend-${BUILD_NUMBER}.yaml -n"
                    touch .jenkins_deployed
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                    set -euo pipefail
                    export KUBECONFIG="${KUBECONFIG:-$HOME/.kube/config}"
                    kubectl rollout status deployment/$APP --timeout=120s
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment successful"
        }

        failure {
            script {
                if (fileExists('.jenkins_deployed')) {
                    sh '''
                        set -euo pipefail
                        export KUBECONFIG="${KUBECONFIG:-$HOME/.kube/config}"
                        kubectl rollout undo deployment/$APP
                    '''
                }
            }
        }

        always {
            sh '''
                set -euo pipefail
                docker rmi "$IMAGE" 2>/dev/null || true
                rm -f k8s/backend-${BUILD_NUMBER}.yaml
                rm -f .jenkins_deployed
                rm -rf .venv
            '''
        }
    }
}
