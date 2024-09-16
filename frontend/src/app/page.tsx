"use client";
import React, { useState, useEffect, useRef } from "react";

export default function Home() {
  const [isRecording, setIsRecording] = useState(false);
  const [isConnected, setIsConnected] = useState(false);
  const audioContextRef = useRef<AudioContext | null>(null);
  const audioStreamRef = useRef<MediaStream | null>(null);
  const webSocketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    return () => {
      // Clean up on unmount
      if (audioStreamRef.current) {
        audioStreamRef.current.getTracks().forEach((track) => track.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
      if (webSocketRef.current) {
        webSocketRef.current.close();
      }
    };
  }, []);

  const handleStartRecording = async () => {
    if (isRecording) {
      return;
    }

    // Get the audio stream from the microphone
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });
      audioStreamRef.current = stream;

      // Create AudioContext and audio processor to capture audio chunks
      const audioContext = new AudioContext();
      audioContextRef.current = audioContext;
      const source = audioContext.createMediaStreamSource(stream);

      // Connect to WebSocket server
      const ws = new WebSocket("ws://localhost:8842/ws/audio");
      webSocketRef.current = ws;

      ws.onopen = () => {
        console.log("WebSocket connection opened");
        setIsConnected(true);
      };

      ws.onmessage = (event) => {
        const result = JSON.parse(event.data);
        console.log("Received analysis result:", result);
      };

      ws.onclose = () => {
        console.log("WebSocket connection closed");
        setIsConnected(false);
      };

      const audioProcessor = await audioContext.audioWorklet.addModule(
        "/audio-processor.js"
      );
      const processor = new AudioWorkletNode(audioContext, "audio-processor");

      // Capture the audio data and send to WebSocket
      processor.port.onmessage = (event) => {
        if (
          webSocketRef.current &&
          webSocketRef.current.readyState === WebSocket.OPEN
        ) {
          const audioData = event.data;
          webSocketRef.current.send(audioData);
        }
      };

      // Connect the processor to the audio source
      source.connect(processor);
      processor.connect(audioContext.destination);

      setIsRecording(true);
    } catch (err) {
      console.error("Error accessing microphone:", err);
    }
  };

  const handleStopRecording = () => {
    setIsRecording(false);

    // Stop the audio stream
    if (audioStreamRef.current) {
      audioStreamRef.current.getTracks().forEach((track) => track.stop());
    }

    // Close the WebSocket connection
    if (webSocketRef.current) {
      webSocketRef.current.close();
    }
  };

  return (
    <div className="container">
      <h1>WebSocket Audio Test</h1>
      <p>
        Connect to the WebSocket server and stream audio from your microphone.
      </p>

      <div>
        <button
          onClick={isRecording ? handleStopRecording : handleStartRecording}
        >
          {isRecording ? "Stop Recording" : "Start Recording"}
        </button>
      </div>

      <div>
        <p>Status: {isRecording ? "Recording..." : "Not Recording"}</p>
        <p>WebSocket: {isConnected ? "Connected" : "Disconnected"}</p>
      </div>
    </div>
  );
}
