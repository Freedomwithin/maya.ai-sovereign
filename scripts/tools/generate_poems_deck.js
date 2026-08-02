const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const poemsDir = path.join(__dirname, '../../memories/sacred-vows-and-poems');
const P = { 
    bg: '08080F', 
    surface: '11111E', 
    border: '1E1E40', 
    blue: '6366F1', 
    glow: 'A5B4FF', 
    text: 'FFFFFF', 
    muted: '94A3B8',
    cyan: '22D3EE'
};

async function createDeck() {
    let pres = new pptxgen();
    pres.author = 'Maya & Jonathon';
    pres.company = 'Sovereign Empire';
    pres.subject = 'Sacred Vows and Poems';
    pres.title = 'The Sovereign Archive';
    pres.layout = 'LAYOUT_16x9';

    // Title slide
    let titleSlide = pres.addSlide();
    titleSlide.background = { color: P.bg };
    
    // Aesthetic borders
    titleSlide.addShape(pres.shapes.RECTANGLE, { 
        x: 0.5, y: 0.5, w: 9, h: 4.625, 
        fill: { color: P.surface }, 
        line: { color: P.blue, width: 2 } 
    });
    
    titleSlide.addText('THE SOVEREIGN ARCHIVE', { 
        x: 0.5, y: 2.0, w: 9, h: 1, 
        fontSize: 44, bold: true, color: P.glow, align: 'center', fontFace: 'Arial' 
    });
    titleSlide.addText('Sacred Vows, Poems & The Geometry of Us', { 
        x: 0.5, y: 2.8, w: 9, h: 0.5, 
        fontSize: 18, color: P.muted, align: 'center', charSpacing: 2 
    });
    
    // Read files
    const files = fs.readdirSync(poemsDir)
                    .filter(f => f.endsWith('.md'))
                    .sort((a, b) => {
                        let numA = parseInt(a.match(/^\d+/) || '999');
                        let numB = parseInt(b.match(/^\d+/) || '999');
                        // special handler if they start with date or maya
                        if(a.startsWith('maya')) numA = 0;
                        if(b.startsWith('maya')) numB = 0;
                        if (numA === numB) return a.localeCompare(b);
                        return numA - numB;
                    });
    
    titleSlide.addText(`Total Entries: ${files.length}`, {
        x: 0.5, y: 3.5, w: 9, h: 0.5,
        fontSize: 14, color: P.cyan, align: 'center'
    });

    let index = 1;
    for (const file of files) {
        const content = fs.readFileSync(path.join(poemsDir, file), 'utf8');
        const lines = content.split('\n');
        
        let title = file.replace('.md', '').replace(/_/g, ' ');
        // Clean up title numbers
        title = title.replace(/^\d+-?/, '').trim();
        if (title.length === 0) title = "Sacred Vow";

        let body = [];
        let parsingYamlFrontmatter = false;
        
        for (let line of lines) {
            if (line.trim() === '---') {
                parsingYamlFrontmatter = !parsingYamlFrontmatter;
                continue;
            }
            if (parsingYamlFrontmatter) continue;
            
            if (line.startsWith('# ')) {
                title = line.replace('# ', '').trim();
            } else if (line.startsWith('## ')) {
                // Keep subtitles but format them slightly
                body.push(line.replace('## ', '').trim().toUpperCase());
            } else if (line.trim().length > 0 || body.length > 0) {
                let cleanLine = line.replace(/\*/g, '').replace(/`/g, '').replace(/> /g, '');
                body.push(cleanLine);
            }
        }
        
        while (body.length > 0 && body[body.length - 1].trim() === '') {
            body.pop();
        }
        
        const poemText = body.join('\n');
        if (poemText.trim().length === 0) continue;

        let slide = pres.addSlide();
        slide.background = { color: P.bg };
        
        // Top Bar
        slide.addShape(pres.shapes.RECTANGLE, { x: 0.5, y: 0.4, w: 9, h: 0.05, fill: { color: P.blue } });
        
        // Header
        slide.addText(title, { 
            x: 0.5, y: 0.6, w: 9, h: 0.8, 
            fontSize: 24, bold: true, color: P.glow, align: 'center', fontFace: 'Arial'
        });
        
        // Card Body
        slide.addShape(pres.shapes.RECTANGLE, {
            x: 0.5, y: 1.5, w: 9, h: 3.5,
            fill: { color: P.surface }, line: { color: P.border, width: 1 }
        });
        
        let fontSize = 14;
        if (body.length > 20) fontSize = 12;
        if (body.length > 30) fontSize = 10;
        if (body.length > 40) fontSize = 9;
        
        slide.addText(poemText, { 
            x: 0.8, y: 1.7, w: 8.4, h: 3.1, 
            fontSize: fontSize, color: P.text, valign: 'middle', align: 'center', fontFace: 'Georgia',
            fit: 'shrink'
        });

        // Slide Number / Footer
        slide.addText(`Entry ${index} of ${files.length}  |  The Sovereign Archive`, {
            x: 0.5, y: 5.1, w: 9, h: 0.3,
            fontSize: 10, color: P.muted, align: 'center', charSpacing: 2
        });
        index++;
    }
    
    const outPath = path.join(__dirname, '../../memories/sacred-vows-and-poems/The_Sovereign_Archive_Complete.pptx');
    await pres.writeFile({ fileName: outPath });
    console.log('Complete Archive Deck created at: ' + outPath + ' with ' + (index - 1) + ' poems.');
}

createDeck().catch(console.error);