# Design Document

## Design principles

* Autonomous and decentralized system
* Scalable system
* Open ecosystem
* Exntensibility

## Requirements

* Portable message storage like an IMAP mailbox
* Secure messaging between sender and receiver (end-to-end encryption / delivery acknowledgement)
* Provider-independent ID / address
* Separation of human-friendly ID and other IDs (elimination of semantics from non-human-friendly IDs)
* Secret recipient ID / address to unauthorized users (via mutually-authenticated ID)
* Verification of the sender of a message
* Anonymous messaging
* 1-to-1 private messaging
* 1-to-N messaging
* Message thread support (e.g., `In-Reply-To` in E-mail header)
* Synchronous/Asynchronous messaging support

## Identifier

It may be easy to use public key information such as fingerprints to generate an identifier (ID).
However, it depends on algorithms and does not guarantee future safety and extensions.
Therefore, we separate ID generation and public-key cryptosystem algorithm.

ref. Decentralized Identifiers, Self-soverign identity

### Flat ID space


