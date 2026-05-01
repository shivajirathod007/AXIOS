import os
from onnxruntime.quantization import quantize_dynamic, QuantType

# The file you just successfully exported
input_fp32_model = "hf_model_export/model.onnx"

# The lightweight file our pipeline is looking for
output_int8_model = "efficientnet_lite_int8.onnx"

print("Starting INT8 Quantization... this might take a minute.")

try:
    quantize_dynamic(
        model_input=input_fp32_model,
        model_output=output_int8_model,
        weight_type=QuantType.QUInt8 
    )
    
    print(f"SUCCESS! Your quantized model is ready: {output_int8_model}")
    print(f"Original Size: {os.path.getsize(input_fp32_model) / (1024*1024):.2f} MB")
    print(f"New INT8 Size: {os.path.getsize(output_int8_model) / (1024*1024):.2f} MB")
    
except Exception as e:
    print(f"Quantization failed: {e}")