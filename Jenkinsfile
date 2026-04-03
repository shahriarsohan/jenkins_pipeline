pipeline {
    agent any

    environment {
        IMAGE = "sohan0077/jenbackend:${env.GIT_COMMIT.take(7)}"
        APP = "jenkins-proj-101-backend"
        KUBE_NAMESPACE = "default"
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
                    sh(script: '''
                        set -euo pipefail
                        python3 -m venv .venv
                        source .venv/bin/activate
                        pip install -q -r requirements.txt
                        pytest -q
                    ''', shell: '/bin/bash')
                }
            }
        }

        stage('Build') {
            steps {
                sh(script: '''
                    set -euo pipefail
                    docker build -t "$IMAGE" ./app
                ''', shell: '/bin/bash')
            }
        }

        stage('Push') {
            steps {
                sh(script: '''
                    set -euo pipefail
                    docker push "$IMAGE"
                ''', shell: '/bin/bash')
            }
        }

        stage('Deploy') {
            steps {
                sh(script: '''
                    set -euo pipefail
                    export KUBECONFIG="${KUBECONFIG:-$HOME/.kube/config}"

                    sed "s|image: sohan0077/jenbackend:.*|image: $IMAGE|" k8s/backend.yaml > k8s/backend-${BUILD_NUMBER}.yaml

                    kubectl apply -f k8s/backend-${BUILD_NUMBER}.yaml -n "$KUBE_NAMESPACE"

                    touch .jenkins_deployed
                ''', shell: '/bin/bash')
            }
        }

        stage('Verify') {
            steps {
                sh(script: '''
                    set -euo pipefail
                    export KUBECONFIG="${KUBECONFIG:-$HOME/.kube/config}"

                    kubectl rollout status deployment/$APP -n "$KUBE_NAMESPACE" --timeout=120s
                ''', shell: '/bin/bash')
            }
        }
    }

    post {

        success {
            echo "✅ Deployment successful"
        }

        failure {
            script {
                if (fileExists('.jenkins_deployed')) {
                    sh(script: '''
                        set -euo pipefail
                        export KUBECONFIG="${KUBECONFIG:-$HOME/.kube/config}"

                        kubectl rollout undo deployment/$APP -n "$KUBE_NAMESPACE"
                        kubectl rollout status deployment/$APP -n "$KUBE_NAMESPACE"
                    ''', shell: '/bin/bash')
                }
            }
        }

        always {
            sh(script: '''
                set -euo pipefail

                docker rmi "$IMAGE" 2>/dev/null || true
                rm -f k8s/backend-${BUILD_NUMBER}.yaml
                rm -f .jenkins_deployed
                rm -rf app/.venv
            ''', shell: '/bin/bash')
        }
    }
}