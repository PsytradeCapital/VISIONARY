#!/usr/bin/env node

// Simple Node.js script to generate app icons
// Run with: node generate-icons.js

const fs = require('fs');
const path = require('path');

// Icon sizes needed for PWA
const iconSizes = [16, 32, 48, 72, 96, 120, 128, 144, 152, 180, 192, 384, 512];

// Simple SVG icon template
function generateSVGIcon(size) {
  return `<svg width="${size}" height="${size}" viewBox="0 0 ${size} ${size}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#667eea;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#764ba2;stop-opacity:1" />
    </linearGradient>
  </defs>
  
  <!-- Background -->
  <rect width="${size}" height="${size}" rx="${size * 0.15}" fill="url(#bgGradient)"/>
  
  <!-- App Icon - Letter V -->
  <text x="${size/2}" y="${size * 0.65}" text-anchor="middle" font-family="Arial, sans-serif" font-size="${size * 0.5}" font-weight="bold" fill="white">V</text>
  
  <!-- AI Indicator -->
  <circle cx="${size * 0.75}" cy="${size * 0.25}" r="${size * 0.08}" fill="#FE6B8B"/>
</svg>`;
}

// Create icons directory if it doesn't exist
const iconsDir = path.join(__dirname, 'frontend', 'public');
if (!fs.existsSync(iconsDir)) {
  fs.mkdirSync(iconsDir, { recursive: true });
}

console.log('🎨 Generating Visionary AI app icons...');

// Generate SVG icons (you can convert these to PNG using online tools)
iconSizes.forEach(size => {
  const svgContent = generateSVGIcon(size);
  const filename = `icon-${size}x${size}.svg`;
  const filepath = path.join(iconsDir, filename);
  
  fs.writeFileSync(filepath, svgContent);
  console.log(`✅ Generated ${filename}`);
});

// Generate a simple favicon.ico placeholder
const faviconContent = generateSVGIcon(32);
fs.writeFileSync(path.join(iconsDir, 'favicon.svg'), faviconContent);

console.log('\n🚀 Icon generation complete!');
console.log('\n📝 Next steps:');
console.log('1. Convert SVG icons to PNG using an online converter');
console.log('2. Replace the SVG files with PNG files');
console.log('3. Or use the generate-icons.html file in your browser');
console.log('4. Start your app: npm start');
console.log('5. Visit http://localhost:3000/generate-icons.html to generate PNG icons');

// Create a simple README for icons
const iconReadme = `# App Icons

This directory contains all the app icons for Visionary AI PWA.

## Generated Icons
${iconSizes.map(size => `- icon-${size}x${size}.png - ${size}x${size} pixels`).join('\n')}

## Usage
- Favicon: 16x16, 32x32, 48x48
- iOS: 120x120, 152x152, 180x180  
- Android: 72x72, 96x96, 144x144, 192x192, 384x384, 512x512
- PWA: 192x192 (maskable), 512x512 (any)

## Converting SVG to PNG
1. Use online converter like convertio.co or cloudconvert.com
2. Upload SVG files and convert to PNG
3. Replace SVG files with PNG files
4. Keep the same filenames

## Alternative: Browser Generator
Visit http://localhost:3000/generate-icons.html to generate PNG icons directly in your browser.
`;

fs.writeFileSync(path.join(iconsDir, 'ICONS_README.md'), iconReadme);
console.log('📄 Created ICONS_README.md');