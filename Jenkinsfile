@Library('prisma-lib') _
pipeline {

    agent{
        label "slave01"
    }

    parameters {
        string(name: 'clusterName', defaultValue: '', description: 'Please insert clustername')
        choice(choices: ['openshift','kubernetes'], name: 'orchestration', description: '')
        booleanParam defaultValue: true, description: '', name: 'proxy'
        booleanParam defaultValue: true, description: '', name: 'deploy'
        booleanParam defaultValue: true, description: '', name: 'nodeselector'
    }

    environment {
        PASS = credentials('pass_pythom') 
        PASSDOCKER =credentials('registry-pass')
        USER = credentials('user_pythom')
        PROXY_KBANK = credentials('proxy-kbank')
        SLACK_TOKEN = credentials('slack-token')
        CLUSTERNAME = "${params.clusterName}"
        LABELKEY = "${params.labelKey}"
        LABELVALUE = "${params.labelValue}"
        ORCHESTRATION = "${params.orchestration}"
    }

 

    stages {

        stage('Hello world') {
            steps {
                hello()
            }
        }

        stage('Build') {
            steps {
                build_images()
            }
        }

        stage('Scan Images') {
            steps {
                scan_images()
            }
        }

        stage('Push Images To Registry') {
            steps {
                push_images("$PASSDOCKER")
            }
        }

        stage('Run') {
            steps {
                script{
                    if (params.nodeselector) {
                    env.KEY = input message: 'Please insert key of labels',
                             parameters: [string(defaultValue: '',
                                          description: '',
                                          name: 'labelKey')]
                    env.VALUE = input message: 'Please insert value of labels',
                             parameters: [string(defaultValue: '',
                                          description: '',
                                          name: 'labelValue')]
                        if (params.proxy){
                        sh """
                            echo "$env.KEY"
                            docker run -v /home/jenkins/workspace/pythom-test-2:/usr/app/src --user 1000 --rm pittimonr/pythom-test:$BUILD_TAG -p $PROXY_KBANK -c $CLUSTERNAME -o $ORCHESTRATION -lk $env.KEY -lv $env.VALUE
                        """
                        }
                        else {
                        sh """
                            docker run -v /home/jenkins/workspace/pythom-test-2:/usr/app/src --user 1000 --rm pittimonr/pythom-test:$BUILD_TAG -c $CLUSTERNAME -o $ORCHESTRATION -lk $env.KEY -lv $env.VALUE
                        """
                        }
                    }
                    else if (params.proxy){
                    sh """
                        echo "$env.KEY"
                        docker run -v /home/jenkins/workspace/pythom-test-2:/usr/app/src --user 1000 --rm pittimonr/pythom-test:$BUILD_TAG -p $PROXY_KBANK -c $CLUSTERNAME -o $ORCHESTRATION
                    """
                    }
                    else {
                    sh """
                        docker run -v /home/jenkins/workspace/pythom-test-2:/usr/app/src --user 1000 --rm pittimonr/pythom-test:$BUILD_TAG -c $CLUSTERNAME -o $ORCHESTRATION
                    """
                    }
                }
            }
        }

        stage('Apply Yaml To Openshift') {
            when {
                equals expected:true, actual: params.deploy
            }
            steps {
                apply_yaml("$USER","$PASS","$CLUSTERNAME")
            }
        }

        stage('Sent Yaml File To Slack') {
            steps {
                script{
                    sh """
                        echo "***Yaml File had sent***"
                    """
                }
            }
            post {
                always {
                    sent_yaml("$CLUSTERNAME")
                    deleteDir()
                    }
                success {
                    echo '\033[0;32m *** Job SUCCESSFUL ***'
                    }
                }
        }

    }
}
