FROM jenkins/jenkins:lts

# Jenkinsの初期設定をコード化
COPY casc/jenkins.yaml /var/jenkins_home/casc_configs/jenkins.yaml

# Jenkinsのプラグインを手動でインストールするスクリプトをコピー
COPY install-plugins.sh /usr/local/bin/install-plugins.sh
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# プラグインをインストール
USER root
RUN chmod +x /usr/local/bin/install-plugins.sh && /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt || { echo 'Failed to install plugins'; exit 1; }

# Jenkins Homeの権限を設定
RUN chown -R jenkins:jenkins /var/jenkins_home
USER jenkins
