pipeline {
    agent {
        label 'pta-controller'
    }
    triggers {
        // Run between 3 AM and 5 AM on Monday.
        cron('H 3-5/3 * * 1')
    }
    parameters {
        string(name: 'PACKER_VM_NAME', defaultValue: 'template-windows-10-test', description: 'The name to give the produced VM.')
        booleanParam(name: "TestSystems", defaultValue: true, description: 'Reprovision the associated TestSystems.')
    }
    environment {
        PACKER_TIMEZONE = "Mountain Standard Time"
        PACKER_HOST_NAME = "PTATemplate"
    }
    options {
        disableConcurrentBuilds()
        buildDiscarder logRotator(numToKeepStr: '10')
    }
    stages {
        stage('Populate Config with Secrets') {
            agent {
                label 'packer'
            }
            steps {
                dir ("cfg") {
                    sh '''
                        /opt/rh/rh-python36/root/usr/bin/virtualenv virt_pylint
                        source virt_pylint/bin/activate
                        pip install -r requirements.txt
                        pylint render_cfg.py --max-line-length=120
                        deactivate
                       '''
                    withCredentials([usernamePassword(credentialsId: 'pta-user-win', usernameVariable: 'PACKER_WIN_USERNAME', passwordVariable: 'PACKER_WIN_PASSWORD')]) {
                        sh '''
                            source virt_pylint/bin/activate
                            python render_cfg.py
                            deactivate
                           '''
                    }
                }
            }
        }
        stage('Run Packer') {
            agent {
                label 'packer'
            }
            steps {
                withCredentials([
                        usernamePassword(credentialsId: 'terraform-vsphere', usernameVariable: 'PACKER_VSPHERE_USER', passwordVariable: 'PACKER_VSPHERE_PASSWORD'),
                        usernamePassword(credentialsId: 'pta-user-win', usernameVariable: 'PACKER_WIN_USERNAME', passwordVariable: 'PACKER_WIN_PASSWORD')]) {
                    // For extra logging, adding "PACKER_LOG=1" to the start of the shell command below.
                    // To keep the VM running for inspection, add -on-error=abort
                    sh "packer build -color=false -force win10x64-enterprise.json"
                }
            }
        }
        stage('TestSystems') {
            when {
                expression { params.TestSystems }
            }
            steps {
                sh 'echo This is a placeholder for adding in downstream jobs in the future if needed.'
                //build job: 'PTA/TestSystems-win-10', propagate: false, wait: true, parameters: [
                //        booleanParam(name: 'Terraform_Apply', value: true),
                //        booleanParam(name: 'Terraform_Verify', value: false),
                //        booleanParam(name: 'Ansible', value: true)]
            }
        }
    }
    post {
        failure {
            emailext body: '''$PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS<br><br>Check the console output at ${BUILD_URL}console to view the results.''', mimeType: 'text/html', recipientProviders: [requestor()], subject: '$PROJECT_NAME - Build # $BUILD_NUMBER - $BUILD_STATUS!', to: "pta.admin@company.com"
        }
    }
}