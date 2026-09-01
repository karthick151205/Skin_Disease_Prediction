from safetensors.torch import load_file

state_dict = load_file("model.safetensors")

print("Total parameters:", len(state_dict))

for key in state_dict.keys():
    print(key, state_dict[key].shape)