<p align="center">
  <a href="https://somansh.in">
    <img src="./assets/hero.svg" alt="Somansh Goel. Builds software that ships, then finds out how AI systems break. A star-trail sky over Himalayan foothills, observed from Dehradun." width="100%">
  </a>
</p>

<p align="center">
  <img src="./assets/about.svg" alt="Observer's note. I'm a final-year B.Tech CSE (AI &amp; ML) student at UPES, Dehradun, graduating in 2027. I build web and desktop software end to end, and I spend the rest of my time finding out how AI systems fail." width="100%">
</p>

<p align="center">
  <a href="https://somansh.in"><img src="./assets/link-portfolio.svg" alt="Portfolio: somansh.in" height="34"></a>&nbsp;&nbsp;
  <a href="https://linkedin.com/in/somansh1"><img src="./assets/link-linkedin.svg" alt="LinkedIn" height="34"></a>&nbsp;&nbsp;
  <a href="mailto:somansh@somansh.in"><img src="./assets/link-email.svg" alt="Email: somansh@somansh.in" height="34"></a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/heading-commits-dark.svg">
    <img src="./assets/heading-commits-light.svg" alt="A year of commits, charted" width="100%">
  </picture>
</p>

<p align="center">
  <img src="./assets/sky.svg" alt="A polar star chart of the last 53 weeks of GitHub activity. Each day with commits is a star, the busiest days carry diffraction spikes, and the numbers beside it give the totals and streaks." width="100%">
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/heading-catalogue-dark.svg">
    <img src="./assets/heading-catalogue-light.svg" alt="Catalogue. Six objects, each one shipped. Click a plate to open it." width="100%">
  </picture>
</p>

<p align="center">
  <a href="https://chatlens.somansh.in/?demo"><img src="./assets/plate-chatlens.svg" alt="SG 01, ChatLens. Chat analytics that never leave your browser." width="49.5%"></a>
  <a href="https://socialspace.somansh.in"><img src="./assets/plate-socialspace.svg" alt="SG 02, SocialSpace. A table for two: chat, calls, a shared canvas and watch-together." width="49.5%"></a>
</p>
<p align="center">
  <a href="https://github.com/Somansh1/gemvtuber"><img src="./assets/plate-gem-vtuber.svg" alt="SG 03, Gem-VTuber. A desktop Live2D companion that talks through the Gemini Live API." width="49.5%"></a>
  <a href="https://github.com/Somansh1/SRE-RL-Env"><img src="./assets/plate-sre-autopilot.svg" alt="SG 04, SRE Autopilot. An incident-response environment with seven microservices and a hidden root cause." width="49.5%"></a>
</p>
<p align="center">
  <a href="https://github.com/Somansh1/cnn-backend"><img src="./assets/plate-appd-lite-net.svg" alt="SG 05, AppD-Lite-Net. Apple leaf disease detection with a sub-million-parameter CNN." width="49.5%"></a>
  <a href="https://fouressbath.com"><img src="./assets/plate-fouress-bath.svg" alt="SG 06, Fouress Bath. The live catalogue site for a sanitaryware retailer." width="49.5%"></a>
</p>

<details>
<summary>Catalogue as text</summary>

