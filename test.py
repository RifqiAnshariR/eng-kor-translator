prompt = "to-koHalo nama saya Dwi"
if "to-ko" in prompt:
    prompt = prompt.replace("to-ko", "", 1)
# prompt = "Halo nama saya Dwi"

print(prompt)