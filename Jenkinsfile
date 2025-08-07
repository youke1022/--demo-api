pipeline {
    agent any
    environment {
    // 显式指定Python路径（覆盖插件自动注入）
    PYTHON_HOME = 'E:\\jenkins_tools\\python3.9'
 }
    tools {
        // 使用ShiningPanda插件完整工具类型名称
        'jenkins.plugins.shiningpanda.tools.PythonInstallation' 'python3.9'  // 全局配置的Python名称
        nodejs 'Node 24'  // 全局配置的NodeJS名称
    }
   
    stages {
        stage('Checkout Code from GitHub') {
            steps {
                git url: 'https://github.com/youke1022/--demo-api.git',
                    branch: 'main',
                    credentialsId: '836f2704-23a0-49a8-b83b-3bdcb19cb2ca'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                // 使用ShiningPanda提供的Python路径创建虚拟环境
                bat '%PYTHON_HOME%\\python.exe -m venv venv'
            }
        }

        stage('Install Python Dependencies') {
            steps {
                // 激活虚拟环境并安装依赖
                bat '''
                    call venv\\Scripts\\activate.bat
                    python --version
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Start Flask API Server') {
            steps {
                script {
                    // 在虚拟环境中启动服务（Windows后台启动）
                    bat '''
                        call venv\\Scripts\\activate.bat
                        start /b python app.py --host=0.0.0.0 > api_server.log 2>&1
                    '''
                    // 等待服务初始化
                    bat 'timeout /t 15 /nobreak'
                }
            }
        }

        stage('Install Newman') {
            steps {
                bat 'npm install -g newman newman-reporter-html'
            }
        }

        stage('Run Postman Tests') {
            steps {
                script {
                    bat '''
                        newman run postman/flask-api-collection.json ^
                            -e postman/dev-env.json ^
                            -r cli,html ^
                            --reporter-html-export postman_reports/api_test_report.html
                    '''
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
            // 停止所有相关进程（虚拟环境+Python服务）
            script {
                bat '''
                    taskkill /F /IM python.exe /FI "WINDOWTITLE eq *app.py*" || echo 服务未运行
                    taskkill /F /IM node.exe /FI "COMMANDLINE eq *newman*" || echo Newman未运行
                '''
            }
        }
        success {
            echo '🎉 API测试全部通过！'
        }
        failure {
            echo '❌ API测试失败，请查看Postman报告'
        }
    }
}


