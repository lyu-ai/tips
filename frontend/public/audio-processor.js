class AudioProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
  }

  process(inputs, outputs, parameters) {
    const input = inputs[0];
    if (input.length > 0) {
      const channelData = input[0];
      let monoData;

      // Convert to mono if there are multiple channels
      if (input.length > 1) {
        const numChannels = input.length;
        monoData = new Float32Array(channelData.length);
        for (let i = 0; i < channelData.length; i++) {
          let sum = 0;
          for (let ch = 0; ch < numChannels; ch++) {
            sum += input[ch][i];
          }
          monoData[i] = sum / numChannels;
        }
      } else {
        monoData = channelData.slice(); // Clone the array
      }

      // Send a copy of the audio data to the main thread
      this.port.postMessage(monoData);
    }
    return true; // Keep the processor alive
  }
}

registerProcessor('audio-processor', AudioProcessor);