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
<img src="./assets/chess-board.svg" width="100%" alt="Chess board with the move list, game 1, move 2, white to move, last move e5">
</p>

<p align="left">
<img src="./assets/chess/p-w-k-e1.svg" height="30" alt="White king on e1:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ce1e2%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Ke2.svg" height="30" alt="Play Ke2"></a><br>
<img src="./assets/chess/p-w-q-d1.svg" height="30" alt="White queen on d1:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd1e2%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Qe2.svg" height="30" alt="Play Qe2"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd1f3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Qf3.svg" height="30" alt="Play Qf3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd1g4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Qg4.svg" height="30" alt="Play Qg4"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd1h5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Qh5.svg" height="30" alt="Play Qh5"></a><br>
<img src="./assets/chess/p-w-b-f1.svg" height="30" alt="White bishop on f1:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1a6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-a6.svg" height="30" alt="Play Ba6"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1b5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-b5.svg" height="30" alt="Play Bb5"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1c4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-c4.svg" height="30" alt="Play Bc4"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1d3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-d3.svg" height="30" alt="Play Bd3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1e2%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-B-e2.svg" height="30" alt="Play Be2"></a><br>
<img src="./assets/chess/p-w-n-b1.svg" height="30" alt="White knight on b1:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb1a3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Na3.svg" height="30" alt="Play Na3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb1c3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Nc3.svg" height="30" alt="Play Nc3"></a><br>
<img src="./assets/chess/p-w-n-g1.svg" height="30" alt="White knight on g1:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg1e2%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Ne2.svg" height="30" alt="Play Ne2"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg1f3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Nf3.svg" height="30" alt="Play Nf3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg1h3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-Nh3.svg" height="30" alt="Play Nh3"></a><br>
<img src="./assets/chess/p-w-pawns.svg" height="30" alt="White pawns:"> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ca2a3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-a3.svg" height="30" alt="Play a3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ca2a4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-a4.svg" height="30" alt="Play a4"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb2b3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-b3.svg" height="30" alt="Play b3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb2b4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-b4.svg" height="30" alt="Play b4"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cc2c3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-c3.svg" height="30" alt="Play c3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cc2c4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-c4.svg" height="30" alt="Play c4"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd2d3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-d3.svg" height="30" alt="Play d3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd2d4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-d4.svg" height="30" alt="Play d4"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf2f3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-f3.svg" height="30" alt="Play f3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf2f4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-f4.svg" height="30" alt="Play f4"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg2g3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-g3.svg" height="30" alt="Play g3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg2g4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-g4.svg" height="30" alt="Play g4"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ch2h3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-h3.svg" height="30" alt="Play h3"></a> <a href="https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ch2h4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute."><img src="./assets/chess/m-h4.svg" height="30" alt="Play h4"></a><br>
</p>

<p align="center">
<img src="./assets/chess-history.svg" width="100%" alt="No finished chess games yet. Game 1 is in progress.">
</p>

<details><summary>Moves as text</summary>

Legal moves for white (29):

- Pawn a2: [a3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ca2a3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [a4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ca2a4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn b2: [b3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb2b3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [b4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb2b4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn c2: [c3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cc2c3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [c4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cc2c4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn d2: [d3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd2d3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [d4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd2d4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn f2: [f3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf2f3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [f4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf2f4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn g2: [g3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg2g3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [g4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg2g4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Pawn h2: [h3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ch2h3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [h4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ch2h4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Knight b1: [Na3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb1a3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Nc3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cb1c3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Knight g1: [Ne2](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg1e2%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Nf3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg1f3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Nh3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cg1h3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Bishop f1: [Ba6](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1a6%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Bb5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1b5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Bc4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1c4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Bd3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1d3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Be2](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cf1e2%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- Queen d1: [Qe2](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd1e2%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Qf3](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd1f3%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Qg4](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd1g4%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.) [Qh5](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Cd1h5%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)
- King e1: [Ke2](https://github.com/Somansh1/Somansh1/issues/new?title=chess%7Cmove%7Ce1e2%7C1&body=Just+press+%22Create%22.+The+board+updates+in+about+a+minute.)

Recent moves:

- 1. e4 by @Somansh1
- 1... e5 by @Somansh1

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
