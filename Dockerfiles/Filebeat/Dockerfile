FROM docker.elastic.co/beats/filebeat:8.1.3

USER root

RUN mkdir -p /filebeat_data/conf && mkdir -p /filebeat_data/log && \
	mv /usr/share/filebeat/filebeat.yml /filebeat_data/conf/filebeat.yml

CMD ["filebeat","-e","--strict.perms=false","-c", "/filebeat_data/conf/filebeat.yml"]