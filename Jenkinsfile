pipeline {
    agent any
    tools {
        shiningpanda-python 'Python3.9'  // 引用全局配置的Python
        nodejs 'Node 24'   // 引用全局配置的NodeJS（用于Newman）
    }
    stages {
        stage('Checkout Code from GitHub') {
            steps {
                git url: 'https://github.com/你的用户名/flask-demo-api.git',
                    branch: 'main',
                    credentialsId: 'github-credentials'  // 替换为你的凭据ID
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh 'python -m pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Start Flask API Server') {
            steps {
                script {
                    // 在后台启动API服务并记录进程ID
                    sh '''
                        nohup python app.py --host=0.0.0.0 > api_server.log 2>&1 &
                        echo $! > api_pid.txt  # 保存进程ID用于后续关闭
                    '''
                    // 等待服务初始化（根据实际情况调整时长）
                    sh 'sleep 15'
                }
            }
        }

        stage('Install Newman (if needed)') {
            steps {
                sh 'npm install -g newman newman-reporter-html'
            }
        }

        stage('Run Postman Tests with Newman') {
            steps {
                script {
                    // 创建报告目录
                    sh 'mkdir -p postman_reports'

                    // 执行Newman测试
                    sh '''
                        newman run postman/flask-api-collection.json \
                            -e postman/dev-env.json \
                            -r cli,html \
                            --reporter-html-export postman_reports/api_test_report.html
                    '''
                }
            }
            post {
                always {
                    // 发布HTML报告
                    publishHTML(target: [
                        allowMissing: false,
                        alwaysLinkToLastBuild: false,
                        keepAll: true,
                        reportDir: 'postman_reports',
                        reportFiles: 'api_test_report.html',
                        reportName: 'Postman API Test Report',
                        // 解决报告样式问题
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
            // 停止API服务（避免端口占用）
            script {
                if (fileExists('api_pid.txt')) {
                    sh 'kill -9 $(cat api_pid.txt) || true'
                    sh 'rm -f api_pid.txt'
                }
            }
        }
        success {
            // 构建成功通知（可选）
            echo 'API测试全部通过！'
        }
        failure {
            // 构建失败通知（可选）
            echo 'API测试失败，请查看报告！'
        }
    }
}