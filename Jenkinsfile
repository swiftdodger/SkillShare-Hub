pipeline {
    agent any

    environment {
        DEPLOY_HOST = "${env.DEPLOY_HOST}"
        DEPLOY_USER = "${env.DEPLOY_USER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy') {
            when {
                branch 'master'
            }
            steps {
                sshagent(credentials: ['deploy-ssh-key']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} '
                            set -e
                            cd /home/flavio-gabriel/PycharmProjects/SkillShare-Hub
                            git fetch --all
                            git reset --hard origin/master
                            ./deploy.sh
                        '
                    '''
                }
            }
        }
    }
}
