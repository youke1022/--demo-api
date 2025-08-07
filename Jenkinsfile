pipeline {
    agent any
    environment {
        // 定义容器名称和端口
        CONTAINER_NAME = 'flask-api-container'
        API_PORT = '5000'
    }
    stages {
        stage('Checkout Code') {
            steps {
                git url: 'https://github.com/youke1022/--demo-api.git', branch: 'main'
            }
        }

        stage('Start Python Container & API Service') {
            steps {
                script {
                    // 停止残留容器（如存在）
                    bat 'docker stop %CONTAINER_NAME% || echo 容器未运行'
                    bat 'docker rm %CONTAINER_NAME% || echo 容器不存在'
                    
                    // 启动Python容器（官方镜像）
                    bat '''
                        docker run -d ^
                        --name %CONTAINER_NAME% ^
                        --network=host ^
                        -v "%WORKSPACE%/flask-demo-api:/app" ^
                        -w /app ^
                        python:3.9-slim ^
                        cmd /c "pip install -r requirements.txt && python app.py --host=0.0.0.0"
                    '''
                    
                    // 等待服务启动（关键！根据服务启动速度调整）
                    bat 'timeout /t 30 /nobreak'
                }
            }
        }

        stage('Run Newman Tests (Windows Bat)') {
            steps {
                script {
                    // 在宿主机安装Newman（Windows批处理）
                    bat 'npm install -g newman newman-reporter-html'
                    
                    // 执行Newman测试（使用相对路径）
                    bat '''
                        cd flask-demo-api
                        newman run tests\\postman\\test1.postman_collection.json ^
                        -r cli,html ^
                        --reporter-html-export newman_report.html
                    '''
                }
            }
            post {
                always {
                    // 归档测试报告
                    archiveArtifacts artifacts: 'flask-demo-api\\newman_report.html'
                }
            }
        }
    }
    post {
        always {
            // 停止并删除容器
            bat 'docker stop %CONTAINER_NAME% || echo 容器未运行'
            bat 'docker rm %CONTAINER_NAME% || echo 容器不存在'
        }
        failure {
            echo '❌ Newman测试失败，请查看报告！'
        }
    }
}
