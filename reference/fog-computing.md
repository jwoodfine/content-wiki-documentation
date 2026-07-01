---
schema: foundry-doc-v1
title: "Fog Computing"
slug: fog-computing
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
short_description: "A distributed computing architecture that places computation, storage, and network services at an intermediate layer between edge devices and centralized cloud data centers — reducing latency and backbone bandwidth requirements for IoT and real-time applications, defined by Cisco in 2012 and standardized through IEEE 1934-2018 via the OpenFog Consortium."
paired_with: fog-computing.es.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - f345f8ea5a699dc244b42a4e8493130ca319a151a5e2a82166115364b99fbda4
thesis_alignment: "Fog computing defines the intermediate distributed computing layer between IoT edge devices and cloud data centers — understanding its architecture is foundational to reasoning about latency, bandwidth, and deployment topology for distributed platform services."
keynote: false
---

Fog computing — also called fog networking or fogging — is a distributed computing architecture that uses edge devices to carry out a substantial amount of computation, storage, and communication locally, with data routed over the internet backbone only when required. The term was coined by Cisco in 2012 to describe an approach to distributed computing that addresses the limitations of cloud computing for real-time, latency-sensitive, and bandwidth-constrained IoT applications.

The "fog" metaphor refers to cloud-like properties brought closer to the "ground" — to IoT and edge devices that generate data. Where cloud computing centralizes processing in remote data centers, fog computing distributes it to computing units co-located with data-generating devices, so that processed rather than raw data is forwarded upstream and bandwidth requirements are reduced.

## Concept

The fog computing paradigm emerged from a specific problem: the proliferation of Internet of Things devices generating voluminous sensor data that, if forwarded entirely to cloud data centers for processing, would exceed available backbone bandwidth and introduce latency incompatible with real-time applications. The approach behind fog computing is to perform as much processing as possible using computing units co-located with the data-generating devices, so that the data reaching the backbone is already processed and the round-trip latency between sensor input and action is minimized.

An additional advantage is that processed data is most likely needed by the same devices that generated it: by processing locally rather than remotely, the latency between input and response is minimized without requiring any change in the cloud architecture. The idea itself is not new — in non-cloud scenarios, special-purpose hardware (signal-processing chips performing Fast Fourier Transforms) has long been used to reduce latency and CPU burden. Fog computing extends this principle to programmable, networked computing infrastructure.

Fog computing is characterized by: proximity to end users; dense geographical distribution; context-awareness regarding computational and IoT resources; latency reduction and backbone bandwidth savings; and redundancy in case of failure. It also enables edge analytics and stream mining, which cloud-based analytics cannot perform at the required latency. Fog nodes can provide security for resource-constrained IoT devices by performing cryptographic computations that the devices themselves cannot execute.

## Architecture

A fog computing architecture consists of a control plane and a data plane. On the data plane, fog computing enables computing services to reside at the edge of the network as opposed to servers in a data center. Fog nodes — intermediate computing units between edge devices and the cloud — receive data from edge devices, process it locally, and forward only the relevant results or aggregated summaries to the cloud.

The NIST Special Publication 500-325 (March 2018) formally defines fog computing as "a horizontal, physical or virtual resource paradigm that resides between smart end-devices and traditional cloud computing or data center" and states that this paradigm "supports vertically-isolated, latency-sensitive applications by providing ubiquitous, scalable, layered, federated, distributed computing, storage, and network connectivity."

NIST further distinguishes fog computing from edge computing: in the theoretical model, fog computing nodes are physically and functionally operative between edge nodes and centralized cloud. "Fog computing is most distinguished by distance from the edge." For smaller deployments, fog and edge computing are often used interchangeably; for large-scale smart city deployments, fog computing is a distinct intermediate layer.

## Comparison with cloud and edge computing

Both cloud computing and fog computing provide storage, applications, and data to end users. Fog computing is closer to end users than cloud computing and provides wider geographical distribution. Fog computing implies distribution of communication, computation, storage resources, and services on or close to devices and systems in the control of end users.

Fog computing is a medium-weight, intermediate level of computing power. Rather than a substitute for cloud computing, fog computing serves as a complement — offloading latency-sensitive or bandwidth-intensive processing locally while relying on cloud infrastructure for storage, analytics, and non-time-critical processing. Fog computing is more energy-efficient than cloud computing when aggregated over large IoT deployments, because the elimination of unnecessary data transit reduces both bandwidth costs and the energy consumed by data center processing of irrelevant raw data.

## History and standards

The term "fog computing" was first developed by Cisco in 2012. On 19 November 2015, Cisco Systems, ARM Holdings, Dell, Intel, Microsoft, and Princeton University founded the OpenFog Consortium to promote the development and adoption of fog computing. The IEEE adopted fog computing standards proposed by the OpenFog Consortium; the primary standard is IEEE 1934-2018.

The IoT use cases supported by fog computing include connected vehicles, wearable health monitoring devices, augmented reality, and smart drone swarms. The US Navy's Space and Naval Warfare Systems Command (SPAWAR) has prototyped scalable, secure Disruption Tolerant Mesh Network implementations using fog computing architecture to protect strategic military assets including stationary and mobile IoT systems.

ISO/IEC 20248 provides a method whereby data from objects identified by edge computing using Automated Identification Data Carriers (AIDC) — barcodes and RFID tags — can be read, interpreted, verified, and made available into the fog and on the edge even when the AIDC tag has moved on.

---

*cites: [[edge-computing]], [[application-programming-interface]], [[computer-appliance]], [[virtual-appliance]]*
