pipeline {
  agent any

  environment {
    GIT_URL = "https://github.com/sh95fit/Bluetooth_Infra.git"
    BRANCH = "main"
    CREDENTIAL_ID = "sh95fit"

    GIT_ORIGIN = "bluetooth_infra"
  }

  stages {
    stage('Checkout') {
      steps {
        git branch: ${BRANCH},
          credentialsId: ${CREDENTIAL_ID},
          url: ${GIT_URL}
      }
    }
  }

}