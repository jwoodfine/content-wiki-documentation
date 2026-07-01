---
schema: foundry-doc-v1
title: "Application Programming Interface"
slug: application-programming-interface
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
short_description: "A defined interface that enables two or more software systems to communicate — specifying the calls or requests that can be made, how to make them, and the data formats used — with origins in 1940s British computer science, formal definition in a 1968 AFIPS paper, and contemporary dominance through REST-based web APIs that form the primary integration mechanism of the modern internet."
paired_with: application-programming-interface.es.md
tags:
  - domain:documentation
  - source:jennifer-cluster
  - batch:iteration-2
source_refs:
  - 4b97263b79ad51000cb9daf66b6f154ef8ea80cc64d9fe220be227e1699ddc99
thesis_alignment: "The API is the foundational integration primitive of distributed computing systems; understanding its definitions, history, and design principles is prerequisite to reasoning about system architecture, inter-service communication, and platform design."
keynote: false
---

An application programming interface (API) is a way for two or more computer programs to communicate with each other. It is a type of software interface that offers services to other pieces of software. A document or standard that describes how to build or use such a connection is called an API specification; a computer system that meets the standard is said to implement or expose an API. The term may refer either to the specification or to the implementation.

An API is distinguished from a user interface by its intended consumer: a user interface connects the human user to the system; an API connects software programs to each other. An API is not intended to be used directly by a person but by a programmer who is incorporating it into a larger piece of software. The calls that make up an API are known as subroutines, methods, requests, or endpoints, depending on the architectural style; an API specification defines these calls — it explains how to use or implement them. One purpose of APIs is to hide the internal details of how a system works while exposing only those parts that a programmer will find useful, keeping them consistent even if the internal details change later.

## History

**1940s–1950s.** The conceptual foundation of the API was established by British computer scientists Maurice Wilkes and David Wheeler in their work developing a modular software library for EDSAC, an early computer, in the 1940s. The subroutines in this library were stored on punched paper tape organized in a filing cabinet, accompanied by what Wilkes and Wheeler called a "library catalog" of notes about each subroutine and how to incorporate it into a program — which would today be called an API or API documentation. Their 1951 book *The Preparation of Programs for an Electronic Digital Computer* contains the first published API specification. Joshua Bloch has argued that Wilkes and Wheeler "latently invented" the API because it is more a concept that is discovered than invented.

**1960s–1970s.** The term "application program interface" (without the *-ing* suffix) first appeared in a 1968 paper titled *Data structures and techniques for remote computer graphics*, presented at an Association for Information Processing Societies (AFIPS) conference. The authors used the term to describe a set of Fortran subroutine calls intended to free programmers from dealing with the idiosyncrasies of graphics display devices and to provide hardware independence if the computer or display were replaced. The term was introduced to the field of databases by C.J. Date in a 1974 paper; it became part of the ANSI/SPARC framework for database management systems. Database professionals in the 1970s observed that different database interfaces could be combined: a sufficiently rich application interface could support query interfaces, report interfaces, and other interfaces as well.

**1990s.** By 1990, the API was defined by technologist Carl Malamud simply as "a set of services available to a programmer for performing certain tasks." The concept was expanded by the rise of remote procedure calls and web APIs. As computer networks became common, programmers wanted to call libraries not only on local computers but on computers elsewhere. In the 1990s, with the spread of the internet, standards including CORBA, COM, and DCOM competed to become the dominant mechanism for exposing API services across networks.

**2000s to present.** Roy Fielding's 2000 dissertation at UC Irvine defined Representational State Transfer (REST) and described the idea of a "network-based Application Programming Interface" that Fielding contrasted with traditional "library-based" APIs. XML and JSON web APIs saw widespread commercial adoption beginning in 2000. The web API is now the most common meaning of the term API, and the term has become broad enough to describe much of the communication on the internet. Tim Berners-Lee's 2001 proposal for the Semantic Web included "semantic APIs" recasting the API as an open distributed data interface. The recent proliferation of microservices architectures — in which applications are decomposed into small, loosely coupled services accessed through public APIs — has made API design central to enterprise software architecture.

## Types

**Library APIs.** The interface to a software library is one type of API. The API describes and prescribes the "expected behavior" (specification) while the library is an "actual implementation" of this set of rules. A single API can have multiple implementations — different libraries that share the same programming interface. The separation of the API from its implementation can allow programs written in one language to use a library written in another; Scala and Java, for example, both compile to compatible bytecode, enabling Scala programs to use Java APIs.

**Operating system APIs.** An API can specify the interface between an application and the operating system. POSIX, for example, provides a set of common API specifications designed to enable applications written for one POSIX-conformant OS to be compiled for another. Linux and the Berkeley Software Distribution (BSD) both implement the POSIX APIs. An API differs from an application binary interface (ABI) in that an API is source-code-based while an ABI is binary-based.

**Remote APIs.** Remote APIs allow developers to manipulate remote resources through protocols — specific standards for communication that allow different technologies to work together regardless of language or platform. The Java Database Connectivity API, for example, allows developers to query many types of databases using the same set of functions. Remote APIs are useful for maintaining object abstraction in object-oriented programming: a method call executed locally on a proxy object invokes the corresponding method on the remote object and returns the result.

**Web APIs.** Web APIs are services accessed from client devices (mobile phones, laptops) to a web server using the Hypertext Transfer Protocol (HTTP). Client devices send a request in the form of an HTTP request and receive a response message typically in JSON or XML format. Web APIs allow the combination of multiple APIs into new applications known as mashups. The recent trend in web API design has moved away from SOAP-based web services and service-oriented architecture toward REST-style web resources and resource-oriented architecture.

## Design considerations

**Synchronous versus asynchronous.** A synchronous API call blocks the call site while waiting for the called code to finish. An asynchronous API call does not block the call site; the calling thread is notified when the reply arrives. The choice between these patterns has significant implications for application responsiveness and resource utilisation.

**Release policies.** APIs are typically classified by their access policy: *Private* APIs are for internal company use only; *Partner* APIs are available only to specific business partners under contractual agreement; *Public* APIs are available for use by the general public, subject to authentication and rate limits.

**Security.** Common threats to public-facing APIs include SQL injection, denial-of-service attacks, broken authentication, and exposure of sensitive data. Security practices include HTTPS for connection security, content security to mitigate data injection attacks, and API keys to authenticate and authorise requests.

---

*cites: [[user-interface-design]], [[user-experience-design]], [[fog-computing]], [[edge-computing]]*
