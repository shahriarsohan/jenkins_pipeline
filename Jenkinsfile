pipeline {
    agent any

    environment {
        IMAGE = "sohan0077/jenbackend:${env.GIT_COMMIT.take(7)}"
        APP = "jenkins-proj-101-backend"
        KUBE_NAMESPACE = "default"
        S3_BUCKET = "jenkins-proj-101-backend"
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '20'))
        timeout(time: 10, unit: 'MINUTES')
    }

    stages {
        stage('Clean') {
            steps {
                deleteDir()
            }
        }

        // stage('Initialize') { ## Dont need this stage as we are using deleteDir()
        //     steps {
        //         sh 'rm -f .jenkins_deployed'
        //     }
        // }

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                dir('app') {
                    sh '''
                    bash -c "
                    set -euo pipefail
                    python3 -m venv .venv
                    source .venv/bin/activate
                    pip install -q -r requirements.txt
                    pytest -q
                    "
                    '''
                }
            }
        }

        stage('Build') {
            steps {
                sh '''
                bash -c "
                set -euo pipefail
                docker build -t $IMAGE ./app
                "
                '''
            }
        }

        stage('Push') {
            steps {
                sh '''
                bash -c "
                set -euo pipefail
                docker push $IMAGE
                "
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                bash -c "
                set -euo pipefail
                export KUBECONFIG=${KUBECONFIG:-$HOME/.kube/config}

                sed 's|image: sohan0077/jenbackend:.*|image: '"$IMAGE"'|' k8s/backend.yaml > k8s/backend-${BUILD_NUMBER}.yaml

                kubectl apply -f k8s/backend-${BUILD_NUMBER}.yaml -n $KUBE_NAMESPACE --validate=false

                touch .jenkins_deployed
                "
                '''
            }
        }

        stage('Verify') {
            steps {
                sh '''
                bash -c "
                set -euo pipefail
                export KUBECONFIG=${KUBECONFIG:-$HOME/.kube/config}

                kubectl rollout status deployment/$APP -n $KUBE_NAMESPACE --timeout=120s 
                "
                '''
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
                    sh '''
                    bash -c "
                    set -euo pipefail
                    export KUBECONFIG=${KUBECONFIG:-$HOME/.kube/config}

                    kubectl rollout undo deployment/$APP -n $KUBE_NAMESPACE
                    kubectl rollout status deployment/$APP -n $KUBE_NAMESPACE
                    "
                    '''
                }
            }
        }

    always {
        withCredentials([
        string(credentialsId: 'AWS_ACCESS_KEY', variable: 'AWS_ACCESS_KEY_ID'),
        string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
        string(credentialsId: 'JENKINS_USER', variable: 'JENKINS_USER'),
        string(credentialsId: 'JENKINS_API_TOKEN', variable: 'JENKINS_API_TOKEN')
    ]) {
            sh '''
            bash -c "
            set -euo pipefail

            if [ -f k8s/backend-${BUILD_NUMBER}.yaml ]; then
                aws s3 cp k8s/backend-${BUILD_NUMBER}.yaml s3://$S3_BUCKET/build-${BUILD_NUMBER}/
            fi

            aws s3 cp $WORKSPACE s3://$S3_BUCKET/build-${BUILD_NUMBER}/workspace/ --recursive --exclude '.git/*' --exclude '*/.venv/*'

            ## Upoading build logs
            curl -u ${JENKINS_USER}:${JENKINS_API_TOKEN} ${BUILD_URL}consoleText -o build-${BUILD_NUMBER}.log
            aws s3 cp build-${BUILD_NUMBER}.log s3://${S3_BUCKET}/build-${BUILD_NUMBER}/

            docker rmi $IMAGE 2>/dev/null || true
            rm -f k8s/backend-${BUILD_NUMBER}.yaml
            rm -f .jenkins_deployed
            rm -rf app/.venv
            "
            '''
            }
        }
    }
}