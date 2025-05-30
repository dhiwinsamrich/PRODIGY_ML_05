import tensorflow as tf
import json
import h5py
import os

def load_model_with_compatibility(model_path):
    """
    Load a Keras model with compatibility fixes for DepthwiseConv2D layers.
    This function handles the 'groups' parameter issue in newer Keras versions.
    
    Args:
        model_path: Path to the .h5 model file
        
    Returns:
        Loaded Keras model
    """
    # First, we need to modify the model configuration to remove 'groups' from DepthwiseConv2D layers
    with h5py.File(model_path, 'r') as h5file:
        # Check if the model config exists in the file
        if 'model_config' in h5file.attrs:
            model_config_str = h5file.attrs['model_config']
            model_config = json.loads(model_config_str.decode('utf-8'))
            
            # Function to recursively process layers and remove 'groups' from DepthwiseConv2D
            def process_layers(layers_config):
                for layer in layers_config:
                    if layer['class_name'] == 'DepthwiseConv2D' and 'config' in layer:
                        if 'groups' in layer['config']:
                            # Remove the problematic 'groups' parameter
                            del layer['config']['groups']
                    
                    # Process nested layers if they exist
                    if 'layers' in layer:
                        process_layers(layer['layers'])
            
            # Process all layers in the model
            if 'layers' in model_config:
                process_layers(model_config['layers'])
            
            # Create a temporary file with the modified configuration
            temp_model_path = model_path + '.temp'
            with h5py.File(temp_model_path, 'w') as temp_file:
                # Copy all attributes except model_config
                for attr_name, attr_value in h5file.attrs.items():
                    if attr_name != 'model_config':
                        temp_file.attrs[attr_name] = attr_value
                
                # Set the modified model_config
                temp_file.attrs['model_config'] = json.dumps(model_config).encode('utf-8')
                
                # Copy all datasets
                def copy_datasets(name, obj):
                    if isinstance(obj, h5py.Dataset):
                        h5file.copy(name, temp_file, name=name)
                
                h5file.visititems(copy_datasets)
            
            # Load the model from the temporary file
            model = tf.keras.models.load_model(temp_model_path)
            
            # Clean up the temporary file
            os.remove(temp_model_path)
            
            return model
    
    # If we couldn't modify the config, try loading directly
    # This might still fail but it's worth a try
    return tf.keras.models.load_model(model_path)