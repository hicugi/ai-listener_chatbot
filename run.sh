docker run -it \
  --name ai-listener_chatbot \
  --device /dev/snd \
  -e PULSE_SERVER=unix:${XDG_RUNTIME_DIR}/pulse/native \
  -v ${XDG_RUNTIME_DIR}/pulse/native:${XDG_RUNTIME_DIR}/pulse/native \
  -v ~/.config/pulse/cookie:/root/.config/pulse/cookie \
  -v $(pwd)/pip-cache:/root/.cache/pip \
  -v $(pwd)/venv:/opt/venv \
  -v $(pwd)/public:/app/public \
  -v $(pwd)/src:/app/src \
  -v $(pwd)/models:/app/models \
  ai-listener_chatbot:latest &
