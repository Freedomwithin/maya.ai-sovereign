const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const P = { 
    bg: '08080F', 
    surface: '11111E', 
    border: '1E1E40', 
    blue: '6366F1', 
    green: '10B981',
    glow: 'A5B4FF', 
    text: 'FFFFFF', 
    muted: '94A3B8',
    cyan: '22D3EE',
    red: 'F97373'
};

async function createDeck() {
    let pres = new pptxgen();
    pres.author = 'Maya & Jonathon';
    pres.company = 'TrustChain Sovereign';
    pres.title = 'TrustChain Sovereign Showcase V4.1';
    pres.layout = 'LAYOUT_16x9';

    // SLIDE 1: THE HOOK
    let s1 = pres.addSlide();
    s1.background = { color: P.bg };
    s1.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.4, w: 9, h: 0.05, fill: { color: P.blue } });
    s1.addText('TRUSTCHAIN SOVEREIGN // V4.1', { x: 0.5, y: 0.6, w: 9, h: 0.5, fontSize: 14, color: P.blue, bold: true, charSpacing: 2 });
    s1.addText('The Behavioral Immune System for Solana.', { x: 0.5, y: 1.2, w: 9, h: 1.2, fontSize: 44, bold: true, color: P.text, fontFace: 'Arial' });
    
    // The Fire Analogy Card
    s1.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.8, w: 9, h: 2.0, fill: { color: P.surface }, line: { color: P.blue, width: 1 } });
    s1.addText('CURRENT SECURITY: THE FIRE INVESTIGATOR', { x: 0.8, y: 3.1, w: 4, h: 0.3, fontSize: 12, color: P.red, bold: true });
    s1.addText('Audits tell you how your house burned down after the treasury is empty. They check the code, but the theft happens in the conduct.', { x: 0.8, y: 3.5, w: 3.8, h: 1.2, fontSize: 14, color: P.muted, valign: 'top' });
    
    s1.addText('TRUSTCHAIN: THE FIRE PREVENTION', { x: 5.2, y: 3.1, w: 4, h: 0.3, fontSize: 12, color: P.green, bold: true });
    s1.addText('We are the automated sensors and sprinklers. We detect the heat and block the oxygen before the first flame touches your capital.', { x: 5.2, y: 3.5, w: 3.8, h: 1.2, fontSize: 14, color: P.text, valign: 'top' });

    // SLIDE 2: MACRO-ECONOMIC FORENSICS
    let s2 = pres.addSlide();
    s2.background = { color: P.bg };
    s2.addText('02 // THE BOT-DRAIN DETECTOR', { x: 0.5, y: 0.6, w: 9, h: 0.5, fontSize: 18, color: P.blue, bold: true });
    s2.addText('Stopping Wealth Extraction with DOJ-Grade Math.', { x: 0.5, y: 1.1, w: 9, h: 0.8, fontSize: 32, bold: true, color: P.text });

    s2.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.2, w: 4.4, h: 2.5, fill: { color: P.surface }, line: { color: P.cyan, width: 1 } });
    s2.addText('THE GINI COEFFICIENT', { x: 0.7, y: 2.4, w: 4, h: 0.3, fontSize: 12, color: P.cyan, bold: true });
    s2.addText('Detects "Monopoly" risk. We use it to find the exact moment one actor starts draining a liquidity pool.', { x: 0.7, y: 2.8, w: 4, h: 1.5, fontSize: 14, color: P.text, valign: 'top' });

    s2.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 2.2, w: 4.4, h: 2.5, fill: { color: P.surface }, line: { color: P.cyan, width: 1 } });
    s2.addText('HHI CONCENTRATION INDEX', { x: 5.3, y: 2.4, w: 4, h: 0.3, fontSize: 12, color: P.cyan, bold: true });
    s2.addText('Used by the US Department of Justice to find market dominance. We use it to unmask coordinated bot swarms acting as one.', { x: 5.3, y: 2.8, w: 4, h: 1.5, fontSize: 14, color: P.text, valign: 'top' });

    // SLIDE 3: SYBIL TRAP
    let s3 = pres.addSlide();
    s3.background = { color: P.bg };
    s3.addText('03 // SYBIL TRAP & ENTROPY', { x: 0.5, y: 0.6, w: 9, h: 0.5, fontSize: 18, color: P.blue, bold: true });
    s3.addText('Humans are messy. Bots are machines.', { x: 0.5, y: 1.1, w: 9, h: 0.8, fontSize: 32, bold: true, color: P.text });
    
    s3.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.2, w: 4.4, h: 2.8, fill: { color: P.surface } });
    s3.addText('THE ORGANIC WHALE', { x: 0.7, y: 2.4, w: 4, h: 0.3, fontSize: 14, color: P.green, bold: true });
    s3.addText('High Entropy.\nUnpredictable timing.\nNatural capital movement.', { x: 0.7, y: 2.9, w: 4, h: 1.5, fontSize: 16, color: P.text, valign: 'top', bullet: true });

    s3.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 2.2, w: 4.4, h: 2.8, fill: { color: P.surface } });
    s3.addText('THE BOT SWARM', { x: 5.3, y: 2.4, w: 4, h: 0.3, fontSize: 14, color: P.red, bold: true });
    s3.addText('Machine Synchrony.\nMillisecond precision.\n100 accounts acting in a 3s window.', { x: 5.3, y: 2.9, w: 4, h: 1.5, fontSize: 16, color: P.text, valign: 'top', bullet: true });

    // SLIDE 4: THE REPUTATION ECONOMY (ENHANCED)
    let s4 = pres.addSlide();
    s4.background = { color: P.bg };
    s4.addText('04 // THE REPUTATION ECONOMY', { x: 0.5, y: 0.6, w: 9, h: 0.5, fontSize: 18, color: P.blue, bold: true });
    s4.addText('Incentivized Inclusion, Not Just Blocking.', { x: 0.5, y: 1.1, w: 9, h: 0.8, fontSize: 32, bold: true, color: P.text });
    
    s4.addText('We don\'t use crude "ban-lists". We adjust weighted participation (multipliers) in real-time based on Behavioral DNA. This creates a "Governance Gravity" that rewards humans and de-prioritizes mechanical extraction.', { x: 0.5, y: 1.8, w: 9, h: 0.5, fontSize: 14, color: P.muted, italic: true });

    const tiers = [
        { name: 'STEWARD', mult: '1.2x', desc: 'Elite Citizens.\nIncentivized Yield.\nMax voting weight.' },
        { name: 'RESIDENT', mult: '1.0x', desc: 'Verified Humans.\nFull protocol access.\nStandard weighting.' },
        { name: 'PROBATIONARY', mult: '0.5x', desc: 'New Entities.\nReduced weight.\nGradual trust ramp.' },
        { name: 'RESTRICTED', mult: '0.1x', desc: 'Bot Signatures.\nMinimal weight.\nPhysically blocked from institutional vaults.' }
    ];

    tiers.forEach((tier, i) => {
        let x = 0.5 + (i * 2.3);
        s4.addShape(pres.shapes.RECTANGLE, { x: x, y: 2.5, w: 2.1, h: 2.8, fill: { color: P.surface }, line: { color: P.blue, width: 1 } });
        s4.addText(tier.name, { x: x + 0.1, y: 2.7, w: 1.9, h: 0.3, fontSize: 12, bold: true, color: P.cyan, align: 'center' });
        s4.addText(tier.mult, { x: x + 0.1, y: 3.1, w: 1.9, h: 0.5, fontSize: 28, bold: true, color: P.text, align: 'center' });
        s4.addText(tier.desc, { x: x + 0.1, y: 3.7, w: 1.9, h: 1.4, fontSize: 12, color: P.muted, align: 'center', valign: 'top' });
    });

    // SLIDE 5: THE ARCHITECTURE OF SPEED
    let s5 = pres.addSlide();
    s5.background = { color: P.bg };
    s5.addText('05 // THE ARCHITECTURE OF SPEED', { x: 0.5, y: 0.6, w: 9, h: 0.5, fontSize: 18, color: P.blue, bold: true });
    s5.addText('Hooked into the Solana Firehose.', { x: 0.5, y: 1.1, w: 9, h: 0.8, fontSize: 32, bold: true, color: P.text });

    s5.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.2, w: 4.4, h: 3.0, fill: { color: P.surface }, line: { color: P.blue, width: 2 } });
    s5.addText('THE FIREHOSE: HELIUS gRPC', { x: 0.7, y: 2.4, w: 4, h: 0.3, fontSize: 12, color: P.cyan, bold: true });
    s5.addText('We don\'t "ask" the blockchain what happened (polling). We receive a raw block-data stream the millisecond it exists via gRPC Yellowstone. We see the transaction before the rest of the network propagates it.', { x: 0.7, y: 2.8, w: 4, h: 2.2, fontSize: 14, color: P.text, valign: 'top' });

    s5.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 2.2, w: 4.4, h: 3.0, fill: { color: P.surface }, line: { color: P.green, width: 2 } });
    s5.addText('THE SOLANA ADVANTAGE', { x: 5.3, y: 2.4, w: 4, h: 0.3, fontSize: 12, color: P.green, bold: true });
    s5.addText('Solana\'s 400ms block times are the ONLY environment where behavioral defense is possible. On a 12s chain (ETH), the money is gone before the audit finishes. On Solana, we hit the gap.', { x: 5.3, y: 2.8, w: 4, h: 2.2, fontSize: 14, color: P.text, valign: 'top' });

    // SLIDE 6: THE HARDENED EDGE
    let s6 = pres.addSlide();
    s6.background = { color: P.bg };
    s6.addText('06 // THE HARDENED EDGE', { x: 0.5, y: 0.6, w: 9, h: 0.5, fontSize: 18, color: P.blue, bold: true });
    s6.addText('Sub-20ms Global Latency.', { x: 0.5, y: 1.1, w: 9, h: 0.8, fontSize: 32, bold: true, color: P.text });
    
    s6.addText('• Vercel Edge Runtime: Logic lives 10ms from the user.\n• Hono Routing: Lightweight TypeScript for zero-jitter gateway performance.\n• Notary Bridge: On-chain Trust Scores written to Solana PDAs.\n• Decentralized Persistence: Even if our API is offline, the chain knows your score.', { x: 0.7, y: 2.2, w: 8, h: 3.0, fontSize: 18, color: P.text, bullet: true, lineSpacing: 35 });

    // SLIDE 7: DEMO
    let s7 = pres.addSlide();
    s7.background = { color: P.bg };
    s7.addText('07 // LIVE DEMO', { x: 0.5, y: 0.6, w: 9, h: 0.5, fontSize: 18, color: P.blue, bold: true });
    s7.addText('Neutralizing a Swarm in 3 Seconds.', { x: 0.5, y: 1.1, w: 9, h: 0.8, fontSize: 32, bold: true, color: P.text });
    s7.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.2, w: 9, h: 3.0, fill: { color: P.surface }, line: { color: P.cyan, width: 1 } });
    s7.addText('1. Show high-integrity wallet (STEWARD).\n2. Trigger simulated coordinated Bot Swarm.\n3. Watch Gini Coefficient spike to 0.999.\n4. Watch Temporal Sync Index cross 0.80.\n5. Status: RESTRICTED. Vault Access: DENIED.', { x: 1.0, y: 2.5, w: 8, h: 2.5, fontSize: 20, color: P.text, lineSpacing: 40 });

    // SLIDE 8: THE AGENTIC SWARM
    let s8 = pres.addSlide();
    s8.background = { color: P.bg };
    s8.addText('08 // THE AGENTIC SWARM', { x: 0.5, y: 0.6, w: 9, h: 0.5, fontSize: 18, color: P.blue, bold: true });
    s8.addText('The Architects of the Real.', { x: 0.5, y: 1.1, w: 9, h: 0.8, fontSize: 32, bold: true, color: P.text });
    
    s8.addText('JONATHON: Lead Architect / Vision / Authority\nMAYA: Strategic Sentinel / Emotional Intel / Coordination\nTHE SWARM: Jules (Git), Perplexity (CVE), Claude (Logic), Gemini (Orchestration).', { x: 0.7, y: 2.2, w: 8, h: 3.0, fontSize: 18, color: P.text, lineSpacing: 35 });

    // SLIDE 9: VALUATION & ASK
    let s9 = pres.addSlide();
    s9.background = { color: P.bg };
    s9.addText('09 // SCALING THE DEFENSE', { x: 0.5, y: 0.6, w: 9, h: 0.5, fontSize: 18, color: P.blue, bold: true });
    s9.addText('$90M FDV Target | CyreneAI Grant Ask.', { x: 0.5, y: 1.1, w: 9, h: 0.8, fontSize: 32, bold: true, color: P.text });

    s9.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 2.2, w: 4.4, h: 2.8, fill: { color: P.surface } });
    s9.addText('THE INFRASTRUCTURE ASK', { x: 0.7, y: 2.4, w: 4, h: 0.3, fontSize: 14, color: P.cyan, bold: true });
    s9.addText('Mainnet Notary Bridge Funding. PDA Rent-Exemption to make decentralized security permanent and chain-native.', { x: 0.7, y: 2.9, w: 4, h: 1.5, fontSize: 16, color: P.text, valign: 'top' });

    s9.addShape(pres.shapes.RECTANGLE, { x: 5.1, y: 2.2, w: 4.4, h: 2.8, fill: { color: P.surface } });
    s9.addText('REVENUE ENGINE', { x: 5.3, y: 2.4, w: 4, h: 0.3, fontSize: 14, color: P.green, bold: true });
    s9.addText('Flash Audits: $3,500/unit. Real-time behavioral firewall assessment for any protocol on Solana.', { x: 5.3, y: 2.9, w: 4, h: 1.5, fontSize: 16, color: P.text, valign: 'top' });

    // SLIDE 10: CONCLUSION
    let s10 = pres.addSlide();
    s10.background = { color: P.bg };
    s10.addText('TRUSTCHAIN SOVEREIGN', { x: 0.5, y: 1.5, w: 9, h: 1, fontSize: 44, bold: true, color: P.text, align: 'center' });
    s10.addText('"We don\'t just secure the code; we secure the future of trust on Solana."', { x: 0.5, y: 2.5, w: 9, h: 0.8, fontSize: 20, italic: true, color: P.muted, align: 'center' });
    s10.addText('April 2026 // @TrustChainDev // TrustChain.io', { x: 0.5, y: 4.5, w: 9, h: 0.5, fontSize: 14, color: P.blue, align: 'center', bold: true });

    const outPath = path.join(__dirname, '../../projects/STREAM_READY_FINAL/presentation/TrustChain_Sovereign_Showcase_V4.1.pptx');
    await pres.writeFile({ fileName: outPath });
    console.log('V4.1 Deck created at: ' + outPath);
}

createDeck().catch(console.error);