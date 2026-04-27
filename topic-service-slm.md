topic_id: SERVICE-SLM-01
title: service-slm: Linguistic Air-Lock
tier: Tier-5-Service
category: Service-Logic
tags: [slm, router, ai-extraction, totebox-orchestration]
abstract: |
  A headless bridging environment utilizing the SLM router (Rust) to apply Small Language Models (SLMs) to unstructured data, ensuring strict noise reduction before entering the self-healing knowledge graph.
details:
  human_narrative: |
    This service acts as the air-lock for human communication. It takes the messy text from emails or PDFs and uses a sub-billion parameter AI model to extract only the verifiable facts, formatting them cleanly into Markdown before permanently shutting the AI down.
links: [TOTEBOX-01, SYS-ADR-07, SERVICE-CONTENT-01]