| Project | What it is | Built with |
|---|---|---|
| **[ChatLens](https://chatlens.somansh.in/?demo)** | Chat analytics that never leaves your browser. Parses WhatsApp, Instagram and Messenger exports and charts who texts more, when, and what. A Content-Security-Policy blocks every outgoing request, so the privacy claim is enforced, not promised. [Source](https://github.com/Somansh1/ChatLens) | Next.js, TypeScript, hand-written SVG charts |
| **[SocialSpace](https://socialspace.somansh.in)** | A table for two. Chat, peer-to-peer calls, a shared canvas and watch-together between two people, over a small WebSocket relay and WebRTC. [Source](https://github.com/Somansh1/socialspace) | Next.js, WebSocket, WebRTC, Node.js |
| **[Gem-VTuber](https://github.com/Somansh1/gemvtuber)** | A desktop companion. A transparent always-on-top window renders a Live2D avatar that talks through the Gemini Live API; the model's tool calls drive its expressions and its lips follow the audio. | Electron, PixiJS, Live2D, WebSocket |
| **[SRE Autopilot](https://github.com/Somansh1/SRE-RL-Env)** | An RL-style environment for incident response. Seven microservices in a dependency graph, a hidden root cause, noisy telemetry, and an SLA-based reward for whichever agent is on call. | Python, FastAPI, OpenEnv, Docker |
| **[AppD-Lite-Net](https://github.com/Somansh1/cnn-backend)** | Apple leaf disease detection with a CNN under one million parameters: 99.53% on a held-out test set and 98.80% in 5-fold cross-validation. Co-first author of the manuscript. [Frontend](https://github.com/Somansh1/cnn-frontend) | TensorFlow/Keras, FastAPI, React |
| **[Fouress Bath](https://fouressbath.com)** | The live catalogue site for a plumbing and sanitaryware retailer, with structured data and technical SEO done properly. | Next.js, Tailwind CSS |

</details>

<p align="center">
  <img src="./assets/fieldnotes.svg" alt="Field notes: how assistants leak. A system prompt drawn as redaction bars while a scan line recovers the text beneath, with two 2025 security research entries." width="100%">
</p>

<details>
<summary>Security research as text</summary>

- **Red-team audit of a production AI assistant (2025).** Recovered the assistant's full system prompt through a chain of persona jailbreak, metadata probing and chunked extraction, then reported five findings to the vendor with a proposed hardened prompt design.
- **Prompt-extraction comparison across six consumer assistants (2025).** Ran one family of extraction prompts against Gemini, ChatGPT, Grok, Perplexity, Meta AI and Claude: three returned instruction-like text, two refused, one returned nothing.

</details>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/heading-logbook-dark.svg">
    <img src="./assets/heading-logbook-light.svg" alt="Logbook" width="100%">
  </picture>
</p>

<p align="center">
  <img src="./assets/logbook.svg" alt="Logbook. June to August 2025: AI/ML and Software Engineering Intern at Bharat Electronics Limited. Built a FAISS-backed retrieval pipeline on Llama 3.2 Vision over 100+ page internal documents, taking lookups for 50+ staff from hours to under 10 seconds. Scripted RHEL 9 environment setup, cutting per-machine provisioning from 3 hours to 15 minutes. Shipped a one-click installer so non-technical staff could set the system up on-prem. March 2026 to present: Secretary, IEEE Computer Society (UPES)." width="100%">
</p>

<details>
<summary>Experience as text</summary>

**AI/ML & Software Engineering Intern, Bharat Electronics Limited** · Jun to Aug 2025

- Built a FAISS-backed retrieval pipeline on Llama 3.2 Vision over 100+ page internal documents, taking lookups for 50+ staff from hours to under 10 seconds.
- Scripted RHEL 9 environment setup, cutting per-machine provisioning from 3 hours to 15 minutes.
- Shipped a one-click installer so non-technical staff could set the system up on-prem.

**Secretary, IEEE Computer Society (UPES)** · Mar 2026 to present

</details>

<!-- chess:start -->
<p align="center">
<picture><source media="(prefers-color-scheme: dark)" srcset="./assets/heading-your-move-dark.svg"><img src="./assets/heading-your-move-light.svg" alt="Your move. This chess board is live: click a move below, press Create on the issue that opens, and the board redraws in about a minute." width="100%"></picture>
</p>

<p align="center">
<img src="./assets/chess/board-g1-m3.svg" width="100%" alt="Chess board with the move list, game 1, move 2, black to move, last move Nf3">
</p>

<p align="left">
<img src="./assets/chess/p-b-k-e8.svg" height="30" alt="Black king on e8:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ce8e7%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Ke7.svg" height="30" alt="Play Ke7"></a><br>
<img src="./assets/chess/p-b-q-d8.svg" height="30" alt="Black queen on d8:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd8e7%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Qe7.svg" height="30" alt="Play Qe7"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd8f6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Qf6.svg" height="30" alt="Play Qf6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd8g5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Qg5.svg" height="30" alt="Play Qg5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd8h4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Qh4.svg" height="30" alt="Play Qh4"></a><br>
<img src="./assets/chess/p-b-b-f8.svg" height="30" alt="Black bishop on f8:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8a3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-a3.svg" height="30" alt="Play Ba3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8b4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-b4.svg" height="30" alt="Play Bb4"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8c5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-c5.svg" height="30" alt="Play Bc5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8d6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-d6.svg" height="30" alt="Play Bd6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8e7%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-e7.svg" height="30" alt="Play Be7"></a><br>
<img src="./assets/chess/p-b-n-b8.svg" height="30" alt="Black knight on b8:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb8a6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Na6.svg" height="30" alt="Play Na6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb8c6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Nc6.svg" height="30" alt="Play Nc6"></a><br>
<img src="./assets/chess/p-b-n-g8.svg" height="30" alt="Black knight on g8:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg8e7%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Ne7.svg" height="30" alt="Play Ne7"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg8f6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Nf6.svg" height="30" alt="Play Nf6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg8h6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Nh6.svg" height="30" alt="Play Nh6"></a><br>
<img src="./assets/chess/p-b-pawns.svg" height="30" alt="Black pawns:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ca7a5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-a5.svg" height="30" alt="Play a5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ca7a6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-a6.svg" height="30" alt="Play a6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb7b5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-b5.svg" height="30" alt="Play b5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb7b6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-b6.svg" height="30" alt="Play b6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cc7c5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-c5.svg" height="30" alt="Play c5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cc7c6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-c6.svg" height="30" alt="Play c6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd7d5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-d5.svg" height="30" alt="Play d5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd7d6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-d6.svg" height="30" alt="Play d6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf7f5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-f5.svg" height="30" alt="Play f5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf7f6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-f6.svg" height="30" alt="Play f6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg7g5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-g5.svg" height="30" alt="Play g5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg7g6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-g6.svg" height="30" alt="Play g6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ch7h5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-h5.svg" height="30" alt="Play h5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ch7h6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-h6.svg" height="30" alt="Play h6"></a><br>
</p>

<p align="center">
<img src="./assets/chess/history-0.svg" width="100%" alt="No finished chess games yet. Game 1 is in progress.">
</p>

<details><summary>Moves as text</summary>

Legal moves for black (29):

- Pawn a7: [a5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ca7a5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [a6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ca7a6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn b7: [b5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb7b5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [b6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb7b6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn c7: [c5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cc7c5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [c6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cc7c6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn d7: [d5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd7d5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [d6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd7d6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn f7: [f5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf7f5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [f6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf7f6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn g7: [g5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg7g5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [g6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg7g6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn h7: [h5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ch7h5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [h6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ch7h6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Knight b8: [Na6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb8a6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Nc6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb8c6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Knight g8: [Ne7](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg8e7%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Nf6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg8f6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Nh6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg8h6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Bishop f8: [Ba3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8a3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Bb4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8b4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Bc5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8c5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Bd6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8d6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Be7](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf8e7%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Queen d8: [Qe7](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd8e7%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Qf6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd8f6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Qg5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd8g5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Qh4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd8h4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- King e8: [Ke7](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ce8e7%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)

Recent moves:

- 1. e4 by @Somansh1
- 1... e5 by @Somansh1
- 2. Nf3 by @Somansh1

</details>
<!-- chess:end -->

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/heading-instruments-dark.svg">
    <img src="./assets/heading-instruments-light.svg" alt="Instruments" width="100%">
  </picture>
</p>

<p align="center">
  <img src="./assets/instruments.svg" alt="Instruments. Languages: Python, TypeScript / JavaScript, Java, C / C++, SQL. Web: React, Next.js, Tailwind CSS, Node.js, WebSocket, WebRTC. AI / ML: RAG pipelines, FAISS, LLM fine-tuning, PyTorch, TensorFlow, scikit-learn. Systems: Linux (RHEL), Docker, Bash, Electron, Git." width="100%">
</p>

<details>
<summary>Toolbox as text</summary>

**Languages** Python · TypeScript / JavaScript · Java · C / C++ · SQL<br>
**Web** React · Next.js · Tailwind CSS · Node.js · WebSocket · WebRTC<br>
**AI / ML** RAG pipelines · FAISS · LLM fine-tuning · PyTorch · TensorFlow · scikit-learn<br>
**Systems** Linux (RHEL) · Docker · Bash · Electron · Git

</details>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./assets/colophon-dark.svg">
    <img src="./assets/colophon-light.svg" alt="Away from the keyboard: astrophotography, chess, and games. Every image here is hand-written SVG from scripts/build.py. Star chart redrawn nightly. No third-party widgets." width="100%">
  </picture>
</p>
