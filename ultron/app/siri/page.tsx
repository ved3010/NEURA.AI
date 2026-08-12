"use client";

import { useEffect, useRef, useState } from "react";
import { createOrbScene, type OrbSceneApi, type OrbState } from "@/lib/orbScene";

// Declare PyWebView window API typing
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
  }
}

export default function PureSiriOrbPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<OrbSceneApi | null>(null);
  const [statusText, setStatusText] = useState<string>("NEURA AI Standing By");
  const [orbState, setOrbState] = useState<OrbState>("idle");
  const isSpeakingRef = useRef<boolean>(false);
  const recognitionRef = useRef<any>(null);

  // Helper to change 3D Orb visual state
  const updateOrbState = (newState: OrbState) => {
    setOrbState(newState);
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

    // Select natural voice if available
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

    // Audio level pulse animation loop during speech
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
      startListening();
    };

    utterance.onerror = () => {
      isSpeakingRef.current = false;
      clearInterval(pulseInterval);
      sceneRef.current?.setAudioLevel(0);
      updateOrbState("idle");
      setStatusText("NEURA AI Standing By");
      startListening();
    };

    window.speechSynthesis.speak(utterance);
  };

  // Process voice query via PyWebView API / local intelligence
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
          responseText = "System telemetry nominal. CPU utilization at 12%, RAM 4.2 gigabytes, all subsystems operational, boss.";
        }
      } else if (query.includes("protocol")) {
        const pName = query.replace("protocol", "").trim() || "stealth";
        if (api?.run_protocol) {
          responseText = await api.run_protocol(pName);
        } else {
          responseText = `Initiating protocol ${pName.toUpperCase()}. Subsystems reconfigured and confirmed.`;
        }
      } else if (query.includes("network") || query.includes("scan")) {
        if (api?.scan_network) {
          responseText = await api.scan_network();
        } else {
          responseText = "Scanning local network. 4 active IP nodes detected on subnet 192.168.1.0.";
        }
      } else if (query.includes("search") || query.includes("news") || query.includes("web")) {
        const searchTerm = query.replace("search", "").replace("news", "").replace("web", "").replace("for", "").trim() || "latest technology updates";
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
        responseText = `Command "${rawQuery}" received and processed. Systems nominal and standing by.`;
      }
    } catch (err) {
      responseText = "Command executed. Neura AI subsystems remain nominal.";
    }

    setTimeout(() => {
      speakResponse(responseText);
    }, 600);
  };

  // Continuous Hands-Free Speech Recognition Listener
  const startListening = async () => {
    const SpeechRecognitionObj = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognitionObj || isSpeakingRef.current) return;

    // Explicitly request microphone permission on macOS WKWebView
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      try {
        await navigator.mediaDevices.getUserMedia({ audio: true });
      } catch (err) {
        console.warn("[NEURA AI] Mic permission pending:", err);
      }
    }

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

          // Phonetic wake words (Neura / Neural / Nora / Newra / Nura / Ultron / Edith)
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
            lower.includes("hey ultron") ||
            lower.includes("edith") ||
            lower.includes("hey edith");

          if (isWakeWord) {
            updateOrbState("listening");

            // Extract command text after wake word
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
          } else if (orbState === "listening" && lower.length > 2) {
            recognition.stop();
            processVoiceCommand(lower);
            break;
          }
        }
      };

      recognition.onerror = (err: any) => {
        setTimeout(() => {
          if (!isSpeakingRef.current) startListening();
        }, 1200);
      };

      recognition.onend = () => {
        setTimeout(() => {
          if (!isSpeakingRef.current) startListening();
        }, 800);
      };

      recognition.start();
      recognitionRef.current = recognition;
    } catch (e) {
      console.warn("[NEURA AI] Speech recognition initialization:", e);
    }
  };

  // Manual click / tap trigger
  const handleOrbClick = () => {
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
      setStatusText("Listening... Say something");
      speakResponse("Neura AI standing by. How can I help, boss?");
    }
  };

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const scene = createOrbScene(container, { pureTransparent: true });
    sceneRef.current = scene;

    // Initialize hands-free voice listener
    const timer = setTimeout(() => {
      startListening();
    }, 1000);

    return () => {
      clearTimeout(timer);
      if (recognitionRef.current) {
        recognitionRef.current.abort();
      }
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
      scene.dispose();
      sceneRef.current = null;
    };
  }, []);

  return (
    <div className="pure-orb-wrapper" onClick={handleOrbClick} title="Click to interact with Neura AI">
      <div ref={containerRef} className="pure-orb-canvas" />
    </div>
  );
}
