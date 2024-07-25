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
            // 원격 디렉토리 존재 여부 확인
            def remoteDirExists = sh(script: "ssh ${REMOTE_USER}@${REMOTE_HOST} '[ -d ${REMOTE_PATH} ] && echo true || echo false'", returnStdout: true).trim()
            echo "Remote directory exists: ${remoteDirExists}"

            if (remoteDirExists == 'true') {
              // .git 디렉토리 존재 여부 확인
              def gitDirExists = sh(script: "ssh ${REMOTE_USER}@${REMOTE_HOST} '[ -d ${REMOTE_PATH}/.git ] && echo true || echo false'", returnStdout: true).trim()
              echo ".git directory exists: ${gitDirExists}"

              if (gitDirExists == 'true') {
                // .git 파일이 존재하는 경우 git reset 및 git pull 실행
                sh "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && git fetch && git reset --hard origin/${BRANCH} && git pull ${GIT_ORIGIN} ${BRANCH}'"
              } else {
                // .git 파일이 존재하지 않는 경우 git init 및 clone
                sh "ssh ${REMOTE_USER}@${REMOTE_HOST} 'cd ${REMOTE_PATH} && git init && git remote add ${GIT_ORIGIN} ${GIT_URL} && git fetch && git checkout -b ${BRANCH} ${GIT_ORIGIN}/${BRANCH}'"
              }
            } else {
              // 디렉토리가 존재하지 않는 경우 디렉토리 생성 및 git init
              sh "ssh ${REMOTE_USER}@${REMOTE_HOST} 'mkdir -p ${REMOTE_PATH} && cd ${REMOTE_PATH} && git init && git remote add ${GIT_ORIGIN} ${GIT_URL} && git fetch && git checkout -b ${BRANCH} ${GIT_ORIGIN}/${BRANCH}'"
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