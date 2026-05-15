import sounddevice as sd

devices = sd.query_devices()
print(sd.default.device)

for idx, device in enumerate(devices):
    print(
        idx,
        device["name"],
        "input_channels=",
        device["max_input_channels"]
    )
