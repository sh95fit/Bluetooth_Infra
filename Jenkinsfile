pipeline {
  agent any

  environment {
    GIT_URL = "https://github.com/sh95fit/Bluetooth_Infra.git"
    BRANCH = "main"
    CREDENTIAL_ID = "sh95fit"
    GIT_ORIGIN = "bluetooth_infra"

    REMOTE_PATH = "/home/developer"
    SSH_CREDENTIALS_ID = "bluetooth"
    REMOTE_USER = "developer"
    REMOTE_HOST = "131.186.19.64"

    DOCKER_COMPOSE_FILE = "docker-compose.yml"

    PROJECT_NAME = "bluetooth"

  }

  stages {
    stage('Checkout') {
      steps {
        git branch: "${BRANCH}",
          credentialsId: "${CREDENTIAL_ID}",
          url: "${GIT_URL}"
      }
    }

    stage('Clone Repository') {
      steps {
        script {
          sshagent (credentials: [SSH_CREDENTIALS_ID]) {
            // 원격 서버에 해당 디렉토리가 존재하는지 유무 체크
            def remoteDirExists = sh(script: "ssh ${REMOTE_USER}@${REMOTE_HOST} '[ -d ${REMOTE_PATH} ] && echo true || echo false'", returnStdout: true).trim() == 'true'

            if (remoteDirExists) {
              // .git 파일 존재 유무 체크 함수
              def gitDirExists = sh(script: "ssh ${REMOTE_USER}@${REMOTE_HOST} '[ -d ${REMOTE_PATH}/.git ] && echo true || echo false'", returnStdout: true).trim() == 'true'

              if (gitDirExists) {
                // .git 파일이 존재하는 경우 바로 git pull 적용
                sh "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && git reset --hard HEAD && git pull ${GIT_ORIGIN} main'"
              } else {
                // .git 파일이 존재하지 않는 경우  git init 후 clone
                sh "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && git init && git branch -M main && git remote add ${GIT_ORIGIN} ${GIT_URL} && git fetch && git checkout ${GIT_ORIGIN}/main -f'"
              }
            } else {
              // 디렉토리가 존재하지 않는 경우 디렉토리를 생성하고 git init 후 clone
              sh "ssh ${REMOTE_USER}@${REMOTE_HOST} 'mkdir -p ${REMOTE_PATH} && cd ${REMOTE_PATH} && git init && git branch -M main && git remote add ${GIT_ORIGIN} ${GIT_URL} && git fetch && git checkout ${GIT_ORIGIN}/main -f'"
            }
          }
        }
      }
    }

    stage('Build with docker-compose') {
      steps {
        script {
          sshagent (credentials: [SSH_CREDENTIALS_ID]) {
            // docker-compose 파일 유무 확인
            def composeFileExists = sh(script: "ssh ${REMOTE_USER}@${REMOTE_HOST} '[ -f ${REMOTE_PATH}/${DOCKER_COMPOSE_FILE} ] && echo true || echo false'", returnStdout: true).trim()

            if (composeFileExists) {
              // 동작 중인 컨테이너가 있는지 확인
              def runningContainers = sh(script: "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && docker-compose ps -q'", returnStatus: true)

              // echo "${runningContainers}"

              if (runningContainers == 0) {
                  echo "Stopping and removing existing docker-compose containers..."
                  // 컨테이너 정지 및 삭제
                  sh "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && docker-compose down -v --remove-orphans && docker image rm \$(docker images -q ${PROJECT_NAME}-* | uniq)'"
              } else {
                  echo "No running docker-compose containers found."
              }

              // docker-compose를 빌드하고 시작
              echo "Building and starting new docker-compose containers..."
              sh "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && docker-compose up --build -d'"

            } else {
                  echo "Error: ${DOCKER_COMPOSE_FILE} not found in ${REMOTE_PATH}"
                  currentBuild.result = 'FAILURE'
                  error "docker-compose file not found"
              }
          }
        }
      }
    }
  }
}