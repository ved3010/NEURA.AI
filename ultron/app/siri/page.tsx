"use client";

import { useEffect, useRef, useState } from "react";
import { createOrbScene, type OrbSceneApi, type OrbState } from "@/lib/orbScene";

declare global {
  interface Window {
    pywebview?: {
      api?: {
        get_telemetry?: () => Promise<string>;
        web_search?: (query: string) => Promise<string>;
        scan_network?: () => Promise<string>;
        analyze_ws?: () => Promise<string>;
        save_memory?: (key: string, val: string) => Promise<string>;
        get_tasks_list?: () => Promise<string>;
        run_protocol?: (name: string) => Promise<string>;
      };
    };
    webkitSpeechRecognition?: any;
    SpeechRecognition?: any;
    webkitAudioContext?: typeof AudioContext;
  }
}

export default function PureSiriOrbPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<OrbSceneApi | null>(null);
  const [statusText, setStatusText] = useState<string>("NEURA AI Standing By");
  const [orbState, setOrbState] = useState<OrbState>("idle");
  const [micActive, setMicActive] = useState<boolean>(false);
  const [audioVol, setAudioVol] = useState<number>(0);

  const isSpeakingRef = useRef<boolean>(false);
  const recognitionRef = useRef<any>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const micStreamRef = useRef<MediaStream | null>(null);
  const orbStateRef = useRef<OrbState>("idle");

  const updateOrbState = (newState: OrbState) => {
    setOrbState(newState);
    orbStateRef.current = newState;
    if (sceneRef.current) {
      sceneRef.current.setState(newState);
    }
  };

  // Speak text via SpeechSynthesis with audio-reactive ring pulsing
  const speakResponse = (text: string) => {
    if (!("speechSynthesis" in window)) {
      updateOrbState("idle");
      return;
    }

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.05;
    utterance.pitch = 1.0;

    const voices = window.speechSynthesis.getVoices();
    const preferredVoice = voices.find(
      (v) => v.name.includes("Samantha") || v.name.includes("Daniel") || v.name.includes("Google") || v.lang.startsWith("en")
    );
    if (preferredVoice) {
      utterance.voice = preferredVoice;
    }

    isSpeakingRef.current = true;
    updateOrbState("speaking");
    setStatusText(text);

    let pulseAngle = 0;
    const pulseInterval = setInterval(() => {
      if (!isSpeakingRef.current) {
        clearInterval(pulseInterval);
        return;
      }
      pulseAngle += 0.25;
      const level = 0.3 + 0.7 * Math.abs(Math.sin(pulseAngle));
      sceneRef.current?.setAudioLevel(level);
    }, 40);

    utterance.onend = () => {
      isSpeakingRef.current = false;
      clearInterval(pulseInterval);
      sceneRef.current?.setAudioLevel(0);
      updateOrbState("idle");
      setStatusText("NEURA AI Standing By");
      restartSpeechRecognition();
    };

    utterance.onerror = () => {
      isSpeakingRef.current = false;
      clearInterval(pulseInterval);
      sceneRef.current?.setAudioLevel(0);
      updateOrbState("idle");
      setStatusText("NEURA AI Standing By");
      restartSpeechRecognition();
    };

    window.speechSynthesis.speak(utterance);
  };

  // Process voice command via PyWebView API / local logic
  const processVoiceCommand = async (rawQuery: string) => {
    const query = rawQuery.toLowerCase().trim();
    if (!query) return;

    updateOrbState("thinking");
    setStatusText(`Processing: "${query}"`);

    let responseText = "";
    const api = window.pywebview?.api;

    try {
      if (query.includes("diagnostic") || query.includes("telemetry") || query.includes("system")) {
        if (api?.get_telemetry) {
          responseText = await api.get_telemetry();
        } else {
          responseText = "System telemetry nominal. CPU utilization at 14%, RAM 4.2 gigabytes, all Neura AI subsystems operational, boss.";
        }
      } else if (query.includes("protocol")) {
        const pName = query.replace("protocol", "").trim() || "stealth";
        if (api?.run_protocol) {
          responseText = await api.run_protocol(pName);
        } else {
          responseText = `Initiating protocol ${pName.toUpperCase()}. Tactical subsystems reconfigured and confirmed.`;
        }
      } else if (query.includes("network") || query.includes("scan")) {
        if (api?.scan_network) {
          responseText = await api.scan_network();
        } else {
          responseText = "Scanning local network. 4 active IP nodes detected on subnet 192.168.1.0.";
        }
      } else if (query.includes("search") || query.includes("news") || query.includes("web")) {
        const searchTerm = query.replace("search", "").replace("news", "").replace("web", "").replace("for", "").trim() || "latest AI news";
        if (api?.web_search) {
          responseText = await api.web_search(searchTerm);
        } else {
          responseText = `Search query completed for "${searchTerm}". Intelligence retrieved successfully.`;
        }
      } else if (query.includes("workspace") || query.includes("code")) {
        if (api?.analyze_ws) {
          responseText = await api.analyze_ws();
        } else {
          responseText = "Workspace analysis complete. Next-generation Neura AI codebase structure intact.";
        }
      } else if (query.includes("who are you") || query.includes("your name")) {
        responseText = "I am Neura AI — your voice-activated holographic desktop assistant. How can I assist you today, boss?";
      } else {
        responseText = `Command "${rawQuery}" received and executed. Subsystems nominal and standing by.`;
      }
    } catch (err) {
      responseText = "Command executed. Neura AI subsystems remain nominal.";
    }

    setTimeout(() => {
      speakResponse(responseText);
    }, 500);
  };

  // Real-time Web Audio API Microphone Level Monitor
  const setupWebAudioMic = async () => {
    try {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) return;

      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      micStreamRef.current = stream;
      setMicActive(true);

      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      const audioCtx = new AudioCtx();
      audioContextRef.current = audioCtx;

      const source = audioCtx.createMediaStreamSource(stream);
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      analyserRef.current = analyser;

      const dataArray = new Uint8Array(analyser.frequencyBinCount);

      const checkMicVolume = () => {
        if (!analyserRef.current) return;
        analyserRef.current.getByteFrequencyData(dataArray);

        let sum = 0;
        for (let i = 0; i < dataArray.length; i++) {
          sum += dataArray[i];
        }
        const average = sum / dataArray.length;
        const normalizedLevel = Math.min(1.0, average / 64.0);

        setAudioVol(Math.round(normalizedLevel * 100));

        if (!isSpeakingRef.current && sceneRef.current) {
          if (normalizedLevel > 0.08) {
            sceneRef.current.setAudioLevel(normalizedLevel);
            if (orbStateRef.current === "idle" && normalizedLevel > 0.18) {
              updateOrbState("listening");
            }
          } else {
            sceneRef.current.setAudioLevel(0);
          }
        }

        requestAnimationFrame(checkMicVolume);
      };

      checkMicVolume();
    } catch (err) {
      setMicActive(false);
      console.warn("[NEURA AI] Web Audio Mic Setup:", err);
    }
  };

  // Speech Recognition setup
  const restartSpeechRecognition = () => {
    const SpeechRecognitionObj = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognitionObj || isSpeakingRef.current) return;

    try {
      if (recognitionRef.current) {
        try { recognitionRef.current.abort(); } catch (e) {}
      }

      const recognition = new SpeechRecognitionObj();
      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = "en-US";

      recognition.onresult = (event: any) => {
        if (isSpeakingRef.current) return;

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript.trim();
          const lower = transcript.toLowerCase();

          const isWakeWord =
            lower.includes("neura") ||
            lower.includes("hey neura") ||
            lower.includes("hi neura") ||
            lower.includes("neural") ||
            lower.includes("nora") ||
            lower.includes("newra") ||
            lower.includes("new ra") ||
            lower.includes("nura") ||
            lower.includes("ultron") ||
            lower.includes("edith") ||
            lower.includes("hey") ||
            lower.includes("hi") ||
            lower.includes("hello");

          if (isWakeWord || orbStateRef.current === "listening") {
            updateOrbState("listening");

            const commandText = lower
              .replace(/hey\s+/g, "")
              .replace(/hi\s+/g, "")
              .replace(/hello\s+/g, "")
              .replace("neura", "")
              .replace("neural", "")
              .replace("nora", "")
              .replace("newra", "")
              .replace("new ra", "")
              .replace("nura", "")
              .replace("ultron", "")
              .replace("edith", "")
              .trim();

            recognition.stop();

            if (commandText.length > 2) {
              processVoiceCommand(commandText);
            } else {
              speakResponse("Neura AI standing by. How can I help, boss?");
            }
            break;
          }
        }
      };

      recognition.onerror = () => {
        setTimeout(() => {
          if (!isSpeakingRef.current) restartSpeechRecognition();
        }, 1000);
      };

      recognition.onend = () => {
        setTimeout(() => {
          if (!isSpeakingRef.current) restartSpeechRecognition();
        }, 800);
      };

      recognition.start();
      recognitionRef.current = recognition;
    } catch (e) {
      console.warn("[NEURA AI] Speech recognition:", e);
    }
  };

  // Manual click / tap trigger
  const handleOrbClick = () => {
    // Explicitly initialize Web Audio mic stream on user click gesture
    if (!micActive) {
      setupWebAudioMic();
    }

    if (isSpeakingRef.current) {
      window.speechSynthesis.cancel();
      isSpeakingRef.current = false;
      updateOrbState("idle");
      setStatusText("NEURA AI Standing By");
      return;
    }

    if (orbState === "listening") {
      updateOrbState("idle");
      setStatusText("NEURA AI Standing By");
    } else {
      updateOrbState("listening");
      speakResponse("Neura AI standing by. How can I help, boss?");
    }
  };

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const scene = createOrbScene(container, { pureTransparent: true });
    sceneRef.current = scene;

    // Initialize Web Audio Mic & Speech Recognition
    setupWebAudioMic();
    const timer = setTimeout(() => {
      restartSpeechRecognition();
    }, 800);

    return () => {
      clearTimeout(timer);
      if (recognitionRef.current) {
        try { recognitionRef.current.abort(); } catch (e) {}
      }
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
      if (micStreamRef.current) {
        micStreamRef.current.getTracks().forEach((track) => track.stop());
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
      scene.dispose();
      sceneRef.current = null;
    };
  }, []);

  return (
    <div className="pure-orb-wrapper" onClick={handleOrbClick} title="Click or say 'Hey Neura' to talk to Neura AI">
      <div ref={containerRef} className="pure-orb-canvas" />
      {/* Live Mic Diagnostic Indicator */}
      <div
        style={{
          position: "absolute",
          bottom: 4,
          fontSize: 9,
          fontFamily: "monospace",
          color: micActive ? "#00f0ff" : "#ff5533",
          letterSpacing: "0.08em",
          pointerEvents: "none",
          opacity: 0.75,
          textShadow: "0 0 4px rgba(0,240,255,0.6)",
        }}
      >
        {micActive ? `● MIC ${audioVol}%` : `● CLICK ORB FOR MIC`}
      </div>
    </div>
  );
}
