pipeline {
    agent any
    tools {
        'jenkins.plugins.shiningpanda.tools.PythonInstallation' 'python3.9'  // Python工具引用
        nodejs 'Node 24'  // NodeJS工具引用
    }
    stages {
        stage('Checkout Code from GitHub') {
            steps {
                git url: 'https://github.com/youke1022/--demo-api.git',
                    branch: 'main',
                    credentialsId: '836f2704-23a0-49a8-b83b-3bdcb19cb2ca'
            }
        }

        stage('Install Python Dependencies') {
            steps {
                // Windows使用bat命令替代sh
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Start Flask API Server') {
            steps {
                script {
                    // Windows后台启动命令（替代nohup）
                    bat 'start /b python app.py --host=0.0.0.0 > api_server.log 2>&1'
                    // Windows等待命令（替代sleep）
                    bat 'timeout /t 15 /nobreak'  // 等待15秒
                }
            }
        }

        stage('Install Newman (if needed)') {
            steps {
                // 使用bat执行npm命令
                bat 'npm install -g newman newman-reporter-html'
            }
        }

        stage('Run Postman Tests with Newman') {
            steps {
                script {
                    // Windows创建目录命令
                    bat 'mkdir postman_reports'
                    // 执行Newman测试（使用bat命令）
                    bat '''newman run postman/flask-api-collection.json ^
                        -e postman/dev-env.json ^
                        -r cli,html ^
                        --reporter-html-export postman_reports/api_test_report.html'''
                }
            }
            post {
                always {
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'postman_reports',
                        reportFiles: 'api_test_report.html',
                        reportName: 'Postman API Test Report',
                        properties: [
                            'hudson.model.DirectoryBrowserSupport.CSP=',
                            'jenkins.model.DirectoryBrowserSupport.CSP='
                        ]
                    ])
                }
            }
        }
    }
    post {
        always {
            // Windows停止服务命令（替代kill）
            script {
                bat 'taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" || echo 服务未运行'
            }
        }
        success {
            echo 'API测试全部通过！'
        }
        failure {
            echo 'API测试失败，请查看报告！'
        }
    }
}

