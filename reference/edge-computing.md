---
schema: foundry-doc-v1
title: "Edge Computing"
slug: edge-computing
category: reference
type: topic
content_type: topic
quality: complete
status: active
audience: customer-woodfine
bcsc_class: current-fact
language_protocol: PROSE-TOPIC
last_edited: 2026-06-30
editor: woodfine-editorial
short_description: "A distributed computing paradigm that brings computation and data storage closer to the sources of data — reducing response times and saving bandwidth by performing processing at network edge nodes near the data-generating devices rather than in centralized cloud data centers — with origins in late-1990s content distribution networks and applications ranging from IoT to autonomous vehicles to edge artificial intelligence."
paired_with: edge-computing.es.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - fb6311089e5a0200771a827bd28ebdf0cd293cbc3ac5e50321fb7efec93dc0ed
thesis_alignment: "Edge computing defines the distributed architecture that moves processing from centralized data centers to the network perimeter, directly relevant to platform deployment topology, IoT system design, and latency-sensitive service delivery."
keynote: false
---

Edge computing is a distributed computing paradigm that brings computation and data storage closer to the sources of data. The primary motivations are improved response times and reduced bandwidth consumption: by performing processing at nodes near the data-generating devices rather than in centralized cloud data centers, edge computing reduces the round-trip latency between input and response and eliminates the need to transmit raw data across wide-area networks.

Edge computing is an architecture rather than a specific technology. It is a topology- and location-sensitive form of distributed computing — the key attribute is physical proximity to data sources, not any particular implementation. A well-designed edge platform would significantly outperform a traditional cloud-based system for applications with strict latency requirements or high bandwidth costs.

## Origins

The origins of edge computing lie in content distribution networks (CDNs) created in the late 1990s to serve web and video content from edge servers deployed close to users, reducing the latency of delivering content from origin servers. In the early 2000s, these networks evolved to host applications and application components on edge servers, resulting in the first commercial edge computing services that hosted applications such as dealer locators, shopping carts, real-time data aggregators, and ad insertion engines.

Internet of Things (IoT) systems are a major contemporary driver of edge computing. A common misconception is that edge computing and IoT are synonymous; edge computing is the broader paradigm and IoT is one application of it.

One widely cited definition, proposed by Karim Arabi at an IEEE DAC 2014 Keynote and developed further at an MIT MTL Seminar in 2015, defines edge computing broadly as "all computing outside the cloud happening at the edge of the network, and more specifically in applications where real-time processing of data is required." Because edge computing nodes do not have the climate-controlled advantages of data centers despite requiring substantial processing power, edge computing system design must account for thermal management, physical security, and power reliability constraints not present in centralized facilities.

## Concept and data volumes

The commercial motivation for edge computing rests on projections about data volume growth. The world's data is expected to grow 61 percent to 175 zettabytes by 2025 (IDC). According to research firm Gartner, approximately 10 percent of enterprise-generated data was created and processed outside a traditional centralized data center or cloud as of the time of the estimate; Gartner projected that this figure would reach 75 percent by 2025. The increase of IoT devices at the edge of the network is producing a massive amount of data: storing and using all of that data in cloud data centers pushes network bandwidth requirements to the limit. Despite improvements in network technology, data centers cannot guarantee acceptable transfer rates and response times, which is often a critical requirement for many applications.

The aim of edge computing is to move computation away from data centers toward the edge of the network, exploiting smart objects, mobile phones, and network gateways to perform tasks and provide services on behalf of the cloud. By moving services to the edge, it becomes possible to provide content caching, service delivery, persistent data storage, and IoT management, resulting in better response times and transfer rates.

## Properties

**Privacy and security.** The distributed nature of edge computing introduces a shift in security schemes. Data travelling between distributed nodes requires encryption mechanisms independent of cloud security models. Edge nodes are often resource-constrained devices, limiting the choice of security methods. A shift from centralized top-down infrastructure to a decentralized trust model is required. On the other hand, by keeping and processing data at the edge, it is possible to increase privacy by minimizing the transmission of sensitive information to the cloud, and data ownership shifts from service providers to end users.

**Scalability.** Distributed edge systems must accommodate heterogeneous devices with different performance and energy constraints, highly dynamic conditions, and variable connection reliability compared to the more robust infrastructure of cloud data centers.

**Reliability.** Management of failovers is crucial to maintaining service continuity. Edge computing devices must maintain awareness of the network topology of the overall distributed system, enabling detection and recovery from node failures.

**Speed.** Edge computing brings analytical resources close to end users, increasing responsiveness and throughput. Applications relying on short response times — IoT systems, autonomous driving, health and public safety applications, facial recognition (which takes a human 370–620 ms to perform) — benefit substantially from edge processing. Edge AI implements artificial intelligence at the edge, close to where data is collected, enabling human-perception-speed responses in applications such as augmented reality.

**Efficiency.** By using servers on a local edge network to perform computationally intensive processing, data need only be transmitted across the local network; avoiding internet transmission results in significant bandwidth savings. Voice recognition is a representative example: performing recognition locally makes it possible to send the recognized text to the cloud rather than raw audio recordings, reducing bandwidth by orders of magnitude.

## Applications

Edge application services reduce the volumes of data that must be moved, the consequent traffic, and the distance data must travel. Applications include:

- **IoT device management** — real-time data collection and control without cloud round-trip latency
- **Autonomous vehicles and connected cars** — latency requirements incompatible with cloud processing
- **Smart cities and Industry 4.0** — distributed sensor networks with real-time analytics requirements
- **Cloud gaming / pixel streaming** — game logic in cloud, rendered video transmitted to lightweight clients on mobile phones or VR glasses
- **Home automation** — local control without internet dependency
- **Edge artificial intelligence (Edge AI)** — AI inference at the edge rather than in centralized data centers, enabling real-time decision-making

Research using cloudlets — resource-rich machines near mobile users that offer services typically found in the cloud — demonstrated improvements in execution time when tasks are offloaded to edge nodes. The feasibility of offloading varies by workload: offloading every task may result in slowdown due to transfer times between device and nodes; optimal configurations balance local processing against network transmission cost.

---

*cites: [[fog-computing]], [[application-programming-interface]], [[computer-appliance]]*
