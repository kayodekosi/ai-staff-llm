# Expected Loss Curve – Staff Persona Adapters

When fine-tuning a small Nemotron (or similar) model on role-derived chat data:

- **Starting loss**: typically 2.8 – 3.6  
- **Early phase**: rapid drop as the model learns the system-prompt style and department vocabulary  
- **Final train loss** (2 epochs, small set): usually 0.9 – 1.4  
- **Validation loss**: should track training loss within ~0.3  

Healthy signs: smooth decline, no large spikes, gradient norm settles after warmup.  
If loss stays high, increase rank to 32 or slightly raise learning rate.  
If validation rises while train falls, stop early or reduce epochs.
