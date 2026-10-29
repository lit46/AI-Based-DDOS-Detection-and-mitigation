#!/bin/bash
# Starts Floodlight with a specific Java. Floodlight is built for Java 8; use 11 (or 8) if 17 fails.
#   archlinux-java status            # list installed JVMs
#   JAVA_HOME=/usr/lib/jvm/java-11-openjdk ./start_floodlight.sh
FL=${FL:-$HOME/floodlight}
JAVA=${JAVA_HOME:+$JAVA_HOME/bin/}java
$JAVA -version 2>&1 | head -1
cd "$FL" && exec $JAVA -Xmx1g -jar target/floodlight.jar
