import torch
import json

path = "models/AITO_Net_PMReg_FinalResidualFusion_v1_LOCKED_COMPLETE/BackboneResidualGatedFusion_v3.pth"

ckpt = torch.load(path, map_location="cpu")

print(type(ckpt))

if isinstance(ckpt, dict):
    print("\nKEYS:")
    for k in ckpt.keys():
        print(k)

    print("\nDETAILS:")
    for k, v in ckpt.items():
        print(k, type(v))

    if "source_checkpoints" in ckpt:
        print("\nSOURCE CHECKPOINTS:")
        print(json.dumps(ckpt["source_checkpoints"], indent=4))